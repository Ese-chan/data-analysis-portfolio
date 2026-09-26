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

- [ ] Walk `sample_cad_files/` with `os.scandir()` or `pathlib`
- [ ] For each file record: filename, project code (parse it from the name), extension, size in KB, last modified date
- [ ] Write the inventory to `cad_inventory.csv`
- [ ] Print totals: number of files and total MB per extension
- [ ] Stretch: write the same inventory to an Excel sheet with one tab per extension
- [ ] Stretch: make the target folder a command-line argument (`python build_inventory.py <folder>`)

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

(your findings here — file counts per project, largest file, etc.)
