# Screening (Stage 1–2) — data dictionary

Two-stage selection over the 1,178 deduplicated records, plus human eligibility
review. See the PRISMA flow in `../06_results/figures/F1_prisma.png`.

## `stage1_terminological_screen.csv`
Automated terminological screen: a record passes if both a digital-twin block and
an engineering-education block are present in the title, abstract, or keywords
(with a rescue for terms appearing only in author/index keywords).
Outcome: 799 retained, 379 set aside.

## `stage2_semantic_screening_trace.csv` (`;`-delimited)
Full per-record trace of the semantic screening performed by three independent LLM
agents plus a fourth moderator agent, all implemented with **DeepSeek-V4-Flash**
(non-reasoning configuration, **temperature 0** for deterministic, reproducible
classification). One row per record. Key columns:

| Column | Meaning |
|---|---|
| `key`, `Author`, `Title`, `Year`, `Abstract`, `Keywords` | Record metadata. |
| `stage1_decision`, `stage1_pass`, `stage1_*` | Stage-1 terminological result and matched blocks. |
| `stage2_reviewerN_decision` (N=1–3) | Each primary agent's decision: `include` / `exclude` / `uncertain`. |
| `stage2_reviewerN_score` | Agent confidence/eligibility score (0–1). |
| `stage2_reviewerN_criterion` | Governing inclusion (IC*) / exclusion (EC*) / uncertainty (UA*) criterion. |
| `stage2_reviewerN_evidence`, `_justification` | Supporting text and rationale. |
| `stage2_reviewer4_*` | Moderator agent; populated only for split/uncertain cases. |
| `stage2_decision`, `stage2_score`, `stage2_consensus`, `stage2_rationale` | Aggregated outcome (`unanimous`, `moderator_resolved_*`, `moderator_uncertain`). |
| `screening_final` | `EXCLUDE` / `UNCERTAIN_HUMAN_REVIEW` / `INCLUDE`. |
| `estadoFinal` | Final status after human review: `includeF` (eligible, n=126) or `EXCLUDE`. |

**Inter-agent reliability** (3 primary agents, n=799): Fleiss' κ = 0.60; pairwise
Cohen's κ = 0.56–0.63; 58% unanimous (466 records); moderator resolved 96 split
cases; 236 escalated to human review (with 11 agent-includes) → 126 eligible.

## `deduplication_report.txt`
Record of duplicate removal (DOI and fuzzy-title matching) bringing 1,466 records
to 1,187 unique, then 1,178 after removing records without an abstract.
