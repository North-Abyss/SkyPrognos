"""Evaluation metrics for RUL prediction."""
import numpy as np
from sklearn.metrics import root_mean_squared_error

def nasa_score(y_true, y_pred):
    """
    Computes the NASA asymmetric scoring function for C-MAPSS.
    Penalizes late predictions (y_pred > y_true) more heavily than early predictions.
    """
    d = y_pred - y_true
    score = 0.0
    for error in d:
        if error < 0:
            score += np.exp(-error / 13.0) - 1
        else:
            score += np.exp(error / 10.0) - 1
    return score

def evaluate_predictions(y_true, y_pred):
    """Returns RMSE and NASA score."""
    rmse = root_mean_squared_error(y_true, y_pred)
    score = nasa_score(y_true, y_pred)
    return {'rmse': rmse, 'nasa_score': score}
