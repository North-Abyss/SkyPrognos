"""Custom Streamlit Theme and UI Utilities."""
import streamlit as st

def apply_theme():
    """Apply dark mission control theme."""
    st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .metric-card {
            background-color: #1E2127;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .metric-card.warning {
            border-left-color: #FFC107;
        }
        .metric-card.critical {
            border-left-color: #F44336;
        }
        </style>
    """, unsafe_allow_html=True)
