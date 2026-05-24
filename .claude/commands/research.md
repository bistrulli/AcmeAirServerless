---
description: Deep literature research with citation verification. Sources: arXiv, Semantic Scholar, DBLP, OpenReview, GitHub. Output: docs/research-notes/<topic>-YYYY-MM-DD.md. Topics include LQN, Markov/mean-field, serverless performance, SPCL serverless-benchmarks.
---

# /research <topic>

Invokes `web-researcher`.

## Workflow

### 1. Query expansion
- Turn topic into 3–5 technical queries
- Example: "mean field for serverless" → ["mean field queueing networks", "fluid approximation serverless", "stochastic Petri net thread pool"]

### 2. Source rotation (≥ 2 sources per query)
```bash
# arXiv API
curl -s "http://export.arxiv.org/api/query?search_query=all:%22mean+field+queueing%22&max_results=5"
# Semantic Scholar
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=mean+field+queueing&limit=5&fields=title,authors,year,externalIds,citationCount,abstract"
```

### 3. Filter
- Year ≥ 2010 unless seminal
- Citations > 10 (Semantic Scholar)
- Venue: top-tier (USENIX, OSDI, NeurIPS, JMLR, IEEE TSE, EuroSys, ICSE, PODC, ACM TOPLAS)

### 4. Verification (mandatory)
- DOI resolve: `curl -sI https://doi.org/<DOI>` → 302 with Location
- arXiv: title match `curl -s https://arxiv.org/abs/<id> | grep -o '<title>.*</title>'`
- GitHub: `curl -s https://api.github.com/repos/<owner>/<name>` → pin SHA

### 5. Synthesis → `docs/research-notes/<topic>-<date>.md`

Template:
```markdown
# <Topic>

## Question
<user question>

## TL;DR
<3–5 lines>

## Verified sources (top 5)
1. Author et al. (Year). *Title*. Venue. DOI:... / arXiv:...
   - **Why relevant**: <one sentence>
   - **Key claim**: <one sentence>

## Open questions / contradictions
- <thing the sources disagree about>

## Recommended next step
<concrete>

## Search queries used (audit)
- "<q1>"
- "<q2>"
```

## When to invoke

- Before `/plan` when approach is unclear
- When a citation in the paper needs verification
- When adopting a new SPCL sb benchmark — pin SHA + paper

## Constraints

- NEVER include a citation without DOI/arXiv ID/URL
- ALWAYS log search queries in the note appendix
- DEFER tool-specific deep dives to domain experts
