import requests
import pandas as pd
import os
import time
from io import StringIO

BASE_URL = "https://rest.uniprot.org/uniprotkb/search"
QUERY = "organism_id:9606 AND reviewed:true"
FIELDS = "accession,protein_name,gene_names,organism_name,length,sequence"
FORMAT = "tsv"
SIZE = 100

OUTPUT_FILE = "data/uniprot_humanreviewed_data.csv"
CURSOR_FILE = "data/uniprot_cursor.txt"

def load_cursor():
    if os.path.exists(CURSOR_FILE):
        with open(CURSOR_FILE, "r") as f:
            return f.read().strip()
    return None


def save_cursor(cursor):
    with open(CURSOR_FILE, "w") as f:
        f.write(cursor)


def fetch_all_uniprot():
    cursor = load_cursor()

    while True:
        params = {
            "query": QUERY,
            "fields": FIELDS,
            "format": FORMAT,
            "size": SIZE
        }

        if cursor:
            params["cursor"] = cursor

        print("Fetching UniProt batch...")
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print("HTTP error:", response.status_code)
            print("Stopping safely. Re-run later.")
            break

        df = pd.read_csv(StringIO(response.text), sep="\t")

        if df.empty:
            print("All proteins fetched.")
            break

        file_exists = os.path.exists(OUTPUT_FILE)
        df.to_csv(OUTPUT_FILE, mode="a", index=False, header=not file_exists)

        print(f"Saved {len(df)} proteins")
        time.sleep(2)

        link_header = response.headers.get("Link", "")
        next_cursor = None

        for part in link_header.split(","):
            if 'rel="next"' in part:
                next_cursor = part.split("cursor=")[1].split(">")[0]

        if not next_cursor:
            print("No next cursor. Finished.")
            if os.path.exists(CURSOR_FILE):
                os.remove(CURSOR_FILE)
            break

        save_cursor(next_cursor)
        cursor = next_cursor
        print("Cursor saved. Ready for next batch.")

if os.path.exists(OUTPUT_FILE) and load_cursor() is None:
    print("⚠️ Warning: CSV exists but no cursor found.")
    print("This may cause duplicate downloads.")

if __name__ == "__main__":
    fetch_all_uniprot()
