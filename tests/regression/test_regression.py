"""
Regression tests — verify that all Milestone 1–3 features still work correctly.

These tests act as a stability guard. If any previously working feature breaks,
these tests will catch it before it reaches production.
"""

import io
import os
import sys
import json
import pytest

ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for p in [ROOT_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)


class TestMilestone1Regression:
    """M1: Resume parsing and entity extraction still work."""

    def test_parse_returns_name(self, ds_resume_text):
        from utils.parser import parse_resume_text
        result = parse_resume_text(ds_resume_text)
        assert result["name"] != ""

    def test_parse_returns_email(self, ds_resume_text):
        from utils.parser import parse_resume_text
        result = parse_resume_text(ds_resume_text)
        assert "@" in result["email"]

    def test_parse_skills_non_empty(self, ds_resume_text):
        from utils.parser import parse_resume_text
        result = parse_resume_text(ds_resume_text)
        assert len(result["skills"]) > 0

    def test_flags_evaluation_returns_both_lists(self, ds_resume_text):
        from utils.parser import parse_resume_text
        from utils.feature_extractor import evaluate_flags
        parsed = parse_resume_text(ds_resume_text)
        flags = evaluate_flags(parsed)
        assert "green_flags" in flags and "red_flags" in flags


class TestMilestone2Regression:
    """M2: Flask API authentication and database operations still work."""

    def test_health_endpoint_ok(self, flask_client):
        resp = flask_client.get("/api/health")
        assert resp.status_code == 200

    def test_admin_login_ok(self, flask_client):
        resp = flask_client.post(
            "/api/login",
            data=json.dumps({"email": "admin@careercast.com", "password": "Admin@123456"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert "token" in json.loads(resp.data)

    def test_history_endpoint_requires_auth(self, flask_client):
        resp = flask_client.get("/api/history")
        assert resp.status_code in (401, 403)

    def test_authenticated_history_works(self, flask_client, user_token):
        resp = flask_client.get(
            "/api/history",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == 200

    def test_ml_comparison_endpoint(self, flask_client):
        resp = flask_client.get("/api/ml-comparison")
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert isinstance(body, dict)


class TestMilestone3Regression:
    """M3: Multi-model prediction and skill gap analysis still work."""

    def test_all_three_models_predict(self, ds_resume_text):
        from utils.ml_service import predict_all_models
        result = predict_all_models(ds_resume_text)
        assert "logistic_regression" in result
        assert "random_forest" in result
        assert "xgboost" in result

    def test_best_prediction_is_returned(self, ds_resume_text):
        from utils.ml_service import predict_all_models
        result = predict_all_models(ds_resume_text)
        assert "best_prediction" in result
        assert result["best_prediction"].get("predicted_role")

    def test_skill_gap_analyze_still_works(self, ds_skills):
        from services.skill_gap import analyze_skill_gap
        result = analyze_skill_gap(ds_skills, "Data Scientist")
        assert result["match_percentage"] >= 0

    def test_skill_gap_via_flask_api(self, flask_client, user_token, ds_skills):
        payload = {"skills": ds_skills, "target_role": "Data Scientist"}
        resp = flask_client.post(
            "/api/skill-gap",
            headers={"Authorization": f"Bearer {user_token}"},
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert "gap_analysis" in body

    def test_upload_response_has_all_predictions(self, flask_client, user_token, swe_resume_text):
        data = {
            "file": (io.BytesIO(swe_resume_text.encode("utf-8")), "swe_reg_test.txt")
        }
        resp = flask_client.post(
            "/api/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            data=data,
            content_type="multipart/form-data",
        )
        assert resp.status_code == 201
        body = json.loads(resp.data)
        all_preds = body.get("all_predictions", {})
        assert "logistic_regression" in all_preds
        assert "random_forest" in all_preds
