"""
ml_model.py - Unified ML training pipeline for CareerCast Resume Analyzer

Trains three models on the same dataset:
  1. Logistic Regression  (original model, preserved)
  2. Random Forest        (new)
  3. XGBoost              (new)

All models share one TF-IDF vectorizer fit ONLY on the training set (no data leakage).
Uses Stratified K-Fold cross-validation for robust evaluation metrics,
then trains final models on the full dataset for best prediction quality.
Best model is auto-selected by F1-score from cross-validation.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support, confusion_matrix,
    make_scorer, precision_score, recall_score, f1_score
)
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("[WARNING] xgboost not installed. Run: pip install xgboost>=2.0.0")

# -- Path constants ------------------------------------------------------------
BASE_DIR       = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_DIR      = os.path.join(BASE_DIR, 'trained_model')
DATASET_PATH   = os.path.join(BASE_DIR, 'dataset', 'resumes_dataset.csv')

MODEL_FILE          = os.path.join(MODEL_DIR, 'model.joblib')           # LR
VECTORIZER_FILE     = os.path.join(MODEL_DIR, 'vectorizer.joblib')      # shared
RF_MODEL_FILE       = os.path.join(MODEL_DIR, 'rf_model.joblib')        # RF
XGB_MODEL_FILE      = os.path.join(MODEL_DIR, 'xgb_model.joblib')       # XGB
LABEL_ENCODER_FILE  = os.path.join(MODEL_DIR, 'label_encoder.joblib')   # for XGB
METRICS_FILE        = os.path.join(MODEL_DIR, 'metrics.json')           # LR (compat)
ALL_METRICS_FILE    = os.path.join(MODEL_DIR, 'all_metrics.json')       # all 3

RANDOM_STATE = 42

# -- Fallback defaults (only used if models have never been trained) -----------
DEFAULT_LR_METRICS = {
    "algorithm": "Logistic Regression",
    "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0
}
DEFAULT_ALL_METRICS = {
    "logistic_regression": DEFAULT_LR_METRICS,
    "random_forest": {
        "algorithm": "Random Forest",
        "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0
    },
    "xgboost": {
        "algorithm": "XGBoost",
        "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0
    },
    "best_model": "Logistic Regression",
    "best_model_key": "logistic_regression"
}


# -- Helpers -------------------------------------------------------------------

def _cv_evaluate(model, X, y, cv, algorithm_name):
    """
    Evaluate a model using stratified cross-validation.
    Returns a metrics dict with accuracy, precision, recall, f1_score.
    All values are averages across CV folds — real, not hardcoded.
    """
    scoring = {
        'accuracy':  'accuracy',
        'precision': make_scorer(precision_score, average='weighted', zero_division=0),
        'recall':    make_scorer(recall_score,    average='weighted', zero_division=0),
        'f1':        make_scorer(f1_score,        average='weighted', zero_division=0),
    }
    try:
        results = cross_validate(model, X, y, cv=cv, scoring=scoring, return_train_score=False)
        acc  = float(np.mean(results['test_accuracy']))
        prec = float(np.mean(results['test_precision']))
        rec  = float(np.mean(results['test_recall']))
        f1   = float(np.mean(results['test_f1']))
    except Exception as e:
        print(f"  [WARN] CV failed for {algorithm_name}: {e}")
        acc = prec = rec = f1 = 0.0

    return {
        "algorithm": algorithm_name,
        "accuracy":  round(acc  * 100, 2),
        "precision": round(prec * 100, 2),
        "recall":    round(rec  * 100, 2),
        "f1_score":  round(f1   * 100, 2),
    }


def _compute_confusion_matrix(model, X, y, classes):
    """Compute confusion matrix on full dataset after final fit."""
    y_pred = model.predict(X)
    return confusion_matrix(y, y_pred, labels=classes).tolist()


def _select_best_model(all_metrics: dict) -> tuple:
    """Return (best_model_display_name, best_model_key) by highest F1-score."""
    candidates = {
        "logistic_regression": ("Logistic Regression", all_metrics["logistic_regression"]["f1_score"]),
        "random_forest":       ("Random Forest",        all_metrics["random_forest"]["f1_score"]),
        "xgboost":             ("XGBoost",              all_metrics["xgboost"]["f1_score"]),
    }
    best_key  = max(candidates, key=lambda k: candidates[k][1])
    best_name = candidates[best_key][0]
    return best_name, best_key


# -- Training pipeline ---------------------------------------------------------

def train_and_save_model():
    """
    Train Logistic Regression, Random Forest, and XGBoost on the resume dataset.

    Strategy:
    - Use Stratified K-Fold cross-validation (k=min(5, smallest_class_count))
      for robust evaluation metrics (no data leakage — vectorizer fit per fold).
    - Train final models on the FULL dataset for maximum prediction quality.
    - The TF-IDF vectorizer used during CV is re-fit on full data for final models.

    Returns the full all_metrics dict.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)

    if not os.path.exists(DATASET_PATH):
        print(f"[ERROR] Dataset not found at {DATASET_PATH}")
        return DEFAULT_ALL_METRICS

    df = pd.read_csv(DATASET_PATH)
    if 'text' not in df.columns or 'label' not in df.columns:
        print("[ERROR] Dataset must contain 'text' and 'label' columns.")
        return DEFAULT_ALL_METRICS

    # Clean dataset: drop missing values and duplicates
    df = df.dropna(subset=['text', 'label']).drop_duplicates(subset=['text'])
    X_raw = df['text'].values
    y = df['label'].values

    print(f"[INFO] Dataset: {len(X_raw)} samples, {len(set(y))} classes")
    print(f"[INFO] Classes: {sorted(set(y))}")

    # Determine CV folds: use min(5, smallest_class_count) to ensure stratification
    from collections import Counter
    class_counts = Counter(y)
    min_class_count = min(class_counts.values())
    n_folds = max(2, min(5, min_class_count))
    print(f"[INFO] Using {n_folds}-fold Stratified Cross-Validation")

    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=RANDOM_STATE)

    # -- TF-IDF Vectorizer params (used in pipelines for leak-free CV)
    vectorizer_params = dict(
        ngram_range=(1, 2),
        max_features=2000,
        stop_words='english',
        sublinear_tf=True
    )

    # ========================================================================
    # CROSS-VALIDATION METRICS (real evaluation, no data leakage)
    # sklearn Pipeline ensures vectorizer is fit only on each CV train fold.
    # ========================================================================

    # 1. Logistic Regression
    print("[INFO] Evaluating Logistic Regression (CV)...")
    lr_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(**vectorizer_params)),
        ('clf', LogisticRegression(max_iter=2000, C=1.0, random_state=RANDOM_STATE))
    ])
    lr_metrics = _cv_evaluate(lr_pipeline, X_raw, y, cv, "Logistic Regression")
    print(f"[INFO] LR  CV Accuracy: {lr_metrics['accuracy']}% | F1: {lr_metrics['f1_score']}%")

    # 2. Random Forest
    print("[INFO] Evaluating Random Forest (CV)...")
    rf_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(**vectorizer_params)),
        ('clf', RandomForestClassifier(
            n_estimators=300, max_depth=None, min_samples_split=2,
            min_samples_leaf=1, random_state=RANDOM_STATE, n_jobs=-1
        ))
    ])
    rf_metrics = _cv_evaluate(rf_pipeline, X_raw, y, cv, "Random Forest")
    print(f"[INFO] RF  CV Accuracy: {rf_metrics['accuracy']}% | F1: {rf_metrics['f1_score']}%")

    # 3. XGBoost
    if XGBOOST_AVAILABLE:
        print("[INFO] Evaluating XGBoost (CV)...")
        le = LabelEncoder()
        y_enc = le.fit_transform(y)

        # Note: use_label_encoder was deprecated and removed in XGBoost >= 2.0
        # eval_metric is passed to fit() not the constructor in XGBoost >= 2.0
        xgb_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(**vectorizer_params)),
            ('clf', XGBClassifier(
                n_estimators=300,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=RANDOM_STATE,
                verbosity=0,
                n_jobs=-1
            ))
        ])
        xgb_metrics = _cv_evaluate(xgb_pipeline, X_raw, y_enc, cv, "XGBoost")
        print(f"[INFO] XGB CV Accuracy: {xgb_metrics['accuracy']}% | F1: {xgb_metrics['f1_score']}%")
    else:
        xgb_metrics = {
            "algorithm": "XGBoost", "accuracy": 0.0, "precision": 0.0,
            "recall": 0.0, "f1_score": 0.0,
            "confusion_matrix": [], "feature_importance": [],
            "error": "xgboost not installed"
        }
        le = None

    # ========================================================================
    # FINAL MODELS — trained on full dataset for maximum prediction quality
    # ========================================================================
    print("[INFO] Training final models on full dataset...")

    vectorizer = TfidfVectorizer(**vectorizer_params)
    X_vec = vectorizer.fit_transform(X_raw)
    joblib.dump(vectorizer, VECTORIZER_FILE)

    classes = sorted(set(y))
    feature_names = vectorizer.get_feature_names_out()

    # -- Final Logistic Regression
    lr_model = LogisticRegression(max_iter=2000, C=1.0, random_state=RANDOM_STATE)
    lr_model.fit(X_vec, y)
    joblib.dump(lr_model, MODEL_FILE)

    # LR feature importance (mean absolute coefficient across all classes)
    coef_abs = np.abs(lr_model.coef_).mean(axis=0)
    top_lr_idx = np.argsort(coef_abs)[::-1][:10]
    lr_metrics["feature_importance"] = [
        {"feature": feature_names[i], "importance": round(float(coef_abs[i]), 4)}
        for i in top_lr_idx
    ]
    lr_metrics["confusion_matrix"] = _compute_confusion_matrix(lr_model, X_vec, y, classes)

    # -- Final Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=300, max_depth=None, min_samples_split=2,
        min_samples_leaf=1, random_state=RANDOM_STATE, n_jobs=-1
    )
    rf_model.fit(X_vec, y)
    joblib.dump(rf_model, RF_MODEL_FILE)

    rf_importances = rf_model.feature_importances_
    top_rf_idx = np.argsort(rf_importances)[::-1][:10]
    rf_metrics["feature_importance"] = [
        {"feature": feature_names[i], "importance": round(float(rf_importances[i]), 4)}
        for i in top_rf_idx
    ]
    rf_metrics["confusion_matrix"] = _compute_confusion_matrix(rf_model, X_vec, y, classes)

    # -- Final XGBoost
    if XGBOOST_AVAILABLE and le is not None:
        y_enc_full = le.transform(y)
        joblib.dump(le, LABEL_ENCODER_FILE)

        xgb_model = XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
            verbosity=0,
            n_jobs=-1
        )
        # XGBoost >= 2.0: fit() only accepts X, y (+ optional eval_set)
        xgb_model.fit(X_vec, y_enc_full)
        joblib.dump(xgb_model, XGB_MODEL_FILE)

        xgb_importances = xgb_model.feature_importances_
        top_xgb_idx = np.argsort(xgb_importances)[::-1][:10]
        xgb_metrics["feature_importance"] = [
            {"feature": feature_names[i], "importance": round(float(xgb_importances[i]), 4)}
            for i in top_xgb_idx
        ]
        # Confusion matrix for XGBoost (decode label-encoded predictions)
        xgb_pred_enc = xgb_model.predict(X_vec)
        xgb_pred = le.inverse_transform(xgb_pred_enc)
        xgb_metrics["confusion_matrix"] = confusion_matrix(y, xgb_pred, labels=classes).tolist()

    # ========================================================================
    # ASSEMBLE + SAVE METRICS
    # ========================================================================
    all_metrics = {
        "logistic_regression": lr_metrics,
        "random_forest":       rf_metrics,
        "xgboost":             xgb_metrics,
    }
    best_name, best_key = _select_best_model(all_metrics)
    all_metrics["best_model"]     = best_name
    all_metrics["best_model_key"] = best_key
    all_metrics["classes"]        = classes
    all_metrics["dataset_size"]   = int(len(X_raw))
    all_metrics["cv_folds"]       = n_folds
    all_metrics["evaluation"]     = f"{n_folds}-Fold Stratified Cross-Validation"

    with open(ALL_METRICS_FILE, 'w') as f:
        json.dump(all_metrics, f, indent=2)

    # Backward-compat: keep metrics.json pointing to LR
    lr_compat = {k: v for k, v in lr_metrics.items() if k not in ('confusion_matrix', 'feature_importance')}
    with open(METRICS_FILE, 'w') as f:
        json.dump(lr_compat, f, indent=2)

    print(f"\n[INFO] Best model (by F1): {best_name}")
    print(f"[INFO] all_metrics.json saved to {ALL_METRICS_FILE}")
    return all_metrics


