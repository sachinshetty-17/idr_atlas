import pandas as pd

genes = pd.read_csv("uniprot_gene_map.tsv", sep="\t")
print(genes.head())
print(genes.columns)
print("Rows:", len(genes))

