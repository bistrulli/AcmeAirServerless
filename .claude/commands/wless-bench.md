---
description: Run a LOCAL Wless benchmark over a subset of variants. Maven build + local serverless start + Locust workload + collect. NEVER deploys to GCR/AWS/Azure - that stays the user's responsibility. Produces results/wless-bench_<run-id>/ with results.csv, REPORT.md, HASHES.txt.
---

# /wless-bench [variant-range] [--scenarios <list>] [--parallel N] [--users U] [--duration D] [--seed S]

Invokes `wless-experiment-runner`.

## Args

| Arg | Default | Notes |
|---|---|---|
| `variant-range` | `Acmeair_0..Acmeair_2` | e.g., `Acmeair_0` or `Acmeair_0..Acmeair_5` or `Acmeair_0,Acmeair_3,Acmeair_7` or `sb_110.dynamic-html` |
| `--scenarios` | `defconc,noconc,wlessconc,propackconc` | Subset comma-separated |
| `--parallel` | `1` | Number of variants to run in parallel (each on its own port range) |
| `--users` | `50` | Locust virtual users |
| `--duration` | `60s` | Locust run time |
| `--seed` | `42` | Workload + ProPack seed |

## Protocol

### Phase 0 — Pre-flight
- Check JDK 17+ and Maven 3.9+
- For each variant: `/audit-deploy <variant>` (fast, ports + build)
- For LQN scenarios: `/calibrate-demands <variant>` if `optSol.csv` stale
- For SPCL sb variants: `spcl-benchmarks-expert` verifies pin

### Phase 1 — Setup
- `RUN_ID=$(date +%Y-%m-%d_%H-%M-%S)`
- `mkdir -p results/wless-bench_$RUN_ID/`
- Write `config.json` with all args + git SHA
- Initialize `experiments.csv`

### Phase 2 — Per-variant loop (sequential or `--parallel`)
For each variant:
1. Allocate port (base 8080 + 10*variant-index for parallel)
2. `mvn -pl <variant>/<entry> -am package -DskipTests=false`
3. For each scenario:
   - Skip-check via `experiments.csv` (idempotent)
   - Apply concurrency knob (`setDefConc` / `setNoConc` / `setWlessConc` / `setProPackConc`)
   - Start function: `java -jar target/*.jar --quarkus.http.port=$port &`
   - Wait ready (`/q/health` or `/actuator/health`, 60s timeout)
   - Run Locust with `--seed`, `--users`, `--duration`
   - Move `<scenario>rt.txt` to run dir
   - Atomic append to `experiments.csv`
4. **Teardown** (always, via `trap`)

### Phase 3 — Collect + report
- Invoke `python-experiment-expert` → `extractExpData.py` → `results.csv`
- Compute SHA256 of inputs → `HASHES.txt`
- Write `REPORT.md`:
  ```markdown
  # Wless local benchmark — <run_id>
  ## Setup: git SHA, JDK, Maven, seed
  ## Scenarios run: ...
  ## Per-variant summary (table P50/P95/billable/throughput)
  ## Sanity (vs M/M/c if applicable): ...
  ## Reproduce: <exact command>
  ```

### Phase 4 — User review
- Show `REPORT.md` head
- Recommend `/replot overall --run-dir results/wless-bench_$RUN_ID` (or run automatically if `--auto-plot`)

## Failure modes

| Mode | Action |
|---|---|
| Build failure | Retry once after `mvn clean`; mark variant FAILED |
| Start timeout | Retry once; mark FAILED |
| Locust connection refused | Wait 5s, retry up to 2x |
| OOM | Abort run, diagnostic in REPORT.md |
| Port leak | Force-kill via `lsof -ti :$port \| xargs kill -9` |

## Output

```
results/wless-bench_<run_id>/
├── REPORT.md
├── config.json
├── experiments.csv
├── HASHES.txt
├── results.csv
├── Acmeair_<N>/
│   └── <scenario>/{loc_stats.csv, <scenario>rt.txt, pids.txt, stdout.log, stderr.log}
```

## Constraints

- NEVER invoke `gcloud`/`aws`/`az`/`kubectl`/`helm`
- NEVER skip teardown (port leaks break next run)
- ALWAYS write atomic experiments.csv updates
- DEFAULT to `--parallel 1` unless machine has many cores
