import pandas as pd

fire = pd.read_csv("data/fire_safety.csv", low_memory=False)
print("Unique LAST_INSP_STAT values:")
print(fire["LAST_INSP_STAT"].value_counts(dropna=False))