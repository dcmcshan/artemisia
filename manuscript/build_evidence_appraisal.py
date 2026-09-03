#!/usr/bin/env python3
"""Build the deterministic, provisional appraisal of antiparasitic records."""
import csv
from pathlib import Path


ROOT = Path(__file__).parent


def read_csv(name):
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def chemistry_resolution(row):
    text = " ".join(row[key] for key in ("material", "preparation")).lower()
    if any(term in text for term in ("purified", "isolated", "defined-compound", "six major compounds")):
        return "C3_defined_or_purified"
    if any(term in text for term in ("gc-ms", "gc/", "composition", "essential oil", "oil", "chromat")):
        return "C2_profiled_mixture"
    return "C1_crude_or_unresolved"


def phenotype_context(row):
    text = " ".join(row[key] for key in ("assay_stage", "endpoint")).lower()
    if any(term in text for term in ("in vivo", "mouse", "sheep", "goat", "swine", "rodent", "murine", "fecrt", "broiler", "caprine", "coccidiosis")):
        return "P3_in_vivo_or_organismal"
    if any(term in text for term in ("promastigote", "amastigote", "blood-stage", "bloodstream", "erythrocytic", "parasite", "nematode", "larvae", "larval", "egg", "mite", "tick", "mosquito", "fluke", "trypanosoma", "plasmodium", "worm", "epimastigote", "trypomastigote", "juvenile", "insect", "stage")):
        return "P2_direct_parasite_or_vector_in_vitro"
    return "P1_indirect_or_surrogate"


def host_control(row):
    text = row["host_control_or_selectivity"].lower()
    if any(term in text for term in ("no mammalian host control", "host selectivity not", "no non-target safety", "not reported")):
        return "S1_absent_or_unresolved"
    if any(term in text for term in ("selectivity", "cytotoxic", "cc50", "macrophage", "erythrocyte", "mammalian cell")):
        return "S3_reported_selectivity_or_host_control"
    if "not interchangeable with mammalian selectivity" in text:
        return "S1_absent_or_unresolved"
    if any(term in text for term in ("comparator", "safety", "toxicity", "histopathology", "not interchangeable")):
        return "S2_partial_control"
    return "S1_absent_or_unresolved"


def mechanism_support(row, interaction_levels):
    levels = interaction_levels.get(row["source_id"], set())
    if levels & {"E4", "E5"}:
        return "M3_direct_or_functional_target_class"
    if levels & {"E2", "E3"}:
        return "M2_hypothesis_or_stage_mechanism"
    text = row["mechanistic_or_translation_boundary"].lower()
    if any(term in text for term in ("mechanism", "apoptosis", "enzyme", "oxidative", "target")) and "unresolved" not in text:
        return "M2_hypothesis_or_stage_mechanism"
    return "M1_phenotype_only_or_unresolved"


def translation_level(row, phenotype, selectivity):
    if phenotype == "P3_in_vivo_or_organismal":
        return "T3_preclinical_in_vivo"
    if selectivity == "S3_reported_selectivity_or_host_control":
        return "T2_in_vitro_with_host_context"
    return "T1_in_vitro_without_host_context"


def overall_tier(chemistry, phenotype, selectivity, mechanism):
    if chemistry == "C3_defined_or_purified" and phenotype in {"P2_direct_parasite_or_vector_in_vitro", "P3_in_vivo_or_organismal"} and selectivity in {"S2_partial_control", "S3_reported_selectivity_or_host_control"} and mechanism == "M3_direct_or_functional_target_class":
        return "A_defined_and_mechanistically_supported"
    if chemistry in {"C2_profiled_mixture", "C3_defined_or_purified"} and phenotype in {"P2_direct_parasite_or_vector_in_vitro", "P3_in_vivo_or_organismal"} and selectivity in {"S2_partial_control", "S3_reported_selectivity_or_host_control"}:
        return "B_characterized_phenotype"
    return "C_phenotype_with_unresolved_attribution"


def basis(row, chemistry, phenotype, selectivity, mechanism, translation):
    return "; ".join([
        f"chemistry={chemistry}",
        f"phenotype={phenotype}",
        f"host={selectivity}",
        f"mechanism={mechanism}",
        f"translation={translation}",
        "rule-based appraisal; inspect source and boundary text before inference",
    ])


def main():
    assays = read_csv("antiparasitic-evidence.csv")
    interactions = read_csv("parasite-protein-interactions.csv")
    interaction_levels = {}
    for row in interactions:
        interaction_levels.setdefault(row["source_id"], set()).add(row["evidence_level"])
    fields = ["record_id", "source_id", "taxon", "parasite", "chemistry_resolution", "phenotype_context", "host_control", "mechanistic_support", "translation_level", "overall_tier", "appraisal_basis"]
    output = []
    for row in assays:
        chemistry = chemistry_resolution(row)
        phenotype = phenotype_context(row)
        selectivity = host_control(row)
        mechanism = mechanism_support(row, interaction_levels)
        translation = translation_level(row, phenotype, selectivity)
        output.append({
            "record_id": row["record_id"],
            "source_id": row["source_id"],
            "taxon": row["taxon"],
            "parasite": row["parasite"],
            "chemistry_resolution": chemistry,
            "phenotype_context": phenotype,
            "host_control": selectivity,
            "mechanistic_support": mechanism,
            "translation_level": translation,
            "overall_tier": overall_tier(chemistry, phenotype, selectivity, mechanism),
            "appraisal_basis": basis(row, chemistry, phenotype, selectivity, mechanism, translation),
        })
    with (ROOT / "evidence-appraisal.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    print(f"wrote {len(output)} appraisal records")


if __name__ == "__main__":
    main()
