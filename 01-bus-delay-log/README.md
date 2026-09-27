# Project 01 — Local Bus Stop Schedule & Delay Log

**Domain:** Transportation · **Focus:** Basic SQL queries + Excel PivotTables

## Goal

Import raw CSV bus arrival logs into both a SQL database and Excel, then use
`GROUP BY` (SQL) and PivotTables (Excel) to calculate the **average arrival
delay per bus stop**.

## Skills shown

- Cleaning raw tabular transportation data
- Foundational aggregate queries (`AVG`, `GROUP BY`, `ORDER BY`)
- Building the same analysis two ways: SQL and Excel

## Data

Run `python generate_data.py` to create `data/bus_arrivals.csv`:

| column | meaning |
|--------|---------|
| `date` | service day |
| `route_id` | bus route number |
| `stop_id` / `stop_name` | bus stop |
| `scheduled_arrival` / `actual_arrival` | HH:MM times |
| `delay_minutes` | negative = early, positive = late |

## Tasks

- [x] Load the CSV into a SQLite database (`bus_delays.db`, via `load_to_sqlite.py` — or use [DB Browser for SQLite](https://sqlitebrowser.org/))
- [x] SQL: average delay per stop, sorted worst first (`queries.sql` / `run_queries.py`)
- [x] SQL: average delay per *route*, and count of arrivals more than 5 minutes late
- [x] Excel: import the CSV, build a PivotTable (Rows = stop, Values = Average of delay) → `bus_delay_analysis.xlsx`
- [x] Write 3 sentences in this README about which stop/route is worst and why that might be

## Hints

```sql
SELECT stop_name, ROUND(AVG(delay_minutes), 1) AS avg_delay
FROM arrivals
GROUP BY stop_name
ORDER BY avg_delay DESC;
```

Excel: `Insert > PivotTable` → drag `stop_name` to Rows, `delay_minutes` to
Values, then change the value aggregation from Sum to **Average**.

## Results

Route 14 is by far the worst performer: its arrivals average **5.1 minutes late** and 689 of its 1,403 logged arrivals (**49%**) were more than 5 minutes behind, versus 3.0 min / 322 late for route 12 and 1.5 min / 107 late for route 27. Stop-level differences are small — all six stops average between 3.1 and 3.4 minutes (University Gate worst at 3.4) — which suggests the lateness is driven by the route itself (traffic congestion or an over-tight schedule) rather than by any particular stop. Delays are also heavier at peak hours and on weekdays (weekday average 3.4 min vs 2.5 min on weekends), consistent with rush-hour congestion as the root cause.

*(81 of 4,320 arrivals have no logged actual time; their delay is treated as NULL/blank and excluded from every average.)*

## Files

| file | what it is |
|------|------------|
| `generate_data.py` | creates the synthetic raw log `data/bus_arrivals.csv` |
| `load_to_sqlite.py` | imports the CSV into `bus_delays.db` (table `arrivals`, missing delays as NULL) |
| `queries.sql` | the analysis queries (stop averages, route averages + >5-min-late counts, and two supporting queries) |
| `run_queries.py` | runs `queries.sql`, prints results, saves `data/stop_delays_summary.csv` and `data/route_delays_summary.csv` |
| `build_excel.py` | builds `bus_delay_analysis.xlsx` (raw data, live-formula summaries + charts, cross-check sheet) |
| `bus_delay_analysis.xlsx` | the Excel deliverable — `Arrivals`, `Stop Summary`, `Route Summary`, `Review`, `Pivot Stop Delays` |
| `bus_delays.db` | SQLite database ready for DB Browser for SQLite |

Reproduce with: `python generate_data.py && python load_to_sqlite.py && python run_queries.py && python build_excel.py`
