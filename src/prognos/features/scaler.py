"""Feature scaling utilities."""

import json

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class RULScaler:
    """Scales sensor features. Fitted only on training data."""

    def __init__(self, feature_cols=None):
        self.scaler = MinMaxScaler()
        self.feature_cols = feature_cols

    def fit(self, df: pd.DataFrame):
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if c.startswith(("s_", "setting_"))]
        self.scaler.fit(df[self.feature_cols])

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_scaled = df.copy()
        df_scaled[self.feature_cols] = self.scaler.transform(df[self.feature_cols])
        return df_scaled

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.fit(df)
        return self.transform(df)

    def save(self, filepath: str):
        state = {
            "min_": self.scaler.min_.tolist(),
            "scale_": self.scaler.scale_.tolist(),
            "feature_cols": self.feature_cols,
        }
        with open(filepath, "w") as f:
            json.dump(state, f)

    def load(self, filepath: str):
        with open(filepath, "r") as f:
            state = json.load(f)
        self.feature_cols = state["feature_cols"]
        self.scaler = MinMaxScaler()
        self.scaler.min_ = np.array(state["min_"])
        self.scaler.scale_ = np.array(state["scale_"])
        self.scaler.data_min_ = np.zeros_like(self.scaler.min_)  # Dummy for consistency
        self.scaler.data_max_ = np.ones_like(self.scaler.scale_)  # Dummy
