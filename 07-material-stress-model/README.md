# Project 07 — Material Stress Test Spreadsheet Model

**Domain:** Structural / Design · **Focus:** Structured lookups + comparative charts

## Goal

Build a structured Excel workbook with **XLOOKUP** formulas and a Python chart
comparing **steel vs. concrete** load capacity limits.

## Skills shown

- Constructing structured engineering lookup tables
- Excel formulas that pull material properties automatically
- Presenting comparative data clearly in a chart

## Data

Run `python generate_data.py` to create two files in `data/`:

- `materials.csv` — property table: material name, type (steel/concrete),
  yield/compressive strength (MPa), density, cost per m³
- `beams.csv` — 10 beams: beam ID, assigned material, applied load (kN), span (m)

## Tasks

- [x] Import both CSVs into one Excel workbook on separate sheets (`Materials`, `Beams`)
- [x] In `Beams`, use `XLOOKUP` to pull each beam's material strength from the `Materials` sheet
- [x] Add a `utilization` column = applied load ÷ allowable capacity (capacity = strength × section factor ÷ 1000)
- [x] Conditional formatting: utilization > 1.0 turns red (overstressed)
- [x] Python: bar chart comparing yield strength (steel) vs compressive strength (concrete) across materials → `material_strength.png`
- [x] Write 2 sentences: which beam is closest to its limit? (below)

> **Note:** the workbook stores XLOOKUP in Excel's native form (`_xlfn.XLOOKUP`), so it needs **Excel 2021/365 or LibreOffice** to recalculate. Everything is pre-computed and verified (see `Review` sheet), so the values also read fine in older Excel.

## Hints

```
=XLOOKUP(B2, Materials!$A$2:$A$7, Materials!$C$2:$C$7, "not found")
```

Python side: `pandas.read_csv` + `df.plot.bar()` or plain Matplotlib —
plot strength in MPa, one bar per material, colored by type.

## Results

**Beam B-010 is the closest to (and furthest past) its limit**: the C25/30 concrete beam with a 60 kN section factor has a capacity of only 1.5 kN against a 1.9 kN applied load — **126.7% utilization**. Three more beams are also overstressed — B-005 (123.9%), B-006 (110.0%) and B-008 (100.7%) — and they light up red automatically via conditional formatting; B-002 sits exactly at 100.0% and deserves a spot-check too.

The material chart makes the design trade-off visible: steel grades carry 250–460 MPa in yield against concrete's 25–60 MPa in compression — roughly an order of magnitude — which is exactly why the concrete beams in this model hit their limits with loads under 2 kN while the steel beams take 10–46 kN to reach theirs.

*Files: `stress_model.xlsx` (Materials + Beams with live XLOOKUP/capacity/utilization formulas + amber `Review` cross-check sheet, all 4 PASS) and `material_strength.png`.*
