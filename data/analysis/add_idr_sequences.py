import pandas as pd

# Load protein sequences
proteins = pd.read_csv("protein_disorder_summary.csv")
proteins = proteins.set_index("accession")

# Load IDR coordinates
idrs = pd.read_csv("idrs.csv")

idr_rows = []

for _, row in idrs.iterrows():
    acc = row["accession"]
    start = int(row["start"])
    end = int(row["end"])

    if acc not in proteins.index:
        continue  # safety

    full_seq = proteins.loc[acc, "sequence"]

    # UniProt coordinates are 1-based
    idr_seq = full_seq[start-1:end]

    idr_rows.append({
        "accession": acc,
        "start": start,
        "end": end,
        "length": len(idr_seq),
        "sequence": idr_seq
    })

out = pd.DataFrame(idr_rows)
out.to_csv("idr_regions.csv", index=False)

print("✅ IDR sequences added:", len(out))
