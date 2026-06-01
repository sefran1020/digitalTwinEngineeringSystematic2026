"""
Canonicalization of free-text extracted values into analysis-ready
categories and derived per-paper feature flags.

The extractor already used a controlled Spanish vocabulary, so most
mappings are light normalisation; the relational layer needs a few
ordinal scales and boolean flags derived by keyword/regex.
"""
from __future__ import annotations
import re
from _lib import norm, is_missing


# ---------------------------------------------------------------------------
# Ordinal / categorical canonicalizers (single-label variables)
# ---------------------------------------------------------------------------
def kritzinger_level(v: str):
    """Kritzinger et al. taxonomy as ordinal: 1 model, 2 shadow, 3 twin."""
    if is_missing(v):
        return None
    n = norm(v)
    if "twin" in n or "bidireccional" in n:
        return 3
    if "shadow" in n:
        return 2
    if "model" in n or "modelo" in n:
        return 1
    return None


KRITZINGER_LABEL = {1: "Digital model", 2: "Digital shadow", 3: "Digital twin"}


def sync_level(v: str):
    """Synchronisation degree as ordinal."""
    if is_missing(v):
        return None
    n = norm(v)
    if "bidireccional" in n:
        return 4
    if "tiempo real" in n or "real-time" in n or "real time" in n:
        return 3
    if "near-real" in n or "near real" in n:
        return 2
    if "asincron" in n or "async" in n:
        return 1
    return None


SYNC_LABEL = {1: "Asynchronous", 2: "Near-real-time", 3: "Real-time",
              4: "Bidirectional"}


def environment_bucket(v: str):
    if is_missing(v):
        return None
    n = norm(v)
    if "inmersiv" in n or "rv" in n or "metaverso" in n or "ra/" in n:
        return "Immersive (VR/AR/MR)"
    if "hibrido" in n or "hibrida" in n:
        return "Hybrid physical-virtual"
    if "remoto" in n:
        return "Remote"
    if "virtual puro" in n or n == "virtual":
        return "Virtual-only"
    if "learning factory" in n:
        return "Learning factory"
    if "cloud" in n:
        return "Cloud-based"
    return "Other"


def design_rigor(v: str):
    """Research design as an ordinal rigor scale for outcome claims.
    5 experiment > 4 quasi > 3 mixed-methods > 2 case/survey/pilot/action
    > 1 conceptual/design-development."""
    if is_missing(v):
        return None
    n = norm(v)
    if "experimento" in n and "cuasi" not in n and "quasi" not in n:
        return 5
    if "cuasi" in n or "quasi" in n:
        return 4
    if "mixed" in n or "mixto" in n:
        return 3
    if any(k in n for k in ("estudio de caso", "case", "encuesta", "survey",
                            "piloto", "pilot", "accion participativa",
                            "acción participativa")):
        return 2
    if "diseno" in n or "diseño" in n or "desarrollo" in n or "conceptual" in n:
        return 1
    return None


DESIGN_LABEL = {1: "Conceptual / design-development",
                2: "Case study / survey / pilot",
                3: "Mixed-methods", 4: "Quasi-experiment", 5: "Experiment"}


def pedagogy_bucket(v: str):
    if is_missing(v):
        return None
    n = norm(v)
    if "proyecto" in n or "pbl" in n or "project" in n:
        return "Project-based (PBL)"
    if "experiencial" in n:
        return "Experiential"
    if "activo" in n or "active" in n:
        return "Active learning"
    if "challenge" in n:
        return "Challenge-based"
    if "learning factory" in n:
        return "Learning factory"
    if "addie" in n:
        return "ADDIE"
    if "gamif" in n:
        return "Gamification"
    if "flip" in n or "blended" in n:
        return "Flipped/Blended"
    if "adaptativ" in n or "adaptive" in n:
        return "Adaptive"
    return "Other"


