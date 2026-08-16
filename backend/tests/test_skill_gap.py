import pytest
import sys
import os

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.skill_gap import analyze_skill_gap, get_required_skills

def test_get_required_skills():
    skills = get_required_skills("Data Scientist")
    assert "Python" in skills
    assert skills["Python"] == "Critical"
    
def test_get_required_skills_fallback():
    skills = get_required_skills("Unknown Job")
    assert "Problem Solving" in skills

def test_analyze_skill_gap():
    candidate_skills = ["Python", "SQL", "Tableau"]
    target_role = "Data Analyst"
    
    result = analyze_skill_gap(candidate_skills, target_role)
    
    assert result["predicted_role"] == "Data Analyst"
    assert "match_percentage" in result
    
    matched = [m["skill"] for m in result["matched_skills"]]
    missing = [m["skill"] for m in result["missing_skills"]]
    
    assert "Python" in matched
    assert "SQL" in matched
    assert "Excel" in missing
