# Review protocol

## Status

The current article is a **living scoping review in progress**. A screened seed set is archived in `screened-seed-set.csv`; the PubMed search snapshot is archived in `search-results.json`; and a title-priority queue with retrieved abstracts is archived in `screening-candidates.csv` and `screening-abstracts.csv`. This is not yet a completed systematic review because manual title/abstract screening, full-text screening, and exhaustive extraction remain open.

The retrieval and screening counts are represented in `review-flow.md`. The 1,387-record queue is a transparent prioritization layer, not an eligibility decision; the final synthesis denominator remains intentionally unset until manual screening is complete.

Abstract-level keyword triage is archived in `screening-abstract-triage.csv`. It is a workload-ordering aid only: domain matches and priority scores cannot independently establish eligibility, study quality, or inclusion.

The archived manual title/abstract decisions are stored in `manual-screening-decisions.csv`. They contain 595 high-priority decisions with bounded evidence scopes and rationale; 581 of those decisions correspond to records in the 1,387-record priority triage queue. The remaining 806 queue records are still pending manual review; 14 manually screened records are outside that archived queue. This log is not an exhaustive inclusion set.

The initial supplementary compound-by-specimen table is archived in `supplementary-compound-specimen.csv`. It is a source-backed extraction of 85 representative records, not a complete genus-wide compound inventory; non-terpene co-occurring volatiles are labeled separately.

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
