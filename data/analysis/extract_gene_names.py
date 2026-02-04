import re
import pandas as pd

records = []

with open("human_reviewed_uniprot.fasta") as f:
    for line in f:
        if line.startswith(">"):
            # Extract accession
            acc = line.split("|")[1]

            # Extract gene name (GN=)
            match = re.search(r"GN=([A-Za-z0-9_-]+)", line)
            gene = match.group(1) if match else None

            records.append({
                "accession": acc,
                "gene_name": gene
            })

df = pd.DataFrame(records)
df.to_csv("uniprot_accession_gene_map.csv", index=False)

print("Total entries:", len(df))
print("Missing gene names:", df["gene_name"].isna().sum())
