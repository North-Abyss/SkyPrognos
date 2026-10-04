import os

import pandas as pd
import streamlit as st
from theme import apply_theme

st.set_page_config(page_title="Maintenance Schedule", layout="wide")
apply_theme()

st.title("Maintenance Schedule")
st.write("Automatically triggered maintenance tasks based on RUL predictions.")

tasks = pd.DataFrame(
    {
        "Task ID": ["T-001", "T-002"],
        "Aircraft": ["AC-104", "AC-103"],
        "Component": ["ENGINE_TURBINE_X", "HYDRAULIC_PUMP_Y"],
        "Due In (Cycles)": [12, 45],
        "Nearest Base": ["B001 (HQ Base Alpha)", "B003 (Reserve Base Charlie)"],
    }
)

st.dataframe(tasks, use_container_width=True)

st.subheader("Inventory Check")
try:
    if os.path.exists("data/parts.csv"):
        parts = pd.read_csv("data/parts.csv")
        st.dataframe(parts)
except (pd.errors.EmptyDataError, FileNotFoundError):
    st.error("Could not load parts data.")
