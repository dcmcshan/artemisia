#!/usr/bin/env python3
"""Archive title/abstract records explicitly excluded from the frozen queue."""
import csv
from pathlib import Path


ROOT = Path(__file__).parent
SOURCE = ROOT / "manual-screening-decisions.csv"
OUTPUT = ROOT / "screening-exclusions.csv"


def main():
    rows = list(csv.DictReader(SOURCE.open(newline="")))
    excluded = [
        {
            "pmid": row["pmid"],
            "title": row["title"],
            "decision": row["decision"],
            "evidence_scope": row["evidence_scope"],
            "exclusion_reason": row["decision_rationale"],
            "source_record_retained": "yes" if "correction" in row["title"].lower() or "erratum" in row["title"].lower() or "retracted" in row["title"].lower() else "no",
        }
        for row in rows
        if row["decision"].startswith("exclude_")
    ]
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(excluded[0]))
        writer.writeheader()
        writer.writerows(excluded)
    print(f"wrote {len(excluded)} explicit exclusions to {OUTPUT.name}")


if __name__ == "__main__":
    main()
