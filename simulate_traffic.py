import requests
import time
import random

API_URL = "http://localhost:8000/log"
users = ["pushkaraj", "priya", "arjun", "simran", "admin"]

def send_log():
    payload = {"user": random.choice(users)}
    try:
        response = requests.post(API_URL, json=payload, timeout=2)
        print(f"Sent: {payload} → {response.status_code}")
    except Exception as e:
        print(f"Error sending request: {e}")

# Simulate bursts of traffic
for i in range(60):  # 60 bursts = ~10 minutes at 10s each
    for _ in range(random.randint(5, 15)):
        send_log()
        time.sleep(random.uniform(0.1, 0.4))  # simulate user activity
    print(f"--- [{i+1}] Burst completed ---")
    time.sleep(10)
