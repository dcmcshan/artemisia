#!/usr/bin/env python3
"""Validate the auditable Artemisia review package and emit a compact audit."""
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).parent


def read_csv(name):
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    registry = json.loads((ROOT / "sources.json").read_text())
    source_ids = {item["id"] for item in registry["sources"]}
    matrix = read_csv("evidence-matrix.csv")
    antiparasitic = read_csv("antiparasitic-evidence.csv")
    interactions = read_csv("parasite-protein-interactions.csv")
    chemotypes = read_csv("chemotype-table.csv")
    safety = read_csv("safety-translation.csv")
    supplementary = read_csv("supplementary-compound-specimen.csv")
    appraisal = read_csv("evidence-appraisal.csv")
    full_text_queue = read_csv("full-text-eligibility-queue.csv")
    full_text_verification = read_csv("full-text-verification.csv")
    manual = read_csv("manual-screening-decisions.csv")
    claims = read_csv("claim-audit.csv")
    assert all(None not in row for row in matrix + antiparasitic + interactions + chemotypes + safety + full_text_queue + full_text_verification + manual + supplementary + claims + appraisal)
    matrix_missing = []
    for row in matrix:
        for source_id in row["source_id"].split("; "):
            if source_id not in source_ids:
                matrix_missing.append([row["record_id"], source_id])
    for table in (antiparasitic, interactions, chemotypes, supplementary):
        for row in table:
            for source_id in row["source_id"].split("; "):
                if source_id not in source_ids:
                    matrix_missing.append([row["record_id"], source_id])
    for row in claims:
        for source_id in row["source_ids"].split("; "):
            if source_id not in source_ids:
                matrix_missing.append([row["claim_id"], source_id])
    assert len(appraisal) == len(antiparasitic) == 128
    assert len(full_text_queue) == len({row["source_id"] for row in antiparasitic}) == 109
    assert {row["source_id"] for row in full_text_queue} == {row["source_id"] for row in antiparasitic}
    verification_ids = [row["source_id"] for row in full_text_verification]
    assert len(verification_ids) == len(set(verification_ids)) == 62
    assert set(verification_ids) <= {row["source_id"] for row in full_text_queue}
    assert all(
        row["full_text_status"] == "full text verified; quantitative eligibility unresolved"
        for row in full_text_verification
    )
    queue_by_source = {row["source_id"]: row for row in full_text_queue}
    assert all(queue_by_source[source_id]["full_text_status"] == full_text_verification[index]["full_text_status"] for index, source_id in enumerate(verification_ids))
    assert {row["record_id"] for row in appraisal} == {row["record_id"] for row in antiparasitic}
    assert {row["source_id"] for row in appraisal} <= source_ids
    assert all(row["overall_tier"] in {"A_defined_and_mechanistically_supported", "B_characterized_phenotype", "C_phenotype_with_unresolved_attribution"} for row in appraisal)
    screening = json.loads((ROOT / "screening-abstract-summary.json").read_text())
    triage = json.loads((ROOT / "screening-abstract-triage-summary.json").read_text())
    queue_pmids = {row["pmid"] for row in read_csv("screening-abstracts.csv")}
    manual_pmids = {row["pmid"] for row in manual}
    assert screening["records"] == len(read_csv("screening-abstracts.csv")) == 1387
    assert screening["abstracts_retrieved"] + screening["no_abstract"] == screening["records"]
    assert triage["manual_status_for_all_records"] == "pending_manual_review"
    bibliography_entries = len(re.findall(r"^@", (ROOT / "references.bib").read_text(), re.MULTILINE))
    assert len(matrix) == 541 and len(antiparasitic) == 128 and len(interactions) == 19 and len(chemotypes) == 10 and len(safety) == 21 and len(full_text_queue) == 109 and len(manual) == 1408 and len(manual_pmids) == len(manual) and len(manual_pmids & queue_pmids) == 1387 and len(supplementary) == 179 and len(claims) == 375 and not matrix_missing
    assert bibliography_entries == len(set(re.findall(r"^@\w+\{([^,]+)", (ROOT / "references.bib").read_text(), re.MULTILINE))) == 536
    result = {
        "validated": True,
        "source_count": len(source_ids),
        "evidence_matrix_records": len(matrix),
        "antiparasitic_records": len(antiparasitic),
        "evidence_appraisal_records": len(appraisal),
        "full_text_queue_source_records": len(full_text_queue),
        "full_text_verified_source_records": len(full_text_verification),
        "full_text_verified_evidence_records": sum(
            len(row["record_ids"].split(";")) for row in full_text_verification
        ),
        "parasite_protein_interaction_records": len(interactions),
        "manual_screening_decisions": len(manual),
        "manual_screening_queue_decided": len(manual_pmids & queue_pmids),
        "pending_queue_records": len(queue_pmids - manual_pmids),
        "supplementary_compound_specimen_records": len(supplementary),
        "claim_audit_records": len(claims),
        "bibliography_entries": bibliography_entries,
        "screening_records": screening["records"],
        "abstracts_retrieved": screening["abstracts_retrieved"],
        "records_without_abstract": screening["no_abstract"],
        "manual_screening_complete": False,
        "referential_integrity": "passed",
        "core_file_sha256": {
            name: sha256(ROOT / name)
            for name in ["article.md", "sources.json", "evidence-matrix.csv", "references.bib", "evidence-appraisal.csv"]
        },
    }
    (ROOT / "package-audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
