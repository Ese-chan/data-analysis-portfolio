"""Generate a single-player GPS track for Project 06.

Stdlib only. Output: data/gps_track.csv

The player starts near midfield, jogs, walks, and puts in two sprints
(minutes ~3 and ~7) toward the right flank.
"""
import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(5)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

PITCH_W, PITCH_H = 105.0, 68.0
N_SECONDS = 600
START = datetime(2025, 9, 14, 15, 0, 0)

x, y = 52.0, 34.0
vx, vy = 0.0, 0.0
rows = []
for s in range(N_SECONDS):
    # speed profile: walk / jog / two sprints / stand
    if s < 60:
        target = 1.4                      # walking
    elif 180 <= s < 210:
        target = 8.2                      # sprint 1
    elif 300 <= s < 360:
        target = 1.2                      # walk
    elif 420 <= s < 450:
        target = 8.6                      # sprint 2
    elif 500 <= s < 560:
        target = 0.2                      # standing
    else:
        target = 3.2                      # jogging

    speed = random.gauss(target, 0.3)
    heading = math.atan2(68 / 2 - y, 96 - x) if 180 <= s < 210 or 420 <= s < 450 \
        else random.gauss(0.0, 1.2)
    vx = speed * math.cos(heading)
    vy = speed * math.sin(heading)
    x = max(0.5, min(PITCH_W - 0.5, x + vx))
    y = max(0.5, min(PITCH_H - 0.5, y + vy))
    rows.append([
        (START + timedelta(seconds=s)).strftime("%H:%M:%S"),
        "P07",
        round(x, 2),
        round(y, 2),
    ])

out = DATA_DIR / "gps_track.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "player_id", "x_m", "y_m"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} GPS snapshots to {out}")
