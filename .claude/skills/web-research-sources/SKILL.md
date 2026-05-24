---
name: web-research-sources
description: Verified web research catalog for Wless topics — LQN/queueing networks, Markov/mean-field, serverless performance, SPCL serverless-benchmarks. Source priority list, query patterns, citation verification protocol. Used by /research.
---

# Wless web research sources

## Source priority (highest first)

1. **arXiv** — `https://export.arxiv.org/api/query`
2. **Semantic Scholar** — `https://api.semanticscholar.org/graph/v1/paper/search`
3. **DBLP** — `https://dblp.org/search` (venues, author bibliographies)
4. **OpenReview** — workshop/conference reviews
5. **GitHub API** — `https://api.github.com/repos/<owner>/<repo>`
6. **Google Scholar** — fallback only (no public API)

## Verified anchors (use these as ground truth)

### LQN / queueing networks
| Source | Verification |
|---|---|
| Franks et al., "Enhanced Modeling and Solution of Layered Queueing Networks" | IEEE TSE 2009, DOI:10.1109/TSE.2008.74 |
| LQNS / LQSim (Carleton UofW) | https://github.com/layeredqueuing/V5 |
| Bolch, Greiner, de Meer, Trivedi, *Queueing Networks and Markov Chains* (Wiley 2006) | ISBN 978-0-471-79156-0 |

### Markov chains / mean-field / fluid models
| Source | Verification |
|---|---|
| Kurtz (1970), "Solutions of ODEs as limits of pure jump Markov processes" | J. Appl. Prob. 7(1), DOI:10.2307/3212147 |
| Benaïm & Le Boudec (2008), "A class of mean field interaction models" | Performance Evaluation 65(11-12), DOI:10.1016/j.peva.2008.03.005 |
| Norris, *Markov Chains* (CUP 1997) | ISBN 978-0-521-63396-3 |

### Serverless performance / FaaS
| Source | Verification |
|---|---|
| Wang et al., "Peeking Behind the Curtains of Serverless Platforms" | USENIX ATC 2018 |
| Shahrad et al., "Serverless in the Wild" | USENIX ATC 2020 |
| Mahgoub et al., "SONIC: Application-aware Data Passing for Chained Serverless Apps" | USENIX ATC 2021 |
| Eismann et al., "Sizeless: Predicting the optimal size of serverless functions" | Middleware 2021, arXiv:2010.15162 |

### SPCL serverless-benchmarks (SeBS)
| Source | Verification |
|---|---|
| Copik et al., "SeBS: A Serverless Benchmark Suite for FaaS Computing" | Middleware 2021, arXiv:2012.14132 |
| Repo | https://github.com/spcl/serverless-benchmarks (BSD-3-Clause) |

## Query patterns (topic → queries)

| Topic | 3 queries to try |
|---|---|
| Thread-pool sizing serverless | "thread pool concurrency cloud function", "right-sizing serverless concurrency", "FaaS instance concurrency model" |
| LQN solver performance | "layered queueing network solver scalability", "LQNS fluid approximation", "Lqns mean value analysis" |
| Mean-field for FaaS | "mean field fluid model serverless", "Markov population process service", "ODE limit queueing network" |
| Heavy-tailed workload | "heavy-tailed inter-arrival cloud benchmark", "Pareto think time HTTP load", "power-law service time queueing" |

## Citation verification protocol

For EVERY citation that ends up in a research note or the paper:

### DOI resolution
```bash
curl -sI "https://doi.org/<DOI>" | grep -i "^location:"
# Expect 302 redirect with venue URL
```

### arXiv check
```bash
curl -s "https://arxiv.org/abs/<arxiv-id>" | grep -o '<title>[^<]*</title>'
# Title should match the cited title
```

### Semantic Scholar metadata
```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:<DOI>?fields=title,authors,year,venue,citationCount"
```

### GitHub repo pin
```bash
curl -s "https://api.github.com/repos/<owner>/<repo>" | jq '.full_name, .default_branch, .pushed_at'
git -C <local-clone> rev-parse HEAD     # pin a SHA when using
```

## Anti-patterns

- ❌ Citing from memory ("In Kurtz 1970 it is shown that…") without verification
- ❌ Citing a paper by title only without DOI/arXiv
- ❌ Quoting an abstract as if it were a confirmed result
- ❌ Inventing co-authors or year
- ❌ Asserting "first to do X" without DBLP cross-check

## Research note template

`docs/research-notes/<topic>-<YYYY-MM-DD>.md`:

```markdown
# <Topic>

## Question
<user question>

## TL;DR
<3–5 lines>

## Verified sources (top 5)
1. Author, B. et al. (Year). *Title*. Venue. DOI:... / arXiv:...
   - Why relevant: <one sentence>
   - Key claim: <one sentence>

## Open questions / contradictions
- ...

## Recommended next step
<concrete>

## Audit (search queries used)
- "<q1>" → arXiv (5 results)
- "<q2>" → Semantic Scholar (3 results)
```

## Constraints

- NEVER include a citation without DOI/arXiv/URL
- ALWAYS log search queries in note appendix
- CROSS-CHECK if a claim contradicts user memory
