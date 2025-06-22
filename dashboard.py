import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Smart API Traffic Dashboard", layout="wide")

st.title("📊 Smart API Traffic Dashboard")

# --- Section: Live Traffic ---
st.header("🔄 Live API Traffic")

try:
    traffic_df = pd.read_csv("app/traffic_logs.csv", parse_dates=["timestamp"])
    traffic_df.set_index("timestamp", inplace=True)

    st.line_chart(traffic_df["request_count"], use_container_width=True)

except Exception as e:
    st.error(f"❌ Could not load traffic data: {e}")

# --- Section: Forecast ---
st.header("🔮 ARIMA Forecast")

try:
    forecast_df = pd.read_csv("forecast_30min.csv", parse_dates=["timestamp"])
    forecast_df.set_index("timestamp", inplace=True)

    st.line_chart(forecast_df["forecast"], use_container_width=True)

except Exception as e:
    st.warning(f"⚠️ No forecast data found yet: {e}")

# --- Section: Scaling Log ---
st.header("📁 Scaling Events Log")

try:
    with open("scaling_events.log", "r", encoding="utf-8") as f:
        logs = f.readlines()

    if logs:
        st.code("".join(logs[-10:]), language="text")
    else:
        st.info("No scaling events logged yet.")

except FileNotFoundError:
    st.info("No scaling events log found.")

# --- Refresh Button ---
st.button("🔁 Refresh")
