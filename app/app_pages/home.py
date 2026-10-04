import streamlit as st

st.title("SKYPROGNOS: FLEET HEALTH")
st.markdown("### 📡 AVIATION PREDICTIVE MAINTENANCE COMMAND CENTER")

# Create some spacing
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><h4>Fleet Availability</h4><h2>92%</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card warning"><h4>Watch Status</h4><h2>3 Units</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card critical"><h4>Critical AOG Risk</h4><h2>1 Unit</h2></div>', unsafe_allow_html=True)

st.write("---")
st.markdown("""
<div style='background: rgba(0,255,204,0.05); border: 1px solid rgba(0,255,204,0.2); padding: 20px; border-radius: 8px;'>
    <h4 style='color: #00ffcc; font-family: Orbitron; margin-top: 0;'>SYSTEM STATUS: ONLINE</h4>
    <p style='color: #e0e1dd; font-family: Inter; margin-bottom: 0;'>
        Telemetry stream synced. AI Prediction engines nominal.<br>
        Navigate using the top menu to view detailed Aircraft Telemetry, Fleet Status, and Maintenance Schedules.
    </p>
</div>
""", unsafe_allow_html=True)
