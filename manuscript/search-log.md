# Literature search and screening log

## Status

This is the pre-registration-style search record for the review. The sources currently in `sources.json` are the seed set used to build the comparative framework. The first PubMed query run is archived in `search-results.json`; full deduplication and title/abstract screening remain open work, so no unscreened search is represented as exhaustive.

- Search date: 2026-09-01
- Review scope: *Artemisia* terpenes, terpenoids, sesquiterpene lactones, biosynthesis, evolution, chemotype/environment variation, antiparasitic activity, and safety
- Databases and discovery surfaces: PubMed/PMC, Crossref/DOI landing pages, NCBI BioProject/GEO, Kew Plants of the World Online, and Terpedia KB records
- Search result counts: recorded in `search-results.json` and the high-cap deduplicated retrieval summary in `search-union-summary.json` (9,741 query hits; 4,765 unique PMIDs; 4,976 duplicate hits)
- Candidate screening: `build_screening_candidates.py` retrieved metadata for all 4,765 unique PMIDs and produced 1,387 title-priority candidates in `screening-candidates.csv`. This is not a final inclusion decision and must be followed by title/abstract and full-text review.
- Abstract retrieval: `fetch_screening_abstracts.py` fetches PubMed XML for the 1,387 title-priority candidates into `screening-abstracts.csv`; missing abstracts are retained explicitly and all records remain pending manual screening.
- Abstract triage: `triage_screening_abstracts.py` applies fixed keyword rules to title plus abstract and emits domain labels and a priority score; every record remains `pending_manual_review`.

## Class-balanced expansion pass (2026-09-01)

Fifty-three additional primary studies already carrying manual inclusion decisions were promoted into the source registry and bibliography. Selection was balanced across enzyme characterization, artemisinin-pathway intermediates, transcriptional and tissue regulation, population/seasonal chemotypes, post-harvest effects, *A. argyi* tissue/temporal/single-cell multi-omics, defined-compound parasite assays, oils, extracts, whole-leaf preparations, wormwood anthelmintic studies, malaria resistance, and safety chemistry. PMID, DOI, title, author, journal, year, volume, issue, page, and PMC metadata were verified against Europe PMC core records; current primary-study discovery was cross-checked against PubMed. This pass increased the registered bibliography from 76 to 129 sources and the source-linked evidence matrix from 60 to 113 records. It is a documented prioritization pass, not completion of the 1,387-record screening queue.

A targeted follow-on expansion added four primary records: a matched *A. annua* mutant whole-leaf malaria experiment, a controlled LED-spectrum chemotype/antiplasmodial experiment, an *A. absinthium*/*Schistosoma mansoni* fractionation study, and a formulated wormwood-oil/*Leishmania amazonensis* study. A subsequent update added two malaria matrix/resistance studies and one comparative wormwood-tincture nematode screen. Review-context updates added current STL biosynthesis/regulation/genomics, species-focused phytochemistry/omics, Artemisia antimalarial medicinal chemistry, and a current whole-plant malaria-tea systematic review. The current package therefore contains 140 registered sources and 125 source-linked matrix records.

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
