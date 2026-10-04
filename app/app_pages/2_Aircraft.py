from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw

st.title("AIRCRAFT TELEMETRY")
st.markdown("### 📡 LIVE SYSTEM HEALTH & DIGITAL TWIN")

aircraft_id = st.selectbox("Select Active Tail Number", ["AC-101", "AC-102", "AC-103", "AC-104"])
st.write("---")

col1, col2 = st.columns([1.2, 2])

BLUEPRINT_PATH = Path(__file__).parent.parent / "assets" / "aircraft_blueprint.jpg"

from typing import TypedDict


class DamageZone(TypedDict):
    name: str
    pos: tuple[int, int]
    radius: int

# Damage hotspot pixel coordinates on the 1024x1024 blueprint
DAMAGE_ZONES: list[DamageZone] = [
    {"name": "Left Engine",    "pos": (340, 580), "radius": 45},
    {"name": "Right Engine",   "pos": (680, 580), "radius": 45},
    {"name": "Avionics Bay",   "pos": (512, 250), "radius": 35},
    {"name": "Tail Hydraulics","pos": (512, 820), "radius": 35},
]

def render_blueprint_with_damage(cycle: int, max_cycle: int = 200):
    """Overlay red damage zones onto the aircraft blueprint."""
    try:
        img = Image.open(BLUEPRINT_PATH).convert("RGBA")
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
    
        damage_pct = min(cycle / max_cycle, 1.0)  # 0.0 → 1.0
    
        for zone in DAMAGE_ZONES:
            alpha = int(180 * damage_pct)       # fade in 0→180
            r = int(zone["radius"] * (0.6 + 0.4 * damage_pct))  # grow radius
            x, y = zone["pos"]
            # Outer glow
            draw.ellipse([x-r*2, y-r*2, x+r*2, y+r*2],
                         fill=(255, 0, 0, alpha // 4))
            # Inner hotspot
            draw.ellipse([x-r, y-r, x+r, y+r],
                         fill=(255, 40, 40, alpha))
        
        return Image.alpha_composite(img, overlay)
    except FileNotFoundError:
        return None

with col2:
    cycle = st.slider("Mission Timeline Replay (Cycles)", min_value=1, max_value=200, value=150)
    
    st.markdown("#### LIVE TELEMETRY FEED")
    # Simulate telemetry degradation over time
    base_noise = np.random.randn(cycle, 3)
    degradation_curve = (np.arange(cycle) / 200.0) ** 2
    chart_data = pd.DataFrame(
        base_noise + degradation_curve[:, np.newaxis] * 5,
        columns=["Turbine Temp (°C)", "Hydraulic Pressure", "Compressor Vibration"],
    )
    st.line_chart(chart_data)
    
    rul_pred = 200 - cycle
    status = "healthy" if rul_pred > 50 else "warning" if rul_pred > 15 else "critical"
    
    st.markdown(f'<div class="metric-card {status}"><h4>Edge Neural Network RUL Prediction</h4><h2>{rul_pred} CYCLES LEFT</h2></div>', unsafe_allow_html=True)


with col1:
    st.markdown("#### DIGITAL TWIN SCAN")
    
    damaged_img = render_blueprint_with_damage(cycle)
    if damaged_img:
        st.image(damaged_img, width="stretch", alt="Aircraft digital twin blueprint with damage overlay")
    else:
        st.error("Blueprint image not found in assets.")
        
    st.caption("SCANNING INTERNAL SENSORS: ENGINE, HYDRAULICS, COMPRESSOR")


st.write("---")
st.markdown("""
<div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;'>
    <p style='color: #8fa6c4; font-family: Inter; margin-bottom: 0; font-size: 0.9em;'>
        <strong>Note:</strong> This panel simulates raw sensor telemetry processing through the onboard 
        Edge AI (Tiny-CNN). The visual blueprint highlights the specific sub-systems currently under extreme load.
    </p>
</div>
""", unsafe_allow_html=True)
