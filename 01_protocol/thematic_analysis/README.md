# Inductive thematic analysis

The eight inductive themes (T1–T8) that structure the review were derived with
three frontier large language models, each run independently and then iteratively
cross-fed and refined under author review to converge on a scheme granular enough
to be exhaustive yet parsimonious enough to remain tractable:

| File | Model |
|---|---|
| `themes_chatgpt.json` | ChatGPT 5.5 |
| `themes_gemini.json`  | Gemini 3.1 Pro |
| `themes_claude.json`  | Claude Opus 4.7 |

The authors adjudicated and synthesised these outputs into the final theme set and
its mapping to the four objectives (recorded in
`../review_protocol_design.json`):

- **O1** = T1 (practical infrastructure) + T2 (enabling architectures) + T3 (AI convergence)
- **O2** = T4 (Industry 4.0/5.0 competencies) + T5 (pedagogical design)
- **O3** = T6 (empirical evidence)
- **O4** = T7 (institutional value) + T8 (barriers)

This is distinct from the **semantic screening** step (`../../03_screening/`), which
used DeepSeek-V4-Flash at temperature 0. See the manuscript's "Statement on
Artificial Intelligence" for the full disclosure.
