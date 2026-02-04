import requests

url = "https://rest.uniprot.org/uniprotkb/stream"
params = {
    "query": "organism_id:9606 AND reviewed:true",
    "format": "tsv",
    "fields": "accession,protein_name,gene_names,organism_name,length,sequence"
}

output_file = "data/uniprot_humanreviewed_data.csv"

print("Downloading full human reviewed proteome...")

with requests.get(url, params=params, stream=True) as r:
    r.raise_for_status()
    with open(output_file, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

print("Download complete.")
