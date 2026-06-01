"""
Synthesis tables with citations (evidencing the most important contributions):
  T-A  strong/moderate empirical studies (design, N, comparator, effect, result)
  T-B  reference architecture configurations (full-stack and architecture+AI+evidence)

Outputs Markdown (Tablas_sintesis.md) + CSV mirrors. Run after analizar.py.
"""
from __future__ import annotations
import csv
import re
import textwrap

import _lib as L
import analizar as A


def _clip(s, n=160):
    s = re.sub(r"\s+", " ", (s or "").strip())
    return (s[: n - 1] + "…") if len(s) > n else s


def _best_result(store, key):
    """Prefer a quantified cognitive/procedural result."""
    for var in ("resultados_cognitivos", "resultados_procedimentales",
                "resultados_afectivos_y_engagement"):
        v = store[key].get(("T6", var), "")
        if not L.is_missing(v) and re.search(r"\d", v):
            return _clip(v, 180)
    for var in ("resultados_cognitivos", "resultados_procedimentales"):
        v = store[key].get(("T6", var), "")
        if not L.is_missing(v):
            return _clip(v, 180)
    return "—"


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    return "\n".join(out)


def main():
    store, cites, _ = A.load_store()
    act = L.load_activacion()
    arts = L.load_articulos()
    cmap = L.build_citation_map()
    feats = A.build_features(store, act, arts, cmap)
    fby = {f["key"]: f for f in feats}
    for f in feats:
        f["eq_score"] = A.evidence_quality(f)
        f["eq_band"] = A.quality_band(f["eq_score"])

    # ----- T-A: strong + moderate empirical studies -----
    emp = [f for f in feats if f["T6"] and f["eq_band"] in ("Strong", "Moderate")]
    emp.sort(key=lambda x: (-(x["eq_score"] or 0), x["cite"]))
    ta_rows = []
    for f in emp:
        k = f["key"]
        domain = _clip(f["dominio"].split(",")[0].split(";")[0], 28) or "—"
        N = _clip(store[k].get(("T6", "tamano_muestral_y_perfil"), ""), 40)
        comp = _clip(store[k].get(("T6", "comparador_o_condicion_control"), ""), 32)
        eff = store[k].get(("T6", "significancia_estadistica_y_tamano_efecto"), "")
        eff = "—" if L.is_missing(eff) else _clip(eff, 70)
        ta_rows.append([f["cite"], f["year"], domain, f["diseno_lbl"] or "—",
                        N or "—", comp or "—", "yes" if f["effect_size"] else "no",
                        _best_result(store, k), f["eq_band"], f["eq_score"]])

    with open(L.TABLAS / "TA_evidencia_fuerte.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["study", "year", "domain", "design", "sample", "comparator",
                    "effect_size", "key_result", "band", "score_0_6"])
        w.writerows(ta_rows)

    # ----- T-B: reference architecture configurations -----
    def has(a, ts): return all(a[t] for t in ts)
    full = [f for f in feats if has(f, ["T1", "T2", "T5", "T6"])]
    archai = [f for f in feats if has(f, ["T2", "T3", "T6"])]
    seen = set()
    tb_rows = []
    for tag, group in [("Full-stack (T1+T2+T5+T6)", full),
                       ("Architecture+AI+evidence (T2+T3+T6)", archai)]:
        for f in sorted(group, key=lambda x: x["cite"]):
            k = f["key"]
            if k in seen:
                tag2 = tag + " *"
            else:
                tag2 = tag
                seen.add(k)
            sysrep = _clip(store[k].get(("T1", "sistema_real_representado"), ""), 38)
            ai = _clip(store[k].get(("T3", "tipo_ia_integrada"), ""), 30) if f["T3"] else "—"
            tb_rows.append([f["cite"], tag2, f["entorno"] or "—",
                            f["kritzinger_lbl"] or "NR", ai,
                            f["pedagogia"] or "—", sysrep or "—",
                            f["eq_band"]])
    with open(L.TABLAS / "TB_arquitecturas_referencia.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["study", "configuration", "environment", "dt_type",
                    "ai", "pedagogy", "system_modelled", "evidence_band"])
        w.writerows(tb_rows)

    # ----- Markdown -----
    md = []
    md.append("# Synthesis tables\n")
    md.append("Exploratory synthesis of the most important contributions, with "
              "author–year citations. Tables are derived from the extraction "
              "artifacts (`capa2_calidad_evidencia.csv`, `capa3_configuraciones.csv`).\n")
    md.append("## Table T-A — Empirical studies with strong/moderate evidence\n")
    md.append("Studies scoring ≥3/6 on the composite evidence-quality index "
              "(design rigour + comparator + inferential statistics + effect "
              "size + declared validity threats). Ordered by score.\n")
    md.append(md_table(
        ["Study", "Year", "Domain", "Design", "Sample", "Comparator",
         "Effect size", "Key reported result", "Band", "Score"],
        [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]] for r in ta_rows]))
    md.append("\n\n## Table T-B — Reference architecture configurations\n")
    md.append("Studies assembling the most complete technology–pedagogy–evidence "
              "stack (full-stack T1+T2+T5+T6) or coupling a detailed architecture "
              "with AI and empirical evaluation (T2+T3+T6). `*` marks a study "
              "appearing in both groups.\n")
    md.append(md_table(
        ["Study", "Configuration", "Environment", "DT type (Kritzinger)",
         "AI", "Pedagogy", "System modelled", "Evidence band"],
        tb_rows))
    md.append("")
    (A.L.OUT.parent / "Tablas_sintesis.md").write_text("\n".join(md), encoding="utf-8")

    print(f"[tablas] T-A: {len(ta_rows)} studies; T-B: {len(tb_rows)} rows")
    print("[tablas] ->", A.L.OUT.parent / "Tablas_sintesis.md")


if __name__ == "__main__":
    main()
