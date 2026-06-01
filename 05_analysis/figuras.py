"""
Results-oriented figures for the systematic review (one figure block per
objective O1-O4, a theme co-occurrence heatmap, and a relational figure).
No PRISMA diagram here -- that belongs to the Methods section.

Run after analizar.py; reuses its feature matrix.
"""
from __future__ import annotations
import re
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import _lib as L
import analizar as A

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "figure.dpi": 150, "savefig.dpi": 200, "axes.grid": True,
    "grid.alpha": 0.25, "axes.axisbelow": True,
})
BLUE = "#2c6fbb"
GREYS = ["#b8c4d0", "#5a7896", "#234a6b"]
FIG = L.FIGURAS


def _save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG / name, bbox_inches="tight")
    plt.close(fig)
    print("  figura:", name)


def _hbar(ax, counter, title, color=BLUE, top=None):
    items = counter.most_common(top) if top else sorted(
        counter.items(), key=lambda x: x[1])
    items = items[::-1] if top else items
    labels = [k for k, _ in items]
    vals = [v for _, v in items]
    y = range(len(labels))
    ax.barh(list(y), vals, color=color)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.set_title(title)
    ax.grid(axis="y", visible=False)
    for i, v in enumerate(vals):
        ax.text(v + 0.1, i, str(v), va="center", fontsize=8)
    ax.set_xlim(0, max(vals) * 1.15 if vals else 1)


def split_multi(values):
    c = Counter()
    for v in values:
        if L.is_missing(v):
            continue
        for part in re.split(r"[;,/]| y ", v):
            p = part.strip().capitalize()
            if len(p) >= 3:
                c[p] += 1
    return c


# ---------------------------------------------------------------------------
def fig_o1(feats):
    """Architecture & deployment: environment, Kritzinger maturity, sync, AI."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    _hbar(axes[0, 0], Counter(f["entorno"] for f in feats if f["entorno"]),
          "DT environment type (T1, n=%d)" % sum(1 for f in feats if f["entorno"]))
    kr = Counter(f["kritzinger_lbl"] for f in feats if f["kritzinger"])
    order = ["Digital model", "Digital shadow", "Digital twin"]
    axes[0, 1].bar(order, [kr.get(k, 0) for k in order], color=GREYS)
    axes[0, 1].set_title("DT maturity — Kritzinger taxonomy (T2)")
    for i, k in enumerate(order):
        axes[0, 1].text(i, kr.get(k, 0) + 0.1, str(kr.get(k, 0)), ha="center", fontsize=8)
    sy = Counter(f["sync_lbl"] for f in feats if f["sync"])
    sorder = ["Asynchronous", "Near-real-time", "Real-time", "Bidirectional"]
    _hbar(axes[1, 0], Counter({k: sy.get(k, 0) for k in sorder if sy.get(k)}),
          "Synchronisation degree (T2)")
    aif = Counter()
    for f in feats:
        if f["ai_families"]:
            for fam in f["ai_families"].split("; "):
                aif[fam] += 1
    _hbar(axes[1, 1], aif, "AI families integrated (T3, n=%d papers)" %
          sum(1 for f in feats if f["has_ai"]), color="#7a3b8f")
    fig.suptitle("O1 — Technological architectures and deployment environments",
                 fontsize=12, fontweight="bold")
    _save(fig, "F1_O1_arquitectura.png")


def fig_o2(feats):
    """Pedagogy & competencies: domains, pedagogical model, level, participation."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
    dom = split_multi([f["dominio"] for f in feats])
    _hbar(axes[0, 0], dom, "Engineering domain (T4)", color="#2a8c6a", top=10)
    _hbar(axes[0, 1], Counter(f["pedagogia"] for f in feats if f["pedagogia"]),
          "Pedagogical model (T5)", color="#2a8c6a")
    _hbar(axes[1, 0], Counter(f["nivel"] for f in feats if f["nivel"]),
          "Educational level (T5)", color="#2a8c6a")
    part = split_multi([f["participacion"] for f in feats])
    _hbar(axes[1, 1], part, "Student participation mode (T5)", color="#2a8c6a", top=8)
    fig.suptitle("O2 — Pedagogical design and competencies",
                 fontsize=12, fontweight="bold")
    _save(fig, "F2_O2_pedagogia.png")


def fig_o3(feats):
    """Empirical evidence: design distribution + quality bands + outcome reporting."""
    emp = [f for f in feats if f["T6"]]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    dl = Counter(f["diseno_lbl"] for f in emp if f["diseno"])
    _hbar(axes[0], dl, "Research design (T6, n=%d)" % len(emp), color="#b5651d")
    band = Counter(f["eq_band"] for f in emp)
    border = ["Weak", "Moderate", "Strong"]
    axes[1].bar(border, [band.get(b, 0) for b in border],
                color=["#d98880", "#e8c468", "#5a9367"])
    axes[1].set_title("Evidence-quality band (0–6 composite)")
    for i, b in enumerate(border):
        axes[1].text(i, band.get(b, 0) + 0.15, str(band.get(b, 0)), ha="center", fontsize=8)
    outc = Counter()
    for f in emp:
        if f["cog_reported"]:
            outc["Cognitive"] += 1
        if f["proc_reported"]:
            outc["Procedural"] += 1
        if f["aff_reported"]:
            outc["Affective/\nengagement"] += 1
        if f["effect_size"]:
            outc["Effect size\nreported"] += 1
    _hbar(axes[2], outc, "Outcome dimensions reported", color="#b5651d")
    fig.suptitle("O3 — Empirical evidence of learning outcomes",
                 fontsize=12, fontweight="bold")
    _save(fig, "F3_O3_evidencia.png")


