# 🚀 Smart API Monitor

A smart, containerized, autoscaling system built to monitor API traffic in real-time, forecast future load using ARIMA, and dynamically scale FastAPI containers based on predicted spikes. It includes a Streamlit dashboard for live insights.

---

## 📊 Project Overview

The **Smart API Monitor** is a production-grade microservice infrastructure that:

- Monitors API traffic in real-time.
- Forecasts request load using time-series analysis.
- Automatically scales FastAPI containers up/down.
- Logs scaling events for audit and analysis.
- Presents all this via an interactive Streamlit dashboard.

---

## 🚀 Objective

To simulate a realistic DevOps + AI setup that combines:

- API traffic ingestion
- Queuing & background processing
- Predictive analytics using ARIMA
- Auto-scaling based on traffic forecasts
- Real-time observability

Ideal for showcasing AI-augmented DevOps skills or bootstrapping a production-ready autoscaling logic demo.

---

## ⚙️ Architecture Diagram

```text
+-------------+       +----------------+       +----------------+       +------------------------+
| API Clients | --->  |  FastAPI App   | --->  |   Redis Queue  | --->  |  Background Consumer   |
+-------------+       +----------------+       +----------------+       +------------------------+
                                                              |
                                                              v
                                                  +---------------------+
                                                  |  traffic_logs.csv   |
                                                  +---------------------+
                                                              |
                                                              v
                +-------------------+        +----------------------+         +-----------------------+
                | ARIMA Forecaster  | -----> | Auto-scaler (Docker) | ----->  | scaling_events.log    |
                +-------------------+        +----------------------+         +-----------------------+
                                                              |
                                                              v
                                                      +----------------+
                                                      | Streamlit UI   |
                                                      +----------------+
```

---

## 🧰 Tech Stack

| Layer           | Tech                                    |
| --------------- | --------------------------------------- |
| API Layer       | FastAPI, Uvicorn                        |
| Messaging Queue | Redis (Pub/Sub)                         |
| Forecasting     | ARIMA (statsmodels), pandas, matplotlib |
| Backend Infra   | Docker, Docker Compose                  |
| Dashboard       | Streamlit                               |
| Autoscaling     | Docker CLI + Python `os.system`         |

---

## 📦 Project Structure

```bash
smart-api-monitor/
|
├── app/                    # FastAPI backend service
│   ├── main.py
│   └── traffic_logs.csv
|
├── consumer/               # Redis log consumer
│   └── log_consumer.py
|
├── dashboard.py            # Streamlit UI
├── arima_forecast.py       # Forecast + autoscale
├── simulate_traffic.py     # Load generator for testing
├── scaling_events.log      # Logs scale-up/scale-down events
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚪 Getting Started

### 1. Clone the Repo

```bash
git clone 'repository_path'
cd smart-api-monitor
```

### 2. Build & Run with Docker

```bash
docker compose up --build
```

### 3. Start Traffic Simulation

```bash
python simulate_traffic.py
```

### 4. Run ARIMA Forecast + Auto-Scaler

```bash
python arima_forecast.py
```

### 5. Launch the Streamlit Dashboard

```bash
streamlit run dashboard.py
```

---

## 🔢 Forecasting Logic & Auto-Scaling

- Uses `ARIMA(3,1,2)` model to predict next 30 minutes of traffic.
- If `forecast > 25 req/min`: scales to 3 FastAPI containers.
- Auto-scales back to 1 container after 30 minutes.
- All actions logged in `scaling_events.log`

---

## 💡 Workflow Summary

1. Simulate incoming traffic via HTTP POST requests.
2. Logs are queued via Redis.
3. Background consumer stores requests in `traffic_logs.csv`.
4. `arima_forecast.py` predicts the next 30 minutes.
5. If spike predicted, it triggers Docker scale up.
6. After cooldown, system auto-scales down.
7. Streamlit dashboard visualizes everything in real-time.

---

## 📘 Dashboard Preview

### 🔄 Live API Traffic

![Live Traffic Graph](screenshots\Smart-API-Dashboard.png)

### 🔮 30-Min ARIMA Forecast

![Forecast Graph](screenshots\ARIMA.png)

### ⚙️ Autoscaling Events Log

![Scaling Events](screenshots\Scaling-Events-Log.png)

---

## ✨ Future Enhancements

- ***

## 📄 License

MIT © 2025 Pushkaraj Bhor

> Designed for intelligent DevOps. Predict, scale, repeat. ✨
