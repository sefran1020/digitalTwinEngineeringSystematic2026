"""
Shared utilities for the deep data analysis of the Digital Twins in
Engineering Education systematic review.

Loads the extraction outputs from ../salida_gemelos and the bibliography
from ../pdfs.bib, and builds a Zotero-key -> citation mapping.
"""
from __future__ import annotations
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SALIDA = ROOT / "salida_gemelos"
BIB = ROOT / "pdfs.bib"
PDFS_CSV = ROOT / "pdfs.csv"
OUT = Path(__file__).resolve().parent / "salidas"
TABLAS = OUT / "tablas"
FIGURAS = OUT / "figuras"

THEMES = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"]
THEME_NAMES = {
    "T1": "Virtual/Remote/Hybrid/Immersive practical infrastructure",
    "T2": "Enabling architectures and technologies",
    "T3": "AI, data analytics and DT convergence",
    "T4": "Industry 4.0/5.0 competencies and disciplinary diversification",
    "T5": "Active/experiential/project-based pedagogical design",
    "T6": "Empirical evidence of learning outcomes and engagement",
    "T7": "Institutional value: sustainability, accessibility, equity",
    "T8": "Barriers, limitations and critical implementation conditions",
}
# Theme -> objective (matriz de trazabilidad del diseno)
THEME_OBJ = {
    "T1": "O1", "T2": "O1", "T3": "O1",
    "T4": "O2", "T5": "O2",
    "T6": "O3",
    "T7": "O4", "T8": "O4",
}
OBJ_THEMES = {
    "O1": ["T1", "T2", "T3"],
    "O2": ["T4", "T5"],
    "O3": ["T6"],
    "O4": ["T7", "T8"],
}
MISSING = {"NR", "NA", "UNCERTAIN", ""}

# Manual citation-label overrides where the .bib first author is an
# institution or a bare initial (verified against pdfs.csv Author field).
CITATION_OVERRIDES = {
    "FSWUL6I2": "de Melo Freires et al., 2025",
    "YXRMLV7A": "Harini S., 2026",
}


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


