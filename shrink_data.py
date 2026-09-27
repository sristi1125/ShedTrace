"""
One-off script: shrink the big NYC datasets down to only the buildings
that actually have a sidewalk shed on file, since the app only ever
looks up shed buildings anyway.
"""
import pandas as pd

DATA_DIR = "data/"

sheds = pd.read_csv(DATA_DIR + "sidewalk_sheds.csv", low_memory=False)
sheds["BIN Number"] = sheds["BIN Number"].astype(str)
shed_bins = set(sheds["BIN Number"].unique())
print(f"Found {len(shed_bins)} unique shed BINs")

def shrink(filename, bin_col, clean_as_float=False):
    path = DATA_DIR + filename
    df = pd.read_csv(path, low_memory=False)
    if clean_as_float:
        df[bin_col] = (
            pd.to_numeric(df[bin_col], errors="coerce")
            .fillna(0)
            .astype(int)
            .astype(str)
        )
    else:
        df[bin_col] = df[bin_col].astype(str)
    before = len(df)
    filtered = df[df[bin_col].isin(shed_bins)]
    after = len(filtered)
    filtered.to_csv(path, index=False)
    print(f"{filename}: {before} rows -> {after} rows")

shrink("dob_violations.csv", "BIN")
shrink("dob_complaints.csv", "BIN")
shrink("elevator_safety.csv", "BIN", clean_as_float=True)
shrink("fire_safety.csv", "BIN", clean_as_float=True)
print("Done. Check file sizes with: ls -lh data/")
