import pandas as pd

genes = pd.read_csv("uniprot_gene_map.tsv")

def clean_uniprot(acc):
    if pd.isna(acc):
        return acc
    if "|" in acc:
        return acc.split("|")[1]
    return acc.strip()

genes["accession"] = genes["accession"].apply(clean_uniprot)

genes.to_csv("uniprot_gene_map_clean.csv", index=False)
print("Accessions cleaned.")
