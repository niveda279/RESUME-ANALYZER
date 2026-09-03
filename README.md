# CareerCast — AI-Powered Resume Analyzer

**CareerCast** is a production-ready, pip-installable **AI Resume Analyzer** that uses three trained Machine Learning models to predict career paths, evaluate resume quality, and provide actionable hiring insights — including an **interactive Skill Gap Analysis** that benchmarks your skills against any target role and generates a downloadable PDF report.

It ships as a fully-tested Python library with a CLI, a FastAPI/Flask dual-server backend, a React dashboard, an enhanced Streamlit review UI, and a CI/CD pipeline with 97 automated tests.

---

## Milestone Changelog

| Milestone | Theme | Key Additions |
|-----------|-------|---------------|
| **M1** | Foundation | SpaCy parser, Green/Red flags, SQLite, React UI |
| **M2** | Auth & ML | JWT auth, 3-model pipeline (LR + RF + XGBoost), Admin dashboard |
| **M3** | Observability | FastAPI `/api/v2`, MLflow model registry, Streamlit prototype, GitHub Actions CI |
| **M4** | Production | pip package, Click CLI, enhanced Streamlit (Cohort, Comparison, PDF), 97-test suite, full docs |

---

## Key Features

### ✨ Milestone 4 — Production-Ready Package & Tooling

#### 📦 pip-Installable Python Library
```bash
pip install -e .                      # editable install from repo root
pip install -e ".[backend,streamlit]" # with all optional extras
```
Public API after install:
```python
from careercast import analyze_resume, predict_career, analyze_skill_gap

parsed = analyze_resume("resume.pdf")
pred   = predict_career("Python developer with ML experience...")
gap    = analyze_skill_gap(["Python", "SQL"], "Data Scientist")
```

#### 🖥️ `careercast` CLI
Installed automatically with the package (`careercast` entry-point):

| Command | Description |
|---------|-------------|
| `careercast analyze <file>` | Parse a resume — extract name, email, skills, education, etc. |
| `careercast predict <file>` | Predict career role (single model or all 3) |
| `careercast skill-gap <file> --role "Data Scientist"` | Full skill gap report against a target role |
| `careercast models` | Show performance metrics for all trained models |
| `careercast version` | Print the installed package version |

```bash
# Quick examples
careercast analyze resume.pdf
careercast predict resume.pdf --all-models --json-output
careercast skill-gap resume.pdf --role "ML Engineer"
careercast models
```

#### 📊 Enhanced Streamlit Review UI (4 tabs)

| Tab | What it does |
|-----|-------------|
| **📄 Resume Analysis** | Upload → call FastAPI v2 → prediction + skill gap + 3-model breakdown |
| **📊 Cohort Analytics** | Live aggregate stats from SQLite: role distribution, confidence tiers, top skills across all resumes |
| **🔀 Career Comparison** | Side-by-side required-skills matrix for up to 4 roles simultaneously |
| **📥 PDF Export** | One-click professional PDF report (ReportLab) — candidate info, prediction, matched/missing skills, priority recommendations |

#### 🧪 97-Test Automated Suite
```
tests/
├── conftest.py              Shared fixtures (Flask client, JWT tokens, resume fixtures)
├── unit/                    41 tests — parser, flags, skill gap logic
├── integration/             37 tests — auth, FastAPI, ML pipeline, resume upload
└── regression/              19 tests — Milestone 1–3 stability guard
```
```
pytest tests/
======================= 97 passed, 1 warning in 12.08s
```

#### 📚 Documentation Suite (`docs/`)

| File | Description |
|------|-------------|
| `API_REFERENCE.md` | All Flask & FastAPI endpoints with request/response schemas |
| `CLI.md` | Full CLI command reference and examples |
| `ARCHITECTURE.md` | System architecture diagrams and data flow |
| `DATASET_CARD.md` | Dataset provenance, stats, bias considerations |
| `MODEL_CARD_LOGISTIC_REGRESSION.md` | LR model card |
| `MODEL_CARD_RANDOM_FOREST.md` | RF model card |
| `MODEL_CARD_XGBOOST.md` | XGBoost model card |
| `TESTING.md` | Test strategy, coverage, running instructions |
| `DEPLOYMENT.md` | Local, Docker, Render, Streamlit Cloud deploy guides |

---

### ✨ Milestone 3 Highlights
- **FastAPI Backend** (`/api/v2`) — modern async REST API alongside Flask
- **MLflow Model Registry** — experiment tracking, metric logging, model versioning
- **GitHub Actions CI** — automated pipeline with model accuracy gate

