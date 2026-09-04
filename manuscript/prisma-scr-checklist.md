# PRISMA-ScR reporting checklist

This checklist maps the current *Artemisia* frozen scoping-review package to the 20 essential and 2 optional PRISMA-ScR reporting items. PRISMA-ScR is used as a reporting framework, not as evidence that the review is complete. The official checklist and explanatory material are available from the [PRISMA-ScR resource page](https://www.prisma-statement.org/scoping).

This is an intentionally frozen, source-auditable scoping review and evidence map rather than an exhaustive systematic review. The retrieval snapshot contains 4,765 unique PubMed records, the priority queue contains 1,387 records, and all queue-level title/abstract decisions plus 21 historical or out-of-queue decisions are archived. Source-level verification is complete for the bounded antiparasitic queue (114 sources covering 133 evidence rows), and the quantitative audit found zero pooling candidates. Exhaustive full-text selection, charting, and formal appraisal of the entire retrieval universe are not claimed; items marked **partial** or **open** identify that deliberate scope boundary.

| PRISMA-ScR item | Requirement | Current location | Status |
|---:|---|---|---|
| 1 | Identify the report as a scoping review | `article-submission.md`, title | Reported; submission is identified as a frozen, source-auditable scoping review |
| 2 | Structured summary | `article.md`, Abstract | Partial; abstract is present but should be converted to the target journal’s structured format if required |
| 3 | Rationale | `article.md`, §1 and §1.1 | Reported |
| 4 | Objectives | `article.md`, §1; `review-protocol.md` | Reported |
| 5 | Protocol and registration | `review-protocol.md`, `search-log.md` | Partial; protocol is archived, but no external registration number is currently claimed |
| 6 | Eligibility criteria | `review-protocol.md`, Eligibility and extraction | Reported for the frozen package; final eligibility denominator remains open |
| 7 | Information sources | `search-log.md`, `search-results.json` | Reported for the frozen PubMed retrieval; additional sources should be listed if searched |
| 8 | Search | `search-log.md`, `search-results.json` | Reported for the frozen search snapshot; rerun date and final strategy must be frozen before submission |
| 9 | Selection of sources of evidence | `review-flow.md`, `manual-screening-decisions.csv` | Reported for the frozen bounded set; queue-level decisions and source-level verification are complete for 114 antiparasitic sources, while exhaustive selection is not claimed |
| 10 | Data charting process | `review-protocol.md`, CSV extraction files | Reported for the source-linked evidence set; the extraction schema and bounded charting are complete, while exhaustive charting is not claimed |
| 11 | Data items | `review-protocol.md`, CSV headers | Reported |
| 12 | Critical appraisal of individual sources | Evidence levels in `evidence-matrix.csv` and `parasite-protein-interactions.csv` | Reported for the bounded evidence set; deterministic provisional appraisal is complete for 133 antiparasitic rows, while a formal appraisal of every registry source is not claimed |
| 13 | Synthesis of results | `article.md`, §§2–8; `evidence-matrix.csv` | Reported for the bounded evidence set |
| 14 | Selection of sources of evidence (results) | `review-flow.md` | Reported for the frozen bounded set; explicit exclusions and reasons are archived, while an exhaustive included-source denominator is not claimed |
| 15 | Characteristics of sources of evidence | `evidence-matrix.csv`, `antiparasitic-evidence.csv`, `supplementary-compound-specimen.csv` | Reported for source-linked records in the frozen evidence set; an exhaustive characteristics table is not claimed |
| 16 | Critical appraisal within sources of evidence | `article.md`, evidence-boundary passages | Reported for the bounded evidence set through explicit qualitative boundaries and provisional appraisal; formal appraisal beyond that set is not claimed |
| 17 | Results of individual sources of evidence | `claim-audit.csv`, evidence tables, `article.md` | Reported for the audited synthesis; remaining eligible sources are not yet charted |
| 18 | Synthesis of results | `article.md`, §§2–8 | Reported for the bounded evidence set |
| 19 | Summary of evidence | `article.md`, Abstract, §§8–9 | Reported, with uncertainty and translation boundaries |
| 20 | Limitations | `article.md`, §§7–9; `review-protocol.md` | Reported; update after final screening and appraisal |
| 21 | Conclusions | `article.md`, §9 | Reported |
| 22 | Funding | Submission back matter | Open; author funding and funder role must be supplied by the authors |

## Submission gate

Before the manuscript is described as a completed scoping review, update this file and `review-flow.md` with the final number screened, full texts assessed, exclusions and reasons, included sources, charting completion, and critical-appraisal judgments. Until then, the accurate submission label is **frozen scoping review and evidence map**. The complete source registry, evidence tables, screening log, and audit outputs remain the Terpedia supplementary record.
