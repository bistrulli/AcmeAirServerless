---
description: Classify a Wless task (trivial/small/medium/large/research/maven/lqn/markov/sb/plot) and recommend the next slash command + expert agents. Does not execute.
---

# /triage <task description>

Diagnostic router. Outputs a one-page recommendation.

## Protocol

### 1. Inspect
- `git status` and `git diff --stat`
- Count files that would plausibly change
- Check if task mentions: `.g4`/grammar (n/a for Wless), `pom.xml`, `runexp.py`, `MPP4Lqn/`, `lqnmodel_*.lqn`, `plot/*.m`, `propack`, `locust`, SPCL/sb

### 2. Classify

| Size | Heuristic | Recommended |
|---|---|---|
| trivial | typo, docstring, 1 line | `/auto` |
| small | 1 file, < 50 LOC | `/auto` |
| medium | 2–3 files, single concern | `/plan` → `/iterate` |
| large | > 3 files OR cross-concern | `/plan` → `/iterate` |
| research | unclear approach / lit review | `/research` first |

### 3. Domain tags

- `maven` → propose `maven-serverless-expert` + pre-flight `/audit-deploy`
- `server` → propose `server-functions-expert`
- `lqn` → propose `lqn-model-expert` + pre-flight `/calibrate-demands`
- `markov` / `mean-field` → propose `markov-chain-expert`
- `python-orchestration` → propose `python-experiment-expert`
- `propack` → propose `propack-optimizer-expert`
- `matlab` / `plot` → propose `matlab-plot-expert` + pre-flight `/audit-data` then `/replot`
- `locust` / `workload` → propose `locust-workload-expert`
- `sb` / `spcl` / `serverless-benchmarks` → propose `spcl-benchmarks-expert` + `/sb-adapt`
- `deploy` / `start` / `port` → propose `local-deploy-expert`

### 4. Output

```markdown
# Triage — "<task>"

## Classification
- **Size**: medium
- **Domain**: lqn + maven
- **Touched files** (estimate): `MPP4Lqn/Lqn2MPP/Lqn2MPP.py`, `Acmeair_variants/Acmeair_0/lqnmodel_*.lqn.py`

## Recommended pre-flight
1. `/calibrate-demands Acmeair_0` (sanity on demands)
2. `/audit-deploy Acmeair_0/MSauthEntry` (maven build OK)

## Recommended pipeline
1. `/research "X-Y theory"` (optional, 5 min)
2. `/plan "<task>"` (will consult: lqn-model-expert, maven-serverless-expert, markov-chain-expert)
3. `/iterate plan/<slug>.md`

## Out of scope (boundary)
- This task does NOT require GCR; agent stays local. If you also want GCR validation, run it yourself after `/iterate` completes.
```

## Constraints

- NEVER recommend `/auto` for >3-file changes
- NEVER skip pre-flight gates for `pom.xml`, LQN demands, or plot regen
- If task mentions `gcloud`/`aws`/`az`: refuse and explain the boundary