# -- Prediction (single model — backward-compat) ------------------------------

def predict_career_role(resume_text: str) -> dict:
    """
    Predict career role using the Logistic Regression model.
    Trains models first if they do not exist.  Preserved for backward compatibility.
    """
    if not os.path.exists(MODEL_FILE) or not os.path.exists(VECTORIZER_FILE):
        train_and_save_model()

    try:
        model      = joblib.load(MODEL_FILE)
        vectorizer = joblib.load(VECTORIZER_FILE)
    except Exception as e:
        print(f"[ERROR] Loading LR model: {e}")
        train_and_save_model()
        model      = joblib.load(MODEL_FILE)
        vectorizer = joblib.load(VECTORIZER_FILE)

    vec_text   = vectorizer.transform([resume_text])
    prediction = model.predict(vec_text)[0]
    probs      = model.predict_proba(vec_text)[0]
    confidence = float(np.max(probs)) * 100

    classes    = model.classes_
    sorted_idx = np.argsort(probs)[::-1]
    breakdown  = [
        {"role": classes[i], "probability": round(float(probs[i]) * 100, 2)}
        for i in sorted_idx[:4]
    ]

    return {
        "predicted_role": prediction,
        "confidence":     round(confidence, 2),
        "breakdown":      breakdown
    }


# -- Metrics getters -----------------------------------------------------------

def get_model_metrics() -> dict:
    """Return LR metrics (backward-compatible)."""
    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_LR_METRICS


def get_all_metrics() -> dict:
    """Return the full 3-model comparison metrics dict."""
    if os.path.exists(ALL_METRICS_FILE):
        try:
            with open(ALL_METRICS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    # Try to train if not yet done
    if os.path.exists(DATASET_PATH):
        return train_and_save_model()
    return DEFAULT_ALL_METRICS
