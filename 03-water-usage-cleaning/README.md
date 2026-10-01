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

- [x] Quantify the mess first: how many missing values, duplicates, negatives, outliers? (record the numbers)
- [x] Standardize `date` to a single ISO format and strip whitespace from `meter_id`
- [x] Decide and justify: drop vs fill missing values? (noted below and in `cleaning_report.md`)
- [x] Remove or correct impossible readings (negative, spike)
- [x] Per-meter summary: mean, median, max daily liters → `data/water_usage_clean.csv` + `data/meter_summary.csv`
- [x] Write a short cleaning report (`cleaning_report.md`) listing each issue and the fix
- [ ] Stretch: run `ydata-profiling` on the raw file and compare its findings to yours (skipped — manual quantification covers it)

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

The raw file had **all six seeded problems**: 164 missing readings (4.5%), 54 duplicate rows (1.5%), 84 negative sensor glitches (2.3%), 35 absurd 99,999-L spikes (1.0%), 1,133 rows in the wrong date format (31%), and 98 meter IDs with trailing whitespace (2.7%). Cleaning kept the file honest — whitespace stripped and dates normalized to ISO *before* deduplicating and grouping — and dropped the 9.2% of rows that were unusable rather than inventing values for them (full reasoning in `cleaning_report.md`).

The cleaned 3,318 meter-days tell a sensible story: the average household uses **~286 L/day** (median 287), the thirstiest meter M017 averages 420 L/day against M032's 137 L/day — roughly a 3× spread across the 40 households — and every meter keeps 78–88 clean days, enough for trustworthy per-household statistics.

*Missing values were **dropped, not filled**: a no-report day is unknown, and filling would fabricate consumption and mute real day-to-day variation.*
