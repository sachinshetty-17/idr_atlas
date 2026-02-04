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
