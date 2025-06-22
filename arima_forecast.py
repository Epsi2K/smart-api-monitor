import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import os
import threading

# --- CONFIGURATION ---
TRAFFIC_LOG = "app/traffic_logs.csv"
FORECAST_CSV = "forecast_30min.csv"
SCALE_LOG = "scaling_events.log"

SCALE_THRESHOLD = 25
SCALE_UP_TO = 3
SCALE_DOWN_TO = 1
SCALE_DOWN_AFTER = 30 * 60  # seconds

# --- Log Function ---
def log_scale_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SCALE_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# --- Load & Preprocess Data ---
df = pd.read_csv(TRAFFIC_LOG, parse_dates=["timestamp"])
df = df.groupby("timestamp", as_index=False).sum()
df.set_index("timestamp", inplace=True)
df = df.asfreq("min").fillna(0)  # Ensure 1-min frequency

# --- Plot Actual Traffic (Optional) ---
df.plot(figsize=(10, 4), title="Actual API Traffic")
plt.ylabel("Requests per Minute")
plt.tight_layout()
plt.show()

# --- Fit ARIMA Model ---
model = ARIMA(df, order=(3, 1, 2))
model_fit = model.fit()
print(model_fit.summary())

# --- Forecast Next 30 Minutes ---
forecast = model_fit.forecast(steps=30)
forecast_index = pd.date_range(start=df.index[-1] + pd.Timedelta(minutes=1), periods=30, freq="min")
forecast_df = pd.DataFrame({"timestamp": forecast_index, "forecast": forecast})
forecast_df.to_csv(FORECAST_CSV, index=False)

# --- Plot Forecast (Optional) ---
plt.figure(figsize=(10, 4))
plt.plot(df.index, df["request_count"], label="Actual")
plt.plot(forecast_index, forecast, label="Forecast", color="orange")
plt.title("ARIMA Forecast - Next 30 Minutes")
plt.legend()
plt.tight_layout()
plt.show()

# --- Auto-Scaling Logic ---
max_forecast = forecast.max()

if max_forecast > SCALE_THRESHOLD:
    msg = f"⚠️ Forecast spike: {max_forecast:.2f} req/min → Scaling up to {SCALE_UP_TO} containers..."
    print(msg)
    log_scale_event(msg)
    os.system(f"docker compose up --scale fastapi-app={SCALE_UP_TO} -d")

    # Schedule scale-down
    def scale_down():
        msg = f"🔽 Scaling down to {SCALE_DOWN_TO} container(s) after cooldown."
        print(msg)
        log_scale_event(msg)
        os.system(f"docker compose up --scale fastapi-app={SCALE_DOWN_TO} -d")

    print(f"⏳ Scheduling scale down in {SCALE_DOWN_AFTER // 60} minutes...")
    log_scale_event(f"Scheduled scale down in {SCALE_DOWN_AFTER // 60} minutes.")
    threading.Timer(SCALE_DOWN_AFTER, scale_down).start()
else:
    msg = f"✅ Forecast normal ({max_forecast:.2f} req/min). No scaling."
    print(msg)
    log_scale_event(msg)
