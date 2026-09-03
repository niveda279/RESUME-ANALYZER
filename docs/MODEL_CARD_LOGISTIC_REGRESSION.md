# Model Card — Logistic Regression Classifier

## Model Overview

| Property         | Value                                          |
|------------------|------------------------------------------------|
| **Model type**   | Logistic Regression (multi-class, OvR scheme)  |
| **Framework**    | scikit-learn                                   |
| **Task**         | 10-class career role classification            |
| **Input**        | TF-IDF vectors (max 3000 features, bigrams)    |
| **Output**       | Predicted career label + class probabilities   |
| **Training data**| CareerCast Resume Dataset (100 samples)        |
| **File**         | `backend/trained_model/career_model.pkl`       |

---

## Performance Metrics

> [!NOTE]
> Cross-validated scores are the reliable generalization estimates.
> In-sample scores are inflated due to the small dataset (100 samples, no hold-out).

| Metric                        | Value   |
|-------------------------------|---------|
| In-sample accuracy            | ~100%   |
| 5-fold CV accuracy (mean)     | ~94%    |
| Weighted F1 (CV mean)         | ~0.93   |
| Training time (100 samples)   | < 1 s   |

---

## Hyperparameters

```python
LogisticRegression(
    solver="lbfgs",
    max_iter=1000,
    multi_class="auto",   # OvR for binary-compatible solvers
    C=1.0,                # default regularisation
)
```

---

## Intended Use

- **Primary use**: Career role classification from resume text for job seekers.
- **Suitable for**: Fast, interpretable predictions where probability calibration matters.
- **Not suitable for**: High-stakes hiring decisions without human review.

---

## Strengths

- Fast inference (< 5 ms per prediction).
- Well-calibrated class probabilities useful for the role breakdown chart.
- Interpretable coefficients (high-weight terms correlate with role keywords).

---

## Limitations

- Vocabulary-dependent — unfamiliar jargon may be ignored.
- Performance degrades significantly on resumes from domains underrepresented in training data.
- Small training set means cross-validated accuracy estimate has high variance.

---

## Feature Importance

The most influential features (by coefficient magnitude) for each class are the domain-specific
technical keywords — e.g., "machine learning", "pytorch", "kubernetes" for ML-adjacent roles.

---

## Training Procedure

```python
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), sublinear_tf=True)
X = vectorizer.fit_transform(texts)
model = LogisticRegression(max_iter=1000)
model.fit(X, labels)
joblib.dump(model, "backend/trained_model/career_model.pkl")
```

See `backend/train_model.py` for the full training script.
