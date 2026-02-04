import pandas as pd

# load the parameters file you created earlier
df = pd.read_csv("idr_")

print(df["kappa"].describe())
print("NaN kappa count:", df["kappa"].isna().sum())

