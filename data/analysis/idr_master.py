import pandas as pd
from parameters_analyser import compute_idr_parameters

regions = pd.read_csv("idr_regions.csv")

rows = []

for _, row in regions.iterrows():
    seq = row["sequence"]

    params = compute_idr_parameters(seq)

    idr_id = f"{row['accession']}_{row['start']}_{row['end']}"

    rows.append({
        "idr_id": idr_id,
        "accession": row["accession"],
        "gene_name": row.get("gene_name", ""),
        "start": row["start"],
        "end": row["end"],
        "sequence": seq,
        "length": len(seq),

        "f_plus": params["f_plus"],
        "f_minus": params["f_minus"],
        "FCR": params["FCR"],
        "NCPR": params["NCPR"],
        "kappa": params["kappa"],
        "hydropathy": params["hydropathy"],
        "aromatic_density": params["aromatic_density"],
        "pro_fraction": params["pro_fraction"],
        "gly_fraction": params["gly_fraction"],
    })

master = pd.DataFrame(rows)
master.to_csv("idr_master.csv", index=False)

print("✅ Master IDR table built:", len(master))

