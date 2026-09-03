#!/usr/bin/env python3
"""Replace source hyperlinks in article-submission.md with BibTeX citations.

The source registry remains the authoritative URL/provenance layer.  This
script only changes the journal-facing manuscript so Pandoc can render a
conventional reference list from references.bib.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent

# A few cited full-text links are repository mirrors rather than the canonical
# URL stored in the registry.  These aliases are stable BibTeX keys already
# present in references.bib.
MANUAL_ALIASES = {
    "PMC11206963": "arango2024peruvin",
    "PMC11698843": "hoshiki2025herbaalbacattle",
    "PMC3270465": "nahrevanian2012sieberi",
    "PMC3279824": "nahrevanian2010khorassanica",
    "PMC3279866": "pirali2011tick",
    "PMC4403078": "mojarrab2015extracts",
    "https://repositorio.inia.gob.pe/server/api/core/bitstreams/81b3222e-0f96-411f-87c3-ee22701e52af/content": "cala2014haemonchus",
    "https://www.degruyterbrill.com/document/doi/10.1515/znc-2015-0109/html": "garciarodriguez2015absinthium",
    "https://www.jstage.jst.go.jp/article/bpb/35/1/35_1_29/_article": "tangnitipong2012heme",
    "https://www.msptm.org/files/257_-_268_Qayyum_M.pdf": "khan2015artemisia_nematodes",
    "https://www.repositorio.unicamp.br/Busca/Download?codigoArquivo=517230&tipoMidia=0": "cala2014haemonchus",
    "https://www.thieme-connect.com/products/ejournals/pdf/10.1055/s-0032-1328324.pdf": "mouton2013artemisininonly",
}


def norm(value: str) -> str:
    return value.strip().rstrip("/").lower()


def bib_entries(path: Path) -> list[dict[str, str]]:
    text = path.read_text()
    starts = list(re.finditer(r"^@\w+\{([^,]+),", text, re.MULTILINE))
    entries: list[dict[str, str]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        block = text[start.start() : end]

        def field(name: str) -> str:
            match = re.search(
                rf"\b{name}\s*=\s*(?:\{{([^{{}}]*)\}}|\(([^()]*)\))",
                block,
                re.IGNORECASE | re.DOTALL,
            )
            return ((match.group(1) or match.group(2)).strip() if match else "")

        entries.append(
            {
                "key": start.group(1),
                "pmid": field("pmid"),
                "pmcid": field("pmcid").upper(),
                "doi": field("doi").lower(),
                "url": norm(field("url")),
            }
        )
    return entries


def build_indexes(entries: list[dict[str, str]]) -> dict[tuple[str, str], list[str]]:
    indexes: dict[tuple[str, str], list[str]] = {}
    for entry in entries:
        for kind in ("pmid", "pmcid", "doi", "url"):
            value = entry[kind]
            if value:
                indexes.setdefault((kind, value), []).append(entry["key"])
    return indexes


def source_for_url(url: str, sources: list[dict]) -> dict | None:
    target = norm(url)
    for source in sources:
        for field in ("url", "full_text_url"):
            if source.get(field) and norm(source[field]) == target:
                return source
    pmid = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", url)
    pmcid = re.search(r"(PMC\d+)", url, re.IGNORECASE)
    doi = re.search(r"doi\.org/(10\.\d{4,9}/[^/?#]+)", url, re.IGNORECASE)
    for source in sources:
        if pmid and source.get("pmid") == pmid.group(1):
            return source
        if pmcid and source.get("pmcid", "").upper() == pmcid.group(1).upper():
            return source
        if doi and source.get("doi", "").lower() == doi.group(1).lower():
            return source
    return None


def citation_key(url: str, sources: list[dict], indexes: dict[tuple[str, str], list[str]]) -> str:
    alias = MANUAL_ALIASES.get(url) or MANUAL_ALIASES.get(norm(url))
    if alias:
        return alias
    pmcid_alias = re.search(r"(PMC\d+)", url, re.IGNORECASE)
    if pmcid_alias and pmcid_alias.group(1).upper() in MANUAL_ALIASES:
        return MANUAL_ALIASES[pmcid_alias.group(1).upper()]

    source = source_for_url(url, sources)
    candidates: list[str] = []
    if source:
        for kind in ("pmid", "pmcid", "doi"):
            value = source.get(kind, "")
            if kind == "pmcid":
                value = value.upper()
            else:
                value = value.lower() if kind == "doi" else value
            if value:
                candidates.extend(indexes.get((kind, value), []))

    if not candidates:
        pmid = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", url)
        pmcid = re.search(r"(PMC\d+)", url, re.IGNORECASE)
        doi = re.search(r"doi\.org/(10\.\d{4,9}/[^/?#]+)", url, re.IGNORECASE)
        if pmid:
            candidates.extend(indexes.get(("pmid", pmid.group(1)), []))
        if pmcid:
            candidates.extend(indexes.get(("pmcid", pmcid.group(1).upper()), []))
        if doi:
            candidates.extend(indexes.get(("doi", doi.group(1).lower()), []))

    # This DOI/PMID appears twice as a legacy and current bibliography key;
    # retain the current citation key in the submission.
    if "33396790" in url or "foods10010065" in url:
        return "trendafilova2021edibleartemisia"

    candidates = list(dict.fromkeys(candidates))
    if len(candidates) != 1:
        raise SystemExit(f"Could not uniquely map citation URL: {url}\nCandidates: {candidates}")
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    manuscript = ROOT / "article-submission.md"
    bibliography = ROOT / "references.bib"
    sources = json.loads((ROOT / "sources.json").read_text())["sources"]
    indexes = build_indexes(bib_entries(bibliography))
    text = manuscript.read_text()

    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    seen: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2)
        key = citation_key(url, sources, indexes)
        seen[url] = key
        return f"[@{key}]"

    converted = pattern.sub(replace, text)
    # The original manuscript placed each source link inside prose
    # parentheses.  Collapse those wrappers so Pandoc does not render
    # double parentheses around author-year citations.
    grouped = re.compile(r"\((\[@[A-Za-z0-9_:.-]+\](?:;\s*\[@[A-Za-z0-9_:.-]+\])*)\)")

    def collapse(match: re.Match[str]) -> str:
        keys = re.findall(r"@([A-Za-z0-9_:.-]+)", match.group(1))
        return "[" + "; ".join("@" + key for key in keys) + "]"

    converted = grouped.sub(collapse, converted)
    if not args.in_place:
        print(converted)
        return
    manuscript.write_text(converted)
    print(f"converted {len(seen)} unique source links to BibTeX citations")
    for url, key in sorted(seen.items()):
        print(f"{key}\t{url}")


if __name__ == "__main__":
    main()
