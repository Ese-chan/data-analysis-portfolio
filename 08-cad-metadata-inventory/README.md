# Project 08 — CAD File Metadata Inventory Script

**Domain:** Structural / Design · **Focus:** Entry-level scripting with `os` and `csv`

## Goal

Write a script that scans a directory of design files and logs project names,
file sizes, and dates into a **master spreadsheet**.

## Skills shown

- Organizing and cataloging digital engineering assets
- File-system scripting with `os` / `pathlib` (no manual clicking)
- Producing a reusable inventory report from nothing but a folder

## Data

Run `python generate_data.py` to create `sample_cad_files/` — 18 dummy CAD
files (`.dwg`, `.dxf`, `.rvt`, `.pdf`) with realistic project-style names,
varied sizes, and varied file dates.

## Tasks

- [x] Walk `sample_cad_files/` with `os.scandir()` or `pathlib`
- [x] For each file record: filename, project code (parse it from the name), extension, size in KB, last modified date
- [x] Write the inventory to `cad_inventory.csv`
- [x] Print totals: number of files and total MB per extension
- [x] Stretch: write the same inventory to an Excel sheet with one tab per extension (`cad_inventory.xlsx`, plus a Summary tab)
- [x] Stretch: make the target folder a command-line argument (`python build_inventory.py <folder>`)

## Hints

```python
from pathlib import Path
from datetime import datetime

for entry in Path("sample_cad_files").iterdir():
    size_kb = entry.stat().st_size / 1024
    modified = datetime.fromtimestamp(entry.stat().st_mtime)
```

Filenames follow `PROJECT-TYPE-###_description.ext`, e.g.
`BRG-DRW-014_bridge_deck_plan.dwg` → project code `BRG`.

## Results

The scan cataloged **18 files totaling 0.85 MB**: 6 PDFs and 6 Revit models dominate the count, with 4 DXFs and only 2 DWGs; by project, **Tunnel (TUN) and Water Treatment Plant (WTP) hold 6 files each**, Plant Layout (PLT) 4, and Bridge (BRG) just 2. The largest file is `WTP-PLN-013_deck_section.dxf` at 85.8 KB (modified 2024-11-13).

Outputs: `cad_inventory.csv` (flat inventory: filename, project code, extension, KB, last-modified) and `cad_inventory.xlsx` (Summary tab with per-extension totals + one tab per extension, live SUM formulas). Re-run on any folder with `python build_inventory.py <folder>`.
