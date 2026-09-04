#!/usr/bin/env python3
"""Build the conservative quantitative-eligibility audit for the antiparasitic rows.

The audit is deliberately not a meta-analysis. It records whether a row has a
descriptive numeric result and assigns an outcome family, while requiring
independent cross-study replication, compatible units, matched preparation,
matched parasite stage, and dispersion data before pooling. The current frozen
extraction does not document that complete combination for any row.
"""
import csv
import re
from pathlib import Path


ROOT = Path(__file__).parent
OUTPUT = ROOT / "quantitative-eligibility-audit.csv"


def resolution(text):
    lowered = text.lower()
    unresolved = (
        "not reported",
        "not available",
        "not recoverable",
        "not given",
        "not specified",
        "not available in retrieved",
        "unresolved",
        "qualitative",
        "study-specific",
    )
    if not re.search(r"\d", text):
        return "not_extractable"
    if any(term in lowered for term in unresolved) or any(
        term in lowered for term in ("approximately", "about ", "range", "greater than", "less than", " +/- ")
    ):
        return "partial_numeric"
    return "numeric"


def outcome_family(row):
    text = " ".join(row[field] for field in ("endpoint", "assay_stage", "dose_or_ic50")).lower()
    if any(term in text for term in ("ic50", "ec50", "mic", "ed50", "ed90")):
        return "concentration_or_dose_effect"
    if any(term in text for term in ("lc50", "lc90", "ld50", "mortality", "lethality")):
        return "arthropod_or_worm_lethality"
    if any(term in text for term in ("fecr", "fecal egg", "epg", "worm burden", "parasitemia", "parasite burden")):
        return "organismal_efficacy"
    if any(term in text for term in ("egg hatch", "larval", "motility", "infectivity")):
        return "life_stage_assay"
    if any(term in text for term in ("hemozoin", "beta-haematin", "fp inhibition", "surrogate")):
        return "surrogate_endpoint"
    if any(term in text for term in ("protein", "redox", "resistance", "pharmacokinetic", "auc", "bioavailability")):
        return "mechanistic_or_exposure"
    return "other_or_unresolved"


def main():
    antiparasitic = list(csv.DictReader((ROOT / "antiparasitic-evidence.csv").open(newline="")))
    verified = {row["source_id"] for row in csv.DictReader((ROOT / "full-text-verification.csv").open(newline=""))}
    fields = [
        "record_id",
        "source_id",
        "taxon",
        "parasite",
        "assay_stage",
        "endpoint",
        "outcome_family",
        "descriptive_numeric_resolution",
        "source_level_verified",
        "pooling_decision",
        "pooling_gate_failures",
        "decision_basis",
    ]
    rows = []
    for row in antiparasitic:
        combined = " ".join(row[field] for field in ("endpoint", "dose_or_ic50"))
        rows.append(
            {
                "record_id": row["record_id"],
                "source_id": row["source_id"],
                "taxon": row["taxon"],
                "parasite": row["parasite"],
                "assay_stage": row["assay_stage"],
                "endpoint": row["endpoint"],
                "outcome_family": outcome_family(row),
                "descriptive_numeric_resolution": resolution(combined),
                "source_level_verified": "yes" if row["source_id"] in verified else "no",
                "pooling_decision": "descriptive_only_not_poolable",
                "pooling_gate_failures": "independent replication; matched taxon/preparation/stage/outcome/unit; dispersion or variance",
                "decision_basis": "No complete cross-study set satisfying the prespecified pooling gates is documented in the frozen extraction; retain as a descriptive result.",
            }
        )
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUTPUT.name}")


if __name__ == "__main__":
    main()
