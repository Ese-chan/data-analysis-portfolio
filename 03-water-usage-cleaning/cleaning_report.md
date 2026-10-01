# Cleaning Report — Daily Residential Water Usage (Project 03)

Source: `data/water_usage_raw.csv` (3,654 rows, 40 meters, 90 days,
generated with intentional noise). Every number below is measured by
`clean_water_usage.py` at run time, not copied by hand.

## The mess, quantified

| # | Issue | Rows affected | Fix applied |
|---|-------|--------------:|-------------|
| 1 | Missing `daily_liters` (meter failed to report) | 164 (4.5%) | Dropped — see decision D1 |
| 2 | Duplicate rows (double-submitted readings) | 54 (1.5%) | Deduplicated after normalization |
| 3 | Negative readings (sensor glitches) | 84 (2.3%) | Dropped — see D2 |
| 4 | Absurd spikes (>= 2,000 L, logger bug) | 35 (1.0%) | Dropped — see D3 |
| 5 | Mixed date formats (`-` vs `/`) | 1133 (31.0%) | Parsed with `format="mixed"`, stored as ISO `YYYY-MM-DD` |
| 6 | Whitespace-polluted `meter_id` (e.g. `"M007 "`) | 98 (2.7%) | `.str.strip()` before any grouping |

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
- **D3 — drop spikes.** 2,000+ L/day is impossible for a single
  residence (the readings are all exactly 99,999.0 — a logger sentinel, not data).

## Result

- 3,654 raw rows -> 3,600 after dedupe -> **3,318 clean rows**
  (9.2% removed in total).
- Every meter retains 78-88 clean days.

## Clean dataset at a glance

| statistic | daily liters |
|-----------|-------------|
| mean | 286.4 |
| median | 287.4 |
| max (per meter-day) | 523.8 |

- Highest-usage household: **M017** (mean 419.8 L/day,
  peak 523.8 L).
- Lowest-usage household: **M032** (mean 136.6 L/day).
- Full per-meter table: `data/meter_summary.csv`; cleaned data: `data/water_usage_clean.csv`.

*The optional `ydata-profiling` stretch was skipped; the manual quantification
above covers the five seeded issue types plus duplicates.*
