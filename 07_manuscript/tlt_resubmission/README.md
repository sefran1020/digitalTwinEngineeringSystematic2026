# IEEE TLT manuscript package

The manuscript prepared for the *IEEE Transactions on Learning Technologies* (TLT)
as a **critical systematic review** of digital twins in engineering and STEM higher
education.

## Key features

- **Evidence-quality appraisal.** Each empirical study is scored on a transparent,
  sensitivity-tested 0–6 composite; the synthesis is organised around the *quality*
  of the learning evidence, not only its quantity.
- **Related-reviews comparison (Table I).** A systematic comparison with prior
  digital-twin and laboratory reviews, showing none specific to digital twins in
  education appraises evidence quality.
- **Instructional-alignment lens.** Constructive alignment, ICAP and Kirkpatrick's
  levels are used to read pedagogy and outcomes.
- **Screening method.** Three role-conditioned LLM reviewers (one base model at
  temperature 0; Principal Investigator / Methodologist / Domain Expert) applying a
  pre-specified, decidable criterion set with a moderator and a recall-favouring
  uncertainty-precedence rule. A blind consensus-exclude audit procedure is included.
- **IEEE format.** IEEEtran two-column, numeric `[x]` citations, single-paragraph
  abstract, Index Terms; the 65-study list is in a separate Supplementary Material PDF.

## Contents

- `TLT_DigitalTwins_Manuscript.pdf`, `TLT_DigitalTwins_Supplementary.pdf` — built PDFs.
- `latex/` — IEEEtran sources: `TLT_DigitalTwins_Manuscript.tex` + `body.tex`
  (generated from `sources_md/` by `build_body.py`), `master.bib`, `IEEEtran.cls`,
  `figs/`, and the supplementary `.tex`. Build: `pdflatex → bibtex → pdflatex ×2`.
- `sources_md/` — editable Markdown section sources (pandoc input).

The corrected extraction data and regenerated derived tables and figures are in
`../../04_data/` and `../../06_results/`.
