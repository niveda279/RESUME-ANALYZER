"""Unit tests for utils/feature_extractor.py (green/red flag evaluation)."""

import os
import sys
import pytest

ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for p in [ROOT_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from utils.feature_extractor import evaluate_flags


def _make_parsed(
    email="user@example.com",
    phone="555-1234",
    skills=None,
    raw_text="",
    certifications="AWS Certified",
):
    return {
        "email": email,
        "phone": phone,
        "skills": skills or ["Python", "SQL", "Machine Learning", "Docker", "Git", "Kubernetes"],
        "raw_text": raw_text,
        "certifications": certifications,
        "education": "B.Tech",
        "experience": "developer intern",
        "projects": "Built a recommender system",
    }


class TestEvaluateFlags:
    """Tests for green and red flag evaluation."""

    def test_returns_both_keys(self):
        result = evaluate_flags(_make_parsed())
        assert "green_flags" in result
        assert "red_flags" in result

    def test_green_flags_is_list(self):
        result = evaluate_flags(_make_parsed())
        assert isinstance(result["green_flags"], list)

    def test_red_flags_is_list(self):
        result = evaluate_flags(_make_parsed())
        assert isinstance(result["red_flags"], list)

    def test_contact_green_flag(self):
        parsed = _make_parsed(email="a@b.com", phone="123-456")
        result = evaluate_flags(parsed)
        assert any("contact" in f.lower() for f in result["green_flags"])

    def test_missing_contact_red_flag(self):
        parsed = _make_parsed(email="Not Provided", phone="Not Provided")
        result = evaluate_flags(parsed)
        assert any("contact" in f.lower() for f in result["red_flags"])

    def test_github_green_flag(self):
        parsed = _make_parsed(raw_text="github.com/johndoe experience python sql projects")
        result = evaluate_flags(parsed)
        assert any("github" in f.lower() for f in result["green_flags"])

    def test_missing_github_red_flag(self):
        parsed = _make_parsed(raw_text="experience python sql projects education skills")
        result = evaluate_flags(parsed)
        assert any("github" in f.lower() for f in result["red_flags"])

    def test_strong_skills_green_flag(self):
        # six or more distinct skills → "Strong technical skill set"
        parsed = _make_parsed(skills=["Python", "SQL", "ML", "Docker", "Git", "Kubernetes"])
        result = evaluate_flags(parsed)
        assert any("skill" in f.lower() for f in result["green_flags"])

    def test_sparse_skills_red_flag(self):
        parsed = _make_parsed(skills=["Python"])
        result = evaluate_flags(parsed)
        assert any("skill" in f.lower() for f in result["red_flags"])

    def test_certifications_green_flag(self):
        parsed = _make_parsed(certifications="AWS Certified Machine Learning")
        result = evaluate_flags(parsed)
        assert any("certif" in f.lower() for f in result["green_flags"])

    def test_no_certifications_red_flag(self):
        parsed = _make_parsed(certifications="None detected")
        result = evaluate_flags(parsed)
        assert any("certif" in f.lower() for f in result["red_flags"])

    def test_measurable_achievements_green(self):
        parsed = _make_parsed(raw_text="improved performance by 30% reduced costs by $5000 skills experience education projects")
        result = evaluate_flags(parsed)
        assert any("measurable" in f.lower() or "achievement" in f.lower() for f in result["green_flags"])

    def test_no_empty_flags(self):
        """Neither list should ever be completely empty (fallback must kick in)."""
        result = evaluate_flags(_make_parsed())
        assert len(result["green_flags"]) > 0