def education_level(v: str):
    if is_missing(v):
        return None
    n = norm(v)
    if "pregrado" in n or "undergrad" in n:
        return "Undergraduate"
    if "posgrado" in n or "maestr" in n or "doctor" in n or "graduate" in n:
        return "Graduate"
    if "tecnic" in n or "profesional" in n or "vocational" in n:
        return "Technical/vocational"
    if "mixto" in n or "mixed" in n:
        return "Mixed"
    if "docente" in n or "teacher" in n:
        return "Teacher training"
    return "Other"


# ---------------------------------------------------------------------------
# Boolean / multi-label flags (keyword & regex based)
# ---------------------------------------------------------------------------
# An effect size counts only when an actual VALUE is present (a bare mention of
# "Cohen's d / η²" as a category, or a negated "sin tamaño del efecto", does not
# count). This avoids false positives from schema-echoed text.
_EFFECT = re.compile(
    r"(cohen'?s?\s*d\s*=?\s*-?\d|(?<![a-z])d\s*=\s*-?\d"
    r"|η²p?\s*=?\s*\d|η2\s*=?\s*\d|ηp²?\s*=?\s*\d|partial\s*eta[^.]{0,14}\d"
    r"|eta\s*squared[^.]{0,14}\d|r\s*=\s*-?0?\.\d|r\s*>\s*0?\.\d)", re.I)
# Inferential statistics count only with a numeric marker (p-value, test
# statistic, CI, alpha); naming a test without any value does not count.
_PVAL = re.compile(
    r"(p\s*[<>=]\s*\.?0?\.?\d|t\(\d+\)|t\s*=\s*-?\d|f\s*=\s*\d|f\(\d"
    r"|ancova[^.]{0,15}\d|anova[^.]{0,15}\d|χ²?\s*=?\s*\d|chi[^.]{0,15}\d"
    r"|mann-?whitney[^.]{0,15}\d|r\s*=\s*-?0?\.\d|η²p?\s*=?\s*\d|d\s*=\s*-?\d"
    r"|α\s*=\s*0?\.\d|95\s*%\s*c|intervalo[s]?\s*de\s*confianza[^.]{0,25}\d)", re.I)


def reports_effect_size(v: str) -> bool:
    return (not is_missing(v)) and bool(_EFFECT.search(v))


def reports_inferential_stats(v: str) -> bool:
    return (not is_missing(v)) and bool(_PVAL.search(v))


def has_ai(tipo_ia: str) -> bool:
    return not is_missing(tipo_ia)


def ai_families(v: str) -> list[str]:
    """Multi-label AI family flags."""
    if is_missing(v):
        return []
    n = norm(v)
    fams = []
    if "deep learning" in n or "cnn" in n or "rnn" in n or "red neuronal" in n \
            or "neural" in n:
        fams.append("Deep/neural")
    if "machine learning" in n or "supervisado" in n or "clustering" in n \
            or "k-means" in n or "apriori" in n:
        fams.append("Classical ML")
    if "generativa" in n or "llm" in n or "gan" in n or "generative" in n:
        fams.append("Generative")
    if "xai" in n or "explicable" in n or "explainable" in n:
        fams.append("XAI")
    if "grafo" in n or "knowledge graph" in n:
        fams.append("Knowledge graph")
    if "agente" in n or "agent" in n:
        fams.append("Agents")
    return fams or ["Other AI"]


def is_open_source(v: str):
    if is_missing(v):
        return None
    n = norm(v)
    if "open" in n or "abierto" in n or "libre" in n:
        return True
    if "propietario" in n or "proprietary" in n or "comercial" in n \
            or "licencia comercial" in n:
        return False
    if "hibrido" in n or "freemium" in n:
        return None
    return None


def cost_bucket(v: str):
    if is_missing(v):
        return None
    n = norm(v)
    if "bajo" in n or "low" in n or "low-cost" in n or "bajo costo" in n:
        return "Low"
    if "alto" in n or "high" in n:
        return "High"
    if "medio" in n or "medium" in n or "moderad" in n:
        return "Medium"
    return "Reported (unclassified)"


def has_content(v: str) -> bool:
    """True if a variable carries reported, non-missing content."""
    return not is_missing(v)
