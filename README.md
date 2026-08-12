# CareerCast — AI-Powered Resume Analyzer

**CareerCast** is a production-ready, enterprise-grade **AI Resume Analyzer** that uses three trained Machine Learning models to predict career paths, evaluate resume quality, and provide actionable hiring insights.

The application features a modern enterprise UI, role-based JWT authentication (User & Admin), automated entity parsing (SpaCy & Regex), dynamic Green/Red Flag evaluation, and a full multi-model ML comparison dashboard.

---

## Key Features

### 1. Multi-Model Machine Learning Pipeline
- **Three ML models trained and compared:**
  - **Logistic Regression** — Original baseline model (fast, interpretable)
  - **Random Forest** — Ensemble classifier with feature importance
  - **XGBoost** — Gradient boosted trees (high accuracy)
- **Best model auto-selected** by F1-score from Stratified K-Fold Cross-Validation
- **Prediction UI** shows results from all 3 models with confidence scores
- **Feature Importance** visualized for Random Forest and XGBoost

### 2. Model Comparison Dashboard
| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | ~94% | ~94% | ~94% | ~94% |
| Random Forest | ~98% | ~98% | ~98% | ~98% |
| XGBoost | ~96% | ~96% | ~96% | ~96% |

> Metrics are calculated from 5-Fold Stratified Cross-Validation on the actual dataset. Values shown above are representative — run `python backend/train_model.py` to see your exact results.

### 3. Modern Enterprise Light Theme UI
- Clean white & light gray palette with professional blue accents
- Responsive layout with micro-animations and interactive elements
- High legibility, crisp typography (Inter font family), optimal whitespace

### 4. Role-Based JWT Authentication
- **User Role**: Register, login, upload resumes (PDF/DOCX), view predictions, view Green/Red flag analyses, examine prediction history, and edit profile.
- **Admin Role**: Executive dashboard with aggregate telemetry (Total Users, Total Uploaded Resumes), ML model comparison table, user management (delete users), and resume management (delete resume records).
- Secure password hashing using `werkzeug.security` and standard `JWT` bearer tokens.

### 5. Resume Entity Parsing
- Powered by SpaCy NLP with robust fallback regex rules.
- Extracts: Name, Email, Phone, Skills, Education, Experience, Certifications, Projects.
- Displays extracted skills using clean, color-coded tags.

### 6. Dynamic Green Flags & Red Flags
- **Green Flags**: Detects strengths (e.g., ✔ Strong technical skill set, ✔ Relevant internship experience, ✔ Multiple projects, ✔ Certifications, ✔ ATS-friendly formatting).
- **Red Flags**: Highlights weaknesses (e.g., ✖ Missing GitHub profile, ✖ Missing LinkedIn profile, ✖ No measurable achievements, ✖ Missing certifications).

---

## Machine Learning Architecture

### Dataset
- **Location**: `dataset/resumes_dataset.csv`
- **Size**: 100 resume text samples across 10 career categories
- **Format**: `text` (resume content) and `label` (career category) columns
- **Classes**: Business Analyst, Cloud Architect, Cyber Security Specialist, Data Analyst, Data Scientist, DevOps Engineer, ML Engineer, Product Manager, Software Engineer, Web Developer

### Preprocessing Pipeline
1. Drop missing values and duplicate resume texts
2. TF-IDF Vectorization (`ngram_range=(1,2)`, `max_features=2000`, `sublinear_tf=True`, `stop_words='english'`)
3. **No data leakage**: Vectorizer is fit only on the training fold during CV (using `sklearn.Pipeline`)

### Evaluation Strategy
- **Stratified K-Fold Cross-Validation** (k = min(5, smallest class count))
- Metrics averaged across all folds: Accuracy, Precision (weighted), Recall (weighted), F1-Score (weighted)
- **Best model automatically selected** by highest CV F1-Score

### Models

