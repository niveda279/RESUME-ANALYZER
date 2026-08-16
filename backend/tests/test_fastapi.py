import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_fastapi_health_check():
    response = client.get("/api/v2/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "FastAPI CareerCast Service v2"}

def test_predict_raw_text():
    payload = {
        "raw_text": "I am a Data Scientist with 5 years of experience in Python, Machine Learning, and SQL."
    }
    response = client.post("/api/v2/predict", data=payload)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"
    assert "prediction" in data
    assert "parsed_data" in data
    
def test_predict_empty_text():
    payload = {"raw_text": ""}
    response = client.post("/api/v2/predict", data=payload)
    assert response.status_code == 400

def test_skill_gap_endpoint():
    payload = {
        "raw_text": "I know HTML, CSS, JavaScript, React, and Node.js.",
        "target_role": "Web Developer"
    }
    response = client.post("/api/v2/skill-gap", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "gap_analysis" in data
    gap = data["gap_analysis"]
    assert gap["predicted_role"] == "Web Developer"
    assert "matched_skills" in gap
    assert "missing_skills" in gap
