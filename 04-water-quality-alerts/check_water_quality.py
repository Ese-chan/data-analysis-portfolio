"""Project 04 — Flag water samples outside safety thresholds.

Encodes the pH and temperature safety limits as named constants, checks every
sample with plain if/else logic, writes all violations to data/alerts.csv with
the broken limit and by how much, and prints a per-sample-point summary.

Severity stretch: a violation within 5% of the broken limit is a `warning`;
anything further out is `critical`.

Output: data/alerts.csv
"""
import csv
from pathlib import Path

BASE = Path(__file__).parent
LOG = BASE / "data" / "water_quality_log.csv"
ALERTS = BASE / "data" / "alerts.csv"

SAFE_PH = (6.5, 8.5)           # pH is unitless
SAFE_TEMP_C = (10.0, 30.0)     # degrees Celsius
WARN_BAND = 0.05               # within 5% of a limit -> warning, else critical


def check_ph(value):
    """Return (reason, severity) if pH is unsafe, else (None, None)."""
    if value < SAFE_PH[0]:
        margin = SAFE_PH[0] * WARN_BAND
        severity = "warning" if SAFE_PH[0] - value <= margin else "critical"
        return f"pH below safe range ({value} < {SAFE_PH[0]}) by {round(SAFE_PH[0] - value, 2)}", severity
    if value > SAFE_PH[1]:
        margin = SAFE_PH[1] * WARN_BAND
        severity = "warning" if value - SAFE_PH[1] <= margin else "critical"
        return f"pH above safe range ({value} > {SAFE_PH[1]}) by {round(value - SAFE_PH[1], 2)}", severity
    return None, None


def check_temperature(value):
    """Return (reason, severity) if temperature is unsafe, else (None, None)."""
    if value < SAFE_TEMP_C[0]:
        margin = SAFE_TEMP_C[0] * WARN_BAND
        severity = "warning" if SAFE_TEMP_C[0] - value <= margin else "critical"
        return (f"temperature below safe range ({value} < {SAFE_TEMP_C[0]}) "
                f"by {round(SAFE_TEMP_C[0] - value, 1)}"), severity
    if value > SAFE_TEMP_C[1]:
        margin = SAFE_TEMP_C[1] * WARN_BAND
        severity = "warning" if value - SAFE_TEMP_C[1] <= margin else "critical"
        return (f"temperature above safe range ({value} > {SAFE_TEMP_C[1]}) "
                f"by {round(value - SAFE_TEMP_C[1], 1)}"), severity
    return None, None


with LOG.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

alerts = []
for row in rows:
    ph = float(row["ph"])
    temp = float(row["temperature_c"])
    reasons, severities = [], []
    for check in (check_ph(ph), check_temperature(temp)):
        if check[0]:
            reasons.append(check[0])
            severities.append(check[1])
    if reasons:
        alerts.append({**row,
                       "alert_reason": "; ".join(reasons),
                       "severity": max(severities, key=["warning", "critical"].index)})

with ALERTS.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]) + ["alert_reason", "severity"])
    writer.writeheader()
    writer.writerows(alerts)

# -------------------------------------------------- per-point summary
points = sorted({row["sample_point"] for row in rows})
print(f"Checked {len(rows):,} samples against pH {SAFE_PH} and temperature {SAFE_TEMP_C} C")
print(f"Violations: {len(alerts)} "
      f"({sum(a['severity'] == 'critical' for a in alerts)} critical, "
      f"{sum(a['severity'] == 'warning' for a in alerts)} warning)\n")
print(f"{'point':<8} {'pH alerts':>9} {'temp alerts':>12} {'total':>6}")
for point in points:
    ph_n = sum(1 for a in alerts if a["sample_point"] == point and "pH" in a["alert_reason"])
    temp_n = sum(1 for a in alerts if a["sample_point"] == point and "temperature" in a["alert_reason"])
    print(f"{point:<8} {ph_n:>9} {temp_n:>12} {ph_n + temp_n:>6}")

worst = max(alerts, key=lambda a: abs(float(a["ph"]) - 7.2) + abs(float(a["temperature_c"]) - 18))
print(f"\nWorst single sample: {worst['timestamp']} at {worst['sample_point']} "
      f"-> {worst['alert_reason']} [{worst['severity']}]")
print(f"Saved {ALERTS.relative_to(BASE)}")
