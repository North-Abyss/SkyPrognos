"""Custom Streamlit Theme and UI Utilities."""
import streamlit as st


def apply_theme():
    """Apply premium aviation command center theme."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Orbitron:wght@500;700&display=swap');
        
        /* Global Background & Font */
        .stApp {
            background: radial-gradient(circle at top right, #050d1a, #000000 80%);
            color: #e0e1dd;
            font-family: 'Inter', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #00ffcc;
            text-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
        }
        
        /* Glassmorphism Metric Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(0, 255, 204, 0.2);
            padding: 25px;
            border-radius: 12px;
            border-left: 5px solid #00ffcc;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px 0 rgba(0, 255, 204, 0.25);
            border-color: rgba(0, 255, 204, 0.6);
        }
        
        /* Sweep Animation Effect */
        .metric-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: -150%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: skewX(-20deg);
            animation: sweep 4s infinite;
        }
        
        @keyframes sweep {
            0% { left: -150%; }
            50% { left: 150%; }
            100% { left: 150%; }
        }
        
        .metric-card h4 {
            font-size: 1rem;
            text-transform: uppercase;
            color: #8fa6c4;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        
        .metric-card h2 {
            font-size: 3.2rem;
            margin: 0;
            color: #ffffff;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        }
        
        /* Status Modifiers */
        .metric-card.warning {
            border-left-color: #ff9f1c;
            border-color: rgba(255, 159, 28, 0.2);
        }
        .metric-card.warning h2 {
            color: #ff9f1c;
            text-shadow: 0 0 20px rgba(255, 159, 28, 0.4);
        }
        .metric-card.warning:hover {
            box-shadow: 0 15px 40px 0 rgba(255, 159, 28, 0.25);
            border-color: rgba(255, 159, 28, 0.6);
        }
        
        .metric-card.critical {
            border-left-color: #e63946;
            border-color: rgba(230, 57, 70, 0.2);
            animation: pulse-red-border 2s infinite;
        }
        .metric-card.critical h2 {
            color: #e63946;
            text-shadow: 0 0 20px rgba(230, 57, 70, 0.6);
        }
        .metric-card.critical:hover {
            box-shadow: 0 15px 40px 0 rgba(230, 57, 70, 0.3);
            border-color: rgba(230, 57, 70, 0.8);
        }
        
        @keyframes pulse-red-border {
            0% { box-shadow: 0 0 0 0 rgba(230, 57, 70, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(230, 57, 70, 0); }
            100% { box-shadow: 0 0 0 0 rgba(230, 57, 70, 0); }
        }
        
        /* Top navigation dock styling */
        [data-testid="stNavigation"] {
            background: rgba(5, 13, 26, 0.95) !important;
            border-bottom: 1px solid rgba(0, 255, 204, 0.15);
        }
        
        /* Dataframes */
        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 10px;
            border: 1px solid rgba(255,255,255,0.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        /* Hide streamlit footer branding */
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
