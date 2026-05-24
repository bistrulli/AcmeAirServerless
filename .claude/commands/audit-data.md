---
description: Pre-flight gate for plot regeneration. Validates results.csv / response-time files / experiments.csv before invoking the plot pipeline. Detects missing scenarios, NaN/Inf, sample-size insufficiencies.
---

# /audit-data <variant-or-run-dir>

Invokes `python-experiment-expert` + `matlab-plot-expert`.

## Scope

- `<variant>` like `Acmeair_0` → audit raw `*rt.txt` files
- `<run-dir>` like `results/wless-bench_2026-05-24_14-32` → audit aggregated `results.csv`

## Phases (5)

### 1. File existence
- For raw mode: each scenario in `{defconc,noconc,wlessconc,propackconc}` must have `<scenario>rt.txt`
- For run-dir mode: `results.csv` must exist with expected columns
- 🔴 if missing

### 2. Schema check
- Required columns (results.csv): `variant, scenario, n_threads, n_concurrency, p50_ms, p95_ms, throughput_rps, billable_s`
- 🔴 if any required column absent

### 3. Value sanity
- No NaN/Inf in numeric columns
- `p50_ms <= p95_ms` (sanity)
- `throughput_rps > 0`
- `billable_s >= 0`
- 🔴 if violated

### 4. Sample size
- Per scenario: `count(rows) >= 10` (boxplot minimum)
- 🟡 if 5–9 rows (warn, still plottable)
- 🔴 if <5 rows

### 5. Scenario coverage
- All expected scenarios from `config.json` present?
- 🟡 if some scenarios missing (e.g., user ran subset)
- 🔴 if user requested `--expect-scenarios` in `/replot` and not all match

## Output

```markdown
# /audit-data report — results/wless-bench_2026-05-24_14-32

## File existence: 🟢
## Schema: 🟢
## Values: 🟢 (no NaN, no Inf, p50 < p95 for all rows)
## Sample size:
- defconc: 30 ✅
- noconc: 30 ✅
- wlessconc: 8 🟡 (low, warn)
- propackconc: 30 ✅

## Scenarios: 🟢 (4/4 expected)

## Overall: 🟡 (low sample for wlessconc)

## Recommendation
- Either rerun wlessconc with `/wless-bench Acmeair_0..Acmeair_X --scenarios wlessconc --users 50` to fill in samples,
- OR proceed with /replot accepting the small wlessconc box.
```

## When to invoke

- Before `/replot`
- As part of `/iterate` Phase 1 when plot/*.m touched

## Constraints

- NEVER suggest `nan_to_num` as a "fix" — find the root cause
- NEVER lower a 🔴 to 🟡 without explanation
