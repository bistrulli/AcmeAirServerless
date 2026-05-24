---
name: propack-optimization-reference
description: ProPack optimizer reference - exponential RT model fit, linear cost model, weighted (cost, RT) Pareto objective, scipy.optimize.minimize idioms, sanity test catalog. Use when editing ProPack/propack.py or extending the optimizer.
---

# ProPack optimization reference (Wless)

## Model

ProPack fits a per-entry response-time model:
```
rt_model(c) = a * exp(α * c)            # response time vs concurrency
cost_model(c) = β * c                   # linear cost
```

Optimization (per entry):
```
minimize  w_rt * Δrt(c) + w_cost * Δcost(c)
s.t.      c ∈ [1, c_max]
where     Δrt(c)   = (rt_model(c) − rt_min) / (rt_max − rt_min)
          Δcost(c) = (cost_model(c) − cost_min) / (cost_max − cost_min)
```

Default weights: `w_rt = 0.5, w_cost = 0.5`.

## scipy idioms

### Fit
```python
from scipy.optimize import curve_fit
import numpy as np

def rt_model(c, a, alpha):
    return a * np.exp(alpha * c)

popt, pcov = curve_fit(rt_model, c_obs, rt_obs, p0=[1.0, 0.01], maxfev=10000)
a_hat, alpha_hat = popt
```

### Optimize
```python
from scipy.optimize import minimize

def objective(c, w_rt=0.5, w_cost=0.5):
    rt   = rt_model(c, a_hat, alpha_hat)
    cost = beta * c
    return w_rt * _normalize(rt, rt_range) + w_cost * _normalize(cost, cost_range)

res = minimize(
    objective,
    x0=[c_max / 2],
    bounds=[(1, c_max)],
    method='SLSQP',
    options={'maxiter': 200, 'ftol': 1e-8},
)
assert res.success, res.message
c_star = res.x[0]
```

### Constraints (e.g., RT ≤ SLA)
```python
constraints = [{'type': 'ineq', 'fun': lambda c: sla - rt_model(c, a_hat, alpha_hat)}]
res = minimize(..., constraints=constraints)
```

`method='SLSQP'` supports both bounds and constraints. `Powell` does not — don't use it if constraints are present.

## Determinism

- `minimize` is deterministic given `(x0, bounds, method)`
- `curve_fit` deterministic given `p0`
- If `Nelder-Mead` with `adaptive=True`: seed via `np.random.default_rng(seed)`
- ALWAYS log `(method, x0, bounds, seed)` in CSV header

## Sanity tests (catalog)

| Case | Expected | Tolerance |
|---|---|---|
| Linear cost + flat RT (α=0) | `c* = 1` (cost minimum) | exact |
| Exp RT, flat cost (β=0) | `c* = 1` (RT minimum) | exact |
| `w_rt=1, w_cost=0` | `c* = argmin rt(c) ≈ 1` | exact |
| `w_rt=0, w_cost=1` | `c* = 1` (linear cost) | exact |
| Symmetric weights, exp RT vs linear cost | interior `c* ∈ (1, c_max)` | check existence |

## Output schema (`ProPackSol.csv`)

```csv
# method=SLSQP, w_rt=0.5, w_cost=0.5, alpha=0.0123, a=0.45, seed=42
entry, c_star, rt_at_c_star_ms, cost_at_c_star
MSauthEntry, 12, 145.3, 12
MSbookflightsEntry, 18, 210.7, 18
```

Header comment lines (`#`) are MANDATORY — they let downstream readers reproduce.

## Extending ProPack

### New objective (e.g., P95 instead of mean)
- Add `rt_p95_model(c, ...)` from quantile of observed RT distribution
- Replace `rt_model` in `objective`
- Add sanity test on degenerate cases

### Multi-entry coupling
Currently per-entry independent. To couple (shared CPU budget):
- Vector `c = [c_1, ..., c_k]`
- Add total-budget constraint: `Σ c_i ≤ budget`
- Use `method='SLSQP'` with `constraints=[{type:'ineq', fun: lambda c: budget - sum(c)}]`

### Curve-fit failure recovery
```python
try:
    popt, pcov = curve_fit(rt_model, c_obs, rt_obs, p0=[1.0, 0.01], maxfev=10000)
except RuntimeError as e:
    raise RuntimeError(f"curve_fit failed for entry {entry}: {e}") from e
```
NEVER fall back to median or hand-fit silently — escalate.

## Constraints

- NEVER drop `maxfev` from `curve_fit` (it can fail silently with too few iterations)
- NEVER use `Powell` with constraints
- ALWAYS assert `res.success` and finiteness
- ALWAYS log optimizer config in CSV header (`# method=..., ...`)
