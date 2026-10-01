# Project 02 — Parking Lot Occupancy Tracker

**Domain:** Transportation · **Focus:** First Pandas automation of a spreadsheet task

## Goal

Replace a manual entry spreadsheet with a Python script that calculates
**hourly parking space occupancy rates** per lot, using Pandas.

## Skills shown

- Transitioning from manual spreadsheet work to automated data manipulation
- Datetime handling and grouped aggregation in Pandas
- Producing a tidy output table others can reuse

## Data

Run `python generate_data.py` to create `data/parking_entries.csv`:

| column | meaning |
|--------|---------|
| `timestamp` | hourly snapshot (date + hour) |
| `lot_id` | parking lot (A, B, C) |
| `occupied_spaces` | spaces in use at that hour |
| `total_spaces` | capacity of the lot (50 / 80 / 120) |

Occupancy follows a realistic weekday curve: ramps up 8–10, peaks midday,
drains after 17:00; weekends stay low.

## Tasks

- [x] Load the CSV with Pandas; parse `timestamp` as a datetime
- [x] Add an `occupancy_rate` column (`occupied_spaces / total_spaces`)
- [x] Average occupancy rate per lot **per hour of day** (0–23)
- [x] Find the single busiest hour across all lots
- [x] Export the hourly summary to `data/hourly_occupancy_summary.csv`
- [x] Stretch: plot one line per lot (hour vs occupancy rate) with Matplotlib and save it as `hourly_occupancy.png`

## Hints

```python
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
summary = df.groupby(["lot_id", "hour"])["occupancy_rate"].mean().round(3)
```

## Results

Over the two weeks, **13:00 is the busiest hour across all lots** (mean occupancy 56%); weekday demand follows a classic commute curve — filling sharply between 08:00 and 10:00, holding a midday plateau near 55%, and draining back below 25% after 18:00. **Lot B (80 spaces) runs hottest**: it peaks at 68% at 15:00 and averages 41% overall, while lot C (120 spaces, the biggest) runs coolest at 32% — even at the midday peak it never exceeds ~49%, so capacity is not the problem; pricing or demand-shifting for lot B might be.

*Output: `data/hourly_occupancy_summary.csv` (tidy hour × lot table) and `hourly_occupancy.png` (one line per lot). Built by `analyze_parking.py`.*
