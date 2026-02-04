import numpy as np

KD = {
    "A": 1.8, "C": 2.5, "D": -3.5, "E": -3.5,
    "F": 2.8, "G": -0.4, "H": -3.2, "I": 4.5,
    "K": -3.9, "L": 3.8, "M": 1.9, "N": -3.5,
    "P": -1.6, "Q": -3.5, "R": -4.5, "S": -0.8,
    "T": -0.7, "V": 4.2, "W": -0.9, "Y": -1.3
}

POS = set("KR")
NEG = set("DE")
ARO = set("FWY")

def compute_kappa(seq):
    charges = [1 if a in POS else -1 if a in NEG else 0 for a in seq]
    if sum(abs(c) for c in charges) < 2:
        return np.nan
    return round(np.var(charges), 4)

def compute_idr_parameters(seq):
    L = len(seq)
    if L == 0:
        return None

    f_plus = sum(a in POS for a in seq) / L
    f_minus = sum(a in NEG for a in seq) / L

    return {
        "length": L,
        "f_plus": round(f_plus, 4),
        "f_minus": round(f_minus, 4),
        "FCR": round(f_plus + f_minus, 4),
        "NCPR": round(f_plus - f_minus, 4),
        "kappa": compute_kappa(seq),
        "hydropathy": round(sum(KD.get(a, 0) for a in seq) / L, 4),
        "aromatic_density": round(sum(a in ARO for a in seq) / L, 4),
        "pro_fraction": round(seq.count("P") / L, 4),
        "gly_fraction": round(seq.count("G") / L, 4)
    }

