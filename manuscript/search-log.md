# Literature search and screening log

## Status

This is the pre-registration-style search record for the review. The sources currently in `sources.json` are the seed set used to build the comparative framework. The first PubMed query run is archived in `search-results.json`; full deduplication and title/abstract screening remain open work, so no unscreened search is represented as exhaustive.

- Search date: 2026-09-01
- Review scope: *Artemisia* terpenes, terpenoids, sesquiterpene lactones, biosynthesis, evolution, chemotype/environment variation, antiparasitic activity, and safety
- Databases and discovery surfaces: PubMed/PMC, Crossref/DOI landing pages, NCBI BioProject/GEO, Kew Plants of the World Online, and Terpedia KB records
- Search result counts: recorded in `search-results.json` and the high-cap deduplicated retrieval summary in `search-union-summary.json` (9,741 query hits; 4,765 unique PMIDs; 4,976 duplicate hits)
- Candidate screening: `build_screening_candidates.py` retrieved metadata for all 4,765 unique PMIDs and produced 1,387 title-priority candidates in `screening-candidates.csv`. This is not a final inclusion decision and must be followed by title/abstract and full-text review.

## Core query families

1. `Artemisia AND (terpene OR terpenoid OR essential oil OR chemotype)`
2. `Artemisia AND (sesquiterpene lactone OR artemisinin OR santonin OR guaianolide OR germacranolide)`
3. `Artemisia AND (diterpene OR triterpene OR phytol OR sterol)`
4. `Artemisia AND (terpene synthase OR TPS OR biosynthesis OR CYP71AV1 OR ADS OR DBR2 OR ALDH1)`
5. `Artemisia AND (genome OR transcriptome OR phylogenomics OR whole genome duplication)`
6. `Artemisia AND (antiparasitic OR antileishmanial OR antimalarial OR anthelmintic)`
7. `Artemisia AND (thujone OR toxicity OR safety OR pharmacokinetics)`

## Screening rules

Include primary analytical, biochemical, genomic, transcriptomic, metabolomic, parasite-assay, toxicology, taxonomic, and authoritative regulatory sources. Include reviews for discovery, historical framing, and synthesis, while retaining the primary source for quantitative or causal claims whenever available. Exclude records that cannot be assigned a taxon or preparation context, but retain them in a rejected-record log with the reason.

## Extraction fields

Extract DOI/PMID/accession, accepted taxon and original taxon label, voucher or sample identifier, tissue, developmental stage, locality, collection date, preparation and extraction, yield, analytical platform, identification confidence, compound and stereochemistry, abundance units, assay organism and life-cycle stage, dose, controls, endpoint, host-cell toxicity, and the claim-level evidence category.

## Synthesis safeguards

Do not pool normalized GC peak areas with absolute concentrations; oils with purified compounds; bulk tissues with secretory trichomes; or promastigote-only assays with intracellular or in-vivo results. Do not treat an absent annotation as biological absence. Any future quantitative synthesis must report missingness, study-level heterogeneity, and the exact denominator used for each comparison.
