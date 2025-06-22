import redis
import time
import json
import sys
import csv
from datetime import datetime

print("[Worker] Starting log consumer...")
sys.stdout.flush()

r = redis.Redis(host='redis', port=6379, decode_responses=True)
csv_file = "traffic_logs.csv"

with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["timestamp", "request_count"])

while True:
    try:
        logs = r.hgetall("api_traffic")
        if logs:
            print(f"[Worker] {len(logs)} logs found:")
            current_minute = datetime.utcnow().replace(second=0, microsecond=0)
            request_count = len(logs)

            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_minute.isoformat(), request_count])

            for timestamp, payload in logs.items():
                print(f" - {timestamp}: {payload}")
            r.delete("api_traffic")
        else:
            print("[Worker] No new logs.")
        sys.stdout.flush()
    except Exception as e:
        print(f"[Worker] Error: {e}")
        sys.stdout.flush()

    time.sleep(60)
