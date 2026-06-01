"""
Robustness checks for the Results:
  (2) sensitivity of the evidence-quality banding to the chosen cut-points,
      plus the threshold-free score distribution.
  (3) non-parametric bootstrap 95% CIs for the attribute associations (phi),
      so the relational layer carries uncertainty and is read as
      hypothesis-generating rather than inferential.

Run after analizar.py. Outputs to salidas/tablas.
"""
from __future__ import annotations
import csv
from collections import Counter

import numpy as np

import _lib as L
import analizar as A
import analisis_avanzado as AV


def _feats():
    store, _, _ = A.load_store()
    act = L.load_activacion()
    arts = L.load_articulos()
    cm = L.build_citation_map()
    feats = A.build_features(store, act, arts, cm)
    for f in feats:
        f["eq_score"] = A.evidence_quality(f)
        f["eq_band"] = A.quality_band(f["eq_score"])
    return feats


# ---------------------------------------------------------------------------
# (2) Evidence-quality threshold sensitivity
# ---------------------------------------------------------------------------
SCHEMES = {
    # name: (strong_min, moderate_min)  -> weak = below moderate_min
    "S1_current (Strong>=5, Mod>=3)": (5, 3),
    "S2_strict  (Strong=6, Mod>=4)": (6, 4),
    "S3_lenient (Strong>=4, Mod>=2)": (4, 2),
}


def band(score, strong_min, mod_min):
    if score >= strong_min:
        return "Strong"
    if score >= mod_min:
        return "Moderate"
    return "Weak"


def sensitivity(feats):
    scores = [f["eq_score"] for f in feats if f["T6"]]
    n = len(scores)
    # threshold-free score distribution
    dist = Counter(scores)
    with open(L.TABLAS / "capa2_score_distribucion.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["score_0_6", "n_studies", "pct"])
        for s in range(7):
            w.writerow([s, dist.get(s, 0), round(100 * dist.get(s, 0) / n, 1)])
    # band distribution under each scheme
    rows = []
    for name, (smin, mmin) in SCHEMES.items():
        c = Counter(band(s, smin, mmin) for s in scores)
        low = c["Weak"] + c["Moderate"]
        rows.append([name, c["Weak"], c["Moderate"], c["Strong"],
                     round(100 * low / n, 1)])
    with open(L.TABLAS / "capa2_sensibilidad_umbral.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["scheme", "Weak", "Moderate", "Strong", "pct_weak_or_moderate"])
        w.writerows(rows)
    print(f"  (2) score distribution (0..6): "
          f"{[dist.get(s,0) for s in range(7)]}  (n={n})")
    for r in rows:
        print(f"      {r[0]:30s} W={r[1]:2d} M={r[2]:2d} S={r[3]:2d}  "
              f"weak+mod={r[4]}%")
    median = int(np.median(scores))
    print(f"      median score = {median}; <=2 (weak under all schemes) = "
          f"{sum(1 for s in scores if s<=2)}/{n}")


# ---------------------------------------------------------------------------
# (3) Bootstrap CIs for attribute associations
# ---------------------------------------------------------------------------
def phi_from_vectors(x, y):
    n11 = np.sum((x == 1) & (y == 1))
    n10 = np.sum((x == 1) & (y == 0))
    n01 = np.sum((x == 0) & (y == 1))
    n00 = np.sum((x == 0) & (y == 0))
    den = np.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    return 0.0 if den == 0 else (n11 * n00 - n10 * n01) / den


# the edges cited in the narrative (objective-spanning + within-cluster)
CITED_PAIRS = [
    ("Bidirectional DT", "Real-time sync"),
    ("Hybrid env", "Bidirectional DT"),
    ("Rigorous design", "Has comparator"),
    ("Has comparator", "Reports effect size"),
    ("Lifecycle project", "Industry collab."),
    ("Immersive env", "Sustainability quant."),
]


def bootstrap_ci(feats, B=5000, seed=20240530):
    cols = {lbl: np.array([int(bool(pred(f))) for f in feats], dtype=int)
            for lbl, pred, _ in AV.ATTRS}
    n = len(feats)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(B, n))  # bootstrap resample indices
    rows = []
    for a, b in CITED_PAIRS:
        xa, xb = cols[a], cols[b]
        point = phi_from_vectors(xa, xb)
        boot = np.empty(B)
        for i in range(B):
            ii = idx[i]
            boot[i] = phi_from_vectors(xa[ii], xb[ii])
        lo, hi = np.percentile(boot, [2.5, 97.5])
        crosses0 = lo <= 0 <= hi
        co = int(np.sum((xa == 1) & (xb == 1)))
        rows.append([a, b, round(point, 3), round(lo, 3), round(hi, 3),
                     co, "yes" if crosses0 else "no"])
    with open(L.TABLAS / "capa4b_attr_associations_ci.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["attr_a", "attr_b", "phi", "ci95_low", "ci95_high",
                    "co_occurrence_n", "ci_crosses_0"])
        w.writerows(rows)
    print(f"  (3) bootstrap 95% CIs (B={B}) for {len(rows)} cited edges:")
    for r in rows:
        print(f"      phi={r[2]:+.3f}  CI[{r[3]:+.2f},{r[4]:+.2f}]  n={r[5]:>2}  "
              f"crosses0={r[6]}  {r[0]} -- {r[1]}")
    return rows


def main():
    feats = _feats()
    print("[robustez] (2) evidence-quality threshold sensitivity ...")
    sensitivity(feats)
    print("[robustez] (3) bootstrap CIs for attribute associations ...")
    bootstrap_ci(feats)
    print("[robustez] done.")


if __name__ == "__main__":
    main()
