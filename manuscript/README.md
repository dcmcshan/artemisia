# Journal article package

This directory is the publication workspace for the *Artemisia* terpene review. It is stored in the `artemisia` repository and uses the Terpedia KB study as its evidence and provenance source.

## Planned article

**Working title:** Terpene diversity, biosynthetic evolution, and antiparasitic evidence across *Artemisia* species: a systematic comparative review

**Article type:** narrative systematic-scoping review with a comparative evolutionary-genomics framework.

## Package

- `article.md` — current journal-style manuscript draft.
- `figures/figure-1-pathway.mmd`, `figures/figure-2-evidence-ladder.mmd`, and the paired SVGs — versioned figure sources and generated vector outputs corresponding to the two Mermaid figures in the manuscript.
- `artemisia-terpene-review-draft.pdf` — visually verified rendering of the current 153-source manuscript, including the focused malaria/wormwood evidence table and both regenerated figures.
- `review-protocol.md` — inclusion, extraction, quality-assessment, and synthesis protocol.
- `evidence-matrix.csv` — 138-record specimen-, compound-, pathway-, genome-, and assay-level evidence table.
- `claim-audit.csv` — claim-level traceability table linking central manuscript statements to source IDs and permitted inference boundaries.
- `sources.json` — stable source registry with identifiers, URLs, evidence class, and retrieval date.
- `chemotype-table.csv` — representative chemistry records with specimen/context qualifiers.
- `supplementary-compound-specimen.csv` — 39 specimen-/tissue-/preparation-level compound records, including explicit non-terpene comparators.
- `antiparasitic-evidence.csv` — quantitative, stage-aware parasite/vector assay records with host-control and translation boundaries.
- `parasite-protein-interactions.csv` — evidence-tiered terpene/terpenoid–parasite-protein interaction map, including direct target evidence, enzyme assays, docking hypotheses, and explicit target gaps.
- `protein-interaction-protocol.md` — extraction rules, evidence ladder, provenance boundaries, and next-experiment requirements for the interaction map.
- `safety-translation.csv` — preparation-specific safety and clinical-translation boundaries.
- `references.bib` — citation-ready bibliography for manuscript tooling.
- `search-log.md` — reproducible literature-search and screening plan.
- `search-results.json` — executed PubMed search snapshot with counts and top identifiers.
- `search-union-summary.json` — high-cap retrieval, overlap, and checksum summary.
- `build_screening_candidates.py` — reproducible ESearch/ESummary candidate-queue builder.
- `screening-summary.json` and `screening-candidates.csv` — title-level prioritization outputs.
- `fetch_screening_abstracts.py` — reproducible PubMed abstract retrieval for the priority queue.
- `screening-abstract-summary.json` and `screening-abstracts.csv` — abstract retrieval outputs; records remain pending manual screening.
- `triage_screening_abstracts.py` — transparent keyword-domain triage over the abstract queue.
- `screening-abstract-triage-summary.json` and `screening-abstract-triage.csv` — abstract-level ranking outputs; all records remain pending manual review.
- `manual-screening-decisions.csv` — 340-record manual title/abstract screening log with bounded decisions and rationale; the full queue remains open.
- `package-audit.json` and `validate_package.py` — machine-readable package integrity audit and its reproducible validator.
- `review-flow.md` — frozen retrieval counts and living-review flow diagram.
- `screened-seed-set.csv` — auditable screening decisions for the current seed sources.
- `submission-checklist.md` — journal-readiness and evidence-audit checklist.
- `journal-targeting.md` — scope-based target-journal recommendation and submission positioning.

Claims are kept at the smallest source-supported unit. Essential-oil mixture activity is not treated as evidence for a single active molecule, and gene presence or expression is not treated as proof of in-vivo flux.
