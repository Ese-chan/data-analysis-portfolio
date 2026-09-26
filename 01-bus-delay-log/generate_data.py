"""Generate a synthetic bus arrival log for Project 01.

Stdlib only - no third-party packages required.
Output: data/bus_arrivals.csv
"""
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

START = date(2025, 6, 2)          # a Monday
DAYS = 60
ROUTES = ["12", "14", "27"]
STOPS = {
    "S001": "Central Station",
    "S002": "Market Street",
    "S003": "Riverside Park",
    "S004": "University Gate",
    "S005": "Industrial Estate",
    "S006": "Harbor Road",
}
# Two routes are chronically worse than the third.
ROUTE_BIAS = {"12": 2.0, "14": 4.0, "27": 0.5}

rows = []
for d in range(DAYS):
    day = START + timedelta(days=d)
    weekday = day.weekday() < 5
    for route in ROUTES:
        for stop_id, stop_name in STOPS.items():
            for seq in range(4):                      # 4 trips: 06:20, 09:20, 12:20, 15:20
                sched = datetime(day.year, day.month, day.day, 6 + seq * 3, 20)
                # Rush-hour trips accumulate more delay than midday trips.
                peak = 2.0 if sched.hour in (6, 15) else 0.5
                weekend = 0.0 if weekday else -1.0
                delay = random.gauss(ROUTE_BIAS[route] + peak + weekend, 2.5)
                delay = round(max(-2.0, min(delay, 25.0)), 1)
                actual = sched + timedelta(minutes=delay)
                rows.append([
                    day.isoformat(),
                    route,
                    stop_id,
                    stop_name,
                    sched.strftime("%H:%M"),
                    actual.strftime("%H:%M"),
                    delay,
                ])

# 2% of buses never logged an actual arrival time.
for row in rows:
    if random.random() < 0.02:
        row[5] = ""
        row[6] = ""

random.shuffle(rows)

out = DATA_DIR / "bus_arrivals.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "route_id", "stop_id", "stop_name",
                     "scheduled_arrival", "actual_arrival", "delay_minutes"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {out}")
