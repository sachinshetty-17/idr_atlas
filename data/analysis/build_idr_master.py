import pandas as pd
from parameters_engine import compute_idr_parameters

idr_df = pd.read_csv("idr_regions.csv")

rows = []

for _, row in idr_df.iterrows():
    seq = row["sequence"]

    params = compute_idr_parameters(seq)
    if params is None:
        continue

    idr_id = f"{row['accession']}_{row['start']}_{row['end']}"

    rows.append({
        "idr_id": idr_id,
        "accession": row["accession"],
        "gene_name": row.get("gene_name", "NA"),
        "organism": row.get("organism", "Homo sapiens"),
        "start": row["start"],
        "end": row["end"],
        "sequence": seq,
        **params
    })

master = pd.DataFrame(rows)
master.to_csv("idr_master.csv", index=False)

print(f"✅ IDR master table built: {len(master)} IDRs")
