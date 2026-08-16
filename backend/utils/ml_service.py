"""
ml_service.py — Prediction service layer for CareerCast Resume Analyzer

Provides multi-model prediction (LR + RF + XGB) via lazy-loaded models.
Models are loaded once and cached in module globals — no re-training per request.
"""

import os
import json
import joblib
import numpy as np

from utils.ml_model import (
    MODEL_FILE, VECTORIZER_FILE, RF_MODEL_FILE,
    XGB_MODEL_FILE, LABEL_ENCODER_FILE, ALL_METRICS_FILE,
    train_and_save_model, get_all_metrics, XGBOOST_AVAILABLE
)
import mlflow.sklearn
import mlflow.pyfunc
from dotenv import load_dotenv

load_dotenv()
if os.environ.get("MLFLOW_TRACKING_URI"):
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))

# ── Module-level model cache ──────────────────────────────────────────────────
_lr_model       = None
_rf_model       = None
_xgb_model      = None
_vectorizer     = None
_label_encoder  = None
_mlflow_model   = None
_models_loaded  = False


def _ensure_models_loaded():
    """Lazy-load all trained models from disk. Train if files are missing."""
    global _lr_model, _rf_model, _xgb_model, _vectorizer, _label_encoder, _models_loaded

    if _models_loaded:
        return

    missing = [
        f for f in [MODEL_FILE, VECTORIZER_FILE, RF_MODEL_FILE]
        if not os.path.exists(f)
    ]
    if missing:
        print(f"[INFO] ml_service: model files missing ({missing}), running training...")
        train_and_save_model()

    # Try to load best registered model from MLflow
    global _mlflow_model
    try:
        model_uri = "models:/CareerCast_BestModel/latest"
        _mlflow_model = mlflow.sklearn.load_model(model_uri)
        print("[INFO] ml_service: Loaded CareerCast_BestModel from MLflow Registry.")
    except Exception as e:
        print(f"[WARN] ml_service: Could not load model from MLflow Registry. Falling back to local files. ({e})")
        _mlflow_model = None

    try:
        _lr_model   = joblib.load(MODEL_FILE)
        _vectorizer = joblib.load(VECTORIZER_FILE)
        print("[INFO] ml_service: Logistic Regression loaded.")
    except Exception as e:
        print(f"[ERROR] ml_service: Failed to load LR model: {e}")

    try:
        _rf_model = joblib.load(RF_MODEL_FILE)
        print("[INFO] ml_service: Random Forest loaded.")
    except Exception as e:
        print(f"[ERROR] ml_service: Failed to load RF model: {e}")

    if XGBOOST_AVAILABLE and os.path.exists(XGB_MODEL_FILE):
        try:
            _xgb_model     = joblib.load(XGB_MODEL_FILE)
            _label_encoder = joblib.load(LABEL_ENCODER_FILE)
            print("[INFO] ml_service: XGBoost loaded.")
        except Exception as e:
            print(f"[ERROR] ml_service: Failed to load XGBoost model: {e}")

    _models_loaded = True


# ── Per-model prediction helpers ─────────────────────────────────────────────

def _predict_lr(vec_text) -> dict:
    if _lr_model is None:
        return {"predicted_role": "Unknown", "confidence": 0.0, "breakdown": [], "error": "LR model not loaded"}
    prediction = _lr_model.predict(vec_text)[0]
    probs      = _lr_model.predict_proba(vec_text)[0]
    confidence = float(np.max(probs)) * 100
    classes    = _lr_model.classes_
    sorted_idx = np.argsort(probs)[::-1]
    breakdown  = [
        {"role": classes[i], "probability": round(float(probs[i]) * 100, 2)}
        for i in sorted_idx[:5]
    ]
    return {
        "predicted_role": str(prediction),
        "confidence":     round(confidence, 2),
        "breakdown":      breakdown
    }


def _predict_rf(vec_text) -> dict:
    if _rf_model is None:
        return {"predicted_role": "Unknown", "confidence": 0.0, "breakdown": [], "error": "RF model not loaded"}
    prediction = _rf_model.predict(vec_text)[0]
    probs      = _rf_model.predict_proba(vec_text)[0]
    confidence = float(np.max(probs)) * 100
    classes    = _rf_model.classes_
    sorted_idx = np.argsort(probs)[::-1]
    breakdown  = [
        {"role": classes[i], "probability": round(float(probs[i]) * 100, 2)}
        for i in sorted_idx[:5]
    ]
    return {
        "predicted_role": str(prediction),
        "confidence":     round(confidence, 2),
        "breakdown":      breakdown
    }


