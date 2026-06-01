"""
Deep data analysis for the systematic review of Digital Twins in
Engineering Education.

Executes the three-layer strategy from disenioRevisionFinal.json plus a
fourth *relational* layer (cross-variable associations across themes,
to surface relationships that per-theme frequencies do not reveal).

Outputs (analisis/salidas/tablas):
  - paper_features.csv      one row per paper with derived flags/scales
  - capa1_*.csv             per-theme descriptive profiles
  - capa2_calidad_evidencia.csv   evidence-quality matrix (T6)
  - capa3_coocurrencia.csv  theme co-occurrence matrix + gap configs
  - capa4_*.csv             cross-variable association tables
  - resumen.json            machine-readable digest for the narrative
"""
from __future__ import annotations
import csv
import json
from collections import Counter, defaultdict
from itertools import combinations

import _lib as L
import clasificar as C


# ---------------------------------------------------------------------------
# Load everything into a per-paper variable store
# ---------------------------------------------------------------------------
def load_store():
    rows = L.load_datos_largo()
    store = defaultdict(dict)        # key -> {(tema,var): valor}
    cites = defaultdict(dict)        # key -> {(tema,var): (cita, ubicacion)}
    for r in rows:
        k = r["key_documento"]
        store[k][(r["tema"], r["variable"])] = r["valor_extraido"].strip()
        cites[k][(r["tema"], r["variable"])] = (r["cita_textual"], r["ubicacion"])
    return store, cites, rows


def get(store, key, tema, var):
    return store[key].get((tema, var), "")


# ---------------------------------------------------------------------------
# Per-paper feature matrix (backbone of the relational layer)
# ---------------------------------------------------------------------------
def build_features(store, act, arts, cmap):
    by_key_art = {a["key_documento"]: a for a in arts}
    by_key_act = {a["key_documento"]: a for a in act}
    feats = []
    for key in store:
        a = by_key_art.get(key, {})
        ac = by_key_act.get(key, {})
        f = {
            "key": key,
            "cite": L.cite(key, cmap),
            "year": a.get("meta__anio_publicacion", ""),
            "tipo_pub": a.get("meta__tipo_publicacion", ""),
            "pais": a.get("meta__pais_institucion_primera_afiliacion", ""),
            "n_temas": ac.get("n_temas", ""),
        }
        for t in L.THEMES:
            f[t] = int(ac.get(t, 0))
        # --- O1 / architecture features ---
        f["entorno"] = C.environment_bucket(get(store, key, "T1", "tipo_entorno_dt"))
        f["kritzinger"] = C.kritzinger_level(
            get(store, key, "T2", "tipo_gemelo_digital_taxonomia_kritzinger"))
        f["kritzinger_lbl"] = C.KRITZINGER_LABEL.get(f["kritzinger"], "")
        f["sync"] = C.sync_level(
            get(store, key, "T2", "grado_sincronizacion_bidireccionalidad"))
        f["sync_lbl"] = C.SYNC_LABEL.get(f["sync"], "")
        tipo_ia = get(store, key, "T3", "tipo_ia_integrada")
        f["has_ai"] = int(f["T3"] == 1 and C.has_ai(tipo_ia))
        f["ai_families"] = "; ".join(C.ai_families(tipo_ia)) if f["has_ai"] else ""
        f["has_immersive"] = int(f["entorno"] == "Immersive (VR/AR/MR)" or
                                 (not L.is_missing(get(store, key, "T1",
                                  "tecnologia_inmersiva_especifica"))))
        # --- O2 / pedagogy features ---
        f["pedagogia"] = C.pedagogy_bucket(get(store, key, "T5", "modelo_pedagogico"))
        f["nivel"] = C.education_level(get(store, key, "T5", "nivel_educativo"))
        f["dominio"] = get(store, key, "T4", "dominio_ingenieria") or ""
        f["participacion"] = get(store, key, "T5", "grado_participacion_estudiantil") or ""
        f["ind_academia"] = int(C.has_content(
            get(store, key, "T4", "colaboracion_industria_academia")))
        # --- O3 / evidence features ---
        f["diseno"] = C.design_rigor(get(store, key, "T6", "diseno_investigacion"))
        f["diseno_lbl"] = C.DESIGN_LABEL.get(f["diseno"], "")
        sig = get(store, key, "T6", "significancia_estadistica_y_tamano_efecto")
        f["effect_size"] = int(C.reports_effect_size(sig))
        f["inferential"] = int(C.reports_inferential_stats(sig))
        f["has_comparator"] = int(C.has_content(
            get(store, key, "T6", "comparador_o_condicion_control")) and
            "sin comparador" not in L.norm(get(store, key, "T6",
                                               "comparador_o_condicion_control")))
        f["cog_reported"] = int(C.has_content(get(store, key, "T6", "resultados_cognitivos")))
        f["proc_reported"] = int(C.has_content(get(store, key, "T6", "resultados_procedimentales")))
        f["aff_reported"] = int(C.has_content(get(store, key, "T6", "resultados_afectivos_y_engagement")))
        f["validity_threats"] = int(C.has_content(
            get(store, key, "T6", "amenazas_validez_y_calidad_evidencia")))
        # --- O4 / institutional features ---
        f["licencia_open"] = C.is_open_source(get(store, key, "T7", "modelo_licenciamiento"))
        f["costo"] = C.cost_bucket(get(store, key, "T7", "costo_implementacion"))
        f["sostenibilidad"] = int(C.has_content(
            get(store, key, "T7", "indicadores_sostenibilidad_ambiental")))
        f["post_covid"] = int(C.has_content(
            get(store, key, "T7", "continuidad_educativa_post_covid")))
        f["barreras_tec"] = int(C.has_content(get(store, key, "T8", "barreras_tecnicas")))
        f["barreras_inst"] = int(C.has_content(get(store, key, "T8", "barreras_institucionales_y_docentes")))
        f["barreras_ped"] = int(C.has_content(get(store, key, "T8", "barreras_pedagogicas_y_curriculares")))
        feats.append(f)
    feats.sort(key=lambda x: (x["year"], x["cite"]))
    return feats


