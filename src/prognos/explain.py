"""Model explainability."""
import shap
import pandas as pd
import numpy as np

def get_xgboost_explanation(model, X_df: pd.DataFrame):
    """Get SHAP values for XGBoost model."""
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_df)
    return shap_values

def get_proxy_explanation(feature_cols: list, feature_values: np.ndarray):
    """
    Proxy explanation for neural models. 
    NOTE: This is a simulated proxy explanation for demonstration in the UI.
    It highlights sensors that deviate most from their scaled mean (0.5).
    """
    deviations = np.abs(feature_values - 0.5)
    
    # Flatten if it's a sequence
    if len(deviations.shape) > 1:
        deviations = deviations.mean(axis=0)
        
    top_indices = np.argsort(deviations)[-3:][::-1]
    
    return [
        {"sensor": feature_cols[i], "deviation": deviations[i]}
        for i in top_indices
    ]
