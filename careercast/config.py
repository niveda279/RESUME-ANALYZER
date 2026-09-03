"""
careercast.config — Centralized configuration for the CareerCast package.

All path resolution is relative to the project root, making the package
importable from any working directory.
"""

import os

# ── Path resolution ──────────────────────────────────────────────────────────
# Project root = one level above the careercast/ package directory
_PKG_DIR     = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(_PKG_DIR, ".."))
BACKEND_DIR  = os.path.join(PROJECT_ROOT, "backend")
UPLOADS_DIR  = os.path.join(PROJECT_ROOT, "uploads")
DOCS_DIR     = os.path.join(PROJECT_ROOT, "docs")

# ── Model artifacts ───────────────────────────────────────────────────────────
TRAINED_MODEL_DIR  = os.path.join(BACKEND_DIR, "trained_model")
LR_MODEL_FILE      = os.path.join(TRAINED_MODEL_DIR, "career_model.pkl")
RF_MODEL_FILE      = os.path.join(TRAINED_MODEL_DIR, "rf_model.pkl")
XGB_MODEL_FILE     = os.path.join(TRAINED_MODEL_DIR, "xgb_model.pkl")
VECTORIZER_FILE    = os.path.join(TRAINED_MODEL_DIR, "vectorizer.pkl")
LABEL_ENCODER_FILE = os.path.join(TRAINED_MODEL_DIR, "label_encoder.pkl")
ALL_METRICS_FILE   = os.path.join(TRAINED_MODEL_DIR, "all_metrics.json")

# ── Database ──────────────────────────────────────────────────────────────────
DEFAULT_DB_PATH = os.path.join(BACKEND_DIR, "careercast.db")

# ── Application defaults ──────────────────────────────────────────────────────
FLASK_PORT   = int(os.environ.get("FLASK_PORT", 5000))
FASTAPI_PORT = int(os.environ.get("FASTAPI_PORT", 5000))
MAX_FILE_SIZE_MB = 10

# ── Supported file types ─────────────────────────────────────────────────────
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}

# ── ML settings ───────────────────────────────────────────────────────────────
SUPPORTED_MODELS = ["logistic_regression", "random_forest", "xgboost"]
DEFAULT_MODEL    = "best"

# ── Career roles supported by the system ─────────────────────────────────────
SUPPORTED_ROLES = [
    "Data Scientist",
    "Software Engineer",
    "Web Developer",
    "Data Analyst",
    "DevOps Engineer",
    "Business Analyst",
    "ML Engineer",
    "Product Manager",
    "Cyber Security Specialist",
    "Cloud Architect",
]