# ---------------------------------------------------------------------------
# Evidence-quality score (used by Capa 2 / O3)
# ---------------------------------------------------------------------------
def evidence_quality(f):
    """0-6 composite for papers that activated T6; None otherwise.
    +2 design rigor (quasi/exp), +1 comparator, +1 inferential stats,
    +1 effect size, +1 declared validity threats."""
    if not f["T6"]:
        return None
    s = 0
    if f["diseno"] and f["diseno"] >= 4:
        s += 2
    elif f["diseno"] and f["diseno"] == 3:
        s += 1
    s += f["has_comparator"]
    s += f["inferential"]
    s += f["effect_size"]
    s += f["validity_threats"]
    return s


def quality_band(score):
    if score is None:
        return "No empirical (T6 not activated)"
    if score >= 5:
        return "Strong"
    if score >= 3:
        return "Moderate"
    return "Weak"


# ---------------------------------------------------------------------------
# CAPA 1 — descriptive profile per theme
# ---------------------------------------------------------------------------
def capa1(rows):
    """Per (theme,variable): n, reported, %reported, top categories."""
    agg = defaultdict(lambda: {"n": 0, "rep": 0, "vals": Counter()})
    for r in rows:
        d = agg[(r["tema"], r["variable"])]
        d["n"] += 1
        v = r["valor_extraido"].strip()
        if not L.is_missing(v):
            d["rep"] += 1
            d["vals"][v] += 1
    out = []
    for (t, var), d in sorted(agg.items()):
        top = "; ".join(f"{k} ({c})" for k, c in d["vals"].most_common(4))
        out.append({
            "tema": t, "objetivo": L.THEME_OBJ[t], "variable": var,
            "n_articulos": d["n"], "reportado": d["rep"],
            "pct_reportado": round(100 * d["rep"] / d["n"], 1),
            "categorias_top": top,
        })
    return out


