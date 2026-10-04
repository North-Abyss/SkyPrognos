import numpy as np
import pandas as pd
import streamlit as st
from theme import apply_theme

st.set_page_config(page_title="Aircraft Telemetry", layout="wide")
apply_theme()

st.title("Aircraft Telemetry & Live Prediction")

aircraft_id = st.selectbox("Select Aircraft", ["AC-101", "AC-102", "AC-103", "AC-104"])
st.write(f"### Replaying telemetry for {aircraft_id} (Simulation)")

cycle = st.slider("Cycle Replay", min_value=1, max_value=200, value=150)

# Dummy telemetry plot
chart_data = pd.DataFrame(
    np.random.randn(cycle, 3),
    columns=["Sensor 1 (Vibration)", "Sensor 2 (Temp)", "Sensor 3 (Pressure)"],
)
st.line_chart(chart_data)

st.subheader("Current Prediction")
rul_pred = 200 - cycle
st.metric("Predicted Remaining Useful Life (RUL)", f"{rul_pred} cycles")

st.markdown("""
**Note:** This is a simulated replay of historical sensor data passing through our ML model.
""")
