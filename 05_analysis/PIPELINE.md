# Deep data analysis — DTs in Engineering Education (systematic review)

Reproducible pipeline that turns the thematic extraction in `../salida_gemelos`
into the analytical artifacts that support the Results, following the
three-layer strategy in `../disenioRevisionFinal.json` plus a fourth
*relational* layer (cross-variable associations across themes).

## Inputs
- `../salida_gemelos/datos_largo.csv` — long-format extraction (1 row per
  paper × theme × variable, with value + verbatim quote + location).
- `../salida_gemelos/activacion.csv` — paper × theme activation matrix.
- `../salida_gemelos/articulos.csv` — per-paper metadata.
- `../pdfs.csv` — Zotero export; its `Key` equals `key_documento` (anchor).
- `../pdfs.bib` — bibliography; supplies clean author-year citation labels.

## How to run
```
python run_all.py          # full pipeline: artifacts + figures + advanced + tables
# or individually:
python figuras.py          # base results figures (runs analizar.py internally)
python analisis_avanzado.py# A2 network, C2 gap map, B1 3D, B2 MCA
python tablas_sintesis.py  # synthesis tables T-A, T-B
```
Python 3.14. Required: `pandas`, `matplotlib`, `numpy`, `scipy`, `networkx`.
Advanced extras: `prince` + `scikit-learn` (MCA), `plotly` (interactive 3D HTML).
Outputs go to `salidas/`.

## Modules
- `_lib.py` — loaders + `build_citation_map()` (anchors on `pdfs.csv` Key,
  maps to `.bib` by title-token overlap; 65/65 mapped). Two institutional/
  initial labels are corrected via `CITATION_OVERRIDES`.
- `clasificar.py` — canonicalises free-text values into ordinal scales
  (Kritzinger maturity, synchronisation, design rigour) and boolean flags
  (effect size, inferential stats, AI family, open-source, …).
- `analizar.py` — builds `paper_features.csv` and Layers 1–4.
- `figuras.py` — base results-oriented figures (no PRISMA; that is Methods).
- `analisis_avanzado.py` — advanced relational layer: attribute association
  network (A2), research-frontier gap map (C2), 3D evidence space (B1) and MCA
  embedding (B2). Exploratory/descriptive; reports n per edge/cell and MCA
  inertia.
- `tablas_sintesis.py` — synthesis tables with citations (T-A, T-B).
- `robustez.py` — robustness checks: evidence-quality threshold sensitivity
  (`capa2_sensibilidad_umbral.csv`, `capa2_score_distribucion.csv`) and
  bootstrap 95% CIs for the cited attribute associations
  (`capa4b_attr_associations_ci.csv`).

## Outputs (`salidas/`)
**tablas/**
- `citas_map.csv` — key_documento → bib citekey → author-year label.
- `paper_features.csv` — one row per paper, all derived flags/scales.
- `capa1_descriptivo_por_tema.csv` — per (theme, variable): n, reported,
  %reported, top categories (Layer 1).
- `capa2_calidad_evidencia.csv` — 0–6 evidence-quality matrix for T6 papers
  (design, comparator, inferential stats, effect size, validity threats,
  band) (Layer 2 / O3).
- `capa3_coocurrencia.csv` — theme co-occurrence matrix (diagonal = frequency).
- `capa3_configuraciones.csv` — robustness/gap configurations with the papers
  in each (Layer 3).
- `capa4_*.csv` — relational cross-tabs and rate tables (Layer 4):
  maturity×quality, AI×effect-size, environment×quality, pedagogy×engagement,
  year×maturity, immersive×affective; effect-size-by-design,
  evidence-share-by-environment, barriers-share-by-quality.
- `capa4b_attr_associations.csv` / `capa4b_attr_centralidad.csv` — attribute
  association edge list (φ, co-occurrence n, Fisher p) and node centralities (A2).
- `capa4c_gapmap_grid.csv` — capability×evidence cell counts (C2).
- `capa4d_mca_categorias.csv` / `capa4d_mca_inercia.csv` — MCA category
  coordinates and per-axis inertia (B2).
- `TA_evidencia_fuerte.csv` / `TB_arquitecturas_referencia.csv` — synthesis
  tables (also rendered in `Tablas_sintesis.md`).
- `resumen.json` — machine-readable digest used to write the narrative.

**figuras/** (200 dpi PNG)
- `F1_O1_arquitectura.png` — environment, Kritzinger maturity, synchronisation,
  AI families.
- `F2_O2_pedagogia.png` — domain, pedagogical model, level, participation.
- `F3_O3_evidencia.png` — research design, evidence-quality bands, outcome
  dimensions.
- `F4_O4_beneficios_barreras.png` — benefits vs barriers.
- `F5_coocurrencia_temas.png` — theme co-occurrence heatmap.
- `F6_relacional.png` — effect-size by design rigour; DT maturity over time.
- `F7_red_atributos.png` — attribute association network (A2).
- `F8_mapa_brechas.png` — research-frontier gap map (C2).
- `F9_espacio_3d.png` / `.html` — 3D evidence space, static + interactive (B1).
- `F10_mca_embedding.png` / `.html` — MCA embedding, static + interactive (B2).

## Narrative
- `Results_synthesis.md` — Results section (English, author-year citations,
  measured tone), grounded in the artifacts above; includes the advanced
  relational analysis (F7–F10, T-A/T-B).
- `Tablas_sintesis.md` — synthesis tables T-A (strong/moderate empirical
  studies) and T-B (reference architecture configurations), with citations.

## Notes / caveats
- Counts are over theme-activated subsets; reporting rates (% non-NR) are
  stated alongside every claim.
- Relational tables have small cells (35 empirical studies); they are
  descriptive associations, not inferential tests.
- The Kritzinger taxonomy is largely author-self-reported and rarely backed by
  latency/jitter measurements; "complete twin" prevalence reflects usage as
  much as verified closed-loop synchronisation.
