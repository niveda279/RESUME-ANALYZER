"""Integration tests for ML model loading and inference."""

import os
import sys
import pytest

ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for p in [ROOT_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from utils.ml_service import predict_all_models, get_best_model_prediction
from utils.ml_model import get_all_metrics, XGBOOST_AVAILABLE


class TestModelLoading:
    """Verify trained models load without errors."""

    def test_get_all_metrics_returns_dict(self):
        metrics = get_all_metrics()
        assert isinstance(metrics, dict)

    def test_metrics_has_model_keys(self):
        metrics = get_all_metrics()
        assert "logistic_regression" in metrics or "best_model" in metrics

    def test_predict_all_models_returns_dict(self, ds_resume_text):
        result = predict_all_models(ds_resume_text)
        assert isinstance(result, dict)

    def test_predict_all_has_three_models(self, ds_resume_text):
        result = predict_all_models(ds_resume_text)
        assert "logistic_regression" in result
        assert "random_forest" in result
        assert "xgboost" in result

    def test_predict_all_has_best_prediction(self, ds_resume_text):
        result = predict_all_models(ds_resume_text)
        assert "best_prediction" in result
        assert "best_model" in result

    def test_best_prediction_has_role(self, ds_resume_text):
        result = get_best_model_prediction(ds_resume_text)
        assert "predicted_role" in result
        assert result["predicted_role"] != ""

    def test_confidence_between_0_and_100(self, ds_resume_text):
        result = get_best_model_prediction(ds_resume_text)
        confidence = result.get("confidence", -1)
        assert 0.0 <= confidence <= 100.0

    def test_breakdown_is_list(self, ds_resume_text):
        result = get_best_model_prediction(ds_resume_text)
        breakdown = result.get("breakdown", [])
        assert isinstance(breakdown, list)

    def test_lr_prediction_role(self, ds_resume_text):
        result = predict_all_models(ds_resume_text)
        lr = result.get("logistic_regression", {})
        assert lr.get("predicted_role")

    def test_rf_prediction_role(self, ds_resume_text):
        result = predict_all_models(ds_resume_text)
        rf = result.get("random_forest", {})
        assert rf.get("predicted_role")

    def test_xgboost_available_or_graceful_fallback(self, ds_resume_text):
        """XGBoost may not be installed in all environments."""
        result = predict_all_models(ds_resume_text)
        xgb = result.get("xgboost", {})
        # Either has a real prediction or an error message (graceful fallback)
        assert "predicted_role" in xgb or "error" in xgb

    def test_webdev_resume_predicts_role(self, webdev_resume_text):
        result = get_best_model_prediction(webdev_resume_text)
        assert result.get("predicted_role")

    def test_swe_resume_predicts_role(self, swe_resume_text):
        result = get_best_model_prediction(swe_resume_text)
        assert result.get("predicted_role")
