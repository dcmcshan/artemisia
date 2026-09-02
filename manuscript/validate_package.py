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
    manual = read_csv("manual-screening-decisions.csv")
    claims = read_csv("claim-audit.csv")
    assert all(None not in row for row in matrix + antiparasitic + interactions + chemotypes + safety + manual + supplementary + claims)
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
    screening = json.loads((ROOT / "screening-abstract-summary.json").read_text())
    triage = json.loads((ROOT / "screening-abstract-triage-summary.json").read_text())
    assert screening["records"] == len(read_csv("screening-abstracts.csv")) == 1387
    assert screening["abstracts_retrieved"] + screening["no_abstract"] == screening["records"]
    assert triage["manual_status_for_all_records"] == "pending_manual_review"
    bibliography_entries = len(re.findall(r"^@", (ROOT / "references.bib").read_text(), re.MULTILINE))
    assert len(matrix) == 466 and len(antiparasitic) == 97 and len(interactions) == 16 and len(chemotypes) == 10 and len(safety) == 21 and len(manual) == 642 and len({row['pmid'] for row in manual}) == len(manual) and len(supplementary) == 125 and len(claims) == 270 and not matrix_missing
    assert bibliography_entries == len(set(re.findall(r"^@\w+\{([^,]+)", (ROOT / "references.bib").read_text(), re.MULTILINE))) == 462
    result = {
        "validated": True,
        "source_count": len(source_ids),
        "evidence_matrix_records": len(matrix),
        "antiparasitic_records": len(antiparasitic),
        "parasite_protein_interaction_records": len(interactions),
        "manual_screening_decisions": len(manual),
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
            for name in ["article.md", "sources.json", "evidence-matrix.csv", "references.bib"]
        },
    }
    (ROOT / "package-audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
