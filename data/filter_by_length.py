import pandas as pd

INPUT = "uniprot_human_clean.csv"
OUTPUT = "human_filter_length.csv"

df = pd.read_csv(INPUT)

df["size_class"] = "normal"
df.loc[df["length"] < 50, "size_class"] = "too_short"
df.loc[df["length"] > 5000, "size_class"] = "giant"

filtered = df[df["size_class"] != "too_short"]

filtered.to_csv(OUTPUT, index=False)

print("Original:", len(df))
print("After filtering:", len(filtered))
print("Giant proteins:", (filtered["size_class"] == "giant").sum())
