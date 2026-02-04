import requests
import pandas as pd
from time import sleep

ACCESSION_FILE = "accessions.txt"
OUT_FILE = "uniprot_gene_map.tsv"
BATCH_SIZE = 50

def fetch_genes(accessions):
    acc_string = " ".join(accessions)
    query = f"accession:({acc_string})"

    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "format": "tsv",
        "fields": "accession,gene_primary",
    }

    r = requests.get(url, params=params)
    print("Query:", query)
    r.raise_for_status()
    return r.text

# Load accessions
with open(ACCESSION_FILE) as f:
    all_accessions = [line.strip() for line in f if line.strip()]

rows = []

for i in range(0, len(all_accessions), BATCH_SIZE):
    batch = all_accessions[i:i+BATCH_SIZE]
    print(f"Fetching {i}–{i+len(batch)}")
    text = fetch_genes(batch)
    lines = text.strip().split("\n")[1:]  # skip header
    rows.extend([line.split("\t") for line in lines])
    sleep(1)  # be nice to UniProt

df = pd.DataFrame(rows, columns=["accession", "gene_name"])
df.to_csv(OUT_FILE, sep="\t", index=False)

print("Gene mapping saved:", OUT_FILE)

