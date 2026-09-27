"""Load data/bus_arrivals.csv into a SQLite database (bus_delays.db).

Rows with no logged actual arrival keep delay_minutes as NULL so averages
are not skewed. Stdlib only. Re-runnable: rebuilds the table each time.
"""
import csv
import sqlite3
from pathlib import Path

BASE = Path(__file__).parent
CSV_PATH = BASE / "data" / "bus_arrivals.csv"
DB_PATH = BASE / "bus_delays.db"

DDL = """
DROP TABLE IF EXISTS arrivals;
CREATE TABLE arrivals (
    id                INTEGER PRIMARY KEY,
    date              TEXT,
    route_id          TEXT,
    stop_id           TEXT,
    stop_name         TEXT,
    scheduled_arrival TEXT,
    actual_arrival    TEXT,
    delay_minutes     REAL
);
"""

with sqlite3.connect(DB_PATH) as conn:
    conn.executescript(DDL)
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            delay = float(row[6]) if row[6] != "" else None
            rows.append((*row[:6], delay))
    conn.executemany(
        "INSERT INTO arrivals (date, route_id, stop_id, stop_name, "
        "scheduled_arrival, actual_arrival, delay_minutes) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    total, missing = conn.execute(
        "SELECT COUNT(*), SUM(delay_minutes IS NULL) FROM arrivals"
    ).fetchone()

print(f"Loaded {total} rows into {DB_PATH.name} (table: arrivals)")
print(f"  columns: {', '.join(header)}")
print(f"  rows with missing delay (no actual arrival logged): {missing}")
