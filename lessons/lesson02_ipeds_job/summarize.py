"""Summarize one IPEDS institutional directory file.

Usage: python3 summarize.py directory_2015.parquet results/
"""
import sys
from pathlib import Path

import pandas as pd

infile = sys.argv[1]
outdir = Path(sys.argv[2])
outdir.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(infile)
print(f"File: {infile}")
print(f"Rows (institutions): {len(df):,}")
print(f"Columns: {df.shape[1]}")
print(f"Year: {sorted(df['year'].unique().tolist())}")

by_state = (
    df.groupby("state_abbr")
    .size()
    .rename("institutions")
    .reset_index()
    .sort_values("institutions", ascending=False)
)
by_state.to_csv(outdir / "institutions_by_state.csv", index=False)

by_sector = (
    df.groupby("sector")
    .size()
    .rename("institutions")
    .reset_index()
    .sort_values("institutions", ascending=False)
)
by_sector.to_csv(outdir / "institutions_by_sector.csv", index=False)

print("\nTop 5 states:")
print(by_state.head(5).to_string(index=False))
print("\nInstitutions by sector code:")
print(by_sector.to_string(index=False))