#### Logistic Regression (Baseline)
- Algorithm: `sklearn.linear_model.LogisticRegression`
- Hyperparameters: `max_iter=2000`, `C=1.0`
- Feature importance: Mean absolute coefficient magnitude per feature

#### Random Forest
- Algorithm: `sklearn.ensemble.RandomForestClassifier`
- Hyperparameters: `n_estimators=300`, `random_state=42`
- Feature importance: Gini importance from trained trees

#### XGBoost
- Algorithm: `xgboost.XGBClassifier`
- Hyperparameters: `n_estimators=300`, `max_depth=6`, `learning_rate=0.1`, `subsample=0.8`, `colsample_bytree=0.8`
- Labels are encoded with `LabelEncoder` before training
- Compatible with XGBoost >= 2.0.0

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
├── backend/
│   ├── app.py                     # Main Flask Server
│   ├── train_model.py             # Reproducible training pipeline (all 3 models)
│   ├── careercast.db              # SQLite database (auto-created)
│   ├── routes/
│   │   ├── auth.py                # Authentication endpoints (JWT)
│   │   ├── resume.py              # Resume upload, parsing & prediction endpoints
│   │   └── admin.py               # Admin control panel endpoints
│   ├── models/
│   │   ├── user.py                # User database model
│   │   └── resume.py              # Resume database model
│   ├── utils/
│   │   ├── parser.py              # SpaCy/Regex resume text parser
│   │   ├── ml_model.py            # Unified ML training pipeline (LR + RF + XGBoost)
│   │   ├── ml_service.py          # Prediction service (multi-model, lazy-loaded)
│   │   ├── feature_extractor.py   # Green Flags & Red Flags evaluator
│   │   └── database.py            # SQLite schema & default seed data
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ResumeCard.jsx
│   │   │   ├── GreenFlags.jsx
│   │   │   ├── RedFlags.jsx
│   │   │   ├── PredictionCard.jsx  # Multi-model prediction tabs (Best/LR/RF/XGB)
│   │   │   ├── ModelComparison.jsx # ML comparison table + feature importance charts
│   │   │   ├── AccuracyCard.jsx
│   │   │   └── HistoryTable.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── UploadResume.jsx
│   │   │   ├── Analysis.jsx
│   │   │   ├── AdminDashboard.jsx  # ML model comparison + admin management
│   │   │   └── Profile.jsx
│   │   ├── services/
│   │   │   └── api.js              # Axios API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css               # Enterprise light theme styling
│   ├── package.json
│   ├── index.html
│   └── vite.config.js
├── dataset/
│   └── resumes_dataset.csv         # Training dataset (100 samples, 10 classes)
├── trained_model/
│   ├── model.joblib                # Logistic Regression
│   ├── vectorizer.joblib           # TF-IDF Vectorizer
│   ├── rf_model.joblib             # Random Forest
│   ├── xgb_model.joblib            # XGBoost
│   ├── label_encoder.joblib        # Label encoder for XGBoost
│   ├── all_metrics.json            # All 3 model metrics
│   └── metrics.json                # LR metrics (backward-compat)
├── uploads/                        # User upload directory (auto-created)
├── README.md
├── requirements.txt                # Python dependencies
├── package.json                    # Root npm scripts
├── render.yaml                     # Render.com deployment config
├── .env.example                    # Environment variables template
├── .gitignore
└── LICENSE
```

---

## Tech Stack

- **Backend**: Python 3.10+, Flask 3.x, SQLite3, PyJWT, Werkzeug, Gunicorn
- **Machine Learning**: Scikit-Learn, XGBoost >= 2.0, Joblib, Pandas, NumPy
- **NLP & Parsing**: SpaCy (en_core_web_sm), PyPDF, Python-Docx
- **Frontend**: React 18, Vite, React Router v6, Axios, Vanilla CSS

---

## Setup & Running Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/careercast.git
cd careercast/RESUME-ANALYZER
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Download SpaCy English model
python -m spacy download en_core_web_sm

# Train all ML models (Logistic Regression + Random Forest + XGBoost)
# This generates all .joblib files and metrics.json in trained_model/
python backend/train_model.py

# Start the Flask API backend
python backend/app.py
```

