# Data Analysis Portfolio — Phase 0

Entry-level analyst portfolio: 8 guided projects covering **SQL, Excel, Python (Pandas/Matplotlib), data hygiene, and exploratory charts** across four engineering domains — transportation, water systems, sports analytics, and structural/design.

Each project folder contains its own `README.md` (goal, tasks, hints) and a `generate_data.py` script that produces realistic sample data, so every project is self-contained and reproducible.

## Roadmap

| # | Project | Domain | Core skills | Status |
|---|---------|--------|-------------|--------|
| 01 | [Local Bus Stop Schedule & Delay Log](01-bus-delay-log/) | Transportation | CSV import, SQL `GROUP BY`, Excel PivotTables | ⬜ Not started |
| 02 | [Parking Lot Occupancy Tracker](02-parking-occupancy/) | Transportation | Pandas datetime handling, groupby aggregation | ⬜ Not started |
| 03 | [Daily Residential Water Usage Report](03-water-usage-cleaning/) | Water Systems | Data hygiene: missing values, duplicates, outliers | ⬜ Not started |
| 04 | [Water pH & Temperature Threshold Alerts](04-water-quality-alerts/) | Water Systems | Conditional logic, threshold flagging | ⬜ Not started |
| 05 | [Single-Match Player Stat Sheet Aggregator](05-match-stats-aggregator/) | Sports | JSON parsing, event aggregation | ⬜ Not started |
| 06 | [Player Distance & Sprint Visualizer](06-player-gps-visualizer/) | Sports | Matplotlib 2D scatter, spatial data | ⬜ Not started |
| 07 | [Material Stress Test Spreadsheet Model](07-material-stress-model/) | Structural / Design | Excel XLOOKUP, comparative Python charts | ⬜ Not started |
| 08 | [CAD File Metadata Inventory Script](08-cad-metadata-inventory/) | Structural / Design | `os`/`csv` file scanning, asset cataloging | ⬜ Not started |

Update the Status column as you complete each project — recruiters love seeing progress.

## Setup

Requires Python 3.10+.

```bash
cd data-analysis-portfolio
python -m venv .venv
source .venv/Scripts/activate      # Git Bash on Windows
pip install -r requirements.txt
```

Generate the sample data for any project (stdlib only, no pandas needed):

```bash
python 01-bus-delay-log/generate_data.py
```

## Suggested workflow per project

1. Read the project README and run its `generate_data.py`.
2. Do the work yourself first — that is the point of Phase 0.
3. Save outputs (cleaned CSVs, charts, Excel files) inside the project folder.
4. Finish the README's "Results" section with 2–3 findings and a screenshot/chart.
5. Commit with a clear message, e.g. `feat(02): hourly occupancy rates per lot`.

## Recommended toolkit

- **DB Browser for SQLite** — free GUI for Project 1's SQL work.
- **ydata-profiling** — one-line EDA reports; use to *check* your manual cleaning.
- **great_expectations** — refactor Project 4's threshold checks into testable data-quality rules.

## License

MIT — sample data is synthetic and generated for learning purposes.
