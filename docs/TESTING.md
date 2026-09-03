# Testing Guide

## Test Suite Structure

```
tests/
├── conftest.py                    # Shared fixtures
├── unit/
│   ├── test_parser.py             # Resume entity extraction
│   ├── test_flags.py              # Green/red flag evaluation
│   └── test_skill_gap.py          # Skill gap logic + data validation
├── integration/
│   ├── test_auth.py               # Login, JWT, protected routes
│   ├── test_resume.py             # Upload, history, skill-gap API
│   ├── test_ml.py                 # Model loading + inference
│   └── test_fastapi.py            # FastAPI v2 endpoints
└── regression/
    └── test_regression.py         # M1–M3 stability guard
```

---

## Running Tests

### Full suite

```bash
cd RESUME-ANALYZER
pip install -e ".[dev]"
pytest tests/ -v --tb=short
```

### Unit tests only

```bash
pytest tests/unit/ -v
```

### Integration tests only

```bash
pytest tests/integration/ -v
```

### Regression tests only

```bash
pytest tests/regression/ -v
```

### With coverage report

```bash
pytest tests/ --cov=backend --cov-report=term-missing
```

### Specific test file

```bash
pytest tests/unit/test_skill_gap.py -v
```

### Specific test

```bash
pytest tests/unit/test_skill_gap.py::TestAnalyzeSkillGap::test_perfect_match -v
```

---

## Prerequisites

The test suite requires the backend to be on `sys.path` and the trained model files
to exist. If models are missing they will be automatically trained.

```bash
# Ensure models are trained first
python backend/train_model.py

# Then run tests
pytest tests/ -v
```

---

## Fixtures (conftest.py)

| Fixture           | Scope   | Description                                       |
|-------------------|---------|---------------------------------------------------|
| `ds_resume_text`  | session | Data Scientist resume text sample                 |
| `swe_resume_text` | session | Software Engineer resume text sample              |
| `webdev_resume_text` | session | Web Developer resume text sample              |
| `ds_skills`       | session | Pre-parsed DS skill list                          |
| `flask_app`       | session | Flask test application (uses test DB)             |
| `flask_client`    | session | Flask test client                                 |
| `admin_token`     | session | Valid JWT for admin user                          |
| `user_token`      | session | Valid JWT for regular user                        |

---

## Test Categories

### Unit Tests
Pure function tests — no HTTP, no database, no file I/O:
- `test_parser.py`: email extraction, skill detection, empty resume handling
- `test_flags.py`: green flag (github, contact, skills) and red flag conditions
- `test_skill_gap.py`: competency mapping validation, skill matching, suggestions

### Integration Tests
Test the full request/response cycle using Flask/FastAPI test clients:
- `test_auth.py`: correct credentials → 200 + token, wrong credentials → 401
- `test_resume.py`: upload, structured response shape, history, skill-gap endpoint
- `test_ml.py`: all 3 models load, return valid role + confidence, graceful XGBoost fallback
- `test_fastapi.py`: FastAPI v2 health, predict, skill-gap, recommendation

### Regression Tests
Guard that Milestone 1–3 features remain intact:
- **M1**: Parser entity extraction (name, email, skills, flags)
- **M2**: Flask auth, health check, ML comparison endpoint
- **M3**: All 3 models predict, best model returned, skill-gap via API, all_predictions in upload response

---

## Known Behaviours

| Test                              | Expected Behaviour                                 |
|-----------------------------------|----------------------------------------------------|
| XGBoost tests                     | Skip prediction if `xgboost` not installed (graceful error dict) |
| FastAPI tests                     | Skipped entirely if `fastapi` not installed        |
| Admin/user login tests            | Require seeded default users in DB (`init_db()`)   |
| Upload tests                      | Write `.txt` files to uploads folder (cleaned up by OS) |

---

## CI Integration

Tests run automatically on every push/PR via GitHub Actions.
See `.github/workflows/ci.yml` for the full pipeline definition.
