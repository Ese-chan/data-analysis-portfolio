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

- [ ] Load the CSV into a SQLite database (or use [DB Browser for SQLite](https://sqlitebrowser.org/))
- [ ] SQL: average delay per stop, sorted worst first
- [ ] SQL: average delay per *route*, and count of arrivals more than 5 minutes late
- [ ] Excel: import the CSV, build a PivotTable (Rows = stop, Values = Average of delay)
- [ ] Write 3 sentences in this README about which stop/route is worst and why that might be

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

(your findings here)
