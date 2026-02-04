from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()

# Templates & static
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load IDR data
df = pd.read_csv("data/idrs.csv")
df.columns = df.columns.str.strip().str.lower()  # normalize

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/idrs")
def search_idrs(search: str):
    df["gene_name"] = df["gene_name"].astype(str)
    df["accession"] = df["accession"].astype(str)

    search = search.lower()

    results = df
        df["gene_name"].str.lower().str.contains(search, na=False)
        df["accession"].str.lower().str.contains(search, na=False)
    ][["gene", "accession"]].head(10)

    return results.to_dict(orient="records")
