import streamlit as st
import pandas as pd
from theme import apply_theme

st.set_page_config(page_title="Fleet Overview", layout="wide")
apply_theme()

st.title("Fleet Overview")
st.write("Ranking all aircraft by Remaining Useful Life (RUL) and Health Score.")

# Mock data for UI demonstration purposes
fleet_data = pd.DataFrame({
    'Aircraft ID': ['AC-101', 'AC-102', 'AC-103', 'AC-104'],
    'RUL (Cycles)': [120, 85, 45, 12],
    'Health Score': [96, 68, 36, 9],
    'Status': ['Healthy', 'Watch', 'Warning', 'Critical']
})

st.dataframe(fleet_data, use_container_width=True)

st.subheader("Base Map")
st.map(pd.DataFrame({'lat': [35.123, 40.712, 34.052], 'lon': [-115.345, -74.006, -118.243]}))

