#!/usr/bin/env python3
"""Reproduce the initial PubMed union and create a transparent screening queue.

This is title-level prioritization only. It is not an automated inclusion decision.
"""
import csv, datetime, json, time, urllib.parse, urllib.request
from pathlib import Path

QUERIES = {
    "terpene_essential_oil": "Artemisia AND (terpene OR terpenoid OR essential oil OR chemotype)",
    "sesquiterpene_lactone": "Artemisia AND (sesquiterpene lactone OR artemisinin OR santonin OR guaianolide OR germacranolide)",
    "diterpene_triterpene": "Artemisia AND (diterpene OR triterpene OR phytol OR sterol)",
    "biosynthesis_genes": "Artemisia AND (terpene synthase OR TPS OR biosynthesis OR CYP71AV1 OR ADS OR DBR2 OR ALDH1)",
    "genomics_phylogenomics": "Artemisia AND (genome OR transcriptome OR phylogenomics OR whole genome duplication)",
    "antiparasitic": "Artemisia AND (antiparasitic OR antileishmanial OR antimalarial OR anthelmintic)",
    "safety": "Artemisia AND (thujone OR toxicity OR safety OR pharmacokinetics)",
}
ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
ROOT = Path(__file__).resolve().parent

def get_json(url, params):
    request = urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers={"User-Agent": "artemisia-review/0.1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)

def main():
    per_query = {}
    for key, query in QUERIES.items():
        result = get_json(ESEARCH, {"db": "pubmed", "term": query, "retmode": "json", "retmax": 10000, "sort": "relevance"})["esearchresult"]
        per_query[key] = result["idlist"]
        time.sleep(0.35)
    pmid_queries = {}
    for key, ids in per_query.items():
        for pmid in ids:
            pmid_queries.setdefault(pmid, []).append(key)
    records = []
    ids = sorted(pmid_queries)
    for start in range(0, len(ids), 200):
        batch = ids[start:start + 200]
        payload = get_json(ESUMMARY, {"db": "pubmed", "id": ",".join(batch), "retmode": "json"})["result"]
        for pmid in batch:
            item = payload.get(pmid, {})
            title = " ".join(str(item.get("title", "")).split())
            lower = title.lower()
            terms = {
                "chemistry": ("terpene", "terpenoid", "essential oil", "chemotype", "phytochemistry"),
                "lactone": ("lactone", "artemisinin", "santonin", "guaianolide", "germacranolide"),
                "genomics": ("genome", "transcriptome", "phylogenom", "terpene synthase", "biosynthesis"),
                "phenotype": ("antiparasitic", "antileishmanial", "antimalarial", "anthelmintic", "toxicity", "thujone"),
            }
            matched = [group for group, words in terms.items() if any(word in lower for word in words)]
            score = len(matched) + (1 if "artemisia" in lower else 0)
            records.append({"pmid": pmid, "title": title, "journal": item.get("fulljournalname", ""), "pubdate": item.get("pubdate", ""), "query_families": ";".join(pmid_queries[pmid]), "keyword_domains": ";".join(matched), "priority_score": score, "candidate_status": "title_priority_only"})
        time.sleep(0.35)
    records.sort(key=lambda row: (-int(row["priority_score"]), row["pubdate"], row["pmid"]))
    candidates = [row for row in records if int(row["priority_score"]) >= 2]
    with (ROOT / "screening-candidates.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
        writer.writeheader(); writer.writerows(candidates)
    summary = {"retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "database": "PubMed", "method": "ESearch union followed by ESummary metadata retrieval and transparent title-keyword prioritization", "unique_pmids": len(records), "candidate_records_score_ge_2": len(candidates), "not_an_inclusion_decision": True, "query_families": list(QUERIES), "output": "screening-candidates.csv"}
    (ROOT / "screening-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
