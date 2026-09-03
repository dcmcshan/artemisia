# PRISMA-ScR reporting checklist

This checklist maps the current *Artemisia* living scoping-review package to the 20 essential and 2 optional PRISMA-ScR reporting items. PRISMA-ScR is used as a reporting framework, not as evidence that the review is complete. The official checklist and explanatory material are available from the [PRISMA-ScR resource page](https://www.prisma-statement.org/scoping).

The review remains in progress: the retrieval snapshot contains 4,765 unique PubMed records, the priority queue contains 1,387 records, 760 bounded title/abstract decisions are archived, and 648 queue records remain pending. Items marked **partial** or **open** must be resolved before submission as a completed scoping review.

| PRISMA-ScR item | Requirement | Current location | Status |
|---:|---|---|---|
| 1 | Identify the report as a scoping review | `article.md`, title | Reported; use “living scoping review” in the submission title |
| 2 | Structured summary | `article.md`, Abstract | Partial; abstract is present but should be converted to the target journal’s structured format if required |
| 3 | Rationale | `article.md`, §1 and §1.1 | Reported |
| 4 | Objectives | `article.md`, §1; `review-protocol.md` | Reported |
| 5 | Protocol and registration | `review-protocol.md`, `search-log.md` | Partial; protocol is archived, but no external registration number is currently claimed |
| 6 | Eligibility criteria | `review-protocol.md`, Eligibility and extraction | Reported for the living package; final eligibility denominator remains open |
| 7 | Information sources | `search-log.md`, `search-results.json` | Reported for the frozen PubMed retrieval; additional sources should be listed if searched |
| 8 | Search | `search-log.md`, `search-results.json` | Reported for the frozen search snapshot; rerun date and final strategy must be frozen before submission |
| 9 | Selection of sources of evidence | `review-flow.md`, `manual-screening-decisions.csv` | Partial; title-priority and abstract retrieval are complete, manual and full-text selection are open |
| 10 | Data charting process | `review-protocol.md`, CSV extraction files | Partial; extraction schema is defined, but exhaustive charting is not complete |
| 11 | Data items | `review-protocol.md`, CSV headers | Reported |
| 12 | Critical appraisal of individual sources | Evidence levels in `evidence-matrix.csv` and `parasite-protein-interactions.csv` | Partial; an explicit source-level appraisal rubric and completed judgments are still needed |
| 13 | Synthesis of results | `article.md`, §§2–8; `evidence-matrix.csv` | Reported for the bounded evidence set |
| 14 | Selection of sources of evidence (results) | `review-flow.md` | Open; no final included-source count or exclusion-reason summary exists yet |
| 15 | Characteristics of sources of evidence | `evidence-matrix.csv`, `antiparasitic-evidence.csv`, `supplementary-compound-specimen.csv` | Partial; representative and source-linked records are available, but not yet exhaustive |
| 16 | Critical appraisal within sources of evidence | `article.md`, evidence-boundary passages | Partial; qualitative evidence boundaries are reported, formal source-level appraisal is open |
| 17 | Results of individual sources of evidence | `claim-audit.csv`, evidence tables, `article.md` | Reported for the audited synthesis; remaining eligible sources are not yet charted |
| 18 | Synthesis of results | `article.md`, §§2–8 | Reported for the bounded evidence set |
| 19 | Summary of evidence | `article.md`, Abstract, §§8–9 | Reported, with uncertainty and translation boundaries |
| 20 | Limitations | `article.md`, §§7–9; `review-protocol.md` | Reported; update after final screening and appraisal |
| 21 | Conclusions | `article.md`, §9 | Reported |
| 22 | Funding | Submission back matter | Open; author funding and funder role must be supplied by the authors |

## Submission gate

Before the manuscript is described as a completed scoping review, update this file and `review-flow.md` with the final number screened, full texts assessed, exclusions and reasons, included sources, charting completion, and critical-appraisal judgments. Until then, the accurate article label is **living scoping review and evidence map**. The complete source registry, evidence tables, screening log, and audit outputs remain the Terpedia supplementary record.
