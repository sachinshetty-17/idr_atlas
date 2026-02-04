import pandas as pd

df = pd.read_csv("data/idrs_with_full_seq.csv")
print(df[["idr_id", "accession", "sequence", "full_sequence"]].head(5))


