import pandas as pd

df = pd.read_csv("backend/data/idrs_with_gene_name.csv")

print("Total rows:", len(df))
print("Gene names filled:", (df["gene_name"] != "").sum())
print("Missing gene names:", (df["gene_name"] == "").sum())

