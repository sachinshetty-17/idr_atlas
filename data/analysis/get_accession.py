import pandas as pd

df = pd.read_csv("idr_master.csv")

accessions = df["accession"].dropna().unique()

pd.Series(accessions).to_csv(
    "accessions.txt",
    index=False,
    header=False
)

print("Unique accessions:", len(accessions))
