---
name: spcl-serverless-benchmarks-reference
description: Reference for github.com/spcl/serverless-benchmarks (SeBS) — repo structure, runner architecture, benchmark catalog, local deployment workflow, adapter pattern into Wless. Use during /sb-adapt or any work touching Acmeair_variants/sb_*/.
---

# SPCL serverless-benchmarks (SeBS) reference

## Upstream

- **Repo**: https://github.com/spcl/serverless-benchmarks
- **Paper**: Copik, Calotoiu, Grosser, Wicki, Wolf, Hoefler (2021). *SeBS: A Serverless Benchmark Suite for Function-as-a-Service Computing*. Middleware '21. arXiv:2012.14132
- **License**: BSD-3-Clause
- **Default local clone**: `~/git/serverless-benchmarks`

**Always pin a SHA** in `docs/research-notes/sb-pin-<date>-<benchmark>.md` when adapting.

## Repo structure (memorize)

```
serverless-benchmarks/
├── benchmarks/
│   ├── 100.webapps/              ← HTTP-style (easier to adapt with Locust)
│   │   ├── 110.dynamic-html/
│   │   ├── 120.uploader/
│   │   └── 130.crud-api/
│   ├── 200.multimedia/
│   │   ├── 210.thumbnailer/
│   │   └── 220.video-processing/
│   ├── 300.utilities/
│   │   ├── 311.compression/
│   │   └── 312.compression-storage/
│   ├── 400.inference/            ← ML
│   ├── 500.scientific/
│   │   └── 501.graph-pagerank/
│   └── wrappers/                 ← runtimes (python, nodejs)
├── benchmarks-data/              ← downloaded inputs
├── config/
│   ├── systems.json              per-deployment defaults
│   └── example.json
├── sebs/                         runner package
│   ├── benchmark.py
│   ├── experiments/
│   └── faas/                     adapters: local, aws, azure, gcf
├── sebs.py                       CLI entry point
├── dockerfiles/
└── tools/
```

## Per-benchmark contract

```
benchmarks/<category>/<id>/
├── config.json                   runtime, memory, timeout, languages
├── input.py                      generates input payload by size: test|small|large
├── python/
│   ├── function.py               handler
│   └── requirements.txt
├── nodejs/                       (some benchmarks only)
│   └── function.js
└── README.md
```

## Deployments (for Wless: ALWAYS `local`)

| Deployment | Underlying | Wless usage |
|---|---|---|
| `local` | Docker + Minio | ✅ ONLY this one (local boundary) |
| `aws` | AWS Lambda | ❌ user-driven |
| `azure` | Azure Functions | ❌ user-driven |
| `gcf` | Google Cloud Functions | ❌ user-driven |

## Local deployment workflow (upstream)

```bash
# Pre-req: Docker running
cd ~/git/serverless-benchmarks
./sebs.py local start-minio                    # storage backend
./sebs.py local invoke 110.dynamic-html --config config/example.json
./sebs.py local stop-minio                     # cleanup
```

## Adapter pattern (SeBS → Wless)

### 1. Pin
```bash
cd ~/git/serverless-benchmarks
git rev-parse HEAD > /Users/emilio-imt/git/Wless/docs/research-notes/sb-pin-$(date +%Y-%m-%d)-<id>.md
```

### 2. Sanity (upstream)
```bash
./sebs.py local invoke 110.dynamic-html --config config/example.json
```

### 3. Wrap as Wless variant
`Acmeair_variants/sb_<id>/`:
- `<langEntry>/function.py` (or `.js`) — copy + thin Wless adapter
- `pom.xml` (only if wrapping Java) — usually not, since SeBS is Python-first
- `lqnmodel_<id>.lqn.py` — skeleton: 1 task per function, 1 entry
- `clientEntry/SimpleWorkload.py` — Locust pointing at local SeBS endpoint or invocation loop
- `SB_ADAPTATION.md` — pinned SHA, deviations, sanity numbers

### 4. Demand calibration
- 10 SeBS invocations (seed=42) → mean `time` → pre-populate `optSol.csv`
- Then `/calibrate-demands sb_<id>` to refine

### 5. Workload generator
- HTTP-style (110, 120, 130): Locust against the local SeBS HTTP endpoint
- Event-style (210 thumbnailer, etc.): Python driver looping `sebs.py local invoke`

## Recommended starting benchmarks

| ID | Name | Why useful for Wless |
|---|---|---|
| `110.dynamic-html` | Template render | Pure CPU, clean LQN |
| `120.uploader` | Upload + storage | I/O + CPU → multi-station LQN |
| `210.thumbnailer` | Image resize | CPU-heavy, deterministic |
| `311.compression` | Stream compression | CPU-bound, easy demand estimation |
| `501.graph-pagerank` | Graph algorithm | Memory-heavy, concurrency cliff |

Start with `110.dynamic-html` (simplest HTTP, no storage).

## Common issues (and fixes)

| Issue | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: docker` | SeBS deps not installed | `pip install -r ~/git/serverless-benchmarks/requirements.txt` |
| Docker daemon down | `local` needs Docker | `open -a Docker` (macOS), wait for ready |
| Storage backend missing | `local` needs Minio | `./sebs.py local start-minio` |
| Cold-start inconsistency | Wless wants steady-state | Use `--warm-runs N`, report median |
| Different metric units | SeBS reports `time` in seconds; Wless `results.csv` in ms | Convert in adapter |

## Wless results.csv schema mapping

| SeBS field | Wless results.csv column |
|---|---|
| `time` (s) | `p50_ms` (×1000) and quantile fields |
| `is_cold` (bool) | (drop or add as separate column) |
| `memory_consumed` | (drop or add as `mem_mb`) |
| `compute_time` | `billable_s` (Wless equivalent) |

## Constraints

- NEVER modify `~/git/serverless-benchmarks/benchmarks/` — always wrap in `Acmeair_variants/sb_*`
- ALWAYS pin SHA in `docs/research-notes/`
- NEVER run SeBS `aws`/`azure`/`gcf` — local only (DENY-listed in settings)
- DEFER LQN refinement to `lqn-model-expert`
- DEFER Locust integration to `locust-workload-expert`
