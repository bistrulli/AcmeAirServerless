---
description: Run estimeDemands.py for a variant range with sanity checks. Validates demand > 0, no NaN/Inf, total < observed RT. Writes calibrated optSol.csv per variant.
---

# /calibrate-demands <variant-range> [--source <log-dir>] [--seed S]

Invokes `lqn-model-expert`.

## Args

| Arg | Default | Notes |
|---|---|---|
| `<variant-range>` | (required) | e.g., `Acmeair_0..Acmeair_5` |
| `--source` | `Acmeair_variants/<v>/logs/` | Where the RT logs live |
| `--seed` | `42` | If solver uses any stochastic step |

## Protocol

### 1. Pre-check (per variant)
- Logs exist? `ls <source>/*.csv | wc -l` > 0
- 🔴 if no logs

### 2. Run estimation
For each variant:
```bash
cd Acmeair_variants/<v>/lqnmodel_*.lqn
python ../../../MPP4Lqn/estimeDemands.py --source ../logs --seed $SEED
```
- Outputs `optSol.csv`

### 3. Sanity checks (per variant)
Validate `optSol.csv`:
- All `demand > 0` (negative = wrong call counts)
- No NaN / Inf
- For each entry: `demand < observed_mean_rt` (host demand can't exceed total)
- Total demand chain ≈ observed end-to-end RT (within 10%)

### 4. Report

```markdown
# /calibrate-demands report

## Acmeair_0: 🟢
- 6 entries calibrated
- Min demand: 0.012ms, Max: 4.5ms
- Sanity (sum vs end-to-end): 5.7 ms vs 6.1 ms observed (94%)

## Acmeair_5: 🔴
- MSbookflightsEntry: demand = -0.3 ms (NEGATIVE)
- Root cause: clientEntry call count = 0 but downstream RTs sum > entry RT
- Action: check trace integrity in logs/clientEntry.csv

## Summary
- ✅ 4 variants calibrated
- 🔴 1 variant failed (Acmeair_5)
```

### 5. (Optional) Trigger LQN solve
If `--solve` flag: also invoke DiffLQN or `Lqn2MPP` to produce predictions per concurrency.

## Constraints

- NEVER mask negative demands with `abs()` or `max(0, …)` — escalate
- NEVER silently `nan_to_num`
- ALWAYS validate against observed end-to-end RT
- DEFER LQN object model questions to `lqn-model-expert`
- DEFER ODE solver questions to `markov-chain-expert`
