import streamlit as st
from theme import apply_theme

st.set_page_config(
    page_title="SkyPrognos - Mission Control",
    page_icon="✈️",
    layout="wide"
)

apply_theme()

st.title("SkyPrognos: Fleet Health Platform")
st.markdown("### Aviation Predictive Maintenance Command Center")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><h4>Fleet Availability</h4><h2>92%</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card warning"><h4>Watch Status</h4><h2>3</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card critical"><h4>Critical AOG Risk</h4><h2>1</h2></div>', unsafe_allow_html=True)

st.write("---")
st.write("Navigate using the sidebar to view Fleet Status, Aircraft Telemetry, and Maintenance Scheduling.")
