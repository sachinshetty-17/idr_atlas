import pandas as pd

idr = pd.read_csv("idr_master_with_genes.csv")
accessions = idr["accession"].dropna().unique()
display_name = gene_name if gene_name else accession

print(len(accessions))

