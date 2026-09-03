"""
conftest.py — Shared pytest fixtures for the CareerCast test suite.

All fixtures are available automatically to every test module.
"""

import os
import sys
import json
import pytest

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

for path in [ROOT_DIR, BACKEND_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# ── Sample resume text fixtures ───────────────────────────────────────────────

SAMPLE_DS_RESUME = """
John Doe
john.doe@example.com | +1-555-123-4567 | linkedin.com/in/johndoe | github.com/johndoe

SUMMARY
Experienced Data Scientist with 4 years of experience applying machine learning and
statistical modelling to real-world business problems.

SKILLS
Python, Machine Learning, SQL, Statistics, Deep Learning, NLP, TensorFlow, PyTorch,
Pandas, NumPy, Scikit-Learn, Tableau, Data Visualization

EXPERIENCE
Senior Data Scientist — Acme Corp (2022–Present)
- Developed predictive models achieving 95% accuracy, reducing churn by 18%
- Built NLP pipeline processing 10,000+ daily documents

Data Analyst Intern — DataTech Inc (2021–2022)
- Automated reporting workflows saving 20 hours/week

PROJECTS
Customer Churn Predictor — XGBoost model deployed to production via Docker
Sentiment Analyzer — BERT-based NLP model for Twitter data

EDUCATION
M.S. Data Science — State University (2021)
B.S. Statistics — City College (2019)

CERTIFICATIONS
AWS Certified Machine Learning Specialty
"""

SAMPLE_SWE_RESUME = """
Jane Smith
jane.smith@email.com | +44-20-1234-5678 | github.com/janesmith

SUMMARY
Software Engineer with expertise in Java and Python backend systems.

SKILLS
Java, Python, Data Structures, Algorithms, Git, System Design, SQL,
Docker, REST API, Microservices

EXPERIENCE
Software Engineer — TechCorp (2021–Present)
- Designed distributed microservices serving 1M+ users
- Reduced API latency by 40% through query optimisation

PROJECTS
Distributed Cache System — Java-based LRU cache with Redis integration
REST API Framework — Lightweight Java HTTP framework

EDUCATION
B.Tech Computer Science — Tech University (2021)
"""

SAMPLE_WEBDEV_RESUME = """
Alex Johnson
alex@webdev.io | github.com/alexj

SKILLS
HTML, CSS, JavaScript, React, Node.js, Git, SQL, TypeScript

EXPERIENCE
Frontend Developer — StartupXYZ (2022–Present)
- Built React SPA serving 50,000 daily active users

EDUCATION
Bachelor Computer Science
"""


@pytest.fixture(scope="session")
def ds_resume_text():
    """Data Scientist sample resume text."""
    return SAMPLE_DS_RESUME


@pytest.fixture(scope="session")
def swe_resume_text():
    """Software Engineer sample resume text."""
    return SAMPLE_SWE_RESUME


@pytest.fixture(scope="session")
def webdev_resume_text():
    """Web Developer sample resume text."""
    return SAMPLE_WEBDEV_RESUME


@pytest.fixture(scope="session")
def ds_skills():
    """Pre-parsed skills list for a Data Scientist profile."""
    return ["Python", "Machine Learning", "SQL", "Statistics", "Deep Learning",
            "NLP", "TensorFlow", "PyTorch", "Pandas"]


@pytest.fixture(scope="session")
def flask_app():
    """Configured Flask test application with an in-memory database."""
    from app import app as _app
    from utils.database import init_db

    # Use a test database to avoid polluting production
    _app.config["TESTING"] = True
    _app.config["DATABASE"] = os.path.join(BACKEND_DIR, "test_careercast.db")

    with _app.app_context():
        init_db()

    return _app


@pytest.fixture(scope="session")
def flask_client(flask_app):
    """Flask test client."""
    return flask_app.test_client()


@pytest.fixture(scope="session")
def admin_token(flask_client):
    """JWT token for the admin user."""
    import json as _json
    resp = flask_client.post(
        "/api/login",
        data=_json.dumps({"email": "admin@careercast.com", "password": "Admin@123456"}),
        content_type="application/json",
    )
    assert resp.status_code == 200, f"Admin login failed: {resp.data}"
    return _json.loads(resp.data)["token"]


@pytest.fixture(scope="session")
def user_token(flask_client):
    """JWT token for a regular user."""
    import json as _json
    resp = flask_client.post(
        "/api/login",
        data=_json.dumps({"email": "user@careercast.com", "password": "User@123456"}),
        content_type="application/json",
    )
    assert resp.status_code == 200, f"User login failed: {resp.data}"
    return _json.loads(resp.data)["token"]
