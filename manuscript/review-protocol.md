# Review protocol

## Status

The current submission is a **frozen, source-auditable scoping review**. A screened seed set is archived in `screened-seed-set.csv`; the PubMed search snapshot is archived in `search-results.json`; and a title-priority queue with retrieved abstracts is archived in `screening-candidates.csv` and `screening-abstracts.csv`. Bounded title/abstract screening is complete for the priority queue, but full-text screening and exhaustive extraction remain open. Terpedia is an updateable archive; records added after the frozen snapshot are not silently included in the submission analysis.

The retrieval and screening counts are represented in `review-flow.md`. The 1,387-record queue is a transparent prioritization layer, not an eligibility decision; the final synthesis denominator remains intentionally unset until full-text screening and extraction are complete.

Abstract-level keyword triage is archived in `screening-abstract-triage.csv`. It is a workload-ordering aid only: domain matches and priority scores cannot independently establish eligibility, study quality, or inclusion.

The archived manual title/abstract decisions are stored in `manual-screening-decisions.csv`. They contain 1,408 bounded decisions with explicit evidence scopes and rationale; 1,387 correspond to records in the priority triage queue and 21 historical or out-of-queue records are retained separately. This log is not an exhaustive inclusion set: full-text eligibility and quantitative extraction remain open.

The full-text gate is archived in `full-text-eligibility-queue.csv`. It covers 111 unique source records underlying the 130-row antiparasitic evidence table and ranks malaria and *A. absinthium* vermifuge sources first. Each row specifies the available full-text route and the chemistry, preparation, parasite-stage, dose, host-control, constituent-attribution, mechanism, and translation checks required before quantitative inclusion.

The completed verification records are archived in `full-text-verification.csv`. They cover 87 source records and 102 linked evidence rows. “Full text verified” means that the accessible article or publisher-indexed methods/results was read and the listed preparation, analytical, parasite-model, outcome, and boundary fields were extracted; it does not mean that the study has passed the final inclusion or quantitative-harmonization gate. The *A. campestris* oil record is explicitly limited by inaccessible complete tables, the *A. scoparia* callus record retains a source-reported IC50 unit conflict, the *A. absinthium*/*H. contortus* record retains unresolved exact effect estimates because complete indexed tables were not recoverable, the two 2026 *A. annua* malaria records retain unresolved exact dose, assay, concentration, and reconstitution details, and the 2025 *A. cina* ewe trial retains unresolved terpene/STL chemistry and combined-treatment interpretation. The remaining 24 queue sources retain the unverified status.

The initial supplementary compound-by-specimen table is archived in `supplementary-compound-specimen.csv`. It is a source-backed extraction of 179 representative records, not a complete genus-wide compound inventory; non-terpene co-occurring volatiles are labeled separately.

## Review questions

1. Which mono-, sesqui-, diterpene, triterpene, and sesquiterpene-lactone classes are reported across *Artemisia*?
2. How do species, populations, chemotypes, tissues, developmental stages, environments, and extraction/analytical methods explain compositional differences?
3. Which biosynthetic genes, gene families, duplications, and expression patterns are supported by comparative genomic evidence?
4. What antiparasitic phenotypes have been tested, against which parasite stages and controls, and how directly can they be connected to terpene chemistry?

## Eligibility and extraction

Include primary analytical, genomic, transcriptomic, biochemical, metabolomic, parasite-assay, and authoritative safety/taxonomic sources. Extract accepted taxon, voucher/accession, tissue, developmental stage, locality, preparation, analytical platform, compound identity and confidence, abundance units, assay organism/stage, dose, controls, endpoint, and source identifier. Reviews are used for discovery and synthesis, not as substitutes for primary evidence where primary evidence is available.

## Quality gates

- Normalize names against Kew Plants of the World Online while retaining original names and synonyms.
- Do not merge essential oils, solvent extracts, purified compounds, or untargeted features.
- Separate confirmed identifications from library-only or putative assignments.
- Preserve stereochemistry and chemical identity where reported.
- Freeze genome assembly/annotation versions, accessions, retrieval dates, and checksums.
- Use phylogeny-aware comparisons and report missing data; absence from an annotation is not biological absence.
- Treat expression, homology, enzyme assays, metabolite detection, and parasite phenotypes as distinct evidence levels.

## Synthesis

Summarize composition by compound class and specimen context. For gene families, infer orthology and duplication/loss on a species tree, then compare candidate pathway completeness with chemistry and assay metadata. Do not infer a demonstrated pathway from graph connectivity alone. Report heterogeneity and publication bias qualitatively unless a sufficiently standardized quantitative dataset is assembled.
