---
name: wless-experiments-catalog
description: Catalog of the Wless experiments — Acmeair_variants layout, scenario taxonomy (defconc/noconc/wlessconc/propackconc), per-variant artifacts, results.csv schema. Use to find the right variant or interpret experiment outputs.
---

# Wless experiments catalog

## Variant catalog

```
Acmeair_variants/
├── Acmeair_0/                ← baseline AcmeAir (smallest, most-edited)
├── Acmeair_1/ ... Acmeair_29/  ← scale-up variants (different MS counts, call patterns)
└── sb_<benchmark-id>/        ← SPCL serverless-benchmarks adapters (when added via /sb-adapt)
```

### Per-variant structure

```
Acmeair_variants/Acmeair_N/
├── MSauthEntry/              ← microservice 1 (Maven module)
│   ├── pom.xml
│   ├── src/{main,test}/java/...
│   ├── deploy.sh             (legacy GCR — DO NOT use; user runs separately if needed)
│   ├── update.sh             (legacy GCR — DO NOT use)
│   └── getLog.sh             (legacy GCR — DO NOT use)
├── MSbookflightsEntry/
├── MSgetrewardmilesEntry/
├── ...
├── clientEntry/              ← Locust workload module
│   ├── SimpleWorkload.py
│   ├── defconcrt.txt         per-request RT, defconc
│   ├── noconcrt.txt
│   ├── wlessconcrt.txt
│   └── propackconcrt.txt
├── lqnmodel_<N>.lqn.py       ← Python LQN builder (canonical)
├── lqnmodel_<N>.lqn/         ← Generated artifacts
│   ├── model.lqn             generated text format
│   ├── optSol.csv            LQN solver output → wlessconc params
│   └── ProPackSol.csv        ProPack output → propackconc params
├── logs/                     observation logs for estimeDemands.py
└── deploy_sys.sh / update_sys.sh    aggregate scripts (legacy GCR)
```

## Scenario taxonomy

| Scenario | Concurrency | Source | Comparison role |
|---|---|---|---|
| `defconc` | 80 (or framework default) | Hard-coded in setDefConc | Baseline: cloud-vendor default |
| `noconc` | 1 | Hard-coded in setNoConc | Baseline: serialized (cost floor) |
| `wlessconc` | `n_threads_opt` from `optSol.csv` | LQN solver | **Wless contribution** |
| `propackconc` | `c_star` from `ProPackSol.csv` | scipy.optimize Pareto | Baseline: empirical Pareto |

When SPCL sb adopted (via `/sb-adapt`): add `sbconc` (SeBS default) or keep the 4 scenarios above.

## Results schema (`results/<run-dir>/results.csv`)

```csv
variant,         scenario,    n_threads, n_concurrency, p50_ms, p70_ms, p95_ms, throughput_rps, billable_s, cpu_s
Acmeair_0,       defconc,     80,        50,            45.2,   58.1,   120.4,  42.3,           48.0,       38.5
Acmeair_0,       noconc,      1,         50,            210.5,  280.3,  450.1,  20.1,           120.0,      35.0
Acmeair_0,       wlessconc,   12,        50,            48.5,   62.0,   115.0,  41.5,           18.5,       38.2
Acmeair_0,       propackconc, 18,        50,            46.1,   59.2,   118.0,  42.0,           21.0,       38.4
...
```

## State tracking (`experiments.csv`)

```csv
modelname,    exptype,     action,    timestamp,                 status, exit_code
Acmeair_0,    defconc,     deploy,    2026-05-24T14:32:11+02:00, ok,     0
Acmeair_0,    defconc,     run,       2026-05-24T14:34:55+02:00, ok,     0
Acmeair_0,    defconc,     collect,   2026-05-24T14:36:02+02:00, ok,     0
Acmeair_0,    wlessconc,   deploy,    2026-05-24T14:37:30+02:00, ok,     0
...
```

Idempotency: skip if `(modelname, exptype, status=ok)` already present.

## Plot artifacts

```
plot/figures/
├── overall_billable.pdf      ← paper-ready, vector
├── overall_billable.png      ← slides, 300 DPI
├── overall_latency.pdf
├── overall_latency.png
└── zoom_<variant>.pdf        ← per-variant zoom (if requested)
```

## Reference experiments

| Variant | Scenario count | What it tests | Notes |
|---|---|---|---|
| `Acmeair_0` | 4 | Baseline AcmeAir, all scenarios | Most-edited; use for smoke tests |
| `Acmeair_0..29` | 4 each | Scale-up (more MS, deeper call chains) | Full sweep is slow; subsets ok |
| `sb_110.dynamic-html` (when adapted) | 4 | SeBS HTTP CPU-bound | Test SPCL adapter end-to-end |
| `sb_120.uploader` (when adapted) | 4 | SeBS I/O + CPU | Multi-station LQN |

## Legacy GCR commands (DO NOT use from agent)

These scripts exist in the repo for the user's manual GCR runs only. The agent must NEVER invoke:
- `./deploy_sys.sh`, `./deploy.sh` (uses `gcloud run deploy`)
- `./update_sys.sh`, `./update.sh`
- `./getLog.sh`

Equivalent LOCAL flow (agent-allowed): `wless-experiment-runner` → mvn build + java -jar + Locust + extractExpData.

## Constraints

- NEVER invoke legacy `*.sh` that calls `gcloud`/`aws`/`az`
- ALWAYS update `experiments.csv` atomically
- DEFER per-component questions to the relevant specialist
