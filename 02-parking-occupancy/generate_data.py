"""Generate hourly parking occupancy snapshots for Project 02.

Stdlib only. Output: data/parking_entries.csv
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(7)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

LOTS = {"A": 50, "B": 80, "C": 120}
START = datetime(2025, 9, 1)
DAYS = 14

rows = []
for d in range(DAYS):
    day = START + timedelta(days=d)
    weekend = day.weekday() >= 5
    for lot, total in LOTS.items():
        base = 0.55 if lot == "A" else (0.70 if lot == "B" else 0.45)
        for hour in range(24):
            if weekend:
                curve = 0.25
            elif 8 <= hour <= 17:
                curve = 0.9 if 10 <= hour <= 15 else 0.6
            else:
                curve = 0.15
            rate = max(0.0, min(1.0, random.gauss(base * curve + 0.15, 0.06)))
            occupied = round(total * rate)
            rows.append([
                (day + timedelta(hours=hour)).strftime("%Y-%m-%d %H:00"),
                lot,
                occupied,
                total,
            ])

out = DATA_DIR / "parking_entries.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "lot_id", "occupied_spaces", "total_spaces"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {out}")
