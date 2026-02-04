import pandas as pd

idr = pd.read_csv("idr_master_with_genes.csv")
genes = pd.read_csv("uniprot_accession_gene_map.csv")

merged = idr.merge(genes, on="accession", how="left")

merged.to_csv("idr_master_final.csv", index=False)

print("Final IDR count:", len(merged))
print("Missing gene names:", merged["gene_name_y"].isna().sum())
