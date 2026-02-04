import pandas as pd

DISORDER_AA = set("EDPGSQ")
WINDOW = 30
THRESHOLD = 0.4

proteins = pd.read_csv("uniprot_human_clean.csv")

def merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals)
    merged = [intervals[0]]
    for curr in intervals[1:]:
        prev = merged[-1]
        if curr[0] <= prev[1] + 1:
            merged[-1] = (prev[0], max(prev[1], curr[1]))
        else:
            merged.append(curr)
    return merged

def predict_idrs(seq):
    raw = []
    for i in range(len(seq) - WINDOW + 1):
        window = seq[i:i+WINDOW]
        score = sum(aa in DISORDER_AA for aa in window) / WINDOW
        if score >= THRESHOLD:
            raw.append((i+1, i+WINDOW))
    return merge_intervals(raw)

print("Predicting IDRs...")

predictions = []

for _, row in proteins.iterrows():
    predictions.append({
        "accession": row["accession"],
        "predicted_idrs": predict_idrs(row["sequence"])
    })

pred_df = pd.DataFrame(predictions)
pred_df.to_csv("idr_predictions_v1.csv", index=False)

print("Saved → idr_predictions_v1.csv")
print(pred_df.head())


