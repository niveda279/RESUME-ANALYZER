"""Unit tests for services/skill_gap.py"""

import os
import sys
import pytest

ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for p in [ROOT_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from services.skill_gap import (
    analyze_skill_gap,
    get_required_skills,
    get_actionable_suggestion,
    COMPETENCY_MAPPING,
    DEFAULT_COMPETENCIES,
)


class TestCompetencyMapping:
    """Tests for the competency data structures."""

    def test_all_roles_present(self):
        expected = [
            "Data Scientist", "Software Engineer", "Web Developer",
            "Data Analyst", "DevOps Engineer", "Business Analyst",
            "ML Engineer", "Product Manager", "Cyber Security Specialist",
            "Cloud Architect",
        ]
        for role in expected:
            assert role in COMPETENCY_MAPPING, f"Missing role: {role}"

    def test_each_role_has_skills(self):
        for role, skills in COMPETENCY_MAPPING.items():
            assert len(skills) >= 3, f"{role} has fewer than 3 skills"

    def test_valid_priority_levels(self):
        valid_priorities = {"Critical", "High", "Moderate", "Low"}
        for role, skills in COMPETENCY_MAPPING.items():
            for skill, priority in skills.items():
                assert priority in valid_priorities, \
                    f"Invalid priority '{priority}' for {skill} in {role}"


class TestGetRequiredSkills:
    """Tests for get_required_skills()."""

    def test_exact_match(self):
        skills = get_required_skills("Data Scientist")
        assert "Python" in skills

    def test_case_insensitive_match(self):
        skills = get_required_skills("data scientist")
        assert skills  # non-empty

    def test_partial_match(self):
        skills = get_required_skills("ML Engineer Specialist")
        assert skills  # matches "ML Engineer"

    def test_unknown_role_returns_defaults(self):
        skills = get_required_skills("Underwater Basket Weaver")
        assert skills == DEFAULT_COMPETENCIES

    def test_software_engineer_has_critical_skills(self):
        skills = get_required_skills("Software Engineer")
        critical = [s for s, p in skills.items() if p == "Critical"]
        assert critical


class TestGetActionableSuggestion:
    """Tests for get_actionable_suggestion()."""

    def test_returns_string(self):
        suggestion = get_actionable_suggestion("Python", "Critical", "Data Scientist")
        assert isinstance(suggestion, str)
        assert len(suggestion) > 20

    def test_known_skill_returns_specific(self):
        suggestion = get_actionable_suggestion("Docker", "High", "DevOps Engineer")
        # Must be a tailored suggestion, not just the default
        assert "docker" in suggestion.lower() or "container" in suggestion.lower()

    def test_unknown_skill_returns_default(self):
        suggestion = get_actionable_suggestion("Quantum Computing", "Low", "Engineer")
        assert "quantum computing" in suggestion.lower()


class TestAnalyzeSkillGap:
    """Integration tests for analyze_skill_gap()."""

    def test_returns_expected_structure(self, ds_skills):
        result = analyze_skill_gap(ds_skills, "Data Scientist")
        assert "predicted_role" in result
        assert "match_percentage" in result
        assert "matched_skills" in result
        assert "missing_skills" in result
        assert "priority_gaps" in result

    def test_match_percentage_range(self, ds_skills):
        result = analyze_skill_gap(ds_skills, "Data Scientist")
        mp = result["match_percentage"]
        assert 0.0 <= mp <= 100.0

    def test_high_match_for_matching_profile(self, ds_skills):
        """A strong DS profile should match well against DS role."""
        result = analyze_skill_gap(ds_skills, "Data Scientist")
        assert result["match_percentage"] >= 50.0

    def test_empty_skills_zero_match(self):
        result = analyze_skill_gap([], "Data Scientist")
        assert result["match_percentage"] == 0.0

    def test_perfect_match(self):
        """Providing all required skills should yield 100%."""
        role = "Web Developer"
        all_skills = list(COMPETENCY_MAPPING[role].keys())
        result = analyze_skill_gap(all_skills, role)
        assert result["match_percentage"] == 100.0
        assert len(result["missing_skills"]) == 0

    def test_matched_skills_format(self, ds_skills):
        result = analyze_skill_gap(ds_skills, "Data Scientist")
        for item in result["matched_skills"]:
            assert "skill" in item
            assert "priority" in item

    def test_priority_gaps_have_suggestions(self, ds_skills):
        """Priority gaps must include actionable suggestions."""
        # Use a skill set with intentionally missing critical skills
        partial_skills = ["SQL"]
        result = analyze_skill_gap(partial_skills, "ML Engineer")
        for gap in result["priority_gaps"]:
            assert "suggestion" in gap
            assert len(gap["suggestion"]) > 10

    def test_case_insensitive_skill_matching(self):
        """Skills like 'python' should match the required 'Python'."""
        result = analyze_skill_gap(["python", "sql", "machine learning"], "Data Scientist")
        assert result["match_percentage"] > 0

    def test_unknown_role_uses_defaults(self):
        result = analyze_skill_gap(["Communication"], "Galactic Overlord")
        assert result["match_percentage"] > 0
