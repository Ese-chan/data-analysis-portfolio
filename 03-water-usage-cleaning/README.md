# Project 03 — Daily Residential Water Usage Report

**Domain:** Water Systems · **Focus:** Data hygiene on a noisy real-world-style file

## Goal

Clean a deliberately **noisy** CSV of daily household water meter readings and
produce a summary statistics report.

## Skills shown

- Detecting and handling missing values, duplicates, impossible values, and inconsistent formats
- Descriptive statistics (mean, median, max) per household
- Documenting what you fixed and why

## Data

Run `python generate_data.py` to create `data/water_usage_raw.csv`
(~3,600 rows, 40 meters over 90 days). The file is **infected on purpose** with:

- ~5% missing `daily_liters`
- ~2% negative readings (sensor glitches)
- A few absurd spikes (e.g. 99,999 L/day)
- Duplicated rows
- Mixed date formats (`2025-06-05` vs `2025/06/05`)
- Trailing whitespace in some `meter_id` values (`"M007 "`)

## Tasks

- [ ] Quantify the mess first: how many missing values, duplicates, negatives, outliers? (record the numbers)
- [ ] Standardize `date` to a single ISO format and strip whitespace from `meter_id`
- [ ] Decide and justify: drop vs fill missing values? (note your choice in this README)
- [ ] Remove or correct impossible readings (negative, spike)
- [ ] Per-meter summary: mean, median, max daily liters → `data/water_usage_clean.csv` + `data/meter_summary.csv`
- [ ] Write a short cleaning report (`cleaning_report.md`) listing each issue and the fix
- [ ] Stretch: run `ydata-profiling` on the raw file and compare its findings to yours

## Hints

```python
df.isnull().sum()          # missing per column
df.duplicated().sum()      # duplicate rows
df["meter_id"] = df["meter_id"].str.strip()
df["date"] = pd.to_datetime(df["date"], format="mixed")
df = df[df["daily_liters"].between(0, 2000)]   # plausible residential range
df.describe()
```

## Results

(your findings here)
