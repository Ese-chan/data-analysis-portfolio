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

- [ ] Import both CSVs into one Excel workbook on separate sheets (`Materials`, `Beams`)
- [ ] In `Beams`, use `XLOOKUP` to pull each beam's material strength from the `Materials` sheet
- [ ] Add a `utilization` column = applied load ÷ allowable capacity (capacity = strength × section factor from `beams.csv`)
- [ ] Conditional formatting: utilization > 1.0 turns red (overstressed)
- [ ] Python: bar chart comparing yield strength (steel) vs compressive strength (concrete) across materials → `material_strength.png`
- [ ] Write 2 sentences: which beam is closest to its limit?

## Hints

```
=XLOOKUP(B2, Materials!$A$2:$A$7, Materials!$C$2:$C$7, "not found")
```

Python side: `pandas.read_csv` + `df.plot.bar()` or plain Matplotlib —
plot strength in MPa, one bar per material, colored by type.

## Results

(your findings here)
