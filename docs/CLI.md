# CareerCast CLI Reference

The `careercast` command-line tool is installed automatically when you `pip install -e .`
from the project root.

## Installation

```bash
cd RESUME-ANALYZER
pip install -e .
careercast version
```

---

## Commands

### `careercast version`
Print the installed package version.

```
$ careercast version
CareerCast v4.0.0
```

---

### `careercast analyze [FILE] [OPTIONS]`
Parse a resume and print extracted entities.

| Argument / Option | Description                                  |
|-------------------|----------------------------------------------|
| `FILE`            | Path to PDF, DOCX, or TXT resume file        |
| `--text / -t`     | Provide raw resume text instead of a file    |
| `--json-output`   | Output as JSON                               |

**Examples:**
```bash
# Parse a PDF
careercast analyze resume.pdf

# Parse inline text
careercast analyze --text "John Doe | Python SQL Docker" --json-output

# JSON output (omits raw_text field)
careercast analyze resume.pdf --json-output
```

**Sample output:**
```
── Parsed Resume Entities ──────────────────
  Name           : Jane Smith
  Email          : jane@example.com
  Phone          : +44-20-1234-5678
  Education      : B.Tech Computer Science — Tech University (2021)
  Experience     : Software Engineer — TechCorp (2021–Present)
  Certifications : None detected
  Skills (8)    : Docker, Git, Java, Kubernetes, Python, REST Api, SQL, System Design
```

---

### `careercast predict [FILE] [OPTIONS]`
Predict the career role for a resume.

| Argument / Option      | Description                                                |
|------------------------|------------------------------------------------------------|
| `FILE`                 | Path to resume file                                        |
| `--text / -t`          | Provide raw resume text                                    |
| `--model / -m`         | `best` (default), `logistic_regression`, `random_forest`, `xgboost` |
| `--all-models`         | Show predictions from all three models                     |
| `--json-output`        | Output as JSON                                             |

**Examples:**
```bash
# Default (best model)
careercast predict resume.pdf

# Specific model
careercast predict resume.pdf --model random_forest

# All models, JSON output
careercast predict resume.pdf --all-models --json-output
```

**Sample output:**
```
── Career Prediction ───────────────────────
  Predicted Role : Data Scientist
  Confidence     : 91.2%

  Top Role Probabilities:
    Data Scientist              91.2% ██████████████████
    ML Engineer                 5.3%  █
    Data Analyst                2.1%
    Software Engineer           1.0%
    Cloud Architect             0.4%
```

---

### `careercast skill-gap [FILE] [OPTIONS]`
Identify skill gaps against a target role.

| Argument / Option  | Description                                                  |
|--------------------|--------------------------------------------------------------|
| `FILE`             | Path to resume file                                          |
| `--text / -t`      | Provide raw resume text                                      |
| `--role / -r`      | Target role (auto-inferred from ML model if omitted)         |
| `--json-output`    | Output as JSON                                               |

**Examples:**
```bash
# Auto-detect role
careercast skill-gap resume.pdf

# Specify role
careercast skill-gap resume.pdf --role "Data Scientist"

# JSON output for programmatic use
careercast skill-gap resume.pdf --role "ML Engineer" --json-output
```

**Sample output:**
```
── Skill Gap Analysis — Data Scientist ──────────────
  Match Score  : 71%
  Matched (5) : Python, Machine Learning, SQL, Statistics, Deep Learning
  Missing (2) : NLP, Data Visualization

  🚨 Priority Gaps (Critical/High):

  [High] Deep Learning
    → Learn PyTorch or TensorFlow and implement a basic neural network...
```

---

### `careercast models [OPTIONS]`
Show performance metrics for all trained models.

| Option         | Description    |
|----------------|----------------|
| `--json-output`| Output as JSON |

**Example:**
```bash
careercast models
```

**Sample output:**
```
── Trained Model Performance ───────────────
  Logistic Regression   : Accuracy=94.0%  F1=93.5%
  Random Forest         : Accuracy=98.0%  F1=97.8%
  XGBoost               : Accuracy=96.0%  F1=95.7%

  Best model: Random Forest
```

---

## Global Options

| Option      | Description            |
|-------------|------------------------|
| `--version` | Show version and exit  |
| `--help`    | Show help message      |

Each subcommand also accepts `--help` for detailed options.

---

## Programmatic Python API

The same functionality is available as a Python library:

```python
from careercast import analyze_resume, predict_career, analyze_skill_gap

# Parse a file
entities = analyze_resume("path/to/resume.pdf")
print(entities["skills"])

# Predict role
prediction = predict_career(entities["raw_text"], model="random_forest")
print(prediction["predicted_role"])  # e.g. "Data Scientist"

# Skill gap
gap = analyze_skill_gap(entities["skills"], target_role=prediction["predicted_role"])
print(f"Match: {gap['match_percentage']}%")
```
