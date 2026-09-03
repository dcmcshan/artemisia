# Journal article package

This directory is the publication workspace for the *Artemisia* terpene review. It is stored in the `artemisia` repository and uses the Terpedia KB study as its evidence and provenance source.

## Planned article

**Working title:** *Artemisia* terpene diversity across scales: biosynthetic evolution and bounded antiparasitic evidence

**Article type:** source-auditable frozen scoping review with a comparative evolutionary-genomics framework.

## Package

- `article.md` — extended evidence-rich manuscript and full narrative archive.
- `article-submission.md` — consolidated submission manuscript with integrated author–year citations, a rendered reference list, a bounded malaria/wormwood evidence-anchor table, and the complete Terpedia package retained as supplementary evidence.
- `submission-front-matter.md` — target-journal title-page, declarations, and submission-interface completion sheet; scientific package fields are complete, while author-specific fields remain explicitly gated for confirmation.
- `cover-letter.md` — draft cover letter aligned to the target journal, with only author-specific and invitation-status fields left for completion.
- `figures/figure-1-pathway.mmd`, `figures/figure-2-evidence-ladder.mmd`, `figures/figure-3-review-flow.mmd`, and the paired SVG/PNG outputs — versioned figure sources and generated outputs corresponding to the three Mermaid figures in the manuscript.
- `latex-header.tex` — PDF-build header for embedded figures.
- `artemisia-terpene-review-draft.pdf` — visually verified rendering of the current 540-source manuscript with 555 evidence records, including the focused malaria/wormwood evidence table, comparative-genomics table, vector-control evidence, structure-confirmed STL tranche, and regenerated figures. Rebuild with `pandoc article.md --from markdown --pdf-engine=xelatex --include-in-header=latex-header.tex --resource-path=. -V geometry:margin=0.5in -V mainfont='STIX Two Text' -o artemisia-terpene-review-draft.pdf`.
- `artemisia-terpene-review-submission.pdf` — visually verified 28-page consolidated submission rendering with integrated author–year citations, a conventional reference list, three figures, and focused chemistry, malaria/wormwood, and comparative-genomics tables. Rebuild after citation conversion with `python build_submission_citations.py --in-place`, then `pandoc article-submission.md --from markdown --citeproc --bibliography=references.bib --pdf-engine=xelatex --include-in-header=latex-header.tex --resource-path=. -V geometry:margin=0.5in -V mainfont='STIX Two Text' -o artemisia-terpene-review-submission.pdf`.
- `artemisia-terpene-review-submission.docx` — visually verified 43-page Word submission artifact with the same cited manuscript, tables, figures, declarations, and reference list; table rows are configured not to split across pages. Use this source file for journal submission where Word is preferred.
- `review-protocol.md` — inclusion, extraction, quality-assessment, and synthesis protocol.
- `prisma-scr-checklist.md` — PRISMA-ScR item-to-file mapping, current completion status, and submission gates.
- `evidence-matrix.csv` — 555-record specimen-, compound-, pathway-, genome-, review-, and assay-level evidence table.
- `claim-audit.csv` — claim-level traceability table linking central manuscript statements to source IDs and permitted inference boundaries.
- `sources.json` — stable source registry with identifiers, URLs, evidence class, and retrieval date.
- `chemotype-table.csv` — representative chemistry records with specimen/context qualifiers.
- `supplementary-compound-specimen.csv` — 179 specimen-/tissue-/preparation-level compound records, including explicit non-terpene comparators.
- `antiparasitic-evidence.csv` — 131 quantitative and stage-aware parasite/vector assay records with host-control and translation boundaries.
- `parasite-protein-interactions.csv` — evidence-tiered terpene/terpenoid–parasite-protein interaction map, including direct target evidence, enzyme assays, docking hypotheses, and explicit target gaps.
- `protein-interaction-protocol.md` — extraction rules, evidence ladder, provenance boundaries, and next-experiment requirements for the interaction map.
- `evidence-appraisal.csv` and `evidence-appraisal-protocol.md` — deterministic, provisional appraisal of all 131 antiparasitic records across chemistry resolution, phenotype context, host control, mechanism, and translation; not a meta-analytic quality score.
- `safety-translation.csv` — preparation-specific safety and clinical-translation boundaries.
- `references.bib` — citation-ready bibliography for manuscript tooling; the submission uses the cited subset through Pandoc citeproc.
- `build_submission_citations.py` — deterministic source-link-to-BibTeX crosswalk used to convert the journal-facing manuscript to conventional citations while preserving URL provenance in `sources.json`.
- `build_submission_docx.py` — deterministic Pandoc/python-docx builder for the journal-facing Word artifact, including explicit page geometry, heading/list/table styles, intact table rows across page breaks, figure sizing, header/footer, and accessibility-oriented structure. Rebuild with `python build_submission_docx.py`.
- `search-log.md` — reproducible literature-search and screening plan.
- `search-results.json` — executed PubMed search snapshot with counts and top identifiers.
- `search-union-summary.json` — high-cap retrieval, overlap, and checksum summary.
- `build_screening_candidates.py` — reproducible ESearch/ESummary candidate-queue builder.
- `screening-summary.json` and `screening-candidates.csv` — title-level prioritization outputs.
- `fetch_screening_abstracts.py` — reproducible PubMed abstract retrieval for the priority queue.
- `screening-abstract-summary.json` and `screening-abstracts.csv` — abstract retrieval outputs for the 1,387-record queue; the separate bounded title/abstract ledger is complete, while full-text eligibility remains open.
- `triage_screening_abstracts.py` — transparent keyword-domain triage over the abstract queue.
- `screening-abstract-triage-summary.json` and `screening-abstract-triage.csv` — abstract-level ranking outputs whose internal status field remains `pending_manual_review`; the separate manual ledger now covers all priority-queue records with bounded title/abstract decisions.
- `manual-screening-decisions.csv` — 1,408-record title/abstract screening log with bounded decisions and rationale; all 1,387 priority-queue records are covered, plus 21 historical or out-of-queue records. Full-text eligibility remains open.
- `extend_screening_pass.py` — reproducible conservative second-pass generator for the 92 target-related records added to the screening ledger; full-text eligibility remains open.
- `complete_screening_pass.py` — reproducible conservative completion pass covering the remaining queue records without asserting full-text eligibility or quantitative inclusion.
- `full-text-eligibility-queue.csv` — source-linked full-text gate for all 112 unique antiparasitic source records (131 evidence rows), ranked for malaria, wormwood vermifuge, other parasite, and vector-control verification.
- `full-text-verification.csv` — forty-nine full-text extraction records: 89 sources covering 104 evidence rows, with preparation-specific findings and explicit unresolved quantitative-eligibility gates; the latest records retain the *A. indica* electronic-reprint mixture/host-control caveat, *A. campestris* inaccessible-tables, *A. scoparia* IC50-unit, *A. absinthium*/*H. contortus* indexed-text, two 2026 *A. annua* indexed-study, 2025 *A. cina* ewe-trial, and low-dose *A. annua* coccidiosis caveats.
- `package-audit.json` and `validate_package.py` — machine-readable package integrity audit and its reproducible validator.
- `review-flow.md` — frozen retrieval counts and scoping-review flow diagram.
- `screened-seed-set.csv` — auditable screening decisions for the current seed sources.
- `submission-checklist.md` — journal-readiness and evidence-audit checklist.
- `journal-targeting.md` — scope-based target-journal recommendation and submission positioning.
- The completed two-proteome OrthoFinder result, annotation-anchored pathway-family mapping, and bounded three-species (*A. annua*, *A. argyi*, *A. tridentata*) diagnostic are archived in the Google Terpedia KB under [`comparative-genomics/results/`](https://github.com/Terpedia/kb/tree/docs-clean/research/artemisia_antiparasitic/comparative-genomics/results); the KB archive is the authoritative location for the large computational outputs.

Claims are kept at the smallest source-supported unit. Essential-oil mixture activity is not treated as evidence for a single active molecule, and gene presence or expression is not treated as proof of in-vivo flux.
