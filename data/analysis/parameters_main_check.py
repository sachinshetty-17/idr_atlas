import pandas as pd

df = pd.read_csv("idr_master.csv")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nKappa statistics:")
print(df["kappa"].describe())

df[df["accession"] == "P04637"]

