#!/usr/bin/env python3
"""Complete the bounded title/abstract screening ledger without asserting full-text eligibility."""

import csv
from pathlib import Path


ROOT = Path(__file__).parent
PASS_SCOPES = {
    "second title/abstract pass; full-text eligibility remains open",
    "completion title/abstract pass; full-text eligibility remains open",
}
DIRECT_TERMS = (
    "anthelmint",
    "nematod",
    "haemonch",
    "ascar",
    "trichin",
    "schistos",
    "eimeria",
    "trematod",
    "plasmodium",
    "antimalarial activity",
    "antimalarial effects",
    "antiprotozoal",
    "anti-leishmanial",
    "anti-leishmania",
    "leishmania",
)
SAFETY_TERMS = (
    "toxicity",
    "toxic",
    "safety",
    "hepatotoxic",
    "neurotoxic",
    "genotoxic",
    "pregnan",
    "reproductive",
    "poisoning",
)
REVIEW_TERMS = (
    "review",
    "overview",
    "progress",
    "advances",
    "perspective",
    "traditional use",
    "traditional medicine",
)
EXCLUDE_TITLE_TERMS = ("retracted", "erratum", "correction:")
CHEMISTRY_TERMS = (
    "terpen",
    "essential oil",
    "sesquiterp",
    "lactone",
    "artemisinin",
    "santonin",
    "thujone",
    "camphor",
    "volatile",
    "phytochem",
    "biosynth",
    "metabol",
    "trichome",
    "genome",
    "transcript",
    "extract",
    "isolation",
    "constituent",
)


def read_rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def classify(row):
    title = row["title"].lower()
    text = f"{row['title']} {row['abstract']}".lower()
    if any(term in title for term in EXCLUDE_TITLE_TERMS):
        return (
            "exclude_out_of_scope",
            "Correction, erratum, or retraction notice; retain the linked primary record where available and do not double count evidence.",
        )
    if row["abstract_status"] == "no_abstract":
        return (
            "include_historical_context",
            "No abstract was retrieved; retain the Artemisia chemistry or pharmacology record as a full-text verification lead without extracting quantitative evidence.",
        )
    if any(term in text for term in DIRECT_TERMS) and not any(
        term in text for term in ("covid", "sars-cov-2", "cancer", "tumor")
    ):
        return (
            "include_primary_synthesis",
            "Title/abstract reports a parasite-related endpoint; retain for full-text eligibility and source-level verification before quantitative synthesis.",
        )
    if any(term in text for term in SAFETY_TERMS):
        return (
            "include_primary_safety",
            "Title/abstract reports a preparation-specific toxicity or safety endpoint relevant to translation; retain for full-text verification without inferring a human safe dose.",
        )
    if any(term in title for term in REVIEW_TERMS):
        return (
            "include_review_context",
            "Title/abstract identifies a review or synthesis relevant to Artemisia chemistry, production, or pharmacology; use for discovery and context while anchoring quantitative claims to primary studies.",
        )
    if any(term in text for term in CHEMISTRY_TERMS):
        return (
            "include_context_only",
            "Title/abstract identifies Artemisia chemistry, pathway, production, or adjacent pharmacology context; retain for full-text eligibility but extract no quantitative finding at this stage.",
        )
    return (
        "include_context_only",
        "Artemisia candidate record retained for full-text eligibility; title/abstract alone does not establish a terpene, antiparasitic, or safety finding.",
    )


def main():
    abstracts = read_rows(ROOT / "screening-abstracts.csv")
    decisions_path = ROOT / "manual-screening-decisions.csv"
    decisions = [row for row in read_rows(decisions_path) if row["evidence_scope"] not in PASS_SCOPES]
    done = {row["pmid"] for row in decisions}
    selected = [row for row in abstracts if row["pmid"] not in done]
    fields = ["pmid", "title", "decision", "evidence_scope", "decision_rationale"]
    with decisions_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(decisions)
        for row in selected:
            decision, rationale = classify(row)
            writer.writerow(
                {
                    "pmid": row["pmid"],
                    "title": row["title"],
                    "decision": decision,
                    "evidence_scope": "completion title/abstract pass; full-text eligibility remains open",
                    "decision_rationale": rationale,
                }
            )
    print(f"appended {len(selected)} completion-pass decisions")


if __name__ == "__main__":
    main()
