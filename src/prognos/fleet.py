"""Fleet management logic."""

import pandas as pd


def rank_fleet(aircraft_data: list[dict]) -> pd.DataFrame:
    """Rank fleet by health score (lowest first)."""
    df = pd.DataFrame(aircraft_data)
    if "health_score" in df.columns:
        return df.sort_values(by="health_score", ascending=True).reset_index(drop=True)
    return df


def calculate_availability(aircraft_data: list[dict]) -> float:
    """Calculate fleet availability % (Healthy or Watch)."""
    if not aircraft_data:
        return 0.0
    available_count = sum(1 for a in aircraft_data if a.get("status") in ["Healthy", "Watch"])
    return (available_count / len(aircraft_data)) * 100.0