def fig_o4(feats):
    """Institutional value vs barriers."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    ben = Counter()
    for f in feats:
        if f["T7"]:
            if f["licencia_open"] is True:
                ben["Open-source licensing"] += 1
            if f["sostenibilidad"]:
                ben["Sustainability metrics"] += 1
            if f["post_covid"]:
                ben["Post-COVID continuity"] += 1
            if f["costo"] == "Low":
                ben["Low cost"] += 1
    _hbar(axes[0], ben, "Reported institutional benefits (T7, n=%d)" %
          sum(1 for f in feats if f["T7"]), color="#3a7d44")
    bar = Counter()
    for f in feats:
        if f["T8"]:
            if f["barreras_tec"]:
                bar["Technical"] += 1
            if f["barreras_inst"]:
                bar["Institutional/\nteacher"] += 1
            if f["barreras_ped"]:
                bar["Pedagogical/\ncurricular"] += 1
    _hbar(axes[1], bar, "Reported barriers (T8, n=%d)" %
          sum(1 for f in feats if f["T8"]), color="#a93226")
    fig.suptitle("O4 — Institutional benefits and critical barriers",
                 fontsize=12, fontweight="bold")
    _save(fig, "F4_O4_beneficios_barreras.png")


def fig_coocurrence(act):
    n, co, _ = A.capa3_coocurrence(act)
    M = [[co[t][u] for u in L.THEMES] for t in L.THEMES]
    fig, ax = plt.subplots(figsize=(7.2, 6))
    cmap = LinearSegmentedColormap.from_list("b", ["#f4f7fb", BLUE])
    im = ax.imshow(M, cmap=cmap)
    ax.set_xticks(range(8)); ax.set_yticks(range(8))
    ax.set_xticklabels(L.THEMES); ax.set_yticklabels(L.THEMES)
    diag = max(M[i][i] for i in range(8))
    for i in range(8):
        for j in range(8):
            v = M[i][j]
            ax.text(j, i, v, ha="center", va="center", fontsize=8,
                    color="white" if v > diag * 0.55 else "#222")
    ax.set_title("Theme co-occurrence matrix (diagonal = theme frequency)")
    fig.colorbar(im, ax=ax, shrink=0.8, label="co-occurring papers")
    ax.grid(False)
    _save(fig, "F5_coocurrencia_temas.png")


def fig_relational(feats):
    """Two non-obvious relationships made explicit."""
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    # (a) effect-size reporting rate by design rigor
    rt = A.rate_table(feats, lambda f: f["diseno_lbl"], lambda f: f["effect_size"],
                      subset=lambda f: f["T6"] and f["diseno"],
                      order=[A.C.DESIGN_LABEL[i] for i in (1, 2, 3, 4, 5)])
    labels = [r[0].split(" /")[0].split(" (")[0] for r in rt]
    pct = [r[3] for r in rt]
    tot = [r[2] for r in rt]
    axes[0].bar(range(len(labels)), pct, color="#b5651d")
    axes[0].set_xticks(range(len(labels)))
    axes[0].set_xticklabels(labels, rotation=25, ha="right", fontsize=7.5)
    axes[0].set_ylabel("% reporting effect size")
    axes[0].set_title("Effect-size reporting by design rigor")
    for i, (p, t) in enumerate(zip(pct, tot)):
        axes[0].text(i, p + 1.5, f"{p:.0f}%\n(n={t})", ha="center", fontsize=7)
    axes[0].set_ylim(0, 115)
    # (b) DT maturity over time (stacked)
    yrs = sorted({f["year"] for f in feats if f["T2"] and f["year"]})
    order = ["Digital model", "Digital shadow", "Digital twin"]
    data = {k: [sum(1 for f in feats if f["T2"] and f["year"] == y
                    and f["kritzinger_lbl"] == k) for y in yrs] for k in order}
    bottom = [0] * len(yrs)
    for k, c in zip(order, GREYS):
        axes[1].bar(yrs, data[k], bottom=bottom, label=k, color=c)
        bottom = [b + d for b, d in zip(bottom, data[k])]
    axes[1].set_title("DT maturity composition over time (T2)")
    axes[1].set_ylabel("papers")
    axes[1].legend(fontsize=7.5, loc="upper left")
    axes[1].grid(axis="x", visible=False)
    fig.suptitle("Cross-cutting relationships", fontsize=12, fontweight="bold")
    _save(fig, "F6_relacional.png")


def main():
    feats, _ = A.main()
    for f in feats:
        f["eq_score"] = A.evidence_quality(f)
        f["eq_band"] = A.quality_band(f["eq_score"])
    act = L.load_activacion()
    print("[figuras] generating ...")
    fig_o1(feats); fig_o2(feats); fig_o3(feats); fig_o4(feats)
    fig_coocurrence(act); fig_relational(feats)
    print("[figuras] done ->", FIG)


if __name__ == "__main__":
    main()
