import pytest
import os
import sys

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ml_model import get_all_metrics

def test_model_accuracy_gate():
    """
    Accuracy gate that fails the CI pipeline if the model accuracy 
    falls below a configurable threshold.
    """
    threshold_str = os.environ.get("MODEL_ACCURACY_THRESHOLD", "0.80")
    threshold = float(threshold_str) * 100  # Convert to percentage
    
    metrics = get_all_metrics()
    
    # We want to check the best model's accuracy
    best_key = metrics.get("best_model_key")
    assert best_key is not None, "Could not determine the best model."
    
    best_metrics = metrics.get(best_key, {})
    accuracy = best_metrics.get("accuracy", 0.0)
    
    assert accuracy >= threshold, f"Model accuracy ({accuracy}%) is below the required threshold ({threshold}%)."
