"""Efficiency footprint tracking."""
import time
import os
import psutil
import pandas as pd
import numpy as np
from typing import Dict, Any

def get_footprint(model: Any, dummy_input: np.ndarray, model_type: str = "xgboost") -> Dict[str, Any]:
    """Measures model footprint: parameters, RAM, inference latency."""
    # 1. Parameter count
    if model_type == "xgboost":
        # Rough estimate of tree size
        params = sum(1 for _ in model.get_booster().get_dump()) * 100 # Approx nodes per tree
    elif model_type == "pytorch":
        params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    else:
        params = 0

    # 2. Peak RAM (approximation by monitoring before and after allocation, though tricky in Python)
    # A better proxy for edge deployment is measuring serialized size
    import tempfile
    import joblib
    with tempfile.NamedTemporaryFile() as tmp:
        if model_type == "xgboost":
            joblib.dump(model, tmp.name)
        elif model_type == "pytorch":
            import torch
            torch.save(model.state_dict(), tmp.name)
        
        size_mb = os.path.getsize(tmp.name) / (1024 * 1024)
        
    # 3. CPU Inference Latency
    times = []
    for _ in range(10): # Warmup
        _ = model.predict(dummy_input) if model_type == "xgboost" else model(dummy_input)
        
    for _ in range(100):
        start = time.perf_counter()
        _ = model.predict(dummy_input) if model_type == "xgboost" else model(dummy_input)
        times.append((time.perf_counter() - start) * 1000) # ms
        
    latency_ms = np.median(times)
    
    return {
        "parameters": params,
        "size_mb": round(size_mb, 2),
        "latency_ms": round(latency_ms, 2)
    }
