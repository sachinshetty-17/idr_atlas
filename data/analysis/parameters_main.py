# parameters_main.py

import pandas as pd
from parameters_engine import compute_idr_parameters

df = pd.read_csv("idr_regions.csv")

records = []

for i, row in df.iterrows():
    seq = row["sequence"]

    params = compute_idr_parameters(seq)

    record = {
        "idr_uid": f"{row['accession']}_{row['start']}_{row['end']}",
        "accession": row["accession"],
        "start": row["start"],
        "end": row["end"],
        **params
    }

    records.append(record)

    if i == 0:
        print("[DEBUG] First IDR:")
        for k, v in params.items():
            print(f"  {k}: {v}")

out = pd.DataFrame(records)
out.to_csv("idr_master.csv", index=False)

print(f"\n✅ Parameters computed for all IDRs: {len(out)}")

