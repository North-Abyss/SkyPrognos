import pandas as pd
import streamlit as st

st.title("Mission Planner")
st.write("Assign aircraft to missions based on their predicted health.")

mission_length = st.number_input("Estimated Mission Duration (Cycles)", min_value=1, value=15)
mission_type = st.selectbox(
    "Mission Type", ["Standard Patrol", "High Stress Combat", "Reconnaissance"]
)

st.subheader("Recommended Aircraft")
# Simulated recommendation
df = pd.DataFrame(
    {
        "Aircraft": ["AC-101", "AC-102"],
        "Current RUL": [120, 85],
        "Risk Level": ["Low", "Low/Medium"],
    }
)
st.table(df)

if st.button("Assign AC-101 to Mission"):
    st.success("Aircraft AC-101 assigned to mission successfully.")
