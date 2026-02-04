import pandas as pd

df = pd.read_csv("protein_disorder_summary.csv")

known_idps = ["TP53", "BRCA1", "MYC", "SNCA", "MAPT"]

print("Known IDP validation:\n")

for gene in known_idps:
    subset = df[df["gene_name"].str.contains(gene, na=False)]
    if subset.empty:
        print(f"{gene}: NOT FOUND")
    else:
        print(f"\n{gene}")
        print(subset[["accession", "length", "percent_disorder"]])

df_sorted = df.sort_values("percent_disorder", ascending=False)

df_sorted["rank"] = range(1, len(df_sorted) + 1)

df_sorted[
    df_sorted["gene_name"].str.contains("TP53|BRCA1|MYC|SNCA|MAPT", na=False)
][["gene_name", "percent_disorder", "rank"]]

import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.hist(df["percent_disorder"], bins=50, alpha=0.7)

for gene in ["TP53", "BRCA1", "SNCA"]:
    vals = df[df["gene_name"].str.contains(gene, na=False)]["percent_disorder"]
    for v in vals:
        plt.axvline(v, linestyle="--", label=gene)

plt.xlabel("% Disorder")
plt.ylabel("Protein count")
plt.title("Biological Validation of Known IDPs")
plt.legend()
plt.show()

