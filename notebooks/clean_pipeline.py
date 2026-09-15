import glob
import pandas as pd

RAW_DIR = "../data/raw"
OUT_CSV = "../data/processed/london_crime_2024_2025_clean.csv"

files = sorted(glob.glob(f"{RAW_DIR}/*.csv"))
print(f"Found {len(files)} files")
assert len(files) == 24, f"Expected 24 files, found {len(files)}"

# Verify all files share identical columns before concatenating
ref_cols = pd.read_csv(files[0], nrows=0).columns.tolist()
for f in files:
    cols = pd.read_csv(f, nrows=0).columns.tolist()
    assert cols == ref_cols, f"Column mismatch in {f}: {cols}"
print("All 24 files share identical columns:", ref_cols)

# Read and concatenate all files
list_df = [pd.read_csv(f) for f in files]
df_all = pd.concat(list_df, ignore_index=True)
print("Merged shape:", df_all.shape)

# Drop the fully-empty Context column
df_all = df_all.drop(columns=["Context"])

# Convert Month to datetime
df_all["Month"] = pd.to_datetime(df_all["Month"])

# Derive Borough from LSOA name (borough name is the text before the trailing area code)
df_all["Borough"] = df_all["LSOA name"].str.extract(r"^(.*?)\s+\S+$")

LONDON_BOROUGHS = [
    "Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley", "Camden",
    "Croydon", "Ealing", "Enfield", "Greenwich", "Hackney",
    "Hammersmith and Fulham", "Haringey", "Harrow", "Havering", "Hillingdon",
    "Hounslow", "Islington", "Kensington and Chelsea", "Kingston upon Thames",
    "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge",
    "Richmond upon Thames", "Southwark", "Sutton", "Tower Hamlets",
    "Waltham Forest", "Wandsworth", "Westminster", "City of London",
]

# Drop rows outside the 33 official London boroughs (~0.44% of rows — crimes
# near the Met Police boundary occasionally snap to a neighbouring county's
# LSOA; not relevant to an in-London borough comparison)
n_before = len(df_all)
df_all = df_all[df_all["Borough"].isin(LONDON_BOROUGHS)]
print(f"Dropped {n_before - len(df_all)} rows outside the 33 London boroughs "
      f"({(n_before - len(df_all)) / n_before * 100:.2f}%)")

# Remove true duplicates: only among rows that have a Crime ID
# (Anti-social behaviour rows lack Crime ID and are NOT true duplicates even if
#  every other column matches — see project notes)
has_id = df_all["Crime ID"].notnull()
df_with_id = df_all[has_id].drop_duplicates()
df_without_id = df_all[~has_id]
df_clean = pd.concat([df_with_id, df_without_id], ignore_index=True)
print("Shape before/after true-duplicate removal:", df_all.shape, "->", df_clean.shape)

# Sanity checks before saving
assert df_clean.shape[0] > 2_000_000, "Row count looks too low for 24 months of London data"
assert df_clean["Borough"].notnull().mean() > 0.99, "Too many missing Borough values"
assert df_clean["Month"].min().strftime("%Y-%m") == "2024-01"
assert df_clean["Month"].max().strftime("%Y-%m") == "2025-12"

df_clean.to_csv(OUT_CSV, index=False)

# Verify what was actually written to disk (this is exactly what caught nothing last time)
import os
size_mb = os.path.getsize(OUT_CSV) / (1024 * 1024)
check = pd.read_csv(OUT_CSV)
print(f"Saved {OUT_CSV} -- {size_mb:.1f} MB on disk, {check.shape[0]} rows read back")
assert check.shape[0] == df_clean.shape[0], "Row count mismatch after re-reading saved file!"
assert size_mb > 50, "File on disk is suspiciously small"
print("Borough sample values:", df_clean["Borough"].dropna().unique()[:10])
print("ALL CHECKS PASSED")
