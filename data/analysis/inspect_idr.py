import pandas as pd
idr = pd.read_csv("idr_master.csv")
genes = pd.read_csv("uniprot_gene_map.tsv", sep="\t")

print("IDR accession examples:")
print(idr["accession"].head(10).tolist())

print("\nUniProt accession examples:")
print(genes.iloc[:10, 0].tolist())
