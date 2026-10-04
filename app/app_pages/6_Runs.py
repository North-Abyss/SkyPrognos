import json
import os

import pandas as pd
import streamlit as st
from theme import apply_theme

st.set_page_config(page_title="Training Runs", layout="wide")
apply_theme()

st.title("ML Training Runs")
st.write("History of model training runs and their footprints.")

runs = []
if os.path.exists("runs"):
    for f in os.listdir("runs"):
        if f.startswith("metadata_") and f.endswith(".json"):
            with open(os.path.join("runs", f), "r") as file:
                data = json.load(file)
                runs.append(
                    {
                        "Model": data.get("model"),
                        "Dataset": data.get("dataset"),
                        "RMSE": round(data.get("metrics", {}).get("rmse", 0), 2),
                        "NASA Score": round(data.get("metrics", {}).get("nasa_score", 0), 2),
                        "Params": data.get("footprint", {}).get("parameters"),
                        "Size (MB)": data.get("footprint", {}).get("size_mb"),
                        "Latency (ms)": data.get("footprint", {}).get("latency_ms"),
                    }
                )

if runs:
    st.dataframe(pd.DataFrame(runs), use_container_width=True)
else:
    st.info("No training runs found in `runs/`.")
