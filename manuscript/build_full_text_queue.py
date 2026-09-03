#!/usr/bin/env python3
"""Build a source-linked full-text eligibility queue for the antiparasitic evidence set."""

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).parent
FIELDS = [
    "source_id",
    "record_ids",
    "title",
    "pmid",
    "pmcid",
    "source_url",
    "taxa",
    "parasites",
    "priority",
    "full_text_route",
    "full_text_status",
    "eligibility_focus",
    "required_checks",
]


def read_csv(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def classify_priority(taxa, parasites):
    text = f"{taxa} {parasites}".lower()
    if "plasmodium" in text or "malaria" in text:
        return "P1_malaria"
    if "absinthium" in text and any(term in text for term in ("haemonch", "nematod", "trichin", "hymenolepis", "eimeria", "fasciola")):
        return "P1_wormwood_vermifuge"
    if any(term in text for term in ("haemonch", "nematod", "helminth", "trichin", "hymenolepis", "eimeria", "fasciola", "schistos", "toxocara")):
        return "P2_helminth_or_protozoan"
    if any(term in text for term in ("leishmania", "trypanosoma", "toxoplasma")):
        return "P2_other_protozoan"
    if any(term in text for term in ("anopheles", "culex", "ixodes", "hyalomma", "rhipicephalus", "aedes", "mite")):
        return "P3_vector_or_ectoparasite"
    return "P4_other_antiparasitic_context"


def focus(priority, taxa, parasites):
    if priority == "P1_malaria":
        return "malaria/artemisinin: verify preparation, parasite stage, artemisinin or co-metabolite attribution, resistance state, and host exposure"
    if priority == "P1_wormwood_vermifuge":
        return "A. absinthium vermifuge: verify voucher/chemotype, thujone and santonin quantitation, helminth stage, dose, host control, and residue limits"
    if priority == "P2_helminth_or_protozoan":
        return "antiparasitic phenotype: verify species/stage, preparation chemistry, dose, comparator, selectivity, and whether a defined constituent was tested"
    if priority == "P2_other_protozoan":
        return "protozoan activity: verify parasite stage, host-cell model, chemical attribution, and mechanism evidence"
    if priority == "P3_vector_or_ectoparasite":
        return "vector or ectoparasite control: verify life stage, exposure route, mixture composition, non-target controls, and field relevance"
    return "context record: verify relevance to Artemisia terpene chemistry or antiparasitic translation before inclusion"


def main():
    evidence = read_csv(ROOT / "antiparasitic-evidence.csv")
    sources = {row["id"]: row for row in json.loads((ROOT / "sources.json").read_text())["sources"]}
    verification = {
        row["source_id"]: row
        for row in read_csv(ROOT / "full-text-verification.csv")
    }
    if len(verification) != len(read_csv(ROOT / "full-text-verification.csv")):
        raise SystemExit("duplicate source_id in full-text-verification.csv")
    grouped = defaultdict(list)
    for row in evidence:
        grouped[row["source_id"]].append(row)
    missing = sorted(set(grouped) - set(sources))
    if missing:
        raise SystemExit(f"missing source metadata: {', '.join(missing)}")

    output = []
    for source_id in sorted(grouped):
        records = grouped[source_id]
        source = sources[source_id]
        taxa = "; ".join(sorted({row["taxon"] for row in records}))
        parasites = "; ".join(sorted({row["parasite"] for row in records}))
        priority = classify_priority(taxa, parasites)
        pmcid = source.get("pmcid", "")
        output.append(
            {
                "source_id": source_id,
                "record_ids": ";".join(row["record_id"] for row in records),
                "title": source["title"],
                "pmid": source.get("pmid", ""),
                "pmcid": pmcid,
                "source_url": source["url"],
                "taxa": taxa,
                "parasites": parasites,
                "priority": priority,
                "full_text_route": "PMC full text/XML candidate" if pmcid else "PubMed abstract plus publisher/full-text lookup",
                "full_text_status": verification.get(source_id, {}).get(
                    "full_text_status", "not yet screened at full text"
                ),
                "eligibility_focus": focus(priority, taxa, parasites),
                "required_checks": "identity; preparation; analytical method; parasite stage; dose/exposure; comparator; host selectivity; constituent attribution; mechanism; translational boundary",
            }
        )
    output.sort(key=lambda row: (row["priority"], row["source_id"]))
    path = ROOT / "full-text-eligibility-queue.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)
    print(f"wrote {len(output)} unique antiparasitic source records covering {len(evidence)} evidence rows")


if __name__ == "__main__":
    main()
