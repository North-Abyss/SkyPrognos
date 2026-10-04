import streamlit as st

st.title("Edge Synchronization")
st.write("Simulating intermittent connectivity from aircraft edge nodes to HQ.")

col1, col2 = st.columns(2)
with col1:
    link_status = st.toggle("Uplink Status", value=True)
    if link_status:
        st.success("Link Established (Online)")
    else:
        st.error("Link Severed (Offline)")

with col2:
    st.metric("Queued Messages (Outbox)", "14" if not link_status else "0")
    st.metric("Bandwidth Saved (vs Raw Telemetry)", "98.5%")

st.subheader("Sync Log")
if link_status:
    st.write("2026-10-04 10:15:22 - Synced Health Score for AC-104 (Critical)")
    st.write("2026-10-04 10:15:23 - Synced Health Score for AC-103 (Warning)")
else:
    st.write("Waiting for connection to flush outbox...")