# ---------------------------------------------------------------------------
# CAPA 3 — theme co-occurrence + gap configurations
# ---------------------------------------------------------------------------
def capa3_coocurrence(act):
    n = len(act)
    co = {t: {u: 0 for u in L.THEMES} for t in L.THEMES}
    for a in act:
        present = [t for t in L.THEMES if a[t]]
        for t in present:
            co[t][t] += 1
        for t, u in combinations(present, 2):
            co[t][u] += 1
            co[u][t] += 1
    # gap / robustness configurations
    def has(a, ts): return all(a[t] for t in ts)
    def lacks(a, ts): return all(not a[t] for t in ts)
    configs = {
        "robust_arch_ai_evidence (T2+T3+T6)": [k["key_documento"] for k in act
                                               if has(k, ["T2", "T3", "T6"])],
        "pedagogy_no_evidence (T5 & !T6)": [k["key_documento"] for k in act
                                            if k["T5"] and not k["T6"]],
        "competencies_no_evidence (T4 & !T6)": [k["key_documento"] for k in act
                                                if k["T4"] and not k["T6"]],
        "benefits_no_barriers (T7 & !T8)": [k["key_documento"] for k in act
                                            if k["T7"] and not k["T8"]],
        "barriers_no_benefits (T8 & !T7)": [k["key_documento"] for k in act
                                            if k["T8"] and not k["T7"]],
        "immersive_proposal_no_evidence (T1 & T5 & !T6)": [k["key_documento"]
            for k in act if k["T1"] and k["T5"] and not k["T6"]],
        "full_stack (T1+T2+T5+T6)": [k["key_documento"] for k in act
                                     if has(k, ["T1", "T2", "T5", "T6"])],
    }
    return n, co, configs


# ---------------------------------------------------------------------------
# CAPA 4 — relational cross-tabulations (the "hidden relationships" layer)
# ---------------------------------------------------------------------------
def crosstab(feats, rowf, colf, subset=None, row_order=None, col_order=None):
    """Generic count crosstab over feature dicts. rowf/colf are callables."""
    sel = [f for f in feats if (subset(f) if subset else True)]
    tab = defaultdict(Counter)
    for f in sel:
        rv, cv = rowf(f), colf(f)
        if rv is None or cv is None or rv == "" or cv == "":
            continue
        tab[rv][cv] += 1
    rows_k = row_order or sorted(tab)
    cols_k = col_order or sorted({c for r in tab.values() for c in r})
    return tab, rows_k, cols_k


def rate_table(feats, group_fn, flag_fn, subset=None, order=None):
    """For each group, share of papers with flag==1 (flag over reported)."""
    sel = [f for f in feats if (subset(f) if subset else True)]
    g = defaultdict(lambda: [0, 0])  # group -> [hits, total]
    for f in sel:
        gv = group_fn(f)
        if gv is None or gv == "":
            continue
        g[gv][1] += 1
        if flag_fn(f):
            g[gv][0] += 1
    keys = order or sorted(g)
    return [(k, g[k][0], g[k][1],
             round(100 * g[k][0] / g[k][1], 1) if g[k][1] else 0.0)
            for k in keys if k in g]