The backend runs on `http://127.0.0.1:5000`.

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:3000`.

### 4. Access the Application

Open `http://localhost:3000` in your browser.

---

## Model Training Instructions

### Re-train All Models

Run this whenever you update the dataset:

```bash
python backend/train_model.py
```

This will:
1. Load and clean `dataset/resumes_dataset.csv`
2. Run 5-fold Stratified Cross-Validation for each model
3. Print real Accuracy, Precision, Recall, F1-Score for each model
4. Train final models on the full dataset
5. Save all `.joblib` model files to `trained_model/`
6. Update `trained_model/all_metrics.json` with actual metrics
7. Automatically identify and save the best-performing model

### Expected Output

```
============================================================
  CareerCast — ML Model Training Pipeline
============================================================

[INFO] Dataset: 100 samples, 10 classes
[INFO] Using 5-fold Stratified Cross-Validation
[INFO] Evaluating Logistic Regression (CV)...
[INFO] LR  CV Accuracy: 94.0% | F1: 93.6%
[INFO] Evaluating Random Forest (CV)...
[INFO] RF  CV Accuracy: 98.0% | F1: 97.87%
[INFO] Evaluating XGBoost (CV)...
[INFO] XGB CV Accuracy: 96.0% | F1: 95.73%
[INFO] Training final models on full dataset...
[INFO] Best model (by F1): Random Forest

  Logistic Regression:
    Accuracy:  94.0%
    F1 Score:  93.6%

  Random Forest:
    Accuracy:  98.0%
    F1 Score:  97.87%

  XGBoost:
    Accuracy:  96.0%
    F1 Score:  95.73%

  [BEST] Best Model (by F1): Random Forest
```

---

## API Endpoints

### Public
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check with model info |
| GET | `/api/ml-comparison` | All 3 model metrics (public) |

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Register new user |
| POST | `/api/login` | Login and get JWT token |
| GET | `/api/profile` | Get current user profile |
| POST | `/api/logout` | Logout |

### Resume (JWT Required)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/upload` | Upload resume → runs all 3 ML models |
| GET | `/api/analysis/:id` | Get specific analysis result |
| GET | `/api/history` | Get user's resume history |

### Admin (JWT + Admin Role Required)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/stats` | Platform statistics |
| GET | `/api/admin/users` | All users |
| DELETE | `/api/admin/user/:id` | Delete user |
| GET | `/api/admin/resumes` | All resumes |
| DELETE | `/api/admin/resume/:id` | Delete resume |
| GET | `/api/admin/ml-metrics` | Full ML comparison metrics |

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Flask secret key for JWT signing
SECRET_KEY=your-secret-key-change-in-production

# Flask environment
FLASK_ENV=development
```

> ⚠️ **Never commit `.env` to version control.** It's excluded by `.gitignore`.

---

## Default Credentials

| Role | Email | Password |
|---|---|---|
| Admin | `admin@careercast.com` | `Admin@123456` |
| User (Demo) | `user@careercast.com` | `User@123456` |

---

## Deployment (Render.com)

The `render.yaml` file is pre-configured for deployment on [Render](https://render.com):

```bash
# Build Command (runs automatically on Render):
pip install -r requirements.txt && \
python -m spacy download en_core_web_sm && \
python backend/train_model.py && \
npm --prefix frontend install && \
npm --prefix frontend run build

# Start Command:
gunicorn backend.app:app --bind 0.0.0.0:$PORT
```

---

## Adding More Data

To improve model accuracy, add more resume samples to `dataset/resumes_dataset.csv`:

```csv
text,label
"Your resume text here...",Software Engineer
```

Then re-run training:

```bash
python backend/train_model.py
```

The best model will be automatically re-selected based on new metrics.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
