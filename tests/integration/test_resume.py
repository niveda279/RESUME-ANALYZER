"""Integration tests for resume upload, parsing, and history endpoints."""

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


def _make_txt_file(text: str, filename="test_resume.txt"):
    """Create an in-memory file-like object to use in multipart uploads."""
    return (io.BytesIO(text.encode("utf-8")), filename)


class TestResumeEndpoints:
    """Tests for /api/upload, /api/analysis/<id>, /api/history, /api/skill-gap."""

    def test_upload_without_token(self, flask_client, ds_resume_text):
        data = {"file": _make_txt_file(ds_resume_text)}
        resp = flask_client.post("/api/upload", data=data, content_type="multipart/form-data")
        assert resp.status_code in (401, 403)

    def test_upload_no_file(self, flask_client, user_token):
        resp = flask_client.post(
            "/api/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            content_type="multipart/form-data",
        )
        assert resp.status_code == 400

    def test_upload_txt_resume_returns_201(self, flask_client, user_token, ds_resume_text):
        data = {"file": _make_txt_file(ds_resume_text, "ds_resume.txt")}
        resp = flask_client.post(
            "/api/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            data=data,
            content_type="multipart/form-data",
        )
        assert resp.status_code == 201, f"Unexpected status: {resp.status_code}\n{resp.data}"

    def test_upload_response_structure(self, flask_client, user_token, ds_resume_text):
        data = {"file": _make_txt_file(ds_resume_text, "ds_resume2.txt")}
        resp = flask_client.post(
            "/api/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            data=data,
            content_type="multipart/form-data",
        )
        assert resp.status_code == 201
        body = json.loads(resp.data)
        assert "id" in body
        assert "prediction" in body
        assert "green_flags" in body
        assert "red_flags" in body
        assert "parsed_entities" in body
        assert "all_predictions" in body

    def test_upload_prediction_has_role(self, flask_client, user_token, ds_resume_text):
        data = {"file": _make_txt_file(ds_resume_text, "ds_resume3.txt")}
        resp = flask_client.post(
            "/api/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            data=data,
            content_type="multipart/form-data",
        )
        assert resp.status_code == 201
        body = json.loads(resp.data)
        pred = body.get("prediction", {})
        assert pred.get("predicted_role")
        assert 0 <= pred.get("confidence", -1) <= 100

    def test_history_returns_list(self, flask_client, user_token):
        resp = flask_client.get(
            "/api/history",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert "resumes" in body
        assert isinstance(body["resumes"], list)

    def test_skill_gap_endpoint(self, flask_client, user_token, ds_skills):
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
        gap = body["gap_analysis"]
        assert "match_percentage" in gap

    def test_skill_gap_missing_role(self, flask_client, user_token):
        payload = {"skills": ["Python", "SQL"]}
        resp = flask_client.post(
            "/api/skill-gap",
            headers={"Authorization": f"Bearer {user_token}"},
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_health_endpoint(self, flask_client):
        resp = flask_client.get("/api/health")
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["status"] == "healthy"
