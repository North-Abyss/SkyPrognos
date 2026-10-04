"""XGBoost baseline model."""
import xgboost as xgb
import pandas as pd
import numpy as np

class XGBoostBaseline:
    def __init__(self, **kwargs):
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
            **kwargs
        )
        
    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        self.model.fit(X_train, y_train)
        
    def predict(self, X_test: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X_test)
        
    def get_booster(self):
        return self.model.get_booster()
