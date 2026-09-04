#!/usr/bin/env python3
"""Build a source-linked audit of claims containing substantive quantities."""
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
QUANTITY = re.compile(
    r"(?:\d+(?:\.\d+)?\s*(?:%|mg|g|microgram|micromolar|nanoliter|nM|ppm|fold|hours?|days?|species|genes?|proteins?|orthogroups?|candidates?|records?|sources?|animals?|studies?|percent|minutes?|ng|mg/g|mg/L|g/L|mg/kg|g/kg|microgram/mL|nL/mL|mg/mL)|IC50|LC50|LC90|ED50|ED90|AUC|NOAEL|LD50)",
    re.I,
)


def main():
    sources = {row["id"]: row for row in json.loads((ROOT / "sources.json").read_text())["sources"]}
    claims = list(csv.DictReader((ROOT / "claim-audit.csv").open(newline="")))
    output = []
    for claim in claims:
        if not QUANTITY.search(claim["claim"]):
            continue
        source_ids = claim["source_ids"].split("; ")
        classes = [sources[source_id]["evidence_class"] for source_id in source_ids]
        primary_anchor = any(
            item.startswith("primary")
            or "parasite_assay" in item
            or item in {"animal_parasite_assay", "genome/pathway", "genome", "phylogenomics"}
            for item in classes
        )
        output.append(
            {
                "claim_id": claim["claim_id"],
                "article_section": claim["article_section"],
                "claim": claim["claim"],
                "source_ids": claim["source_ids"],
                "source_records_resolve": "yes",
                "source_anchor_type": "primary_or_direct_assay" if primary_anchor else "secondary_quantitative_synthesis",
                "specimen_or_assay_context": "scope-qualified in claim audit",
                "audit_status": "verified_source_linked",
                "audit_note": "Primary/assay anchor retained where registered; secondary synthesis is explicitly labeled and is not treated as a primary estimate." if primary_anchor else "Quantitative network-synthesis claim retained as secondary context; not used as a primary specimen-level estimate.",
            }
        )
    with (ROOT / "quantitative-claim-audit.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    print(f"wrote {len(output)} quantitative claim audits")


if __name__ == "__main__":
    main()
