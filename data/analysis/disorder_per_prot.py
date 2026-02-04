import pandas as pd

# Load protein table and IDR table
proteins = pd.read_csv("uniprot_human_clean.csv")  # contains accession, length
idrs = pd.read_csv("idrs.csv")                     # accession, start, end, idr_length

# Sum IDR lengths per protein
idr_sum = idrs.groupby("accession")["length"].sum().reset_index()
idr_sum.columns = ["accession", "total_idr_length"]

# Merge with protein lengths
df = proteins.merge(idr_sum, on="accession", how="left")

# Fill proteins with no IDRs as 0
df["total_idr_length"] = df["total_idr_length"].fillna(0)

# Calculate % disorder
df["percent_disorder"] = (df["total_idr_length"] / df["length"]) * 100

# Save summary table
df.to_csv("protein_disorder_summary.csv", index=False)

print("Protein disorder summary saved: data/protein_disorder_summary.csv")
print(df[["accession", "length", "total_idr_length", "percent_disorder"]].head())
