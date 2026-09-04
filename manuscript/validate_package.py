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
    quantitative_audit = read_csv("quantitative-eligibility-audit.csv")
    manual = read_csv("manual-screening-decisions.csv")
    exclusions = read_csv("screening-exclusions.csv")
    claims = read_csv("claim-audit.csv")
    assert all(None not in row for row in matrix + antiparasitic + interactions + chemotypes + safety + full_text_queue + full_text_verification + quantitative_audit + manual + exclusions + supplementary + claims + appraisal)
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
    assert len(appraisal) == len(antiparasitic) == 133
    assert len(full_text_queue) == len({row["source_id"] for row in antiparasitic}) == 114
    assert {row["source_id"] for row in full_text_queue} == {row["source_id"] for row in antiparasitic}
    verification_ids = [row["source_id"] for row in full_text_verification]
    assert len(verification_ids) == len(set(verification_ids))
    assert set(verification_ids) <= {row["source_id"] for row in full_text_queue}
    assert all(
        row["full_text_status"] == "full text verified; quantitative eligibility unresolved"
        for row in full_text_verification
    )
    queue_by_source = {row["source_id"]: row for row in full_text_queue}
    assert all(queue_by_source[source_id]["full_text_status"] == full_text_verification[index]["full_text_status"] for index, source_id in enumerate(verification_ids))
    assert {row["record_id"] for row in appraisal} == {row["record_id"] for row in antiparasitic}
    assert len(quantitative_audit) == len(antiparasitic) == 133
    assert {row["record_id"] for row in quantitative_audit} == {row["record_id"] for row in antiparasitic}
    assert all(row["source_level_verified"] == "yes" for row in quantitative_audit)
    assert all(row["pooling_decision"] == "descriptive_only_not_poolable" for row in quantitative_audit)
    assert {row["source_id"] for row in appraisal} <= source_ids
    assert all(row["overall_tier"] in {"A_defined_and_mechanistically_supported", "B_characterized_phenotype", "C_phenotype_with_unresolved_attribution"} for row in appraisal)
    screening = json.loads((ROOT / "screening-abstract-summary.json").read_text())
    triage = json.loads((ROOT / "screening-abstract-triage-summary.json").read_text())
    submission = (ROOT / "article-submission.md").read_text()
    abstract_match = re.search(r"^## Abstract\n\n(.*?)\n\n## 1\.", submission, re.MULTILINE | re.DOTALL)
    assert abstract_match
    abstract_words = abstract_match.group(1).split()
    keyword_match = re.search(r"^\\*\\*Keywords:\*\\* (.+)$", submission, re.MULTILINE)
    assert keyword_match is not None or "**Keywords:** " in submission
    keyword_text = next(line.split("**Keywords:** ", 1)[1] for line in submission.splitlines() if line.startswith("**Keywords:** "))
    keyword_count = len([item for item in keyword_text.split(";") if item.strip()])
    assert 150 <= len(abstract_words) <= 250
    assert 4 <= keyword_count <= 6
    queue_pmids = {row["pmid"] for row in read_csv("screening-abstracts.csv")}
    manual_pmids = {row["pmid"] for row in manual}
    assert screening["records"] == len(read_csv("screening-abstracts.csv")) == 1387
    assert screening["abstracts_retrieved"] + screening["no_abstract"] == screening["records"]
    # The triage file is deliberately a rank-only artifact and therefore keeps
    # its pending label. The separate manual ledger is the authoritative
    # title/abstract decision record.
    assert triage["manual_status_for_all_records"] == "pending_manual_review"
    assert triage["records"] == 1387
    manual_screening_complete = len(manual_pmids & queue_pmids) == 1387 and not (queue_pmids - manual_pmids)
    excluded_pmids = {row["pmid"] for row in exclusions}
    expected_excluded_pmids = {row["pmid"] for row in manual if row["decision"].startswith("exclude_")}
    assert len(manual_pmids) == len(manual) and excluded_pmids == expected_excluded_pmids
    bibliography_entries = len(re.findall(r"^@", (ROOT / "references.bib").read_text(), re.MULTILINE))
    assert len(matrix) == 557 and len(antiparasitic) == 133 and len(interactions) == 20 and len(chemotypes) == 10 and len(safety) == 21 and len(full_text_queue) == 114 and len(manual) == 1408 and len(manual_pmids) == len(manual) and len(manual_pmids & queue_pmids) == 1387 and len(exclusions) == 16 and len(supplementary) == 179 and len(claims) == 411 and len(quantitative_audit) == 133 and not matrix_missing
    assert bibliography_entries == len(set(re.findall(r"^@\w+\{([^,]+)", (ROOT / "references.bib").read_text(), re.MULTILINE))) == 541
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
        "quantitative_eligibility_audit_records": len(quantitative_audit),
        "quantitative_pooling_candidates": sum(
            row["pooling_decision"] != "descriptive_only_not_poolable" for row in quantitative_audit
        ),
        "parasite_protein_interaction_records": len(interactions),
        "manual_screening_decisions": len(manual),
        "manual_screening_queue_decided": len(manual_pmids & queue_pmids),
        "screening_exclusion_records": len(exclusions),
        "pending_queue_records": len(queue_pmids - manual_pmids),
        "supplementary_compound_specimen_records": len(supplementary),
        "claim_audit_records": len(claims),
        "bibliography_entries": bibliography_entries,
        "screening_records": screening["records"],
        "abstracts_retrieved": screening["abstracts_retrieved"],
        "records_without_abstract": screening["no_abstract"],
        "manual_screening_complete": manual_screening_complete,
        "submission_abstract_words": len(abstract_words),
        "submission_keyword_count": keyword_count,
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
