# Project 04 — Water pH & Temperature Threshold Alert Script

**Domain:** Water Systems · **Focus:** Translating engineering constraints into code

## Goal

Write a script that parses a water quality log and **flags every sample that
falls outside safety thresholds**, using plain `if/else` logic.

## Skills shown

- Encoding domain rules (safe pH range, safe temperature range) as programmatic checks
- Reading structured logs and producing an actionable alert file
- Summarizing violations so an operator knows where to look first

## Data

Run `python generate_data.py` to create `data/water_quality_log.csv`:
one sample every 30 minutes for 7 days at three points (`Inlet`, `Tank`, `Outlet`),
with occasional genuine excursions (rain events, dosing failures).

Safety limits to encode:

| parameter | safe range |
|-----------|-----------|
| pH | 6.5 – 8.5 |
| temperature | 10 – 30 °C |

## Tasks

- [x] Read the CSV and define the thresholds as named constants
- [x] Flag every out-of-range row with which limit it broke and by how much
- [x] Write all violations to `data/alerts.csv` (same columns + `alert_reason`, `severity`)
- [x] Print a per-`sample_point` summary: number of pH alerts, number of temperature alerts
- [x] Stretch: severity = `warning` if within 5% of a limit, `critical` otherwise
- [ ] Stretch (portfolio upgrade): rewrite the same checks as [Great Expectations](https://greatexpectations.io/) expectations (left as a follow-up — see main README "Recommended toolkit")

## Hints

```python
SAFE_PH = (6.5, 8.5)

def check_ph(value):
    if value < SAFE_PH[0]:
        return f"pH below safe range ({value} < {SAFE_PH[0]})"
    if value > SAFE_PH[1]:
        return f"pH above safe range ({value} > {SAFE_PH[1]})"
    return None
```

## Results

Over the 7 days (1,008 samples at three points), **22 violations** were flagged — **20 critical, 2 warnings**. The **Tank is the problem child** with 10 alerts (6 pH, 4 temperature): a pH excursion up to ~9.4 on day 3 and a cold-water dip to ~8 °C on day 6. The Outlet's 8 temperature alerts are one coherent heat event on July 5 (up to 34 °C, 3.7 °C over the limit), and the Inlet saw a brief low-pH rain-event window (4 alerts). No sample broke both limits at once, so each alert has a single clear cause — `data/alerts.csv` gives the operator the exact timestamp, point, limit broken, and overshoot for every event.