### ✨ Milestone 1–2 Highlights
- **Multi-Model ML Pipeline**: Logistic Regression, Random Forest, XGBoost — best auto-selected by CV F1-score
- **Role-Based JWT Auth**: User + Admin roles, protected routes, secure password hashing
- **Resume Entity Parsing**: SpaCy NLP + regex — Name, Email, Phone, Skills, Education, Certifications, Projects
- **Dynamic Green/Red Flags**: Strengths and weaknesses automatically detected from resume content
- **React Dashboard**: Prediction cards, history, admin panel, animated skill gap analysis

---

## Skill Gap Analysis — Supported Roles

All 10 ML classifier categories are fully mapped with curated competency requirements:

| Role | Critical Skills | High Skills | Moderate Skills |
|---|---|---|---|
| **Data Scientist** | Python, Machine Learning | SQL, Statistics | Data Visualization, Deep Learning |
| **Software Engineer** | Python, Java, Data Structures | Algorithms, Git | System Design, SQL |
| **Web Developer** | HTML, CSS, JavaScript | React, Node.js | Git, SQL |
| **Data Analyst** | SQL, Excel | Python, Tableau | Data Cleaning, Statistics |
| **DevOps Engineer** | Linux, Docker | Kubernetes, CI/CD, AWS | Python, Bash |
| **Business Analyst** | SQL, Jira | Requirements Gathering, Agile, Excel | UML, User Stories |
| **ML Engineer** | Python, PyTorch, TensorFlow | Scikit-Learn, Docker | MLOps, MLflow |
| **Product Manager** | Product Roadmap, User Research | Agile, Jira | Figma, Product Strategy |
| **Cyber Security Specialist** | Network Security, Penetration Testing | SIEM, Wireshark, Firewalls | Cryptography, Vulnerability Assessment |
| **Cloud Architect** | AWS, Azure | Terraform, Kubernetes, CloudFormation | Microservices, Serverless |

---

## Machine Learning Architecture

### Dataset
- **Location**: `dataset/resumes_dataset.csv`
- **Size**: 100 resume text samples across 10 career categories
- **Format**: `text` (resume content) + `label` (career category) columns

### Preprocessing Pipeline
1. Drop nulls & duplicate texts
2. TF-IDF Vectorization (`ngram_range=(1,2)`, `max_features=2000`, `sublinear_tf=True`, `stop_words='english'`)
3. **No data leakage** — vectorizer fitted only on training fold inside `sklearn.Pipeline`

### Evaluation Strategy
- **Stratified K-Fold Cross-Validation** (k = min(5, smallest class count))
- Metrics averaged across folds: Accuracy, Precision (weighted), Recall (weighted), F1-Score (weighted)
- **Best model auto-selected** by highest CV F1-Score

### Model Comparison Dashboard

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | ~94% | ~94% | ~94% | ~94% |
| Random Forest | ~98% | ~98% | ~98% | ~98% |
| XGBoost | ~96% | ~96% | ~96% | ~96% |

> Metrics computed from 5-Fold Stratified Cross-Validation. Run `python backend/train_model.py` for your exact numbers.

### Saved Model Files
| File | Description |
|---|---|
| `trained_model/model.joblib` | Logistic Regression model |
| `trained_model/vectorizer.joblib` | Shared TF-IDF vectorizer |
| `trained_model/rf_model.joblib` | Random Forest model |
| `trained_model/xgb_model.joblib` | XGBoost model |
| `trained_model/label_encoder.joblib` | LabelEncoder for XGBoost |
| `trained_model/all_metrics.json` | All 3 model metrics + best model |
| `trained_model/metrics.json` | LR metrics (backward-compatible) |

---

## Project Structure