def norm(s: str) -> str:
    return strip_accents(s or "").lower().strip()


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def load_articulos() -> list[dict]:
    with open(SALIDA / "articulos.csv", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_activacion() -> list[dict]:
    with open(SALIDA / "activacion.csv", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for t in THEMES:
            r[t] = int(r[t])
        r["n_temas"] = int(r["n_temas"])
    return rows


def load_datos_largo() -> list[dict]:
    with open(SALIDA / "datos_largo.csv", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_pdfs_csv() -> dict[str, dict]:
    """Zotero export keyed by Key (== key_documento). Has clean DOI/Url,
    Manual Tags and Abstract (note: accented chars may be corrupted)."""
    with open(PDFS_CSV, encoding="utf-8-sig", errors="replace") as f:
        return {r["Key"]: r for r in csv.DictReader(f)}


def is_missing(value: str) -> bool:
    v = (value or "").strip()
    if v in MISSING:
        return True
    # values like "NR (no se reporta ...)" are also missing
    return bool(re.match(r"^(NR|NA|UNCERTAIN)\b", v, re.I))


# ---------------------------------------------------------------------------
# Bibliography parsing + key mapping
# ---------------------------------------------------------------------------
def parse_bib() -> list[dict]:
    text = BIB.read_text(encoding="utf-8")
    entries = []
    # split on @type{citekey,
    for m in re.finditer(r"@(\w+)\{([^,]+),", text):
        citekey = m.group(2).strip()
        start = m.end()
        # capture fields within ~3000 chars of the entry
        chunk = text[start:start + 3000]
        ym = re.search(r"year\s*=\s*\{?(\d{4})", chunk)
        am = re.search(r"author\s*=\s*\{(.+?)\}", chunk, re.S)
        tm = re.search(r"title\s*=\s*\{(.+?)\},?\s*\n", chunk, re.S)
        year = ym.group(1) if ym else ""
        author = am.group(1).strip() if am else ""
        title = re.sub(r"[{}]", "", tm.group(1)) if tm else ""
        first = author.split(" and ")[0].strip()
        surname = first.split(",")[0].strip()
        entries.append({
            "citekey": citekey,
            "year": year,
            "author_full": author,
            "first_surname": surname,
            "title": title,
            "title_tokens": _tokens(title),
        })
    return entries


def _first_surname_from_paper(paper: str) -> str:
    # paper field looks like "Baranov et al. - 2022 - Title"
    head = paper.split(" - ")[0]
    head = re.split(r"\bet al\.?|\by\b|&|,", head)[0]
    return head.strip()


_STOP = {"the", "of", "and", "for", "in", "on", "to", "a", "an", "with",
         "et", "al", "as", "by", "its", "via"}


def _tokens(s: str) -> set[str]:
    s = norm(s).replace("�", " ")
    return {t for t in re.split(r"[^a-z0-9]+", s)
            if len(t) >= 2 and t not in _STOP}


def build_citation_map() -> dict[str, dict]:
    """Return {key_documento: {citekey, label, year, authors, first_surname}}.

    Anchored on the Zotero export (pdfs.csv), whose ``Key`` equals
    ``key_documento``. Each article is mapped to its pdfs.bib entry by
    title-token overlap within the same year (titles are highly
    distinctive), and the clean UTF-8 author from the .bib supplies the
    author-year label.
    """
    arts = load_articulos()
    pdfs = load_pdfs_csv()
    bib = parse_bib()
    by_year: dict[str, list[dict]] = {}
    for b in bib:
        by_year.setdefault(b["year"], []).append(b)

    # Score every (article, bib) pair of the same year by title overlap,
    # then assign greedily by descending score (global, order-independent).
    triples = []  # (score, key_documento, bib_entry)
    for a in arts:
        key = a["key_documento"]
        year = (a["meta__anio_publicacion"] or "").strip()
        title = (pdfs.get(key, {}).get("Title")
                 or a["meta__titulo_completo"] or "")
        ttoks = _tokens(title)
        for b in by_year.get(year, []):
            inter = len(ttoks & b["title_tokens"])
            union = len(ttoks | b["title_tokens"]) or 1
            score = inter / union  # Jaccard, robust to length
            if inter >= 2:
                triples.append((score, key, b))
    triples.sort(key=lambda t: -t[0])
    chosen_for: dict[str, dict] = {}
    used = set()
    for score, key, b in triples:
        if key in chosen_for or b["citekey"] in used:
            continue
        chosen_for[key] = b
        used.add(b["citekey"])

    mapping = {}
    unmatched = []
    for a in arts:
        key = a["key_documento"]
        year = (a["meta__anio_publicacion"] or "").strip()
        b = chosen_for.get(key)
        if b:
            label = f"{b['first_surname']} et al., {year}" \
                if " and " in b["author_full"] else \
                f"{b['first_surname']}, {year}"
            label = CITATION_OVERRIDES.get(key, label)
            mapping[key] = {
                "citekey": b["citekey"], "label": label, "year": year,
                "authors": b["author_full"], "first_surname": b["first_surname"],
            }
        else:
            surname = _first_surname_from_paper(a["paper"])
            unmatched.append((key, surname, year, a["paper"][:50]))
            mapping[key] = {
                "citekey": "", "label": f"{surname}, {year}", "year": year,
                "authors": a["meta__autores"] or "", "first_surname": surname,
            }
    # disambiguate labels shared by >1 study (e.g. two "Wang et al., 2025"):
    # append a/b/... ordered by bib citekey for stability.
    by_label: dict[str, list[str]] = {}
    for k, v in mapping.items():
        by_label.setdefault(v["label"], []).append(k)
    for label, keys in by_label.items():
        if len(keys) < 2:
            continue
        for suffix, k in zip("abcdefg",
                             sorted(keys, key=lambda x: mapping[x]["citekey"])):
            mapping[k]["label"] = label.replace(
                f", {mapping[k]['year']}", f", {mapping[k]['year']}{suffix}")

    if unmatched:
        print(f"[citation_map] {len(unmatched)} unmatched:")
        for u in unmatched:
            print("   ", u)
    return mapping


def cite(key: str, cmap: dict) -> str:
    """Author-year citation label for a Zotero key."""
    info = cmap.get(key)
    return info["label"] if info else key


if __name__ == "__main__":
    cmap = build_citation_map()
    TABLAS.mkdir(parents=True, exist_ok=True)
    with open(TABLAS / "citas_map.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["key_documento", "citekey_bib", "label", "year", "first_surname"])
        for k, v in cmap.items():
            w.writerow([k, v["citekey"], v["label"], v["year"], v["first_surname"]])
    matched = sum(1 for v in cmap.values() if v["citekey"])
    print(f"[citation_map] matched {matched}/{len(cmap)} -> {TABLAS/'citas_map.csv'}")
