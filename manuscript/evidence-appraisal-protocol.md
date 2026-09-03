# Provisional evidence-appraisal protocol

This protocol provides a transparent, conservative appraisal of the 123 records in
`antiparasitic-evidence.csv`. It is a structured evidence map, not a validated
risk-of-bias instrument and not a meta-analytic quality score. The appraisal is
performed by `build_evidence_appraisal.py` so that the same inputs produce the same
labels.

## Dimensions

- **Chemistry resolution:** `C3_defined_or_purified` requires a purified or
  explicitly defined compound comparison; `C2_profiled_mixture` requires a
  composition or chromatographic profile for an oil or extract; `C1_crude_or_unresolved`
  is used when the tested preparation is not chemically resolved in the record.
- **Phenotype context:** `P3_in_vivo_or_organismal` identifies an in-vivo host,
  infected-animal, or organismal endpoint; `P2_direct_parasite_or_vector_in_vitro`
  identifies a direct parasite, helminth, vector, or ectoparasite assay;
  `P1_indirect_or_surrogate` identifies an indirect or surrogate endpoint.
- **Host control:** `S3_reported_selectivity_or_host_control` requires an explicit
  mammalian, erythrocyte, macrophage, cell, or non-target control; `S2_partial_control`
  records a comparator or safety observation that is not a selectivity estimate;
  `S1_absent_or_unresolved` means that a relevant host/non-target control is absent
  or explicitly unresolved.
- **Mechanistic support:** `M3_direct_or_functional_target_class` is assigned only
  when the record is linked to an interaction-map entry at evidence level E4/E5;
  `M2_hypothesis_or_stage_mechanism` is assigned for E2/E3 interaction evidence or
  a stated cellular mechanism without target validation; `M1_phenotype_only_or_unresolved`
  is the default for preparation-level activity without protein or pathway support.
- **Translation level:** `T3_preclinical_in_vivo` marks an in-vivo host model;
  `T2_in_vitro_with_host_context` marks an in-vitro assay with an explicit host or
  selectivity context; `T1_in_vitro_without_host_context` marks an in-vitro assay
  without that context. These labels do not imply human efficacy or safety.

## Overall tier

The overall tier is deliberately non-compensatory:

- **A — defined and mechanistically supported:** `C3`, `P2` or `P3`, `S2` or `S3`,
  and `M3`; `M2` remains hypothesis-level support and is not sufficient for tier A.
- **B — characterized phenotype:** `C2` or `C3`, `P2` or `P3`, and `S2` or `S3`,
  without adequate target-level support.
- **C — phenotype with unresolved attribution:** all remaining direct assay records.

An A or B label is not a recommendation. Every row retains its source identifier
and the fields that generated the label. The output should be read together with
the assay-specific boundary text and the parasite–protein interaction map.
