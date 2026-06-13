# Manuscript — IEEE Transactions on Learning Technologies package

This folder holds the manuscript prepared for the *IEEE Transactions on Learning
Technologies* (TLT) as a **critical systematic review**.

## Contents

| Item | Description |
|---|---|
| `TLT_DigitalTwins_Manuscript.pdf` | Built manuscript (IEEEtran, two-column, numeric citations). |
| `TLT_DigitalTwins_Supplementary.pdf` | Supplementary material — the full list of the 65 included studies. |
| `latex/` | IEEEtran sources: `TLT_DigitalTwins_Manuscript.tex` + `body.tex` (generated from `sources_md/` by `build_body.py`), `master.bib`, `IEEEtran.cls`, `figs/`, and the supplementary `.tex`. |
| `sources_md/` | Editable section Markdown (pandoc input): introduction, related reviews, conceptual framework, methods, results, discussion, conclusions, AI statement, availability, title page, cover letter. |

## Build

```bash
cd 07_manuscript/latex
# (optional) regenerate body.tex from the Markdown sources:
#   python build_body.py
pdflatex TLT_DigitalTwins_Manuscript.tex
bibtex   TLT_DigitalTwins_Manuscript
pdflatex TLT_DigitalTwins_Manuscript.tex
pdflatex TLT_DigitalTwins_Manuscript.tex
```

The manuscript follows the IEEE author format: two-column IEEEtran, single-paragraph
abstract, Index Terms, numeric `[x]` citations (IEEEtran.bst), PRISMA 2020, and an
instructional-alignment reading (constructive alignment, ICAP, Kirkpatrick).
