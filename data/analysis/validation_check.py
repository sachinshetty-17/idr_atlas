import pandas as pd

df = pd.read_csv("idr_master_final.csv")

tp53 = df[df["gene_name_y"] == "TP53"]

print("Number of TP53 IDRs:", len(tp53))
print(tp53[["idr_id", "accession", "start", "end", "length", "FCR", "NCPR", "kappa"]])

