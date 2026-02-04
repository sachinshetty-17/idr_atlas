import pandas as pd
import ast

pred = pd.read_csv("idr_predictions_v1.csv")

rows = []

for _, row in pred.iterrows():
    accession = row["accession"]
    idrs = ast.literal_eval(row["predicted_idrs"])

    for start, end in idrs:
        rows.append({
            "accession": accession,
            "start": start,
            "end": end,
            "length": end - start + 1
        })

idr_df = pd.DataFrame(rows)
idr_df.to_csv("idrs.csv", index=False)

print("IDR regions saved:", len(idr_df))



