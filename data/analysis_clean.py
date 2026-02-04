import pandas as pd
import re

INPUT_FILE = "uniprot_human.tsv"
OUTPUT_FILE = "uniprot_human_clean.csv"

df = pd.read_csv(INPUT_FILE, sep="\t")

print("Columns found:", df.columns.tolist())

# Normalize column names
df.columns = [c.lower().strip() for c in df.columns]

# Rename common UniProt variants
if "sequence" not in df.columns:
    for col in df.columns:
        if "sequence" in col:
            df = df.rename(columns={col: "sequence"})
            break

print("Using sequence column:", "sequence" in df.columns)

# Drop missing sequences
df = df.dropna(subset=["sequence"])

# Validate amino acids
valid_aa = re.compile("^[ACDEFGHIKLMNPQRSTVWY]+$")

df = df[df["sequence"].apply(lambda x: bool(valid_aa.match(str(x))))]

# Remove duplicates
if "accession" in df.columns:
    df = df.drop_duplicates(subset=["accession"])

df.to_csv(OUTPUT_FILE, index=False)

print("Clean proteins saved:", len(df))

