# CareerCast — System Architecture

## Overview

CareerCast is a layered, modular system that combines a Flask REST API, a FastAPI v2 layer,
three trained ML models, and a React single-page application.

```
┌─────────────────────────────────────────────────────┐
│                   Client Layer                       │
│  React SPA (Vite)  │  Streamlit Review UI           │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────┐
│              FastAPI v2 (Port 5000)                  │
│  /api/v2/predict  /api/v2/skill-gap  /api/v2/health  │
│        ↕ WSGIMiddleware mount                        │
│              Flask API  (/api/*)                     │
│  auth │ resume upload │ history │ admin │ health     │
└───────────────────┬─────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
 ┌──────┐     ┌──────────┐    ┌──────────┐
 │SQLite│     │ML Models │    │ Uploads  │
 │  DB  │     │(joblib)  │    │  Folder  │
 └──────┘     └──────────┘    └──────────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
    LR Model    RF Model    XGBoost
    (.pkl)      (.pkl)      (.pkl)
                    │
                MLflow
             Model Registry
```

---

## Component Breakdown

### 1. Flask API (`backend/app.py`)
- Entry point for auth (`/api/login`, `/api/register`)
- Resume upload, parsing, prediction, history
- Admin panel endpoints
- SQLite database access via `utils/database.py`

### 2. FastAPI v2 (`backend/main.py`)
- Mounted on top of Flask via `WSGIMiddleware`
- Provides stateless prediction endpoints — no auth required
- Interactive Swagger UI at `/docs`
- Reuses all backend utilities via direct Python imports

### 3. ML Subsystem (`backend/utils/`)

| File                | Responsibility                             |
|---------------------|--------------------------------------------|
| `train_model.py`    | Trains all 3 models, logs metrics to MLflow|
| `ml_model.py`       | File path constants, metric helpers        |
| `ml_service.py`     | Lazy-loaded model cache, prediction API    |
| `feature_extractor.py` | Green/red flag evaluation              |

**Prediction pipeline:**
```
Resume Text → TF-IDF Vectorizer → [LR | RF | XGBoost] → Role + Confidence
```

### 4. Resume Parser (`backend/utils/parser.py`)
- Extracts: name (via spaCy NER or heuristics), email, phone
- Detects skills via `SKILLS_DB` keyword set
- Identifies education, experience, certifications, and projects

### 5. Skill Gap Service (`backend/services/skill_gap.py`)
- `COMPETENCY_MAPPING`: 10 roles × 4–8 skills × priority levels
- Weighted scoring: Critical=4, High=3, Moderate=2, Low=1
- Generates actionable suggestions for missing skills

### 6. React Frontend (`frontend/`)
- Vite + React SPA
- Components: `PredictionCard`, `SkillGapAnalysis`, `ResumeUploader`
- API client at `frontend/src/services/api.js`

### 7. Streamlit Review UI (`streamlit/review_app.py`)
- Tab 1: Resume upload + analysis
- Tab 2: Cohort analytics (reads DB directly)
- Tab 3: Career comparison matrix
- Tab 4: PDF export via reportlab

### 8. Database (`backend/careercast.db`)
```sql
-- users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    password_hash TEXT,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- resumes table
CREATE TABLE resumes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    filename TEXT,
    prediction TEXT,
    confidence REAL,
    accuracy REAL,
    green_flags TEXT,       -- JSON array
    red_flags TEXT,         -- JSON array
    parsed_entities TEXT,   -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Data Flow — Resume Upload

```
1. Client: POST /api/upload (multipart file + JWT)
2. Flask: Authenticate token → extract user_id
3. parser.extract_text_from_file() → raw text
4. parser.parse_resume_text() → entities dict
5. feature_extractor.evaluate_flags() → green/red flags
6. ml_service.predict_all_models() → {LR, RF, XGB predictions}
7. ResumeModel.save_resume() → SQLite record
8. Return 201 JSON with all results
```

---

## Deployment

| Environment | Description                                |
|-------------|--------------------------------------------|
| Local dev   | `uvicorn main:app --reload` (port 5000)    |
| Render      | Gunicorn via `Procfile`                    |
| Vercel      | React frontend via `vercel.json`           |

See `docs/DEPLOYMENT.md` for full deployment instructions.

---

## Python Package

The `careercast` package wraps the backend modules:
```
careercast/
├── __init__.py    # Public API: analyze_resume, predict_career, analyze_skill_gap
├── cli.py         # Click CLI: careercast analyze | predict | skill-gap | models
└── config.py      # Centralized path and settings constants
```

Install with: `pip install -e .`
