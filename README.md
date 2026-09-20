# London Crime Trends, 2023–2025

**What is the trend of crime in London, and where does it happen?**

An analysis of 3.39 million street-level crime records from the Metropolitan Police
Service (data.police.uk), January 2023 – December 2025, broken down by crime type,
borough and month. Cleaned with Python (pandas), aggregated with SQL (SQLite) and
presented in a two-page Power BI dashboard.

## Key Findings

### 1. The trend: total volume is flat, the mix is changing

| Year | Records | Change |
|---|---|---|
| 2023 | 1,126,529 | |
| 2024 | 1,134,243 | +0.7% |
| 2025 | 1,134,139 | 0.0% |

London recorded about 94,000 crimes a month in each of the three years. There is no
upward or downward trend in the total. What changed is *what* is being recorded:

| Crime type | 2023 | 2025 | Change |
|---|---|---|---|
| Shoplifting | 57,611 | 86,735 | **+51%** |
| Drugs | 36,639 | 53,624 | **+46%** |
| Theft from the person | 72,869 | 85,187 | +17% (peaked in 2024 at 97,375) |
| Violence and sexual offences | 259,819 | 266,707 | +3% |
| Anti-social behaviour | 222,768 | 234,894 | +5% |
| Robbery | 32,566 | 31,271 | −4% |
| Bicycle theft | 16,238 | 13,809 | −15% |
| Burglary | 56,060 | 47,629 | −15% |
| Vehicle crime | 105,893 | 83,775 | **−21%** |
| Other theft | 135,735 | 99,630 | **−27%** |

- **Shoplifting** roughly doubled from about 4,000 a month in early 2023 to about
  8,000 by autumn 2024, then held between 6,700 and 8,000 through 2025.
- **Drugs** fell through 2023, stayed around 2,500–2,800 a month in the first half of
  2024, then rose from autumn 2024 to between 3,700 and 5,000 a month in 2025.
- **Theft from the person** stepped up from October 2023 (about 5,000–5,500 a month before,
  8,300 in November 2023) and hit its highest month in November 2024 (10,199). It was 12.5%
  lower in 2025 than in 2024, but still 17% above 2023.
- **Vehicle crime, burglary and bicycle theft** fell in each year.

### 2. Seasonality: summer peak, February low, and an autumn bump

Averaged over the three years, crime is lowest in February (about 85,000 records) and highest in
June–July (about 101,000). October is a second peak (about 100,000). The second half of the
year is 4–6% busier than the first half in every year. Individual types have their own
rhythm: anti-social behaviour peaks in July and is 47% higher than in February, while
theft from the person peaks in November every year and is lowest in August–September.

### 3. Where: crime is concentrated in central London

- **Westminster** has 300,566 records over the three years, 8.9% of everything and about
  twice the next borough (Camden, 148,100). The top five boroughs (Westminster, Camden,
  Newham, Southwark, Tower Hamlets) account for 26% of records that have a borough, the top ten
  for 45%.
- The lowest counts are in outer south-west boroughs: Kingston upon Thames (44,209), Richmond
  upon Thames (44,693) and Sutton (48,130). Westminster's count is 6.8 times Kingston's.
- **Westminster has a different crime profile from the rest of London.** Theft from the person
  makes up 27% of its records against 7.5% London-wide, and Westminster alone holds 32% of
  all theft from the person in London. Violence and anti-social behaviour are a smaller share
  of its mix than elsewhere.
- **2024 → 2025:** 19 of the 32 boroughs (excluding City of London) recorded more crime.
  The biggest falls were Westminster (−6.2%), Waltham Forest (−5.8%) and Camden (−4.3%). The
  biggest rises were Kingston upon Thames (+6.1%), Hillingdon (+5.3%) and Ealing (+4.1%).
  Westminster's fall is consistent with the 12.5% drop in theft from the person in 2025, but
  this analysis does not prove the link.

### What these numbers can and cannot say