def capa4(feats):
    """Build the relational association tables. Returns dict of named tables."""
    tables = {}

    # R1: DT maturity (Kritzinger) x evidence quality band  [T2 & T6]
    sub = lambda f: f["T2"] and f["T6"]
    tab, rk, ck = crosstab(
        feats, lambda f: f["kritzinger_lbl"], lambda f: quality_band(evidence_quality(f)),
        subset=sub, row_order=["Digital model", "Digital shadow", "Digital twin"],
        col_order=["Weak", "Moderate", "Strong"])
    tables["R1_maturity_x_quality"] = (tab, rk, ck)

    # R2: AI present vs absent x reports effect size  [T6 papers]
    tab, rk, ck = crosstab(
        feats, lambda f: "AI-augmented DT" if f["has_ai"] else "DT without AI",
        lambda f: "Effect size reported" if f["effect_size"] else "No effect size",
        subset=lambda f: f["T6"],
        row_order=["AI-augmented DT", "DT without AI"],
        col_order=["Effect size reported", "No effect size"])
    tables["R2_ai_x_effectsize"] = (tab, rk, ck)

    # R3: Environment x evidence quality band  [T1 & T6]
    tab, rk, ck = crosstab(
        feats, lambda f: f["entorno"], lambda f: quality_band(evidence_quality(f)),
        subset=lambda f: f["T1"] and f["T6"], col_order=["Weak", "Moderate", "Strong"])
    tables["R3_environment_x_quality"] = (tab, rk, ck)

    # R4: Pedagogy x reports affective/engagement outcome  [T5 & T6]
    tab, rk, ck = crosstab(
        feats, lambda f: f["pedagogia"],
        lambda f: "Engagement reported" if f["aff_reported"] else "Not reported",
        subset=lambda f: f["T5"] and f["T6"],
        col_order=["Engagement reported", "Not reported"])
    tables["R4_pedagogy_x_engagement"] = (tab, rk, ck)

    # R5: Year x DT maturity (temporal trend)
    tab, rk, ck = crosstab(
        feats, lambda f: f["year"], lambda f: f["kritzinger_lbl"],
        subset=lambda f: f["T2"],
        col_order=["Digital model", "Digital shadow", "Digital twin"])
    tables["R5_year_x_maturity"] = (tab, rk, ck)

    # R6: Immersive vs non-immersive x reports cognitive-load/affective  [T6]
    tab, rk, ck = crosstab(
        feats, lambda f: "Immersive" if f["has_immersive"] else "Non-immersive",
        lambda f: "Affective/engagement reported" if f["aff_reported"] else "Not reported",
        subset=lambda f: f["T6"],
        row_order=["Immersive", "Non-immersive"])
    tables["R6_immersive_x_affective"] = (tab, rk, ck)

    # Derived rate tables -----------------------------------------------------
    rates = {}
    rates["effect_size_by_design"] = rate_table(
        feats, lambda f: f["diseno_lbl"], lambda f: f["effect_size"],
        subset=lambda f: f["T6"] and f["diseno"],
        order=[C.DESIGN_LABEL[i] for i in (1, 2, 3, 4, 5)])
    rates["evidence_share_by_environment"] = rate_table(
        feats, lambda f: f["entorno"], lambda f: bool(f["T6"]),
        subset=lambda f: f["T1"])
    rates["barriers_share_by_quality"] = rate_table(
        feats, lambda f: quality_band(evidence_quality(f)),
        lambda f: bool(f["T8"]), subset=lambda f: f["T6"],
        order=["Weak", "Moderate", "Strong"])
    return tables, rates


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------
def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def write_crosstab(path, named, cmap_note=""):
    tab, rk, ck = named
    rows = []
    for r in rk:
        rows.append([r] + [tab[r].get(c, 0) for c in ck] +
                    [sum(tab[r].values())])
    rows.append(["TOTAL"] + [sum(tab[r].get(c, 0) for r in rk) for c in ck] +
                [sum(sum(tab[r].values()) for r in rk)])
    write_csv(path, [""] + ck + ["row total"], rows)


