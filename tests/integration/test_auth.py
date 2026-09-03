"""Integration tests for authentication endpoints (Flask API)."""

import os
import sys
import json
import pytest

ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for p in [ROOT_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)


class TestAuthEndpoints:
    """Tests for /api/register and /api/login."""

    # ── Login ──────────────────────────────────────────────────────────────

    def test_admin_login_success(self, flask_client):
        resp = flask_client.post(
            "/api/login",
            data=json.dumps({"email": "admin@careercast.com", "password": "Admin@123456"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "token" in data
        assert data["user"]["role"] == "admin"

    def test_user_login_success(self, flask_client):
        resp = flask_client.post(
            "/api/login",
            data=json.dumps({"email": "user@careercast.com", "password": "User@123456"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "token" in data

    def test_invalid_password(self, flask_client):
        resp = flask_client.post(
            "/api/login",
            data=json.dumps({"email": "admin@careercast.com", "password": "wrong_password"}),
            content_type="application/json",
        )
        assert resp.status_code in (401, 403)

    def test_unknown_email(self, flask_client):
        resp = flask_client.post(
            "/api/login",
            data=json.dumps({"email": "nobody@nowhere.com", "password": "pass"}),
            content_type="application/json",
        )
        assert resp.status_code in (401, 404)

    def test_missing_email_field(self, flask_client):
        resp = flask_client.post(
            "/api/login",
            data=json.dumps({"password": "Admin@123456"}),
            content_type="application/json",
        )
        assert resp.status_code in (400, 401)

    # ── Token validation ───────────────────────────────────────────────────

    def test_protected_route_without_token(self, flask_client):
        """History endpoint should reject requests without token."""
        resp = flask_client.get("/api/history")
        assert resp.status_code in (401, 403)

    def test_protected_route_with_invalid_token(self, flask_client):
        resp = flask_client.get(
            "/api/history",
            headers={"Authorization": "Bearer invalidtoken123"},
        )
        assert resp.status_code in (401, 403)

    def test_protected_route_with_valid_token(self, flask_client, user_token):
        resp = flask_client.get(
            "/api/history",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == 200
