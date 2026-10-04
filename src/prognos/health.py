"""Health scoring logic."""

def calculate_health_score(rul: float, max_rul: float = 125.0) -> float:
    """Convert RUL to a 0-100 Health Score."""
    score = (rul / max_rul) * 100
    return min(max(score, 0.0), 100.0)

def get_status_band(health_score: float) -> str:
    """Get the status band (Healthy/Watch/Warning/Critical)."""
    if health_score >= 75:
        return "Healthy"
    elif health_score >= 50:
        return "Watch"
    elif health_score >= 25:
        return "Warning"
    else:
        return "Critical"
