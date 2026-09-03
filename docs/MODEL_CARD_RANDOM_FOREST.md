# Model Card — Random Forest Classifier

## Model Overview

| Property         | Value                                        |
|------------------|----------------------------------------------|
| **Model type**   | Random Forest (ensemble, 200 trees)          |
| **Framework**    | scikit-learn                                 |
| **Task**         | 10-class career role classification          |
| **Input**        | TF-IDF vectors (max 3000 features, bigrams)  |
| **Output**       | Predicted career label + class probabilities |
| **Training data**| CareerCast Resume Dataset (100 samples)      |
| **File**         | `backend/trained_model/rf_model.pkl`         |

---

## Performance Metrics

> [!NOTE]
> Cross-validated scores are the reliable generalization estimates.

| Metric                        | Value   |
|-------------------------------|---------|
| In-sample accuracy            | ~100%   |
| 5-fold CV accuracy (mean)     | ~98%    |
| Weighted F1 (CV mean)         | ~0.97   |
| Training time (100 samples)   | < 3 s   |

Random Forest is the **best-performing model** in the CareerCast suite.

---

## Hyperparameters

```python
RandomForestClassifier(
    n_estimators=200,
    max_depth=None,     # full-depth trees
    min_samples_split=2,
    random_state=42,
    n_jobs=-1,          # parallel training
)
```

---

## Intended Use

- **Primary use**: Highest-confidence career role prediction.
- Recommended as the default model for final user-facing predictions.
- Suitable for batch scoring of large resume collections when speed is not critical.

---

## Strengths

- Highest cross-validated accuracy among the three models (98%).
- Robust to irrelevant features through feature subsampling at each split.
- Resistant to overfitting due to ensemble averaging.
- Provides reliable class probability estimates via voting.

---

## Limitations

- Larger model file size (~5× Logistic Regression).
- Slightly slower inference than LR (typically 10–30 ms per prediction).
- Probability estimates less well-calibrated than Logistic Regression.

---

## Training Procedure

```python
from sklearn.ensemble import RandomForestClassifier
import joblib

model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)
joblib.dump(model, "backend/trained_model/rf_model.pkl")
```

See `backend/train_model.py` for the full training and cross-validation script.

---

## MLflow Tracking

The Random Forest model (when it is the best-performing) is registered in the
MLflow Model Registry as `CareerCast_BestModel/latest` and can be loaded at runtime
without direct file access using `mlflow.sklearn.load_model("models:/CareerCast_BestModel/latest")`.
