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

- [ ] Read the CSV and define the thresholds as named constants
- [ ] Flag every out-of-range row with which limit it broke and by how much
- [ ] Write all violations to `data/alerts.csv` (same columns + `alert_reason`, `severity`)
- [ ] Print a per-`sample_point` summary: number of pH alerts, number of temperature alerts
- [ ] Stretch: severity = `warning` if within 5% of a limit, `critical` otherwise
- [ ] Stretch (portfolio upgrade): rewrite the same checks as [Great Expectations](https://greatexpectations.io/) expectations

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

(your findings here)