```
CareerCast/
├── careercast/                        # pip-installable package (Milestone 4)
│   ├── __init__.py                    # Public API: analyze_resume, predict_career, analyze_skill_gap
│   ├── cli.py                         # Click CLI — analyze, predict, skill-gap, models, version
│   └── config.py                      # Centralized config (env-var driven)
├── backend/
│   ├── app.py                         # Flask server (port 5000)
│   ├── main.py                        # FastAPI server (port 8000, /api/v2)
│   ├── train_model.py                 # Reproducible training pipeline (LR + RF + XGBoost)
│   ├── careercast.db                  # SQLite database (auto-created)
│   ├── routes/
│   │   ├── auth.py                    # JWT auth endpoints
│   │   ├── resume.py                  # Upload, parsing, prediction, /skill-gap (PDF/DOCX/TXT)
│   │   └── admin.py                   # Admin panel endpoints
│   ├── models/
│   │   ├── user.py                    # User DB model
│   │   └── resume.py                  # Resume DB model
│   ├── services/
│   │   └── skill_gap.py               # Skill Gap logic + 10-role competency map
│   └── utils/
│       ├── parser.py                  # SpaCy/Regex resume parser
│       ├── ml_model.py                # ML training pipeline
│       ├── ml_service.py              # Multi-model prediction service (lazy-loaded)
│       ├── feature_extractor.py       # Green Flags & Red Flags evaluator
│       └── database.py                # SQLite schema & seed data
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PredictionCard.jsx     # Multi-model tabs + clickable roles → Skill Gap
│   │   │   ├── SkillGapAnalysis.jsx   # SVG gauge, skill grids, checklist
│   │   │   ├── ModelComparison.jsx    # ML comparison table + feature importance
│   │   │   └── ...                    # Navbar, ResumeCard, GreenFlags, RedFlags, etc.
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx          # Manages Skill Gap state + auto-scroll
│   │   │   ├── AdminDashboard.jsx     # Admin ML comparison + management
│   │   │   └── ...
│   │   └── index.css                  # Design system — Glassmorphism & Indigo theme
│   └── vite.config.js
├── streamlit/
│   └── review_app.py                  # Enhanced 4-tab Streamlit UI (Milestone 4)
├── tests/                             # 97-test suite (Milestone 4)
│   ├── conftest.py                    # Shared fixtures
│   ├── unit/                          # Parser, flags, skill gap unit tests
│   ├── integration/                   # Auth, FastAPI, ML, resume endpoint tests
│   └── regression/                   # Milestone 1–3 stability guard
├── docs/                              # Full documentation suite (Milestone 4)
│   ├── API_REFERENCE.md
│   ├── CLI.md
│   ├── ARCHITECTURE.md
│   ├── DATASET_CARD.md
│   ├── MODEL_CARD_LOGISTIC_REGRESSION.md
│   ├── MODEL_CARD_RANDOM_FOREST.md
│   ├── MODEL_CARD_XGBOOST.md
│   ├── TESTING.md
│   └── DEPLOYMENT.md
├── .github/
│   └── workflows/
│       ├── ci.yml                     # CI pipeline — install, train, CLI verify, 97 tests, coverage
│       └── deploy.yml                 # Render deployment workflow
├── dataset/
│   └── resumes_dataset.csv
├── trained_model/                     # Auto-generated by train_model.py
├── pyproject.toml                     # Package config — pip install, entry points, extras
├── backend/requirements.txt           # All Python dependencies incl. reportlab, xgboost, click
├── render.yaml                        # Render.com deployment config
├── .env.example                       # Environment variables template
├── start_backend.ps1                  # One-command backend launcher (Windows)
├── start_frontend.ps1                 # One-command frontend launcher (Windows)
└── LICENSE
```

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Python Package** | `setuptools`, `click >= 8.1`, `pyproject.toml` |
| **Backend (Flask)** | Python 3.9+, Flask 3.x, SQLite3, PyJWT, Werkzeug, Gunicorn |
| **Backend (FastAPI)** | FastAPI, Uvicorn, HTTPx, python-multipart |
| **Machine Learning** | Scikit-Learn, XGBoost >= 2.0, Joblib, Pandas, NumPy, MLflow |
| **NLP & Parsing** | SpaCy (en_core_web_sm), PyPDF, Python-Docx |
| **Streamlit UI** | Streamlit >= 1.25, Altair >= 5.0, ReportLab >= 4.0 |
| **Frontend** | React 18, Vite, React Router v6, Axios, Vanilla CSS |
| **Testing** | pytest, pytest-cov, HTTPX (async FastAPI client) |
| **CI/CD** | GitHub Actions |

---

## Setup & Running Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/niveda279/RESUME-ANALYZER.git
cd RESUME-ANALYZER
```

### 2. Install the Python Package

```bash
# Editable install — registers the `careercast` CLI entry point
pip install -e ".[backend,streamlit,dev]"

# Download SpaCy language model
python -m spacy download en_core_web_sm

# Train all ML models
python backend/train_model.py
```

### 3. Start the Flask Backend

```bash
python backend/app.py
# Runs on http://127.0.0.1:5000
```

Or on Windows:
```powershell
./start_backend.ps1
```

### 4. Start the FastAPI Backend (optional, for Streamlit UI)

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
# Runs on http://127.0.0.1:8000  (docs at /docs)
```

### 5. Streamlit Review UI

```bash
streamlit run streamlit/review_app.py --server.port 8501
# Runs on http://localhost:8501
```

### 6. React Frontend

```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

Or on Windows:
```powershell
./start_frontend.ps1
```

---

## CLI Reference

```bash
# Show version
careercast version

# Parse a resume
careercast analyze resume.pdf
careercast analyze resume.pdf --json-output

# Predict career role
careercast predict resume.pdf
careercast predict resume.pdf --model random_forest
careercast predict resume.pdf --all-models

# Skill gap analysis (auto-detects role)
careercast skill-gap resume.pdf
# Against a specific role
careercast skill-gap resume.pdf --role "Data Scientist"
careercast skill-gap resume.pdf --role "ML Engineer" --json-output