# ---------------------------------------------------------------------------
def main():
    L.TABLAS.mkdir(parents=True, exist_ok=True)
    store, cites, rows = load_store()
    act = L.load_activacion()
    arts = L.load_articulos()
    cmap = L.build_citation_map()
    feats = build_features(store, act, arts, cmap)

    # ---- paper_features.csv ----
    fkeys = list(feats[0].keys())
    write_csv(L.TABLAS / "paper_features.csv", fkeys,
              [[f[k] for k in fkeys] for f in feats])

    # add evidence quality to each feature row for downstream use
    for f in feats:
        f["eq_score"] = evidence_quality(f)
        f["eq_band"] = quality_band(f["eq_score"])

    # ---- CAPA 1 ----
    c1 = capa1(rows)
    write_csv(L.TABLAS / "capa1_descriptivo_por_tema.csv",
              ["tema", "objetivo", "variable", "n_articulos", "reportado",
               "pct_reportado", "categorias_top"],
              [[r["tema"], r["objetivo"], r["variable"], r["n_articulos"],
                r["reportado"], r["pct_reportado"], r["categorias_top"]]
               for r in c1])

    # ---- CAPA 2: evidence-quality matrix ----
    eq_rows = []
    for f in sorted((f for f in feats if f["T6"]),
                    key=lambda x: (-(x["eq_score"] or 0), x["cite"])):
        eq_rows.append([f["cite"], f["year"], f["diseno_lbl"],
                        "yes" if f["has_comparator"] else "no",
                        "yes" if f["inferential"] else "no",
                        "yes" if f["effect_size"] else "no",
                        "yes" if f["validity_threats"] else "no",
                        f["eq_score"], f["eq_band"]])
    write_csv(L.TABLAS / "capa2_calidad_evidencia.csv",
              ["cita", "anio", "diseno", "comparador", "stats_inferencial",
               "tamano_efecto", "amenazas_validez", "score_0_6", "banda"],
              eq_rows)

    # ---- CAPA 3: co-occurrence + gaps ----
    n, co, configs = capa3_coocurrence(act)
    write_csv(L.TABLAS / "capa3_coocurrencia.csv",
              ["tema"] + L.THEMES,
              [[t] + [co[t][u] for u in L.THEMES] for t in L.THEMES])
    write_csv(L.TABLAS / "capa3_configuraciones.csv",
              ["configuracion", "n_articulos", "pct_corpus", "claves"],
              [[name, len(keys), round(100 * len(keys) / n, 1),
                "; ".join(L.cite(k, cmap) for k in keys)]
               for name, keys in configs.items()])

    # ---- CAPA 4: relational ----
    tables, rates = capa4(feats)
    for name, named in tables.items():
        write_crosstab(L.TABLAS / f"capa4_{name}.csv", named)
    for name, rt in rates.items():
        write_csv(L.TABLAS / f"capa4_rate_{name}.csv",
                  ["grupo", "hits", "total", "pct"], rt)

    # ---- resumen.json digest ----
    resumen = build_resumen(feats, act, rows, co, configs, n, c1, tables, rates)
    with open(L.TABLAS / "resumen.json", "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)

    print(f"[analizar] {len(feats)} papers, wrote artifacts to {L.TABLAS}")
    print(f"[analizar] evidence bands: "
          f"{Counter(f['eq_band'] for f in feats if f['T6'])}")
    return feats, resumen


def build_resumen(feats, act, rows, co, configs, n, c1, tables, rates):
    def share(flag):
        return sum(1 for f in feats if f.get(flag))
    band = Counter(f["eq_band"] for f in feats if f["T6"])
    return {
        "n_papers": n,
        "theme_counts": {t: sum(a[t] for a in act) for t in L.THEMES},
        "evidence_bands": dict(band),
        "kritzinger": dict(Counter(f["kritzinger_lbl"] for f in feats if f["kritzinger"])),
        "environment": dict(Counter(f["entorno"] for f in feats if f["entorno"])),
        "pedagogy": dict(Counter(f["pedagogia"] for f in feats if f["pedagogia"])),
        "design": dict(Counter(f["diseno_lbl"] for f in feats if f["diseno"])),
        "n_has_ai": share("has_ai"),
        "n_immersive": share("has_immersive"),
        "n_effect_size": sum(1 for f in feats if f["T6"] and f["effect_size"]),
        "configs": {k: len(v) for k, v in configs.items()},
        "capa1": c1,
    }


if __name__ == "__main__":
    main()
