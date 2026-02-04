import random

def charge_correlation(charges):
    L = len(charges)
    total = 0.0
    count = 0
    for i in range(L):
        for j in range(i + 1, L):
            total += charges[i] * charges[j] / (j - i)
            count += 1
    return total / count if count > 0 else 0.0


def compute_kappa(seq, n_shuffle=20):
    charges = []
    for aa in seq:
        if aa in "KR":
            charges.append(1)
        elif aa in "DE":
            charges.append(-1)
        else:
            charges.append(0)

    L = len(charges)
    if L < 10:
        return 0.0

    obs = charge_correlation(charges)

    # shuffled expectation
    shuffled_vals = []
    for _ in range(n_shuffle):
        shuffled = charges.copy()
        random.shuffle(shuffled)
        shuffled_vals.append(charge_correlation(shuffled))

    exp = sum(shuffled_vals) / len(shuffled_vals)
    max_dev = max(abs(v - exp) for v in shuffled_vals)

    if max_dev == 0:
        return 0.0

    kappa = abs(obs - exp) / max_dev
    return round(min(kappa, 1.0), 4)