def _predict_xgb(vec_text) -> dict:
    if _xgb_model is None or _label_encoder is None:
        return {"predicted_role": "Unknown", "confidence": 0.0, "breakdown": [], "error": "XGBoost model not loaded"}
    pred_enc   = _xgb_model.predict(vec_text)[0]
    prediction = _label_encoder.inverse_transform([pred_enc])[0]
    probs      = _xgb_model.predict_proba(vec_text)[0]
    confidence = float(np.max(probs)) * 100
    classes    = _label_encoder.classes_
    sorted_idx = np.argsort(probs)[::-1]
    breakdown  = [
        {"role": classes[i], "probability": round(float(probs[i]) * 100, 2)}
        for i in sorted_idx[:5]
    ]
    return {
        "predicted_role": str(prediction),
        "confidence":     round(confidence, 2),
        "breakdown":      breakdown
    }


# ── Public API ────────────────────────────────────────────────────────────────

def predict_all_models(resume_text: str) -> dict:
    """
    Run the resume text through all three trained models.

    Returns:
        {
          "logistic_regression": { predicted_role, confidence, breakdown },
          "random_forest":       { predicted_role, confidence, breakdown },
          "xgboost":             { predicted_role, confidence, breakdown },
          "best_model":          "Random Forest",       # display name
          "best_model_key":      "random_forest",       # JSON key
          "best_prediction":     { predicted_role, confidence, breakdown }
        }
    """
    _ensure_models_loaded()

    if _vectorizer is None:
        return {
            "logistic_regression": {"error": "Vectorizer not loaded"},
            "random_forest":       {"error": "Vectorizer not loaded"},
            "xgboost":             {"error": "Vectorizer not loaded"},
            "best_model": "Logistic Regression",
            "best_model_key": "logistic_regression",
            "best_prediction": {"predicted_role": "Unknown", "confidence": 0.0, "breakdown": []}
        }

    vec_text = _vectorizer.transform([resume_text])

    lr_result  = _predict_lr(vec_text)
    rf_result  = _predict_rf(vec_text)
    xgb_result = _predict_xgb(vec_text)

    # Determine best model from saved metrics
    all_metrics   = get_all_metrics()
    best_key      = all_metrics.get("best_model_key", "logistic_regression")
    best_name     = all_metrics.get("best_model", "Logistic Regression")
    results_map   = {
        "logistic_regression": lr_result,
        "random_forest":       rf_result,
        "xgboost":             xgb_result
    }
    best_prediction = results_map.get(best_key, lr_result)

    return {
        "logistic_regression": lr_result,
        "random_forest":       rf_result,
        "xgboost":             xgb_result,
        "best_model":          best_name,
        "best_model_key":      best_key,
        "best_prediction":     best_prediction
    }


def get_best_model_prediction(resume_text: str) -> dict:
    """Predict using only the best-performing model."""
    _ensure_models_loaded()
    
    # Use MLflow registered model if available
    if _mlflow_model is not None and _vectorizer is not None:
        try:
            vec_text = _vectorizer.transform([resume_text])
            
            # Predict
            pred = _mlflow_model.predict(vec_text)[0]
            probs = _mlflow_model.predict_proba(vec_text)[0]
            confidence = float(np.max(probs)) * 100
            
            # Handling classes based on model type
            if hasattr(_mlflow_model, "classes_"):
                classes = _mlflow_model.classes_
            elif _label_encoder is not None:
                # Assuming XGBoost wrapped, we might need inverse transform if output is numeric
                # but if we registered it directly, it depends.
                classes = _label_encoder.classes_
                if isinstance(pred, (int, np.integer)):
                    pred = _label_encoder.inverse_transform([pred])[0]
            else:
                classes = []
            
            sorted_idx = np.argsort(probs)[::-1]
            breakdown = [
                {"role": classes[i] if i < len(classes) else f"Class_{i}", "probability": round(float(probs[i]) * 100, 2)}
                for i in sorted_idx[:5]
            ]
            
            return {
                "predicted_role": str(pred),
                "confidence": round(confidence, 2),
                "breakdown": breakdown,
                "source": "MLflow Registry"
            }
        except Exception as e:
            print(f"[WARN] Error predicting with MLflow model: {e}. Falling back to local.")
            
    all_predictions = predict_all_models(resume_text)
    return all_predictions.get("best_prediction", all_predictions.get("logistic_regression", {}))


def reload_models():
    """Force-reload all models from disk (useful after retraining)."""
    global _models_loaded
    _models_loaded = False
    _ensure_models_loaded()
