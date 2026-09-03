#!/usr/bin/env python3
"""Append a conservative second title/abstract screening pass for target records."""
import csv
from pathlib import Path


ROOT = Path(__file__).parent
TARGET_TERMS = (
    "absinthium", "wormwood", "santonin", "anthelmint", "nematod", "haemonch",
    "ascar", "trichin", "schistos", "eimeria", "trematod", "plasmod", "malaria",
)
DIRECT_TERMS = (
    "anthelmint", "nematod", "haemonch", "ascar", "trichin", "schistos",
    "eimeria", "trematod", "plasmodium", "antimalarial activity",
    "antimalarial effects", "antiprotozoal", "anti-leishmanial", "anti-leishmania",
)
SAFETY_TERMS = (
    "toxicity", "toxic", "safety", "hepatotoxic", "neurotoxic", "genotoxic",
    "pregnan", "reproductive", "poisoning",
)
EXCLUDE_TERMS = ("retracted", "erratum", "correction:")


def read_rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def classify(row):
    title = row["title"].lower()
    text = (row["title"] + " " + row["abstract"]).lower()
    if any(term in title for term in EXCLUDE_TERMS):
        return (
            "exclude_out_of_scope",
            "Correction, erratum, or retraction notice; retain the linked primary record where available and do not double count evidence.",
        )
    if row["abstract_status"] == "no_abstract":
        return (
            "include_historical_context",
            "Title identifies a target-related Artemisia record, but no abstract was retrieved; retain as a full-text verification lead and do not extract quantitative evidence.",
        )
    if any(term in title for term in DIRECT_TERMS) and not any(term in text for term in ("covid", "sars-cov-2", "cancer", "tumor")):
        return (
            "include_primary_synthesis",
            "Title/abstract reports a direct malaria, helminth, or parasite-related endpoint; retain for full-text eligibility and source-level verification before quantitative synthesis.",
        )
    if any(term in text for term in SAFETY_TERMS):
        return (
            "include_primary_safety",
            "Title/abstract reports a preparation-specific toxicity or safety endpoint relevant to translation; retain for full-text verification without inferring a human safe dose.",
        )
    return (
        "include_context_only",
        "Title/abstract identifies relevant Artemisia chemistry, santonin, production, or adjacent pharmacology context; retain for full-text eligibility but extract no quantitative finding at this stage.",
    )


def main():
    abstracts = read_rows(ROOT / "screening-abstracts.csv")
    decisions_path = ROOT / "manual-screening-decisions.csv"
    decisions = [
        row for row in read_rows(decisions_path)
        if row["evidence_scope"] != "second title/abstract pass; full-text eligibility remains open"
    ]
    done = {row["pmid"] for row in decisions}
    selected = [
        row for row in abstracts
        if row["pmid"] not in done
        and any(term in (row["title"] + " " + row["abstract"]).lower() for term in TARGET_TERMS)
    ]
    fields = ["pmid", "title", "decision", "evidence_scope", "decision_rationale"]
    with decisions_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(decisions)
        for row in selected:
            decision, rationale = classify(row)
            writer.writerow({
                "pmid": row["pmid"],
                "title": row["title"],
                "decision": decision,
                "evidence_scope": "second title/abstract pass; full-text eligibility remains open",
                "decision_rationale": rationale,
            })
    print(f"appended {len(selected)} second-pass decisions")


if __name__ == "__main__":
    main()
