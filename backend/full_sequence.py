import pandas as pd
import requests
import time
from tqdm import tqdm
import os

INPUT_CSV  = "data/idrs_with_gene_name.csv"
OUTPUT_CSV = "data/idrs_with_full_seq.csv"

# ---------------------------
# Load / resume
# ---------------------------
if os.path.exists(OUTPUT_CSV):
    df = pd.read_csv(OUTPUT_CSV, low_memory=False)
    print("🔄 Resuming from saved file")
else:
    df = pd.read_csv(INPUT_CSV, low_memory=False)
    df["full_sequence"] = df["full_sequence"].fillna("")
    print("📄 Fresh start")

# ---------------------------
# Unique accessions to fetch
# ---------------------------
to_fetch = (
    df[df["full_sequence"].isna() | (df["full_sequence"] == "")]
    ["accession"]
    .dropna()
    .unique()
)

print("🔬 Proteins remaining:", len(to_fetch))

# ---------------------------
# Batch fetcher
# ---------------------------
def fetch_batch(accessions):
    query = " OR ".join(f"accession:{a}" for a in accessions)

    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "format": "fasta",
        "size": len(accessions)
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.text

# ---------------------------
# Parse FASTA
# ---------------------------
def parse_fasta(fasta_text):
    sequences = {}
    acc = None
    seq = []
    for line in fasta_text.splitlines():
        if line.startswith(">"):
            if acc:
                sequences[acc] = "".join(seq)
            acc = line.split("|")[1]
            seq = []
        else:
            seq.append(line.strip())
    if acc:
        sequences[acc] = "".join(seq)
    return sequences

# ---------------------------
# Process batches
# ---------------------------
BATCH_SIZE = 100

for i in tqdm(range(0, len(to_fetch), BATCH_SIZE)):
    batch = to_fetch[i:i+BATCH_SIZE]

    try:
        fasta = fetch_batch(batch)
        seqs = parse_fasta(fasta)

        for acc, seq in seqs.items():
            df.loc[df["accession"] == acc, "full_sequence"] = seq

    except Exception as e:
        print(f"⚠️ Batch failed: {e}")

    # Save every batch
    df.to_csv(OUTPUT_CSV, index=False)
    time.sleep(1)  # UniProt-safe pause

print("✅ DONE — sequences fetched efficiently")

print("Total rows:", len(df))
print("Columns:", df.columns.tolist())

if "full_sequence" in df.columns:
    print("Non-empty full_sequence:",
          df["full_sequence"].notna().sum())
    print("Empty string full_sequence:",
          (df["full_sequence"] == "").sum())
else:
    print("❌ full_sequence column missing")
