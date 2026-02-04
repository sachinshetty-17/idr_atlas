from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend JS to call backend (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/statics", StaticFiles(directory="statics"), name="static")

# Mock IDR data
mock_idrs = [
    {"id": 1, "protein_name": "ProteinA", "start": 5, "end": 50, "length": 46, "fcr": 0.2, "ncpr": "neutral"},
    {"id": 2, "protein_name": "ProteinB", "start": 100, "end": 200, "length": 101, "fcr": 0.4, "ncpr": "positive"},
    {"id": 3, "protein_name": "ProteinC", "start": 50, "end": 90, "length": 41, "fcr": 0.1, "ncpr": "negative"},
]

# Homepage
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to fetch IDRs
@app.get("/idrs")
def get_idrs(search: str = "", minLength: int = None, maxLength: int = None,
             minFCR: float = None, maxFCR: float = None, ncpr: str = ""):

    results = mock_idrs

    if search:
        results = [idr for idr in results if search.lower() in idr["protein_name"].lower()]

    if minLength is not None:
        results = [idr for idr in results if idr["length"] >= minLength]

    if maxLength is not None:
        results = [idr for idr in results if idr["length"] <= maxLength]

    if minFCR is not None:
        results = [idr for idr in results if idr["fcr"] >= minFCR]

    if maxFCR is not None:
        results = [idr for idr in results if idr["fcr"] <= maxFCR]

    if ncpr:
        results = [idr for idr in results if idr["ncpr"] == ncpr]

    return JSONResponse(results)
