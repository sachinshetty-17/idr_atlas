import pandas as pd

genes = pd.read_csv("uniprot_gene_map.tsv")

print(genes.columns)
print(genes.head())
