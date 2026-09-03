"""Integration tests for FastAPI v2 endpoints (/api/v2/*)."""

import os
import sys
import pytest

ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for p in [ROOT_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from fastapi.testclient import TestClient
    from main import app as fastapi_app
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not FASTAPI_AVAILABLE, reason="FastAPI dependencies not installed"
)


@pytest.fixture(scope="module")
def fastapi_client():
    if not FASTAPI_AVAILABLE:
        pytest.skip("FastAPI not available")
    return TestClient(fastapi_app)


class TestFastAPIHealth:
    def test_v2_health_returns_200(self, fastapi_client):
        resp = fastapi_client.get("/api/v2/health")
        assert resp.status_code == 200

    def test_v2_health_status_field(self, fastapi_client):
        resp = fastapi_client.get("/api/v2/health")
        body = resp.json()
        assert body.get("status") == "healthy"


class TestFastAPIPredict:
    def test_predict_with_raw_text(self, fastapi_client, ds_resume_text):
        resp = fastapi_client.post(
            "/api/v2/predict",
            data={"raw_text": ds_resume_text},
        )
        assert resp.status_code == 200

    def test_predict_response_structure(self, fastapi_client, ds_resume_text):
        resp = fastapi_client.post(
            "/api/v2/predict",
            data={"raw_text": ds_resume_text},
        )
        body = resp.json()
        assert "prediction" in body
        assert "parsed_data" in body

    def test_predict_missing_body_returns_error(self, fastapi_client):
        resp = fastapi_client.post("/api/v2/predict")
        assert resp.status_code in (400, 422)


class TestFastAPISkillGap:
    def test_skill_gap_endpoint(self, fastapi_client, ds_resume_text):
        payload = {
            "raw_text": ds_resume_text,
            "target_role": "Data Scientist",
        }
        resp = fastapi_client.post("/api/v2/skill-gap", json=payload)
        assert resp.status_code == 200

    def test_skill_gap_response_structure(self, fastapi_client, ds_resume_text):
        payload = {"raw_text": ds_resume_text, "target_role": "Data Scientist"}
        resp = fastapi_client.post("/api/v2/skill-gap", json=payload)
        body = resp.json()
        assert "gap_analysis" in body
        assert "candidate_skills" in body

    def test_skill_gap_auto_role_inference(self, fastapi_client, ds_resume_text):
        """If target_role is omitted, the API should infer it from the resume."""
        payload = {"raw_text": ds_resume_text}
        resp = fastapi_client.post("/api/v2/skill-gap", json=payload)
        assert resp.status_code == 200


class TestFastAPIRecommendation:
    def test_recommendation_endpoint(self, fastapi_client, ds_resume_text):
        payload = {"raw_text": ds_resume_text}
        resp = fastapi_client.post("/api/v2/recommendation", json=payload)
        assert resp.status_code == 200

    def test_recommendation_has_all_models(self, fastapi_client, ds_resume_text):
        payload = {"raw_text": ds_resume_text}
        resp = fastapi_client.post("/api/v2/recommendation", json=payload)
        body = resp.json()
        recs = body.get("recommendations", {})
        assert "logistic_regression" in recs
        assert "random_forest" in recs
