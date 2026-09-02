# Artemisia parasite–protein interaction protocol

This living Terpedia table records interaction claims without collapsing distinct evidence types.

## Evidence ladder

- **E5:** direct purified-protein binding, activity-based covalent labeling, or orthogonally validated target engagement.
- **E4:** recombinant-enzyme inhibition or strong mechanism-level cellular evidence without a complete direct-binding demonstration.
- **E3:** target-associated cellular, complex, genetic, or stage-resolved evidence.
- **E2:** docking, pharmacophore, or structure-based prediction only.
- **E1:** parasite phenotype with no resolved protein target.

The `artemisia_context` field distinguishes compounds derived from *Artemisia* from artemisinin as a drug originally sourced from *A. annua*, and from non-*Artemisia* natural products used only as target-class context. A target is not transferred from one compound, species, stage, or preparation to another by chemical similarity alone.

## Retrieval and normalization

Primary records were retrieved on 2026-09-01 from PubMed Central/Europe PMC and the publisher record for the cruzain study. Exact source identifiers are in `sources.json`; the full texts used for extraction are not copied into this repository. Protein names and PDB identifiers are retained only when the source explicitly supports them. Empty identifiers mean that the current extraction did not establish a stable mapping.

The current table is a literature evidence map, not a new docking run. No docking result was generated locally because a validated ligand-preparation and docking workflow is not yet part of the Terpedia package. Future docking must archive structures, protonation/tautomer rules, software versions, parameters, raw poses, scores, and negative controls in the KB before any prediction is promoted above E2.

## Required next experiments

For *H. contortus*, prioritize fractionated *Artemisia* constituents from voucher-linked material, recombinant parasite targets, thermal-shift or surface-binding assays, enzyme kinetics, and matched host-protein counterscreens. For malaria, distinguish covalent heme-activated labeling from reversible interactions and test stage-specific target engagement. For Leishmania and trypanosomes, pair purified-compound enzyme assays with parasite permeability, target-rescue/genetic perturbation, and mammalian selectivity measurements.
