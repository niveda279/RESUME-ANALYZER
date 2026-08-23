# CareerCast — AI-Powered Resume Analyzer

**CareerCast** is a production-ready, enterprise-grade **AI Resume Analyzer** that uses three trained Machine Learning models to predict career paths, evaluate resume quality, and provide actionable hiring insights — including an **interactive Skill Gap Analysis** that compares your resume's skills against any predicted role's requirements in real time.

The application features a modern enterprise UI, role-based JWT authentication (User & Admin), automated entity parsing (SpaCy & Regex), dynamic Green/Red Flag evaluation, a full multi-model ML comparison dashboard, and a clickable skill gap analysis card with an animated SVG match gauge and actionable improvement checklist.

---

## Key Features

### ✨ Milestone 3 — Interactive Skill Gap Analysis
- **Click any predicted role** in the Career Path Prediction card to instantly trigger a skill gap analysis.
- **Three clickable trigger points** in the Prediction Card:
  - The **main role box** (primary prediction).
  - Each **multi-model card** (Logistic Regression / Random Forest / XGBoost) — selects the model and starts analysis simultaneously.
  - Every row in the **Role Probability Distribution** table — each has an "Analyze Gap ➔" badge.
- **Analysis card shows:**
  - 🟢 **Animated SVG ring gauge** — match percentage, color-coded (green ≥ 70%, amber ≥ 40%, red < 40%).
  - ✅ **Available Skills** — green chips for resume skills that match the role's requirements.
  - ❌ **Missing Required Skills** — red chips for Critical/High priority gaps, indigo for Moderate/Low.
  - 📋 **Actionable Recommendations checklist** — one task per skill gap, with specific learning advice and a checkbox you can tick off as you learn.
- **10 roles fully mapped** with curated competency requirements and suggestions.
- State resets automatically when a new resume is uploaded or a history item is selected.

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
- Clean white & light gray palette with professional indigo/blue accents
- Responsive layout with micro-animations and interactive elements
- High legibility, crisp typography (Inter font family), optimal whitespace
- Glassmorphism-inspired cards with smooth slide-in animations

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

## Skill Gap Analysis — Supported Roles

The Skill Gap engine covers all 10 career categories from the ML classifier. Each role has curated required competencies with priority levels:

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
│   ├── main.py                    # FastAPI entry point (Milestone 3+)
│   ├── train_model.py             # Reproducible training pipeline (all 3 models)
│   ├── careercast.db              # SQLite database (auto-created)
│   ├── routes/
│   │   ├── auth.py                # Authentication endpoints (JWT)
│   │   ├── resume.py              # Resume upload, parsing & prediction + /skill-gap
│   │   └── admin.py               # Admin control panel endpoints
│   ├── models/
│   │   ├── user.py                # User database model
│   │   └── resume.py              # Resume database model
│   ├── services/
│   │   └── skill_gap.py           # Skill Gap Analysis logic + 10-role competency map
│   └── utils/
│       ├── parser.py              # SpaCy/Regex resume text parser
│       ├── ml_model.py            # Unified ML training pipeline (LR + RF + XGBoost)
│       ├── ml_service.py          # Prediction service (multi-model, lazy-loaded)
│       ├── feature_extractor.py   # Green Flags & Red Flags evaluator
│       └── database.py            # SQLite schema & default seed data
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ResumeCard.jsx
│   │   │   ├── GreenFlags.jsx
│   │   │   ├── RedFlags.jsx
│   │   │   ├── PredictionCard.jsx  # Multi-model tabs + clickable roles → Skill Gap
│   │   │   ├── SkillGapAnalysis.jsx # NEW — SVG gauge, skill grids, checklist
│   │   │   ├── ModelComparison.jsx # ML comparison table + feature importance charts
│   │   │   ├── AccuracyCard.jsx
│   │   │   └── HistoryTable.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx       # Manages Skill Gap state + auto-scroll
│   │   │   ├── UploadResume.jsx
│   │   │   ├── Analysis.jsx
│   │   │   ├── AdminDashboard.jsx  # ML model comparison + admin management
│   │   │   └── Profile.jsx
│   │   ├── services/
│   │   │   └── api.js              # Axios API client (includes getSkillGap)
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css               # Design system — Glassmorphism & Indigo theme
│   ├── package.json
│   ├── index.html
│   └── vite.config.js
├── streamlit/
│   └── review_app.py               # Streamlit prototype UI for Milestone 3
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI pipeline with Accuracy Gate
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
├── start_backend.ps1               # One-command backend launcher (Windows)
├── start_frontend.ps1              # One-command frontend launcher (Windows)
├── render.yaml                     # Render.com deployment config
├── .env.example                    # Environment variables template
├── .gitignore
└── LICENSE
```

---

## Tech Stack

- **Backend**: Python 3.10+, Flask 3.x, FastAPI, SQLite3, PyJWT, Werkzeug, Gunicorn
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
git clone https://github.com/niveda279/RESUME-ANALYZER.git
cd RESUME-ANALYZER
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Download SpaCy English model
python -m spacy download en_core_web_sm

# Train all ML models
python backend/train_model.py

# Start the Flask backend
python backend/app.py
```

Or use the provided launcher script (Windows):
```powershell
./start_backend.ps1
```

The backend runs on `http://127.0.0.1:5000`.

### 3. Streamlit Review UI (Optional)

Open a new terminal:
```bash
streamlit run streamlit/review_app.py --server.port 8501
```
The Streamlit UI runs on `http://localhost:8501`.

### 4. React Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Or use the provided launcher script (Windows):
```powershell
./start_frontend.ps1
```

The frontend runs on `http://localhost:3000`.

### 5. Access the Application

Open `http://localhost:3000` in your browser.

---

## How to Use Skill Gap Analysis

1. **Upload a resume** or select one from the history panel.
2. The **Career Path Prediction** card will show your predicted roles.
3. **Click on any predicted role** — you can click:
   - The large **Predicted Role Match** box at the top.
   - Any of the three **model cards** (LR / RF / XGBoost) in the multi-model comparison.
   - Any role row in the **Role Probability Distribution** list (each has an "Analyze Gap ➔" badge).
4. The **Skill Gap Analysis card** will slide in below showing:
   - A **circular match gauge** with your overall score.
   - **Available Skills** — what you already have.
   - **Missing Skills** — what the role requires that's absent.
   - **Actionable Recommendations** — specific steps to bridge each gap (tick them off as you complete them!).
5. Click the **✕ close button** to dismiss the analysis and try a different role.

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
| **POST** | **`/api/skill-gap`** | **Run skill gap analysis for a role** |

#### `POST /api/skill-gap` — Request Body
```json
{
  "skills": ["Python", "SQL", "Machine Learning"],
  "target_role": "Data Scientist"
}
```
#### Response
```json
{
  "status": "success",
  "skills": ["Python", "SQL", "Machine Learning"],
  "gap_analysis": {
    "match_percentage": 57.14,
    "matched_skills": [
      { "skill": "Python", "priority": "Critical" },
      { "skill": "Machine Learning", "priority": "Critical" },
      { "skill": "SQL", "priority": "High" }
    ],
    "missing_skills": [
      { "skill": "Statistics", "priority": "High" },
      { "skill": "Data Visualization", "priority": "Moderate" },
      { "skill": "Deep Learning", "priority": "Moderate" },
      { "skill": "NLP", "priority": "Low" }
    ],
    "priority_gaps": [
      {
        "skill": "Statistics",
        "priority": "High",
        "suggestion": "Practice complex SQL queries..."
      }
    ]
  }
}
```

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
