"""
Advanced relational analysis (exploratory, descriptive — n=65):
  A2  attribute association network (phi coefficient + Fisher exact)
  C2  research-frontier gap map (capability x evidence-strength density)
  B1  3D evidence space (maturity x evidence-quality x participation)
  B2  MCA embedding of papers over populated categorical variables

All edges/cells report n; nothing here is inferential. Run after analizar.py.
"""
from __future__ import annotations
import csv
import math
from collections import Counter

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.colors import Normalize
import networkx as nx
from scipy.stats import fisher_exact

import _lib as L
import analizar as A

OUT = L.FIGURAS
TAB = L.TABLAS


def _save(fig, name, dpi=None):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight", dpi=dpi)
    plt.close(fig)
    print("  figura:", name)


# ---------------------------------------------------------------------------
# Derived ordinal helpers
# ---------------------------------------------------------------------------
def participation_level(f):
    p = L.norm(f.get("participacion", ""))
    if not p or p in L.MISSING:
        return None
    if "ciclo de vida" in p or "construccion del dt" in p or "co-diseno" in p:
        return 4
    if "experimentacion activa" in p:
        return 3
    if "exploracion guiada" in p:
        return 2
    if "pasivo" in p:
        return 1
    return 2


def capability_score(f):
    """0-1 technical capability: maturity + sync + AI + immersive."""
    parts, w = 0.0, 0.0
    if f["kritzinger"]:
        parts += (f["kritzinger"] - 1) / 2; w += 1
    if f["sync"]:
        parts += (f["sync"] - 1) / 3; w += 1
    parts += 0.5 * f["has_ai"]; w += 0.5
    parts += 0.5 * f["has_immersive"]; w += 0.5
    return round(parts / w, 3) if w else None


# ---------------------------------------------------------------------------
# A2 — attribute association network
# ---------------------------------------------------------------------------
ATTRS = [
    # (label, predicate, objective)
    ("Immersive env", lambda f: f["entorno"] == "Immersive (VR/AR/MR)", "O1"),
    ("Hybrid env", lambda f: f["entorno"] == "Hybrid physical-virtual", "O1"),
    ("Bidirectional DT", lambda f: f["kritzinger"] == 3, "O1"),
    ("Real-time sync", lambda f: bool(f["sync"]) and f["sync"] >= 3, "O1"),
    ("AI-augmented", lambda f: bool(f["has_ai"]), "O1"),
    ("Active learning", lambda f: f["pedagogia"] == "Active learning", "O2"),
    ("Experiential", lambda f: f["pedagogia"] == "Experiential", "O2"),
    ("Lifecycle project", lambda f: (participation_level(f) or 0) >= 4, "O2"),
    ("Undergraduate", lambda f: f["nivel"] == "Undergraduate", "O2"),
    ("Industry collab.", lambda f: bool(f["ind_academia"]), "O2"),
    ("Rigorous design", lambda f: bool(f["diseno"]) and f["diseno"] >= 4, "O3"),
    ("Has comparator", lambda f: bool(f["has_comparator"]), "O3"),
    ("Reports effect size", lambda f: bool(f["effect_size"]), "O3"),
    ("Affective outcomes", lambda f: bool(f["aff_reported"]), "O3"),
    ("Open-source", lambda f: f["licencia_open"] is True, "O4"),
    ("Sustainability quant.", lambda f: bool(f["sostenibilidad"]), "O4"),
    ("Technical barriers", lambda f: bool(f["barreras_tec"]), "O4"),
    ("Institutional barriers", lambda f: bool(f["barreras_inst"]), "O4"),
]
OBJ_COLOR = {"O1": "#2c6fbb", "O2": "#2a8c6a", "O3": "#b5651d", "O4": "#a93226"}


def phi(x, y):
    n11 = sum(a and b for a, b in zip(x, y))
    n10 = sum(a and not b for a, b in zip(x, y))
    n01 = sum((not a) and b for a, b in zip(x, y))
    n00 = sum((not a) and (not b) for a, b in zip(x, y))
    den = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    if den == 0:
        return 0.0, (n11, n10, n01, n00)
    return (n11 * n00 - n10 * n01) / den, (n11, n10, n01, n00)


