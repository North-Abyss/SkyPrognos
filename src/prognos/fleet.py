"""Fleet management logic."""
import pandas as pd
from typing import List, Dict

def rank_fleet(aircraft_data: List[Dict]) -> pd.DataFrame:
    """Rank fleet by health score (lowest first)."""
    df = pd.DataFrame(aircraft_data)
    if 'health_score' in df.columns:
        return df.sort_values(by='health_score', ascending=True).reset_index(drop=True)
    return df

def calculate_availability(aircraft_data: List[Dict]) -> float:
    """Calculate fleet availability % (Healthy or Watch)."""
    if not aircraft_data:
        return 0.0
    available_count = sum(1 for a in aircraft_data if a.get('status') in ['Healthy', 'Watch'])
    return (available_count / len(aircraft_data)) * 100.0
