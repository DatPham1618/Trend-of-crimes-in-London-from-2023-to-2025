# London Crime Trends (2024–2025)

A Data Analyst portfolio project analyzing how different crime types trend over time
across London's boroughs, using official police data.

## Business Question

**Which crime types are trending up or down across London boroughs between
January 2024 and December 2025, and what might explain those trends?**

## Data Source

- **[data.police.uk](https://data.police.uk/)** — official UK police open data
- Street-level crime data for the **Metropolitan Police Service** (London)
- 24 monthly files, January 2024 – December 2025
- ~2.27 million records after cleaning

Raw data is not committed to this repository (see `.gitignore`) — it can be
re-downloaded directly from data.police.uk for the same date range and force.

## Tools

| Tool | Role |
|---|---|
| Python (pandas) | Reading, merging, and cleaning the 24 raw monthly files |
| SQL (SQLite) | Exploratory data analysis (trends by month / crime type / borough) |
| Power BI | Final dashboard |
| Excel / Google Sheets | Quick spot-checks |

## Repository Structure

```
notebooks/    Data cleaning pipeline (Python/pandas)
sql/          SQL queries used for exploratory analysis
data/         Raw & processed data (gitignored — see Data Source above)
reports/      Project plan and final write-up
```

## Data Cleaning — Key Decisions

A few non-obvious decisions made during cleaning, worth calling out since they
affect the validity of everything downstream:

- **`Context` column dropped** — 100% empty across all 24 months, no information.
- **Missing `Crime ID` is not a data error.** Every record with `Crime type` =
  *Anti-social behaviour* has a null `Crime ID` and null `Last outcome category`
  by design — these incidents aren't tracked as individual cases with an
  outcome. This is a real characteristic of the source data, not something to
  impute or fix.
- **Duplicate handling was done carefully, not with a blanket `drop_duplicates()`.**
  Because Anti-social behaviour records have no `Crime ID`, two genuinely
  different incidents in the same borough/month can look identical across
  every other column. Deduplication was therefore applied **only** to rows
  that have a `Crime ID` (true duplicates — the same case appearing twice,
  likely from overlap between adjacent monthly extracts). Rows without a
  `Crime ID` were left untouched to avoid undercounting real incidents.
- **Borough was derived from `LSOA name`**, which embeds the borough name as a
  prefix (e.g. `"Westminster 013A"` → `Westminster`). About 0.44% of rows fell
  outside the 33 official London boroughs (crimes near the Met Police
  boundary occasionally snap to a neighbouring county's LSOA) and were
  excluded from the borough-level analysis.

## Project Status

- [x] Data collection (24 monthly files from data.police.uk)
- [x] Data cleaning (merge, deduplication, borough extraction)
- [ ] Exploratory analysis in SQL (trend by month / crime type / borough)
- [ ] Power BI dashboard
- [ ] Key findings & recommendations
- [ ] Final write-up

## Key Findings

_To be added once the SQL exploratory analysis is complete._

## Dashboard

_To be added — Power BI dashboard screenshot/link will go here._

## Limitations

- Scope is limited to Greater London (Metropolitan Police Service); no
  external variables (weather, economic indicators, policy changes) are
  joined in to explain trends — explanations are inferred, not proven.
- Crime location coordinates are anonymized/snapped by the source, so
  borough-level (not street-level) analysis is the appropriate granularity.
