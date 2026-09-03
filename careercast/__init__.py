"""
CareerCast — AI-Powered Resume Analyzer
========================================
Python package providing a public API for career prediction,
resume parsing, and skill gap analysis.

Usage
-----
>>> from careercast import analyze_resume, predict_career, analyze_skill_gap
>>> result = predict_career("Python developer with ML experience...")
>>> print(result["predicted_role"])
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("careercast")
except PackageNotFoundError:
    __version__ = "4.0.0"

__author__ = "CareerCast Team"
__email__ = "support@careercast.ai"

import os
import sys

# Ensure backend is importable when used as a library
_BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "backend")
_BACKEND_DIR = os.path.abspath(_BACKEND_DIR)
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)


def analyze_resume(file_path: str) -> dict:
    """
    Parse a resume file and extract structured entities.

    Parameters
    ----------
    file_path : str
        Absolute path to a PDF, DOCX, or TXT resume file.

    Returns
    -------
    dict with keys: name, email, phone, skills, education,
                    experience, certifications, projects, raw_text
    """
    from utils.parser import extract_text_from_file, parse_resume_text

    raw_text = extract_text_from_file(file_path)
    if not raw_text or raw_text.startswith("Error"):
        raise ValueError(f"Could not extract text from file: {raw_text}")
    return parse_resume_text(raw_text)


def predict_career(resume_text: str, model: str = "best") -> dict:
    """
    Predict the most suitable career role for a given resume text.

    Parameters
    ----------
    resume_text : str
        Plain-text content of a resume.
    model : str
        Which model to use: "best", "logistic_regression",
        "random_forest", or "xgboost".

    Returns
    -------
    dict with keys: predicted_role, confidence, breakdown
    """
    from utils.ml_service import predict_all_models, get_best_model_prediction

    if model == "best":
        return get_best_model_prediction(resume_text)

    all_preds = predict_all_models(resume_text)
    model_map = {
        "logistic_regression": "logistic_regression",
        "random_forest": "random_forest",
        "xgboost": "xgboost",
    }
    key = model_map.get(model.lower().replace(" ", "_"), "logistic_regression")
    return all_preds.get(key, all_preds.get("logistic_regression", {}))


def analyze_skill_gap(candidate_skills: list, target_role: str) -> dict:
    """
    Identify skill gaps between candidate's current skills and a target role.

    Parameters
    ----------
    candidate_skills : list of str
        Skills extracted from the resume (e.g. ["Python", "SQL"]).
    target_role : str
        The role to benchmark against (e.g. "Data Scientist").

    Returns
    -------
    dict with keys: predicted_role, match_percentage, matched_skills,
                    missing_skills, priority_gaps
    """
    from services.skill_gap import analyze_skill_gap as _analyze

    return _analyze(candidate_skills, target_role)


__all__ = ["analyze_resume", "predict_career", "analyze_skill_gap", "__version__"]
