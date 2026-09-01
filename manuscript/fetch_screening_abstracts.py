#!/usr/bin/env python3
"""Fetch PubMed abstracts for the transparent title-priority queue.

The output is an evidence-retrieval aid, not an automated inclusion decision.
Records remain pending manual title/abstract and full-text screening.
"""
import csv
import datetime
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH_SIZE = 100


def fetch_xml(pmids):
    params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
    request = urllib.request.Request(
        EFETCH + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "artemesia-review/0.1"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return ET.fromstring(response.read())


def text(node, path):
    value = node.find(path)
    return " ".join("".join(value.itertext()).split()) if value is not None else ""


def main():
    input_path = ROOT / "screening-candidates.csv"
    output_path = ROOT / "screening-abstracts.csv"
    rows = list(csv.DictReader(input_path.open(newline="")))
    output = []
    for start in range(0, len(rows), BATCH_SIZE):
        batch = rows[start:start + BATCH_SIZE]
        root = fetch_xml([row["pmid"] for row in batch])
        articles = {text(article, "./MedlineCitation/PMID"): article for article in root.findall("PubmedArticle")}
        for row in batch:
            article = articles.get(row["pmid"])
            if article is None:
                output.append({**row, "abstract": "", "abstract_status": "not_returned"})
                continue
            abstract_parts = []
            for item in article.findall("./MedlineCitation/Article/Abstract/AbstractText"):
                label = item.attrib.get("Label", "")
                value = " ".join("".join(item.itertext()).split())
                abstract_parts.append((label + ": " if label else "") + value)
            output.append({**row, "abstract": " ".join(abstract_parts), "abstract_status": "retrieved" if abstract_parts else "no_abstract"})
        time.sleep(0.35)
    with output_path.open("w", newline="") as handle:
        fields = list(rows[0]) + ["abstract", "abstract_status"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    summary = {
        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "database": "PubMed",
        "input": "screening-candidates.csv",
        "output": "screening-abstracts.csv",
        "records": len(output),
        "abstracts_retrieved": sum(row["abstract_status"] == "retrieved" for row in output),
        "no_abstract": sum(row["abstract_status"] == "no_abstract" for row in output),
        "not_returned": sum(row["abstract_status"] == "not_returned" for row in output),
        "not_an_inclusion_decision": True,
        "next_action": "manual title/abstract screening followed by full-text verification",
    }
    (ROOT / "screening-abstract-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
