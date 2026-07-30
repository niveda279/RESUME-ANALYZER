import os
import sys

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(__file__))

from utils.ml_model import train_and_save_model

if __name__ == '__main__':
    print("Training Logistic Regression model on dataset...")
    metrics = train_and_save_model()
    print("Model Training Completed Successfully!")
    print("Model Metrics:")
    print(f"  Algorithm: {metrics.get('algorithm')}")
    print(f"  Accuracy:  {metrics.get('accuracy')}%")
    print(f"  Precision: {metrics.get('precision')}%")
    print(f"  Recall:    {metrics.get('recall')}%")
    print(f"  F1 Score:  {metrics.get('f1_score')}%")
