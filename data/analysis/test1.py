import pandas as pd

df = pd.read_csv("idr_parameters.csv")

tp53_idrs = df[df["accession"] == "P04637"]

print("Number of TP53 IDRs:", len(tp53_idrs))
print(tp53_idrs[[
    "idr_id", "start", "end", "length",
    "f_plus", "f_minus", "FCR", "NCPR",
    "kappa", "hydropathy",
    "pro_fraction", "gly_fraction"
]])

