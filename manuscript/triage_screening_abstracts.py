#!/usr/bin/env python3
"""Rank, but do not decide, the abstract-screening queue.

Every emitted record remains pending manual review. Domain labels are based on
transparent keyword rules over the title and abstract and are intended only
to make the next human-screening pass reproducible.
"""
import csv
import datetime
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULES = {
    "chemistry": (r"terpene|terpenoid|essential oil|phytochem|chemotype|gc[- ]ms|lc[- ]ms|nmr|sesquiterpene lactone", 2),
    "genomics": (r"genome|transcriptome|phylogen|terpene synthase|biosynth|tps gene|gene family|duplication", 2),
    "antiparasitic": (r"antiparasit|antileishman|leishmania|antimalar|plasmodium|anthelmint|haemonchus|trypanosom|nematicid|larvicid", 2),
    "safety": (r"toxic|safety|cytotox|thujone|pharmacokinetic|selectivity index|erythrocyte", 1),
    "primary_methods": (r"isolat|characteriz|recombinant|expression|assay|in vivo|in vitro|metabolom", 1),
}


def main():
    rows = list(csv.DictReader((ROOT / "screening-abstracts.csv").open(newline="")))
    output = []
    for row in rows:
        text = (row["title"] + " " + row["abstract"]).lower()
        domains = []
        score = 0
        for domain, (pattern, weight) in RULES.items():
            if re.search(pattern, text):
                domains.append(domain)
                score += weight
        output.append({
            "pmid": row["pmid"],
            "title": row["title"],
            "query_families": row["query_families"],
            "keyword_domains": ";".join(domains),
            "abstract_priority_score": score,
            "manual_status": "pending_manual_review",
            "abstract_status": row["abstract_status"],
        })
    output.sort(key=lambda r: (-int(r["abstract_priority_score"]), r["pmid"]))
    with (ROOT / "screening-abstract-triage.csv").open("w", newline="") as handle:
        fields = list(output[0])
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(output)
    summary = {
        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "input": "screening-abstracts.csv",
        "output": "screening-abstract-triage.csv",
        "records": len(output),
        "domain_counts": {domain: sum(domain in row["keyword_domains"].split(";") for row in output) for domain in RULES},
        "priority_score_counts": dict(sorted(Counter(int(row["abstract_priority_score"]) for row in output).items())),
        "manual_status_for_all_records": "pending_manual_review",
        "not_an_inclusion_decision": True,
    }
    (ROOT / "screening-abstract-triage-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
