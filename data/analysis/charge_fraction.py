import pandas as pd

# Load protein disorder summary (must include percent_disorder)
df = pd.read_csv("protein_disorder_summary.csv")

# Define charged amino acids
charged_aa = set("EDKR")

# Function to calculate charge fraction
def compute_charge_fraction(seq):
    if len(seq) == 0:
        return 0
    return sum(aa in charged_aa for aa in seq) / len(seq)

# Add charge fraction
df["charge_fraction"] = df["sequence"].apply(compute_charge_fraction)

# Calculate refined disorder score
df["refined_disorder_score"] = df["percent_disorder"] + 0.5 * df["charge_fraction"]*100

# Save updated CSV
df.to_csv("protein_disorder_scored.csv", index=False)

print("Charge fractions and refined disorder score added!")
print(df[["accession","percent_disorder","charge_fraction","refined_disorder_score"]].head())

