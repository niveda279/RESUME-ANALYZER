# Dataset Card — CareerCast Resume Dataset

## Dataset Summary

A synthetic, balanced dataset of short resume-style text documents spanning **10 career categories**.
Created specifically for training and evaluating the CareerCast multi-class career classifier.

---

## Dataset Details

| Property       | Value                         |
|----------------|-------------------------------|
| **Size**       | 100 samples (10 per class)    |
| **Format**     | CSV (`dataset/`)              |
| **Language**   | English                       |
| **Task**       | Multi-class text classification |
| **Labels**     | 10 career roles (balanced)    |
| **Created**    | 2026                          |
| **License**    | MIT                           |

---

## Label Distribution

Each class contains exactly **10 samples** (perfectly balanced).

| Label                     | Samples |
|---------------------------|---------|
| Data Scientist            | 10      |
| Software Engineer         | 10      |
| Web Developer             | 10      |
| Data Analyst              | 10      |
| DevOps Engineer           | 10      |
| Business Analyst          | 10      |
| ML Engineer               | 10      |
| Product Manager           | 10      |
| Cyber Security Specialist | 10      |
| Cloud Architect           | 10      |
| **Total**                 | **100** |

---

## Data Fields

| Field    | Type   | Description                                               |
|----------|--------|-----------------------------------------------------------|
| `text`   | string | Resume-style text containing skills, experience, keywords |
| `label`  | string | One of the 10 career category labels                      |

---

## Collection Methodology

- Text samples were **synthetically generated** to cover the vocabulary and keyword patterns
  representative of each career category.
- Each sample contains a mix of technical skills, tooling keywords, and industry terminology
  typical for the given role.
- No real candidate PII is included.

---

## Important Limitations

> [!IMPORTANT]
> **Small Dataset**: With only 100 samples and 10 per class, this dataset is intended for
> **demonstration and rapid prototyping only**. The models trained on this data should not
> be used for production hiring decisions without retraining on a significantly larger,
> real-world dataset.

> [!NOTE]
> **In-sample vs. Cross-validated Metrics**: Since models are trained on the full dataset
> (no hold-out split), confusion matrices show near-perfect in-sample performance. The
> **cross-validated accuracy figures** (reported in the model cards) are the realistic
> generalization estimates.

---

## Preprocessing

- Text is vectorized using **TF-IDF** with the following settings:
  - `max_features=3000`
  - `ngram_range=(1, 2)` (unigrams and bigrams)
  - `sublinear_tf=True`
  - `stop_words='english'`
- Labels are encoded using `sklearn.preprocessing.LabelEncoder`.

---

## Usage

```python
import pandas as pd
df = pd.read_csv("dataset/career_dataset.csv")
print(df["label"].value_counts())
```

---

## Citation

If you use this dataset in a research project, please cite:

```
CareerCast Team (2026). CareerCast Resume Dataset (v1.0).
GitHub: https://github.com/careercast/resume-analyzer
```
