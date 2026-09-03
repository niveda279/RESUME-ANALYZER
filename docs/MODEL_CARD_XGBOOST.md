# Model Card — XGBoost Classifier

## Model Overview

| Property         | Value                                       |
|------------------|---------------------------------------------|
| **Model type**   | XGBoost (gradient boosted trees)            |
| **Framework**    | xgboost + scikit-learn API                  |
| **Task**         | 10-class career role classification         |
| **Input**        | TF-IDF vectors (max 3000 features, bigrams) |
| **Output**       | Predicted career label + class probabilities|
| **Training data**| CareerCast Resume Dataset (100 samples)     |
| **File**         | `backend/trained_model/xgb_model.pkl`       |
| **Encoder file** | `backend/trained_model/label_encoder.pkl`   |

---

## Performance Metrics

> [!NOTE]
> Cross-validated scores are the reliable generalization estimates.

| Metric                        | Value   |
|-------------------------------|---------|
| In-sample accuracy            | ~100%   |
| 5-fold CV accuracy (mean)     | ~96%    |
| Weighted F1 (CV mean)         | ~0.95   |
| Training time (100 samples)   | < 5 s   |

---

## Hyperparameters

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.3,
    use_label_encoder=False,
    eval_metric="mlogloss",
    random_state=42,
)
```

---

## Intended Use

- An ensemble complement to the Logistic Regression and Random Forest models.
- Useful for comparison in the "All Model Predictions" view in the React dashboard.
- Particularly effective when training data grows — XGBoost tends to scale well with more data.

---

## Strengths

- Strong generalisation capability via gradient boosting with regularisation.
- Handles feature interactions implicitly.
- Second-best cross-validated performance in the suite (96%).

---

## Limitations

- Requires the `xgboost` Python package (not installed by default in all environments).
- Label encoding step required (uses `LabelEncoder` stored separately).
- Slowest inference of the three models (~40–80 ms for TF-IDF + XGBoost pass).

> [!WARNING]
> If `xgboost` is not installed, predictions for this model will return a graceful error
> (`{"error": "XGBoost model not loaded"}`) and the system will fall back to the
> best available model automatically.

---

## Fallback Behaviour

```python
# In utils/ml_service.py
if XGBOOST_AVAILABLE and os.path.exists(XGB_MODEL_FILE):
    _xgb_model     = joblib.load(XGB_MODEL_FILE)
    _label_encoder = joblib.load(LABEL_ENCODER_FILE)
else:
    # Graceful no-op; XGBoost slot returns {"error": "..."} 
    pass
```

---

## Training Procedure

```python
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

le = LabelEncoder()
y_enc = le.fit_transform(labels)
model = XGBClassifier(n_estimators=100, max_depth=4, eval_metric="mlogloss")
model.fit(X_train, y_enc)
joblib.dump(model, "backend/trained_model/xgb_model.pkl")
joblib.dump(le,    "backend/trained_model/label_encoder.pkl")
```

See `backend/train_model.py` for the complete training script.
