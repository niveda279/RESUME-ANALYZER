"""
train_model.py — Retrain all CareerCast ML models

Trains Logistic Regression, Random Forest, and XGBoost on the resume dataset.
Run:  python train_model.py
"""

import os
import sys

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(__file__))

from utils.ml_model import train_and_save_model

if __name__ == '__main__':
    print("=" * 60)
    print("  CareerCast — ML Model Training Pipeline")
    print("=" * 60)
    print()

    all_metrics = train_and_save_model()

    print()
    print("=" * 60)
    print("  Training Complete — Results Summary")
    print("=" * 60)

    for key, name in [
        ("logistic_regression", "Logistic Regression"),
        ("random_forest",       "Random Forest"),
        ("xgboost",             "XGBoost")
    ]:
        m = all_metrics.get(key, {})
        print(f"\n  {name}:")
        print(f"    Accuracy:  {m.get('accuracy',  0)}%")
        print(f"    Precision: {m.get('precision', 0)}%")
        print(f"    Recall:    {m.get('recall',    0)}%")
        print(f"    F1 Score:  {m.get('f1_score',  0)}%")
        if m.get("error"):
            print(f"    ⚠  {m['error']}")

    best = all_metrics.get("best_model", "Unknown")
    print(f"\n  [BEST] Best Model (by F1): {best}")
    print("=" * 60)
