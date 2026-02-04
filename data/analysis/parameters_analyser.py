import pandas as pd
from parameters_main import compute_idr_parameters

df = pd.read_csv("idr_regions.csv")

all_params = []

for _, row in df.iterrows():
    seq = row["sequence"]
    params = compute_idr_parameters(seq)

    params["idr_id"] = f"{row['accession']}_{row['start']}_{row['end']}"
    params["accession"] = row["accession"]
    params["start"] = row["start"]
    params["end"] = row["end"]

    all_params.append(params)

out = pd.DataFrame(all_params)
out.to_csv("idr_parameters.csv", index=False)

print("✅ Parameters computed for all IDRs:", len(out))

import numpy as np

POS = set("KR")
NEG = set("DE")

def compute_kappa(sequence):
    L = len(sequence)
    if L < 2:
        return None

    charges = np.array([
        1 if aa in POS else -1 if aa in NEG else 0
        for aa in sequence
    ])

    pos_idx = np.where(charges == 1)[0]
    neg_idx = np.where(charges == -1)[0]

    if len(pos_idx) == 0 or len(neg_idx) == 0:
        return None  # biologically undefined

    distances = [(i - j) ** 2 for i in pos_idx for j in neg_idx]
    mean_unlike = np.mean(distances)
    max_dist = (L - 1) ** 2

    return round(mean_unlike / max_dist, 4)
df["kappa"] = df["sequence"].apply(compute_kappa)
