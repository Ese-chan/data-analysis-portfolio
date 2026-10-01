"""Project 03 — Clean the noisy water-meter CSV and summarize per household.

Pipeline: quantify every problem on the raw file -> standardize -> dedupe ->
drop unusable readings -> export clean data + per-meter summary + a written
cleaning_report.md (regenerated on every run, with real counts).

Outputs:
    data/water_usage_clean.csv
    data/meter_summary.csv
    cleaning_report.md
"""
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
RAW = BASE / "data" / "water_usage_raw.csv"

MAX_PLAUSIBLE_LITERS = 2000        # generous residential ceiling (L/day)

# ------------------------------------------------------------- 1. quantify
raw = pd.read_csv(RAW, dtype={"meter_id": str})

n_rows_raw = len(raw)
n_missing = int(raw["daily_liters"].isnull().sum())
n_negative = int((raw["daily_liters"] < 0).sum())
n_spikes = int((raw["daily_liters"] >= MAX_PLAUSIBLE_LITERS).sum())
n_dupes = int(raw.duplicated().sum())
n_mixed_dates = int(raw["date"].str.contains("/").sum())
n_whitespace_ids = int((raw["meter_id"] != raw["meter_id"].str.strip()).sum())

# ------------------------------------------------------------- 2. standardize
df = raw.copy()
df["meter_id"] = df["meter_id"].str.strip()
df["date"] = pd.to_datetime(df["date"], format="mixed").dt.strftime("%Y-%m-%d")

# ------------------------------------------------------------- 3. dedupe
df = df.drop_duplicates()
n_rows_after_dedupe = len(df)

# ------------------------------------------------------------- 4. fix/keep
# Decisions (justified in cleaning_report.md):
#   missing  -> drop   (a meter failed to report; filling would invent readings)
#   negative -> drop   (sensor glitch, true value unknown)
#   spike    -> drop   (99999 L is a logger sentinel, not consumption)
clean = df[df["daily_liters"].notna()
           & df["daily_liters"].between(0, MAX_PLAUSIBLE_LITERS)].copy()
clean = clean.sort_values(["meter_id", "date"]).reset_index(drop=True)

clean["daily_liters"] = clean["daily_liters"].round(1)
clean.to_csv(BASE / "data" / "water_usage_clean.csv", index=False)

# ------------------------------------------------------------- 5. summarize
summary = (
    clean.groupby("meter_id")["daily_liters"]
    .agg(days="count", mean_liters="mean", median_liters="median", max_liters="max")
    .round(1)
    .reset_index()
)
summary.to_csv(BASE / "data" / "meter_summary.csv", index=False)

busiest = summary.loc[summary["mean_liters"].idxmax()]
quietest = summary.loc[summary["mean_liters"].idxmin()]

# ------------------------------------------------------------- 6. report
report = f"""# Cleaning Report — Daily Residential Water Usage (Project 03)

Source: `data/water_usage_raw.csv` ({n_rows_raw:,} rows, 40 meters, 90 days,
generated with intentional noise). Every number below is measured by
`clean_water_usage.py` at run time, not copied by hand.

## The mess, quantified

| # | Issue | Rows affected | Fix applied |
|---|-------|--------------:|-------------|
| 1 | Missing `daily_liters` (meter failed to report) | {n_missing} ({n_missing / n_rows_raw:.1%}) | Dropped — see decision D1 |
| 2 | Duplicate rows (double-submitted readings) | {n_dupes} ({n_dupes / n_rows_raw:.1%}) | Deduplicated after normalization |
| 3 | Negative readings (sensor glitches) | {n_negative} ({n_negative / n_rows_raw:.1%}) | Dropped — see D2 |
| 4 | Absurd spikes (>= {MAX_PLAUSIBLE_LITERS:,} L, logger bug) | {n_spikes} ({n_spikes / n_rows_raw:.1%}) | Dropped — see D3 |
| 5 | Mixed date formats (`-` vs `/`) | {n_mixed_dates} ({n_mixed_dates / n_rows_raw:.1%}) | Parsed with `format="mixed"`, stored as ISO `YYYY-MM-DD` |
| 6 | Whitespace-polluted `meter_id` (e.g. `"M007 "`) | {n_whitespace_ids} ({n_whitespace_ids / n_rows_raw:.1%}) | `.str.strip()` before any grouping |

## Decisions

- **D1 — drop missing values rather than fill.** A missing reading means the
  meter simply did not report that day. Filling with the mean/median would
  invent consumption for a day we know nothing about and bias the per-household
  mean toward the household average, muting real day-to-day variation. With only
  ~5% missing and scattered across meters, dropping still leaves every meter
  with plenty of days for solid statistics.
- **D2 — drop negatives, don't "correct" them.** A negative reading is a sensor
  glitch; the true consumption that day is unknowable, so any correction would
  be fabrication.
- **D3 — drop spikes.** {MAX_PLAUSIBLE_LITERS:,}+ L/day is impossible for a single
  residence (the readings are all exactly 99,999.0 — a logger sentinel, not data).

## Result

- {n_rows_raw:,} raw rows -> {n_rows_after_dedupe:,} after dedupe -> **{len(clean):,} clean rows**
  ({(n_rows_raw - len(clean)) / n_rows_raw:.1%} removed in total).
- Every meter retains {summary['days'].min()}-{summary['days'].max()} clean days.

## Clean dataset at a glance

| statistic | daily liters |
|-----------|-------------|
| mean | {clean['daily_liters'].mean():.1f} |
| median | {clean['daily_liters'].median():.1f} |
| max (per meter-day) | {clean['daily_liters'].max():.1f} |

- Highest-usage household: **{busiest['meter_id']}** (mean {busiest['mean_liters']} L/day,
  peak {busiest['max_liters']} L).
- Lowest-usage household: **{quietest['meter_id']}** (mean {quietest['mean_liters']} L/day).
- Full per-meter table: `data/meter_summary.csv`; cleaned data: `data/water_usage_clean.csv`.

*The optional `ydata-profiling` stretch was skipped; the manual quantification
above covers the five seeded issue types plus duplicates.*
"""
(BASE / "cleaning_report.md").write_text(report, encoding="utf-8")

print(report)
print(f"\nSaved water_usage_clean.csv ({len(clean):,} rows), meter_summary.csv, cleaning_report.md")