These are counts of *recorded* crime, not rates per resident, and they say nothing about why
crime moved. Possible explanations (none tested here): drug offences are mostly found by
police action, so the 2025 rise may reflect enforcement activity as much as drug use; the
fall in "Other theft" alongside rises in shoplifting and theft from the person may partly be
a change in how offences are categorised (the three combined: 266,215 → 290,245 → 271,552);
and Westminster's high count reflects the people who work in and visit the area, not only
those who live there. See [Limitations](#limitations).

## Dashboard

A Power BI project in [`dashboard/`](dashboard/london_crime_v1.pbip) with two pages:

- **Overview**: total and monthly average crimes, monthly trend by crime type (small
  multiples), year-on-year comparison, and boroughs ranked by volume, with a year slicer.
- **Borough drill-down**: pick a crime type and borough to see its monthly timeline, next to a
  borough × crime type heatmap that always compares all 33 boroughs.

The dashboard reads the aggregated table `data/processed/monthly_crimes_by_type_borough.csv`
(one row per month × borough × crime type). If you open it on another machine, point the
`crimes` query in Power Query to that file's location.

## Data

- **Source:** [data.police.uk](https://data.police.uk/), street-level crime for the Metropolitan
  Police Service, published under the Open Government Licence v3.0.
- **Coverage:** 36 monthly files, January 2023 – December 2025.
- **Size:** 3,414,776 raw records, 3,394,911 after cleaning.

The raw and cleaned row-level files are too large for the repository and are gitignored. To
reproduce, download the Metropolitan Police street-level files for the same months and place
them in `data/raw/`.

## Method

| Step | Tool | What it does |
|---|---|---|
| 1. Clean | Python / pandas | Merge 36 monthly files, drop empty columns, derive borough, remove duplicates |
| 2. Aggregate | SQL (SQLite) | `GROUP BY` borough, month and crime type ([query](sql/monthly_borough_crime.sql)) |
| 3. Visualise | Power BI | Two-page dashboard on the aggregated table |

### Cleaning decisions

Each of these changes the numbers, so they are recorded here.

- **`Context` column dropped.** It is empty in all 3,414,776 rows.
- **Missing `Crime ID` is not an error.** All 690,218 raw records with no `Crime ID` are
  *Anti-social behaviour*, and they also have no `Last outcome category`. The two columns are
  null on exactly the same rows. This is how the source records these incidents, so nothing is
  imputed and `dropna()` is deliberately not used.
- **Borough is derived from `LSOA name`**, which starts with the borough name
  (`"Westminster 013A"` → `Westminster`).
- **Rows outside London were dropped:** 13,509 rows (0.40%) sit in LSOAs belonging to
  neighbouring counties, where crimes near the Met boundary snap to an outside area.
- **Rows with no location were kept.** 24,151 rows (0.71%) have no coordinates or LSOA and are
  labelled `Unknown` rather than dropped or guessed. They count towards London totals and are
  excluded from borough comparisons.
- **Duplicates were removed only where a `Crime ID` exists.** Anti-social behaviour rows have no
  ID, so two real incidents can look identical in every other column; a blanket
  `drop_duplicates()` would delete genuine records. 6,356 exact duplicate rows were removed.

Row count: 3,414,776 raw → 3,401,267 after dropping non-London rows → **3,394,911** after
removing duplicates.

## Limitations

- **Counts, not rates.** There is no population data, so a high count does not mean a higher
  risk per resident. Westminster and the City draw large daytime populations.
- **Recorded crime, not actual crime.** Reporting and police activity shape what appears,
  especially for drugs and possession offences.
- **2023 is weaker at borough level.** 23,486 of 2023's records (2.1%) have no location,
  including 7,317 in October 2023, versus 665 in 2024 and none in 2025. Borough counts for
  2023 are therefore understated, which is why borough changes above compare 2024 with 2025.
  Totals by year and by crime type are not affected.
- **Rows are records, not unique crimes.** About 40,000 rows (1.2%) repeat a `Crime ID` that
  already appears in the same month, usually with a different outcome (sometimes a different
  crime type). They were kept as separate records.
- **Category changes.** The source may record or classify offences differently over time, which
  this analysis cannot check.
- **City of London is not comparable.** It has its own police force; the Met files contain only
  5,055 City records over three years.
- **Location is approximate.** The source anonymises coordinates to street level ("On or near
  ..."), so borough is the appropriate level of detail.
- **No external variables** (weather, events, policing policy) were joined, so explanations
  are hypotheses.

## Repository Structure

```
notebooks/clean_pipeline.ipynb              Read, merge and clean the 36 raw files
sql/monthly_borough_crime.sql               Aggregate to month × borough × crime type
data/processed/monthly_crimes_by_type_borough.csv   Aggregated table used by the dashboard
dashboard/london_crime_v1.pbip              Power BI project
```
