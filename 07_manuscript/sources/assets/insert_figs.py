# -*- coding: utf-8 -*-
"""Insert figure image+caption blocks before given anchor headings."""
import io
B = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/entrega/build"
FIG = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/analisis/salidas/figuras"
PR = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/entrega/build/figs"

def block(path, cap, width="6in"):
    return f"\n![]({path}){{width={width}}}\n\n{cap}\n\n"

# (file, anchor-text-that-block-is-inserted-BEFORE, image, caption)
INS = [
 ("02_methods.md", "## Data extraction",
  f"{PR}/F1_prisma.png",
  "**Figure 1.** PRISMA 2020 flow diagram of identification, screening and "
  "inclusion. Title/abstract screening combined an automated terminological "
  "screen with semantic screening by three independent large language model "
  "(LLM) agents and a fourth moderator agent (inter-agent Fleiss' κ = 0.60).",
  "5in"),
 ("03_results.md", "## O2 — Pedagogical design",
  f"{FIG}/F1_O1_arquitectura.png",
  "**Figure 2.** Technological architectures and deployment environments "
  "(Objective O1): category distributions and per-variable reporting rates for "
  "deployment environment, modelled system, enabling architecture and AI "
  "convergence. AR = augmented reality; MR = mixed reality; VR = virtual "
  "reality; AAS = Asset Administration Shell; AI = artificial intelligence; "
  "OPC UA = Open Platform Communications Unified Architecture."),
 ("03_results.md", "## O3 — Empirical evidence",
  f"{FIG}/F2_O2_pedagogia.png",
  "**Figure 3.** Pedagogical design and Industry 4.0/5.0 competencies "
  "(Objective O2): engineering domains, targeted competencies, pedagogical "
  "models and participation modes, with reporting rates. "
  "IIoT = industrial Internet of Things."),
 ("03_results.md", "## O4 — Institutional benefits",
  f"{FIG}/F3_O3_evidencia.png",
  "**Figure 4.** Empirical evidence of learning outcomes (Objective O3): "
  "research designs, comparators, reported outcome dimensions and the 0–6 "
  "evidence-quality composite. NASA-TLX = NASA Task Load Index."),
 ("03_results.md", "## Cross-cutting analysis",
  f"{FIG}/F4_O4_beneficios_barreras.png",
  "**Figure 5.** Institutional benefits and barriers (Objective O4): articulated "
  "benefits (accessibility, cost, sustainability, continuity) and reported "
  "barrier types (technical, institutional, pedagogical), with reporting rates. "
  "WEEE = waste electrical and electronic equipment."),
 ("03_results.md", "## Advanced relational analysis",
  f"{FIG}/F5_coocurrencia_temas.png",
  "**Figure 6.** Theme co-occurrence matrix: number of studies jointly "
  "activating each pair of the eight inductive themes (T1–T8).") ,
 ("03_results.md", "## Advanced relational analysis",
  f"{FIG}/F6_relacional.png",
  "**Figure 7.** Relational analyses: (a) rate of effect-size reporting by "
  "research design; (b) digital-twin maturity (Kritzinger taxonomy) by "
  "publication year.") ,
]
# Figures 8-11 appended at end of the advanced-relational section (before ## Summary)
TAIL = (
 block(f"{FIG}/F7_red_atributos.png",
  "**Figure 8.** Attribute-association network. Nodes are binary study "
  "attributes; edges are pairwise φ associations whose bootstrap 95% "
  "confidence interval (CI) excludes zero (B = 5,000). Communities: technical "
  "capability, evaluation rigour, curricular design.")
 + block(f"{FIG}/F8_mapa_brechas.png",
  "**Figure 9.** Capability-by-evidence gap map: each empirical study plotted by "
  "technical-capability composite (0–1: maturity, synchronisation, AI, "
  "immersion) against evidence-quality score (0–6). The high-capability, "
  "strong-evidence corner is near-empty.")
 + block(f"{FIG}/F9_espacio_3d.png",
  "**Figure 10.** Three-dimensional evidence space (technical capability × "
  "evidence quality × publication year). An interactive version is provided "
  "as supplementary material.")
 + block(f"{FIG}/F10_mca_embedding.png",
  "**Figure 11.** Multiple correspondence analysis (MCA) embedding of study "
  "attributes. The first axis (12.3% of inertia) separates empirical from "
  "non-empirical/conceptual studies.")
)

# apply anchored insertions
files = {}
for fn,*_ in INS:
    files.setdefault(fn, open(f"{B}/{fn}",encoding='utf-8').read())
for fn, anchor, img, cap, *w in INS:
    width = w[0] if w else "6in"
    t = files[fn]
    assert anchor in t, f"anchor not found: {anchor}"
    t = t.replace(anchor, block(img,cap,width)+anchor, 1)
    files[fn] = t

# append tail figures before "## Summary" in results
r = files.get("03_results.md", open(f"{B}/03_results.md",encoding='utf-8').read())
assert "## Summary" in r
r = r.replace("## Summary", TAIL + "## Summary", 1)
files["03_results.md"] = r

for fn,t in files.items():
    open(f"{B}/{fn}",'w',encoding='utf-8').write(t)
    print("updated", fn)
