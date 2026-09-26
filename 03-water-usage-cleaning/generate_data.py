"""Generate a deliberately NOISY water meter dataset for Project 03.

Stdlib only. Output: data/water_usage_raw.csv

The noise is the project: missing values, negatives, spikes, duplicates,
mixed date formats, and whitespace-polluted IDs. Cleaning it is the exercise.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2024)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

START = date(2025, 6, 1)
DAYS = 90
METERS = [f"M{i:03d}" for i in range(1, 41)]

rows = []
for m in METERS:
    base = random.uniform(120, 420)          # household baseline L/day
    for d in range(DAYS):
        day = START + timedelta(days=d)
        weekend = day.weekday() >= 5
        liters = random.gauss(base + (25 if weekend else 0), 45)
        liters = round(max(30.0, liters), 1)

        # 1 in 3 meters occasionally forgets to report
        if random.random() < 0.05:
            liters = None
        # sensor glitch: negative reading
        elif random.random() < 0.02:
            liters = round(-random.uniform(5, 60), 1)
        # logger bug: absurd spike
        elif random.random() < 0.01:
            liters = 99999.0

        date_str = day.isoformat() if random.random() < 0.7 else day.strftime("%Y/%m/%d")
        meter_id = m + " " if random.random() < 0.03 else m   # trailing whitespace
        rows.append([meter_id, date_str, liters])

# duplicate ~1.5% of rows (double-submission)
rows += [list(r) for r in random.sample(rows, int(len(rows) * 0.015))]
random.shuffle(rows)

out = DATA_DIR / "water_usage_raw.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["meter_id", "date", "daily_liters"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} noisy rows to {out}")
