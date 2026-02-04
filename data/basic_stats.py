import pandas as pd

INPUT_FILE = "uniprot_human_clean.csv"

df = pd.read_csv(INPUT_FILE)

print("Proteins:", len(df))
print("Min length:", df["length"].min())
print("Max length:", df["length"].max())
print("Mean length:", int(df["length"].mean()))

# Optional but useful
print("Median length:", int(df["length"].median()))

# Count very small and very large proteins
print("Proteins < 50 aa:", (df["length"] < 50).sum())
print("Proteins > 5000 aa:", (df["length"] > 5000).sum())

