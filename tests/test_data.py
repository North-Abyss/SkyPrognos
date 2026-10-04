"""Tests for data pipeline."""

import numpy as np
import pandas as pd

from prognos.data.dataset import clip_rul, get_train_val_split


def test_leak_free_split():
    """Ensure no engine unit exists in both train and validation sets."""
    # Create mock dataframe
    df = pd.DataFrame(
        {
            "unit_nr": np.repeat(np.arange(1, 11), 5),  # 10 units, 5 rows each
            "time_cycles": np.tile(np.arange(1, 6), 10),
            "RUL": np.random.randint(0, 100, 50),
        }
    )

    train_df, val_df = get_train_val_split(df, val_ratio=0.2)

    train_units = set(train_df["unit_nr"].unique())
    val_units = set(val_df["unit_nr"].unique())

    # Assert no intersection (leak-free guarantee)
    assert len(train_units.intersection(val_units)) == 0, (
        "Data Leakage Detected! Engines overlapped."
    )
    assert len(train_units) == 8
    assert len(val_units) == 2


def test_rul_clipping():
    """Ensure RUL clipping works."""
    df = pd.DataFrame({"RUL": [100, 150, 200, 10]})
    clipped_df = clip_rul(df, max_rul=125)

    assert clipped_df["RUL"].max() == 125
    assert clipped_df["RUL"].iloc[0] == 100
    assert clipped_df["RUL"].iloc[3] == 10
