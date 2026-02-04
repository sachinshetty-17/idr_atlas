import pandas as pd
import requests
from tqdm import tqdm
import os

CSV_IN  = "backend/data/idrs.csv"
CSV_OUT = "backend/data/idrs_with_gene_name.csv"

# --------------------------------------------------
# Load existing progress if present
# --------------------------------------------------
if os.path.exists(CSV_OUT):
    print("🔁 Resuming from existing file...")
    df = pd.read_csv(CSV_OUT)
else:
    print("🆕 Starting fresh...")
    df = pd.read_csv(CSV_IN)
    df["gene_name"] = ""

# --------------------------------------------------
# Find unfinished accessions
# --------------------------------------------------
pending = (
    df.loc[df["gene_name"].isna() | (df["gene_name"] == ""), "accession"]
    .dropna()
    .unique()
)

print(f"⏳ Pending accessions: {len(pending)}")

# --------------------------------------------------
# UniProt bulk fetch
# --------------------------------------------------
BASE_URL = "https://rest.uniprot.org/uniprotkb/search"

def fetch_batch(acc_list):
    query = " OR ".join(f"accession:{a}" for a in acc_list)
    params = {
        "query": query,
        "format": "json",
        "fields": "accession,gene_names"
    }

    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json()

    mapping = {}
    for entry in data["results"]:
        acc = entry["primaryAccession"]
        genes = entry.get("genes", [])
        if genes and "geneName" in genes[0]:
            mapping[acc] = genes[0]["geneName"]["value"]
        else:
            mapping[acc] = ""

    return mapping

# --------------------------------------------------
# Batch processing with autosave
# --------------------------------------------------
BATCH_SIZE = 300
SAVE_EVERY = 5   # batches

gene_map = {}

for i in tqdm(range(0, len(pending), BATCH_SIZE)):
    batch = pending[i:i+BATCH_SIZE]

    try:
        gene_map.update(fetch_batch(batch))
    except Exception as e:
        print("⚠️ Batch failed:", e)
        continue

    # Write to dataframe
    df.loc[df["accession"].isin(gene_map.keys()), "gene_name"] = (
        df["accession"].map(gene_map)
    )

    # Autosave
    if (i // BATCH_SIZE) % SAVE_EVERY == 0:
        df.to_csv(CSV_OUT, index=False)

pending = pending[:20]

# Final save
df.to_csv(CSV_OUT, index=False)
print("✅ DONE — safely saved.")