#def a2_network(feats, thr=0.30, pmax=0.10):
def a2_network(feats, thr=0.05, pmax=0.10):
    cols = {lbl: [int(bool(pred(f))) for f in feats] for lbl, pred, _ in ATTRS}
    prev = {lbl: sum(v) for lbl, v in cols.items()}
    edges = []
    labels = [lbl for lbl, _, _ in ATTRS]
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            a, b = labels[i], labels[j]
            r, (n11, n10, n01, n00) = phi(cols[a], cols[b])
            try:
                _, p = fisher_exact([[n11, n10], [n01, n00]])
            except Exception:
                p = 1.0
            edges.append((a, b, round(r, 3), n11, p))
    # write full edge list
    edges_sorted = sorted(edges, key=lambda e: -abs(e[2]))
    with open(TAB / "capa4b_attr_associations.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["attr_a", "attr_b", "phi", "co_occurrence_n", "fisher_p"])
        w.writerows(edges_sorted)

    # pairs of attributes that are mutually exclusive categories of the same
    # single-label variable -> their negative association is a coding artifact
    SAME_VAR = [frozenset({"Active learning", "Experiential"})]

    # graph with thresholded edges
    G = nx.Graph()
    obj_of = {lbl: o for lbl, _, o in ATTRS}
    for lbl in labels:
        G.add_node(lbl, prev=prev[lbl], obj=obj_of[lbl])
    drawn = [(a, b, r, n, p) for a, b, r, n, p in edges
             if abs(r) >= thr and p <= pmax and frozenset({a, b}) not in SAME_VAR]
    for a, b, r, n, p in drawn:
        G.add_edge(a, b, phi=r, n=n)

    # --- circular layout grouped by objective (each objective on a contiguous
    #     arc), labels placed radially outside the ring for clear separation ---
    OBJ_ORDER = ["O1", "O2", "O3", "O4"]
    nodes_ord = [lbl for o in OBJ_ORDER for lbl in labels if obj_of[lbl] == o]
    Nn = len(nodes_ord)
    ang = {lbl: (math.pi / 2 - 2 * math.pi * i / Nn)  # start top, go clockwise
           for i, lbl in enumerate(nodes_ord)}
    pos = {lbl: (math.cos(ang[lbl]), math.sin(ang[lbl])) for lbl in nodes_ord}

    fig, ax = plt.subplots(figsize=(13, 13))
    # faint objective guide ring
    ring = plt.Circle((0, 0), 1.0, fill=False, color="#dddddd", lw=1.2, zorder=0)
    ax.add_patch(ring)
    # edges as Bézier arcs bowing toward the centre (chord-diagram style):
    # the control point is the midpoint pulled in toward the origin, so the
    # curvature grows with the angular separation of the two nodes.
    #
    # both line width *and* colour tone scale with |phi|: strong associations
    # are thick and dark, weak ones thin and pale. |phi| is normalised across
    # the drawn edges (from thr up to the strongest edge present).
    phis = [abs(d["phi"]) for _, _, d in G.edges(data=True)]
    phi_hi = max(phis) if phis else 1.0
    norm = Normalize(vmin=thr, vmax=phi_hi if phi_hi > thr else thr + 1e-9)
    pos_cmap = plt.get_cmap("Blues")
    neg_cmap = plt.get_cmap("Reds")
    for a, b, d in G.edges(data=True):
        r = abs(d["phi"])
        shade = 0.35 + 0.6 * norm(r)          # 0.35 (pale) .. 0.95 (dark)
        col = (pos_cmap if d["phi"] > 0 else neg_cmap)(shade)
        (xa, ya), (xb, yb) = pos[a], pos[b]
        ctrl = ((xa + xb) / 2 * 0.45, (ya + yb) / 2 * 0.45)
        path = Path([(xa, ya), ctrl, (xb, yb)],
                    [Path.MOVETO, Path.CURVE3, Path.CURVE3])
        ax.add_patch(PathPatch(path, facecolor="none", edgecolor=col,
                               alpha=0.85, lw=1.0 + 6.0 * r,
                               capstyle="round", zorder=1))
    sizes = [240 + 300 * math.sqrt(G.nodes[x]["prev"]) for x in nodes_ord]
    ncolors = [OBJ_COLOR[obj_of[x]] for x in nodes_ord]
    ax.scatter([pos[x][0] for x in nodes_ord], [pos[x][1] for x in nodes_ord],
               s=sizes, c=ncolors, alpha=0.95, edgecolors="white",
               linewidths=2.0, zorder=2)
    # radial labels outside the ring
    for lbl in nodes_ord:
        a = ang[lbl]
        deg = math.degrees(a) % 360
        x, y = math.cos(a) * 1.16, math.sin(a) * 1.16
        rot = deg
        ha = "left"
        if 90 < deg < 270:
            rot = deg - 180
            ha = "right"
        ax.text(x, y, lbl, rotation=rot, rotation_mode="anchor",
                ha=ha, va="center", fontsize=11, fontweight="bold",
                color=OBJ_COLOR[obj_of[lbl]], zorder=3)
    legend = [Line2D([0], [0], marker="o", color="w", label=f"{o} attributes",
                     markerfacecolor=c, markersize=13)
              for o, c in OBJ_COLOR.items()]
    legend += [Line2D([0], [0], color="#08519c", lw=3.5, label="positive association (φ>0)"),
               Line2D([0], [0], color="#a50f15", lw=3.5, label="negative association (φ<0)"),
               Line2D([0], [0], color="#000000", lw=0,
                      label="edge width & tone ∝ |φ|")]
    ax.legend(handles=legend, loc="lower left", bbox_to_anchor=(-0.02, -0.02),
              fontsize=10, framealpha=0.95,
              title="node size ∝ prevalence (n=65)", title_fontsize=9)
    ax.set_title(f"Attribute association network  (φ ≥ {thr}, Fisher p ≤ {pmax})",
                 fontweight="bold", fontsize=15, pad=18)
    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-1.7, 1.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, "F7_red_atributos.png", dpi=300)

    # centrality table
    if G.number_of_edges():
        deg = nx.degree_centrality(G)
        btw = nx.betweenness_centrality(G, weight=None)
        with open(TAB / "capa4b_attr_centralidad.csv", "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh)
            w.writerow(["attribute", "objetivo", "prevalence_n", "degree", "degree_centrality", "betweenness"])
            for lbl in sorted(G, key=lambda x: -deg[x]):
                w.writerow([lbl, obj_of[lbl], prev[lbl], G.degree[lbl],
                            round(deg[lbl], 3), round(btw[lbl], 3)])
    print(f"  A2: {len(drawn)} edges drawn of {len(edges)} pairs")
    return edges_sorted


# ---------------------------------------------------------------------------
# C2 — research-frontier gap map
# ---------------------------------------------------------------------------
def c2_gapmap(feats):
    pts = [(capability_score(f), f["eq_score"]) for f in feats
           if capability_score(f) is not None and f["eq_score"] is not None]
    cap = np.array([p[0] for p in pts])
    eq = np.array([p[1] for p in pts])
    # grid: capability (0-1, 4 bins) x evidence quality (0-6 -> 4 bins)
    xb = np.linspace(0, 1, 5)
    yb = np.array([0, 1.5, 3, 4.5, 6.01])
    H, _, _ = np.histogram2d(cap, eq, bins=[xb, yb])
    fig, ax = plt.subplots(figsize=(8.2, 6))
    im = ax.imshow(H.T, origin="lower", aspect="auto", cmap="YlGnBu",
                   extent=[0, 1, 0, 6])
    for i in range(H.shape[0]):
        for j in range(H.shape[1]):
            cx = (xb[i] + xb[i + 1]) / 2
            cy = (yb[j] + min(yb[j + 1], 6)) / 2
            v = int(H[i, j])
            ax.text(cx, cy, v, ha="center", va="center", fontsize=11,
                    color="white" if v > H.max() * 0.5 else "#333",
                    fontweight="bold")
    # jittered points
    rng = np.random.default_rng(3)
    ax.scatter(cap + rng.normal(0, 0.012, len(cap)),
               eq + rng.normal(0, 0.12, len(eq)),
               s=22, c="#d6604d", edgecolors="white", linewidths=0.4, zorder=3)
    # highlight empty high-high frontier region
    ax.add_patch(plt.Rectangle((0.5, 4.5), 0.5, 1.5, fill=False,
                 edgecolor="#b2182b", linewidth=2, linestyle="--", zorder=4))
    ax.text(0.75, 5.6, "research frontier\n(high capability + strong evidence)",
            ha="center", va="center", fontsize=8.5, color="#b2182b", fontweight="bold")
    ax.set_xlabel("Technical capability  (maturity + sync + AI + immersive, 0–1)")
    ax.set_ylabel("Evidence-quality score (0–6)")
    ax.set_title("C2 — Research-frontier gap map (cell counts; n=%d studies)" % len(pts),
                 fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.85, label="studies in cell")
    _save(fig, "F8_mapa_brechas.png")
    # export grid
    with open(TAB / "capa4c_gapmap_grid.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["capability_bin", "evidence_bin", "n_studies"])
        for i in range(H.shape[0]):
            for j in range(H.shape[1]):
                w.writerow([f"{xb[i]:.2f}-{xb[i+1]:.2f}",
                            f"{yb[j]:.1f}-{min(yb[j+1],6):.1f}", int(H[i, j])])
    print(f"  C2: {len(pts)} studies plotted")


# ---------------------------------------------------------------------------
# B1 — 3D evidence space
# ---------------------------------------------------------------------------
BAND_COLOR = {"Weak": "#d98880", "Moderate": "#e8c468", "Strong": "#5a9367"}


def b1_3d(feats):
    # restrict to empirical (T6) studies; maturity (T2) is too sparse to be an
    # axis (the decoupling finding), so the x-axis is the broad capability score
    sel = [f for f in feats if f["T6"] and capability_score(f) is not None and
           participation_level(f) is not None]
    xs = [capability_score(f) for f in sel]
    ys = [f["eq_score"] for f in sel]
    zs = [participation_level(f) for f in sel]
    cs = [BAND_COLOR.get(f["eq_band"], "#999") for f in sel]
    rng = np.random.default_rng(11)
    jit = lambda a, s: np.array(a) + rng.normal(0, s, len(a))
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(jit(xs, .015), jit(ys, .12), jit(zs, .05), c=cs, s=45,
               edgecolors="white", linewidths=0.5, depthshade=True)
    ax.set_xlabel("Technical capability (0–1)")
    ax.set_ylabel("Evidence quality (0–6)")
    ax.set_zlabel("Student participation (1–4)")
    ax.set_zticks([1, 2, 3, 4])
    ax.set_title("B1 — Evidence space (n=%d empirical studies)" % len(sel),
                 fontweight="bold")
    leg = [Line2D([0], [0], marker="o", color="w", label=b,
                  markerfacecolor=c, markersize=10) for b, c in BAND_COLOR.items()]
    ax.legend(handles=leg, loc="upper left", fontsize=8)
    ax.view_init(elev=18, azim=-60)
    _save(fig, "F9_espacio_3d.png")

    # interactive HTML
    try:
        import plotly.graph_objects as go
        txt = [f["cite"] for f in sel]
        figp = go.Figure(go.Scatter3d(
            x=xs, y=ys, z=zs, mode="markers", text=txt,
            marker=dict(size=6, color=cs, line=dict(width=0.5, color="white")),
            hovertemplate="%{text}<br>maturity=%{x}<br>quality=%{y}<br>participation=%{z}<extra></extra>"))
        figp.update_layout(
            title="B1 — Evidence space (interactive)",
            scene=dict(xaxis_title="DT maturity (1-3)",
                       yaxis_title="Evidence quality (0-6)",
                       zaxis_title="Participation (1-4)"))
        figp.write_html(str(OUT / "F9_espacio_3d.html"))
        print("  figura: F9_espacio_3d.html")
    except Exception as e:
        print("  [plotly B1 skipped]", e)
    print(f"  B1: {len(sel)} studies in evidence space")


# ---------------------------------------------------------------------------
# B2 — MCA embedding
# ---------------------------------------------------------------------------
def b2_mca(feats):
    import pandas as pd
    import prince

    def cat(f, key, fallback="NR"):
        v = f.get(key)
        return v if (v not in (None, "", 0) or isinstance(v, str)) and v else fallback

    rows = []
    for f in feats:
        rows.append({
            "Environment": f["entorno"] or "NR",
            "Maturity": f["kritzinger_lbl"] or "NR",
            "Sync": f["sync_lbl"] or "NR",
            "AI": "AI" if f["has_ai"] else "no-AI",
            "Immersive": "immersive" if f["has_immersive"] else "non-immersive",
            "Pedagogy": f["pedagogia"] or "NR",
            "Level": f["nivel"] or "NR",
            "Design": f["diseno_lbl"] or "NR",
            "EvidenceBand": f["eq_band"] if f["T6"] else "non-empirical",
            "Barriers": "barriers" if (f["barreras_tec"] or f["barreras_inst"]
                                       or f["barreras_ped"]) else "no-barriers",
        })
    df = pd.DataFrame(rows)
    mca = prince.MCA(n_components=3, random_state=42)
    mca = mca.fit(df)
    coords = mca.transform(df).to_numpy()
    # inertia per axis (robust to prince version)
    try:
        inertia = list(mca.percentage_of_variance_)
    except Exception:
        try:
            ev = np.array(mca.eigenvalues_, dtype=float)
            inertia = list(100 * ev / ev.sum())
        except Exception:
            inertia = [float("nan")] * 3
    cites = [f["cite"] for f in feats]
    bands = [(f["eq_band"] if f["T6"] else "non-empirical") for f in feats]
    palette = {**BAND_COLOR, "non-empirical": "#b0b0b0"}
    cs = [palette.get(b, "#999") for b in bands]

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=cs, s=42,
               edgecolors="white", linewidths=0.5)
    ax.set_xlabel(f"MCA-1 ({inertia[0]:.1f}%)")
    ax.set_ylabel(f"MCA-2 ({inertia[1]:.1f}%)")
    ax.set_zlabel(f"MCA-3 ({inertia[2]:.1f}%)")
    ax.set_title("B2 — MCA embedding of studies (color = evidence band)",
                 fontweight="bold")
    leg = [Line2D([0], [0], marker="o", color="w", label=b,
                  markerfacecolor=c, markersize=10) for b, c in palette.items()]
    ax.legend(handles=leg, loc="upper left", fontsize=8)
    ax.view_init(elev=18, azim=-50)
    _save(fig, "F10_mca_embedding.png")

    try:
        import plotly.graph_objects as go
        figp = go.Figure(go.Scatter3d(
            x=coords[:, 0], y=coords[:, 1], z=coords[:, 2], mode="markers",
            text=cites, marker=dict(size=6, color=cs, line=dict(width=0.5, color="white")),
            hovertemplate="%{text}<extra></extra>"))
        figp.update_layout(title="B2 — MCA embedding (interactive)",
                           scene=dict(xaxis_title=f"MCA-1 ({inertia[0]:.1f}%)",
                                      yaxis_title=f"MCA-2 ({inertia[1]:.1f}%)",
                                      zaxis_title=f"MCA-3 ({inertia[2]:.1f}%)"))
        figp.write_html(str(OUT / "F10_mca_embedding.html"))
        print("  figura: F10_mca_embedding.html")
    except Exception as e:
        print("  [plotly B2 skipped]", e)

    # column (category) coordinates to interpret axes
    try:
        cc = mca.column_coordinates(df)
        cc.to_csv(TAB / "capa4d_mca_categorias.csv", encoding="utf-8-sig")
    except Exception as e:
        print("  [mca columns skipped]", e)
    with open(TAB / "capa4d_mca_inercia.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["axis", "pct_inertia"])
        for i, v in enumerate(inertia[:3], 1):
            w.writerow([f"MCA-{i}", round(v, 2)])
    print(f"  B2: MCA inertia (axes 1-3) = "
          f"{', '.join(f'{v:.1f}%' for v in inertia[:3])}")


def main():
    feats, _ = A.main()
    for f in feats:
        f["eq_score"] = A.evidence_quality(f)
        f["eq_band"] = A.quality_band(f["eq_score"])
    print("[avanzado] A2 attribute network ...")
    a2_network(feats)
    print("[avanzado] C2 gap map ...")
    c2_gapmap(feats)
    print("[avanzado] B1 3D evidence space ...")
    b1_3d(feats)
    print("[avanzado] B2 MCA embedding ...")
    b2_mca(feats)
    print("[avanzado] done ->", OUT)


if __name__ == "__main__":
    main()
