"""Generate a week of water quality samples for Project 04.

Stdlib only. Output: data/water_quality_log.csv

pH drifts around 7.2 with occasional excursions; temperature follows a
daily cycle around 18 C with a few failure spikes.
"""
import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(11)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

START = datetime(2025, 7, 1)
SAMPLES_PER_DAY = 48          # every 30 minutes
DAYS = 7
POINTS = ["Inlet", "Tank", "Outlet"]

# Pre-choose a handful of excursion windows (point, start_hour, duration_hours, kind)
excursions = [
    ("Tank", 52, 3, "ph_high"),
    ("Inlet", 83, 2, "ph_low"),
    ("Outlet", 101, 4, "temp_high"),
    ("Tank", 130, 2, "temp_low"),
]

rows = []
for d in range(DAYS):
    for s in range(SAMPLES_PER_DAY):
        ts = START + timedelta(days=d, minutes=30 * s)
        hour_index = d * 24 + s // 2
        for point in POINTS:
            ph = round(random.gauss(7.2, 0.15), 2)
            # temperature: daily sine wave 15-21 C + noise
            temp = round(18 + 3 * math.sin((hour_index % 24 - 6) / 24 * 2 * math.pi)
                         + random.gauss(0, 0.6), 1)
            for p, start, dur, kind in excursions:
                if p == point and start <= hour_index < start + dur:
                    if kind == "ph_high":
                        ph = round(random.uniform(8.8, 9.4), 2)
                    elif kind == "ph_low":
                        ph = round(random.uniform(5.9, 6.3), 2)
                    elif kind == "temp_high":
                        temp = round(random.uniform(31.5, 34.0), 1)
                    elif kind == "temp_low":
                        temp = round(random.uniform(7.5, 9.5), 1)
            rows.append([ts.strftime("%Y-%m-%d %H:%M"), point, ph, temp])

out = DATA_DIR / "water_quality_log.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "sample_point", "ph", "temperature_c"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} samples to {out}")
