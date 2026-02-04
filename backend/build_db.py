import pandas as pd
import sqlite3

CSV = "backend/data/idrs_with_gene_name.csv"
DB  = "backend/database.db"

df = pd.read_csv(CSV, low_memory=False)

conn = sqlite3.connect(DB)
df.to_sql("idr_table", conn, if_exists="replace", index=False)

# Add indexes (CRITICAL)
conn.execute("CREATE INDEX idx_idr_id ON idr_table(idr_id)")
conn.execute("CREATE INDEX idx_accession ON idr_table(accession)")
conn.execute("CREATE INDEX idx_gene_name ON idr_table(gene_name)")

conn.close()

print("✅ Database built with indexes")
