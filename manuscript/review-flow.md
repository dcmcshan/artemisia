# Review-flow record

This is a living scoping-review flow record, not a completed PRISMA diagram. Counts are frozen from the 2026-09-01 PubMed retrieval and can change when the search is rerun.

```mermaid
flowchart TB
  Q[Seven PubMed query families<br/>9,741 query hits] --> U[Deduplicated union<br/>4,765 unique PMIDs]
  U --> T[Title-keyword prioritization<br/>1,387 candidate records]
  T --> A[PubMed XML abstract retrieval<br/>1,323 abstracts retrieved]
  T --> N[64 records without abstract<br/>retained for manual lookup]
  A --> M[Manual title/abstract screening<br/>pending]
  N --> M
  M --> F[Full-text verification and extraction<br/>pending]
  F --> S[Final synthesis set<br/>pending]
```

## Interpretation of counts

| Stage | Count | Evidence file | Status |
|---|---:|---|---|
| Query-family hits, including overlap | 9,741 | `search-union-summary.json` | frozen retrieval snapshot |
| Unique PubMed IDs | 4,765 | `search-union-summary.json` | deduplicated by PMID |
| Title-priority candidates | 1,387 | `screening-summary.json` | machine-assisted triage only |
| Abstracts retrieved | 1,323 | `screening-abstract-summary.json` | retrieval complete |
| Records without abstract | 64 | `screening-abstract-summary.json` | manual full-record lookup required |
| Included after manual screening | — | not yet available | open |

The title-priority threshold is a reproducibility aid and must not be reported as an eligibility criterion. No record is included in the final review solely because it appears in `screening-candidates.csv` or `screening-abstracts.csv`.
