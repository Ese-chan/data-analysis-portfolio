"""Run queries.sql against bus_delays.db and save the two main results
as summary CSVs in data/. Stdlib only.

Usage:
    python load_to_sqlite.py   # first, if bus_delays.db does not exist yet
    python run_queries.py
"""
import sqlite3
import csv
from pathlib import Path

BASE = Path(__file__).parent
DB_PATH = BASE / "bus_delays.db"
DATA_DIR = BASE / "data"

# Parse SQL bodies out of queries.sql: strip comment lines, then split on ";"
with (BASE / "queries.sql").open(encoding="utf-8") as f:
    sql_text = "\n".join(
        ln for ln in f.read().splitlines() if not ln.strip().startswith("--")
    )
clean = [s.strip() for s in sql_text.split(";") if s.strip()]

MAIN_QUERIES = [
    (clean[0], DATA_DIR / "stop_delays_summary.csv", "Average delay per stop (worst first)"),
    (clean[1], DATA_DIR / "route_delays_summary.csv", "Average delay per route + late-arrival counts"),
]

with sqlite3.connect(DB_PATH) as conn:
    for i, (sql, out_path, title) in enumerate(MAIN_QUERIES, 1):
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()

        print(f"\n=== {title} ===")
        print(" | ".join(cols))
        for row in rows:
            print(" | ".join(str(v) for v in row))

        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)
        print(f"-> saved {out_path.relative_to(BASE)}")

    print("\n=== Supporting queries ===")
    for sql in clean[2:]:
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description]
        print("\n" + " | ".join(cols))
        for row in cur.fetchall():
            print(" | ".join(str(v) for v in row))
