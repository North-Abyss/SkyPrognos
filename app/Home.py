import streamlit as st
from theme import apply_theme

st.set_page_config(
    page_title="SkyPrognos - Mission Control",
    page_icon="✈️",
    layout="wide"
)

apply_theme()

pages = [
    st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
    st.Page("app_pages/1_Fleet.py", title="Fleet Overview", icon=":material/flight:"),
    st.Page("app_pages/2_Aircraft.py", title="Aircraft Telemetry", icon=":material/speed:"),
    st.Page("app_pages/3_Mission_Planner.py", title="Mission Planner", icon=":material/map:"),
    st.Page("app_pages/4_Maintenance.py", title="Maintenance", icon=":material/build:"),
    st.Page("app_pages/5_Edge_Sync.py", title="Edge Sync", icon=":material/sync:"),
    st.Page("app_pages/6_Runs.py", title="Training Runs", icon=":material/analytics:"),
]

page = st.navigation(pages, position="top")
page.run()
