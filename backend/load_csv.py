from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "backend" / "data" / "idrs.csv"
DB_PATH = BASE_DIR / "backend" / "database.db"

df = pd.read_csv(CSV_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}")

df.to_sql("idr_table", engine, if_exists="replace", index=False)

print("Loaded:", len(df))
