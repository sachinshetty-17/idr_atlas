import pandas as pd
import matplotlib.pyplot as plt

# Load protein disorder summary
df = pd.read_csv("protein_disorder_summary.csv")

# Histogram: % disorder
plt.figure(figsize=(8,5))
plt.hist(df["percent_disorder"], bins=50, color='skyblue', edgecolor='black')
plt.xlabel("% Disorder")
plt.ylabel("Number of Proteins")
plt.title("Distribution of % Disorder Across Human Proteome")
plt.grid(axis='y', alpha=0.5)
plt.show()

# Optional: Scatter plot disorder vs protein length
plt.figure(figsize=(8,5))
plt.scatter(df["length"], df["percent_disorder"], alpha=0.3)
plt.xlabel("Protein Length (aa)")
plt.ylabel("% Disorder")
plt.title("Protein Length vs % Disorder")
plt.show()