# Show trained model metrics
careercast models
careercast models --json-output
```

> All commands also accept `--text "raw text"` instead of a file path.

---

## Running Tests

```bash
# Full suite
pytest tests/

# By category
pytest tests/unit/        # 41 tests — parser, flags, skill gap logic
pytest tests/integration/ # 37 tests — API, ML, auth
pytest tests/regression/  # 19 tests — stability guard for M1–M3

# With coverage report
pytest tests/ --cov=backend --cov-report=term-missing
```

Expected output:
```
======================= 97 passed, 1 warning in 12.08s
```

---

## Model Training

```bash
python backend/train_model.py
```

This will:
1. Load and clean `dataset/resumes_dataset.csv`
2. Run 5-fold Stratified Cross-Validation for each model
3. Train final models on the full dataset
4. Save all `.joblib` files and update `trained_model/all_metrics.json`
5. Automatically select and record the best-performing model

### Expected Output
```
============================================================
  CareerCast — ML Model Training Pipeline
============================================================
[INFO] Dataset: 100 samples, 10 classes
[INFO] LR  CV Accuracy: 94.0% | F1: 93.6%
[INFO] RF  CV Accuracy: 98.0% | F1: 97.87%
[INFO] XGB CV Accuracy: 96.0% | F1: 95.73%
[INFO] Best model (by F1): Random Forest
```

---

## API Endpoints

### Flask API — `http://127.0.0.1:5000`

#### Public
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check with model info |
| GET | `/api/ml-comparison` | All 3 model metrics |

#### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Register new user |
| POST | `/api/login` | Login → get JWT token |
| GET | `/api/profile` | Current user profile |
| POST | `/api/logout` | Logout |

#### Resume (JWT Required)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/upload` | Upload resume (PDF/DOCX/TXT) → runs all 3 ML models |
| GET | `/api/analysis/:id` | Get specific analysis result |
| GET | `/api/history` | Get user's resume history |
| POST | `/api/skill-gap` | Run skill gap analysis for a role |

**`POST /api/skill-gap`**
```json
// Request
{ "skills": ["Python", "SQL", "Machine Learning"], "target_role": "Data Scientist" }

// Response
{
  "status": "success",
  "gap_analysis": {
    "match_percentage": 57.14,
    "matched_skills": [{"skill": "Python", "priority": "Critical"}, ...],
    "missing_skills": [{"skill": "Statistics", "priority": "High"}, ...],
    "priority_gaps": [{"skill": "Statistics", "priority": "High", "suggestion": "..."}]
  }
}
```

#### Admin (JWT + Admin Role)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/stats` | Platform statistics |
| GET | `/api/admin/users` | All users |
| DELETE | `/api/admin/user/:id` | Delete user |
| GET | `/api/admin/resumes` | All resumes |
| DELETE | `/api/admin/resume/:id` | Delete resume |
| GET | `/api/admin/ml-metrics` | Full ML comparison metrics |

### FastAPI — `http://127.0.0.1:8000/api/v2`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v2/health` | Health check |
| POST | `/api/v2/predict` | Upload file → predict career role (all 3 models) |
| POST | `/api/v2/skill-gap` | JSON skill gap analysis |
| POST | `/api/v2/recommendation` | Multi-model recommendation |

> Interactive docs: `http://127.0.0.1:8000/docs`

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Flask secret key for JWT signing
SECRET_KEY=your-secret-key-change-in-production

# Flask environment
FLASK_ENV=development

# Streamlit — override API and DB paths
API_URL=http://127.0.0.1:5000/api/v2
DB_PATH=backend/careercast.db
```

> ⚠️ **Never commit `.env` to version control.** It's excluded by `.gitignore`.

---

## Default Credentials

| Role | Email | Password |
|---|---|---|
| Admin | `admin@careercast.com` | `Admin@123456` |
| User (Demo) | `user@careercast.com` | `User@123456` |

---

## Deployment

### Render.com

The `render.yaml` is pre-configured:

```bash
# Build command (Render runs automatically):
pip install -e ".[backend,streamlit]" && \
python -m spacy download en_core_web_sm && \
python backend/train_model.py && \
npm --prefix frontend install && \
npm --prefix frontend run build

# Start command:
gunicorn backend.app:app --bind 0.0.0.0:$PORT
```

### Streamlit Cloud

Deploy `streamlit/review_app.py` separately. Set these secrets in the Streamlit dashboard:
```
API_URL = https://your-render-backend.onrender.com/api/v2
DB_PATH = /path/to/careercast.db
```

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for full deployment guides.

---

## Adding More Training Data

```csv
# dataset/resumes_dataset.csv
text,label
"Your resume text here...",Software Engineer
```

Then re-train:
```bash
python backend/train_model.py
```

The best model is automatically re-selected based on updated metrics.

---

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.
