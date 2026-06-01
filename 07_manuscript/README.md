# Manuscript — JEE submission package

Built with pandoc + citeproc (APA 7th). The manuscript follows the *Journal of
Engineering Education* author guidelines for a **review article**.

## Prebuilt files (this folder)

| File | Role |
|---|---|
| `JEE_DigitalTwins_Manuscript_anonymized.docx` | Main manuscript, anonymized for peer review. Times New Roman 12 pt, double-spaced. 11 figures + 2 tables embedded, ~8,200-word main text, 250-word structured abstract, 5 keywords, ~74 references, Appendix A (65 included studies). |
| `JEE_DigitalTwins_TitlePage.docx` | Title page (NOT anonymized): authors, ORCIDs, affiliation, corresponding author, conflict-of-interest, biographies. |
| `JEE_DigitalTwins_CoverLetter.docx` | Cover letter. |

## `sources/` (editable)

Section Markdown (citations already in `@citekey` form), plus `assets/`
(`master.bib`, `apa.csl`, the `reference.docx` formatting template, and the build
helper scripts). Figure image links are relative to `../../06_results/figures/`,
so the manuscript rebuilds from within the repository.

Rebuild:

```bash
cd sources
pandoc 00_front.md 01_introduction.md 01b_positionality.md 02_methods.md \
  03_results.md 04_discussion.md 05_conclusions.md 06_ai_statement.md \
  09_availability.md 07_refs.md 08_appendix.md \
  --citeproc --bibliography=assets/master.bib --csl=assets/apa.csl \
  --reference-doc=assets/reference.docx -M link-citations=true \
  -o ../JEE_DigitalTwins_Manuscript_anonymized.docx
```

## Structure of the assembled manuscript

Title → structured abstract → keywords → Introduction → Positionality Statement →
Methods (PRISMA flow = Figure 1, search-chain sensitivity, inter-agent
reliability) → Results (Figures 2–11, Tables 1–2) → Discussion → Conclusions →
Statement on Artificial Intelligence → Data and Code Availability → References →
Appendix A (65 included studies).

## Items the authors must complete before submission

1. Title-page biographies: confirm each author's professional title and department
   (placeholders marked `[professional title]` / `[department]`).
2. Title-page Acknowledgements: funding sources / grant numbers (blank for
   anonymized review; add at acceptance).
3. Cover letter: insert the submission date.
4. Register the protocol (PROSPERO/OSF) and add its identifier; state exact
   last-search dates (flagged in Methods).
5. Complete the planned 20% double-coded extraction Cohen's κ (screening κ is
   already reported).
