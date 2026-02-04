import pandas as pd

df = pd.read_csv("protein_disorder_summary.csv")

subset = df[(df["percent_disorder"] == 100) & (df["length"] > 300)]

print("Number of proteins with 100% disorder and length > 300:")
print(len(subset))

print("\nTop examples:")
print(subset[["gene_name", "length"]].head(10))

