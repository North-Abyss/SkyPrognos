"""C-MAPSS Data Loader and processing."""

import numpy as np
import pandas as pd

COLUMN_NAMES = ["unit_nr", "time_cycles", "setting_1", "setting_2", "setting_3"] + [
    f"s_{i}" for i in range(1, 22)
]


def load_data(data_path: str, is_test: bool = False, rul_path: str | None = None) -> pd.DataFrame:
    """Load C-MAPSS data from text file."""
    df = pd.read_csv(data_path, sep=r"\s+", header=None, names=COLUMN_NAMES)

    if not is_test:
        # Calculate RUL based on max cycle per unit
        rul = pd.DataFrame(df.groupby("unit_nr")["time_cycles"].max()).reset_index()
        rul.columns = ["unit_nr", "max_cycle"]
        df = df.merge(rul, on=["unit_nr"], how="left")
        df["RUL"] = df["max_cycle"] - df["time_cycles"]
        df.drop("max_cycle", axis=1, inplace=True)
    else:
        # For test data, we just have the features up to a cutoff point.
        # If rul_path is provided, we can reconstruct the RUL at the LAST cycle of each unit.
        pass

    return df


def clip_rul(df: pd.DataFrame, max_rul: int = 125) -> pd.DataFrame:
    """Clip RUL values to a maximum threshold (e.g., 125)."""
    if "RUL" in df.columns:
        df["RUL"] = df["RUL"].clip(upper=max_rul)
    return df


def get_train_val_split(
    df: pd.DataFrame, val_ratio: float = 0.2, random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split data strictly by engine unit, never by row. Ensures leak-free validation."""
    units = df["unit_nr"].unique()
    np.random.seed(random_state)
    np.random.shuffle(units)

    split_idx = int(len(units) * (1 - val_ratio))
    train_units = units[:split_idx]
    val_units = units[split_idx:]

    train_df = df[df["unit_nr"].isin(train_units)].copy()
    val_df = df[df["unit_nr"].isin(val_units)].copy()

    return train_df, val_df


def create_sliding_windows(
    df: pd.DataFrame, sequence_length: int, feature_cols: list
) -> tuple[np.ndarray, np.ndarray]:
    """Generate 3D sequences for neural networks (batch, seq_len, features)."""
    X, y = [], []
    for unit_id, group in df.groupby("unit_nr"):
        data = group[feature_cols].values
        labels = group["RUL"].values if "RUL" in group.columns else np.zeros(len(data))

        for i in range(len(data) - sequence_length + 1):
            X.append(data[i : i + sequence_length])
            y.append(labels[i + sequence_length - 1])

    return np.array(X), np.array(y)
