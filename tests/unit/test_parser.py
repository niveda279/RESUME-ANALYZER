"""Unit tests for utils/parser.py"""

import os
import sys
import pytest

ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for p in [ROOT_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from utils.parser import parse_resume_text, SKILLS_DB


class TestParseResumeText:
    """Tests for the parse_resume_text() function."""

    def test_returns_all_keys(self, ds_resume_text):
        result = parse_resume_text(ds_resume_text)
        expected_keys = {"name", "email", "phone", "skills", "education",
                         "experience", "certifications", "projects", "raw_text"}
        assert expected_keys.issubset(result.keys())

    def test_email_extraction(self, ds_resume_text):
        result = parse_resume_text(ds_resume_text)
        assert "john.doe@example.com" == result["email"]

    def test_phone_extraction(self, ds_resume_text):
        result = parse_resume_text(ds_resume_text)
        assert result["phone"] != "Not Provided"

    def test_skills_extracted_as_list(self, ds_resume_text):
        result = parse_resume_text(ds_resume_text)
        assert isinstance(result["skills"], list)
        assert len(result["skills"]) > 0

    def test_known_skills_detected(self, ds_resume_text):
        result = parse_resume_text(ds_resume_text)
        skills_lower = [s.lower() for s in result["skills"]]
        # Python and SQL should be detected reliably
        assert any("python" in s for s in skills_lower)
        assert any("sql" in s for s in skills_lower)

    def test_education_detected(self, ds_resume_text):
        result = parse_resume_text(ds_resume_text)
        assert result["education"] and result["education"] != ""

    def test_raw_text_preserved(self, ds_resume_text):
        result = parse_resume_text(ds_resume_text)
        assert "john.doe@example.com" in result["raw_text"]

    def test_empty_resume_returns_defaults(self):
        result = parse_resume_text("")
        assert result["email"] == "Not Provided"
        assert result["phone"] == "Not Provided"
        assert result["skills"] == []

    def test_skills_db_is_set(self):
        """SKILLS_DB should be a non-empty set of lowercase strings."""
        assert isinstance(SKILLS_DB, set)
        assert len(SKILLS_DB) > 10
        assert all(isinstance(s, str) for s in SKILLS_DB)

    def test_webdev_skills_detected(self, webdev_resume_text):
        result = parse_resume_text(webdev_resume_text)
        skills_lower = [s.lower() for s in result["skills"]]
        assert any("react" in s for s in skills_lower)
        assert any("javascript" in s for s in skills_lower)
