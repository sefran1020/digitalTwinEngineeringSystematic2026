# Digital Twins in Engineering and STEM Higher Education — Systematic Review

A reproducible **systematic review** (PRISMA 2020) of how digital twins (DTs) are
designed, implemented, and evaluated in higher-education engineering and STEM
settings. This repository contains the protocol, search exports, full screening
trace, extracted data, the end-to-end analysis pipeline, the figures and tables,
and the manuscript package submitted to the *Journal of Engineering Education*.

> **Review question.** How are digital twins designed, implemented, and evaluated
> in higher-education engineering and STEM settings?
> Decomposed into four objectives — **O1** technological architectures and
> deployment environments; **O2** pedagogy and Industry 4.0/5.0 competencies;
> **O3** empirical learning outcomes; **O4** institutional benefits and barriers.

**Corpus:** 65 primary studies (2018–2026), selected from 1,178 screened records.

## Headline finding

The technical maturity of the twin is largely **decoupled** from the rigour of its
evaluation: architectures are described more than instrumented, pedagogy is active
but seldom named, and the learning evidence is weak-dominated (median
evidence-quality score 2/6; 20 weak / 10 moderate / 5 strong of 35 empirical
studies). Competence and institutional-benefit claims outpace demonstrated
outcomes.

## Repository layout

| Folder | Contents |
|---|---|
| `01_protocol/` | Review protocol/design (`review_protocol_design.json`), extraction schemas, methodology notes, and the inductive `thematic_analysis/` (three-model theme derivation → T1–T8 / O1–O4). |
| `02_search/` | Raw database exports (`raw_exports/`: Scopus, Web of Science, Dimensions `.ris`; IEEE, EBSCO `.bib`/`.bibtex`), the merged record set, and the search-string sensitivity log (`search_log.txt`). |
| `03_screening/` | Stage-1 terminological screen, the full per-record **semantic screening trace** (3 LLM agents + moderator, with scores and criteria), and the deduplication report. |
| `04_data/` | `corpus.bib` (65 included studies) + Zotero export; `references_master.bib` (193 refs); `extraction/` (long-format extraction with verbatim quotations and activations); `derived_tables/` (Layer 1–4 outputs, evidence-quality scoring, synthesis Tables A/B). |
| `05_analysis/` | The reproducible Python pipeline (`run_all.py` orchestrates classification, Layer 1–4 analysis, robustness checks, figures, and synthesis tables). See `PIPELINE.md`. |
| `06_results/` | All figures (`figures/`: PRISMA flow + F1–F10, incl. interactive HTML), the synthesis narrative, and synthesis tables. |
| `07_manuscript/` | The JEE submission package (anonymized manuscript, title page, cover letter) and editable `sources/` (section Markdown, `master.bib`, APA CSL, formatting template, build scripts). |

## Method summary (PRISMA 2020)

```
Identified (5 databases)        1,504   Scopus 772 · Dimensions 409 · IEEE 181 · EBSCO 81 · WoS 61
  − no title/author                38
  − duplicates                    279
  − no abstract                     9
Records screened              = 1,178
  − terminological screen        379
Semantic screening            =   799   (3 LLM agents + moderator; Fleiss' κ = 0.60)
  − excluded                     552
Human eligibility review      =   247   (236 uncertain + 11 agent-include)
  − excluded                     121
Eligible (full text sought)   =   126
  − reports not retrieved         61
Studies included              =    65
```

Inter-agent reliability (3 primary agents, n = 799): **Fleiss' κ = 0.60**; pairwise
Cohen's κ = 0.56–0.63; 58% unanimous. See `03_screening/` and `06_results/figures/F1_prisma.png`.

## Reproducing the analysis

Requires Python ≥ 3.11 (developed on 3.14). Install dependencies and run the pipeline:

```bash
pip install -r requirements.txt
cd 05_analysis
python run_all.py        # regenerates derived tables and figures
```

Rebuilding the manuscript DOCX requires [pandoc](https://pandoc.org) (≥ 3.x):

```bash
cd 07_manuscript/sources
pandoc 00_front.md 01_introduction.md 01b_positionality.md 02_methods.md \
  03_results.md 04_discussion.md 05_conclusions.md 06_ai_statement.md \
  09_availability.md 07_refs.md 08_appendix.md \
  --citeproc --bibliography=assets/master.bib --csl=assets/apa.csl \
  --reference-doc=assets/reference.docx -M link-citations=true \
  -o ../JEE_DigitalTwins_Manuscript.docx
```

## Use of AI

Three large language model agents performed semantic screening (with a moderator
agent and human confirmation); an automated pipeline (Marker) converted PDFs to
text for human-verified extraction; and generative AI assisted manuscript
drafting. All decisions, data, and analytical results were produced or verified by
the authors. See `07_manuscript/sources/06_ai_statement.md`.

## What is **not** included

Full-text PDFs of the included and supporting studies are **not** redistributed
here for copyright reasons. Each record is fully identified (DOI/URL) in
`04_data/corpus.bib` and `references_master.bib`.

## Licensing

- **Code** (`05_analysis/`, build scripts): MIT License — see [`LICENSE`](LICENSE).
- **Data, tables, figures, and text** (everything else): Creative Commons
  Attribution 4.0 International (CC BY 4.0) — see [`LICENSE-CC-BY-4.0.txt`](LICENSE-CC-BY-4.0.txt).

## Citation

See [`CITATION.cff`](CITATION.cff). Please cite the article (once published) and,
if you reuse the data or code, this repository.

## Status

Manuscript under submission to the *Journal of Engineering Education*. The protocol
will be registered (PROSPERO/OSF) before any update; see the manuscript's
"Information that remains to be supplied".
