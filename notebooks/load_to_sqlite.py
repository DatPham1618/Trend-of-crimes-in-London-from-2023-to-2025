import sqlite3
import pandas as pd

CSV_PATH = "../data/processed/london_crime_2024_2025_clean.csv"
DB_PATH = "../data/processed/london_crime.db"

df = pd.read_csv(CSV_PATH, low_memory=False)
print("Loaded from CSV:", df.shape)

conn = sqlite3.connect(DB_PATH)
df.to_sql("crimes", conn, if_exists="replace", index=False, chunksize=50000)

# Verify what actually landed in the DB file
n_rows = conn.execute("SELECT COUNT(*) FROM crimes").fetchone()[0]
cols = [r[1] for r in conn.execute("PRAGMA table_info(crimes)").fetchall()]
conn.close()

import os
size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
print(f"DB file size: {size_mb:.1f} MB")
print(f"Row count in DB: {n_rows}")
print(f"Columns in DB: {cols}")
assert n_rows == df.shape[0], "Row count mismatch between CSV and DB!"
assert size_mb > 50, "DB file suspiciously small"
print("ALL CHECKS PASSED")
