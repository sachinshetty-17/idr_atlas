import matplotlib
matplotlib.use("Agg")

from flask import Flask, render_template, request, abort, send_file
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

df = pd.read_csv("backend/data/idrs_with_full_seq.csv", low_memory=False)

df["idr_id"] = df["idr_id"].astype(str)
df["gene_name"] = df["gene_name"].astype(str)
df["accession"] = df["accession"].astype(str)

# ---------------- SEARCH ----------------

def search_df(q):
    if not q:
        return df.iloc[0:0]

    q = q.lower()
    return df[
        df["idr_id"].str.lower().str.contains(q) |
        df["gene_name"].str.lower().str.contains(q) |
        df["accession"].str.lower().str.contains(q)
    ]

@app.route("/")
def index():
    q = request.args.get("q","")
    view = request.args.get("view","card")

    results = search_df(q).head(200)

    return render_template(
        "index.html",
        results=results.to_dict(orient="records"),
        q=q,
        view=view
    )

# ---------------- SEQUENCE ----------------

@app.route("/sequence/<idr_id>")
def sequence(idr_id):
    row = df[df["idr_id"] == idr_id]
    if row.empty:
        abort(404)

    row = row.iloc[0]

    full_seq = row["full_sequence"]
    start = int(row["start"]) - 1
    end = int(row["end"])

    highlighted = (
        full_seq[:start] +
        f"<span class='idr'>" + full_seq[start:end] + "</span>" +
        full_seq[end:]
    )

    wrapped = "<br>".join(
        highlighted[i:i+60] for i in range(0, len(highlighted), 60)
    )

    return render_template(
        "sequence.html",
        idr=row.to_dict(),
        sequence=wrapped
    )

# ---------------- DATASET PLOTS ----------------

@app.route("/plots/length_histogram")
def length_hist():
    fig, ax = plt.subplots(figsize=(6,4))
    ax.hist(df["length"], bins=50, log=True)
    ax.set_xlabel("Length")
    ax.set_ylabel("Count (log)")
    ax.set_title("IDR Length Distribution")

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=300)
    plt.close(fig)
    buf.seek(0)

    return send_file(buf, mimetype="image/png")

@app.route("/plots/length_categories")
def length_cat():
    short = (df["length"] < 50).sum()
    medium = ((df["length"] >= 50) & (df["length"] <= 150)).sum()
    long = (df["length"] > 150).sum()

    fig, ax = plt.subplots(figsize=(5,4))
    ax.pie([short, medium, long],
           labels=["Short","Medium","Long"],
           autopct="%1.1f%%")
    ax.set_title("IDR Length Categories")

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=300)
    plt.close(fig)
    buf.seek(0)

    return send_file(buf, mimetype="image/png")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
