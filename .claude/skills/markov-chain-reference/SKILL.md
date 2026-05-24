---
name: markov-chain-reference
description: Verified Markov chain reference — DTMC/CTMC definitions, mean-field/fluid approximation, Kurtz's theorem, Benaïm-Le Boudec interaction models, ODE derivation from population processes, stiffness-aware solver hygiene. Use when deriving or auditing Lqn2MPP transformations.
---

# Markov chain reference (Wless)

## DTMC — discrete-time Markov chain

- State space `S` (finite or countable)
- Transition matrix `P` with `P[i,j] = Pr(X_{n+1}=j | X_n=i)`, rows sum to 1
- Stationary distribution `π`: `π = π P`, `Σπ = 1`
- Ergodicity ⇒ unique `π`
- **Reference**: Norris, *Markov Chains* (Cambridge UP, 1997), ISBN 978-0-521-63396-3

## CTMC — continuous-time Markov chain

- Generator matrix `Q`: `Q[i,j] ≥ 0` (i≠j), row sums = 0
- Forward Kolmogorov: `dp/dt = p Q`
- Stationary: `π Q = 0`
- Birth-death chain → M/M/1, M/M/c (Wless's most common simplification)

## Mean-field / fluid approximation

- State = empirical distribution over `N` interacting agents (here: requests in entries)
- Transitions per agent depend on the empirical distribution
- As `N → ∞`, distribution converges to deterministic limit governed by an ODE

### Kurtz (1970) — pure-jump Markov ODE limit

`X_N(t) / N → x(t)` uniformly on compact intervals, where `x(t)` solves `dx/dt = F(x)` and `F` is the mean drift.

**Citation**: Kurtz, T.G. (1970). "Solutions of ordinary differential equations as limits of pure jump Markov processes." *J. Appl. Prob.* 7(1), 49–58. **DOI:10.2307/3212147**

### Benaïm & Le Boudec (2008) — interacting agents

Extension to interacting agents with finite local state. Convergence to ODE if drift is Lipschitz and noise scales as `1/√N`.

**Citation**: Benaïm, M., Le Boudec, J.-Y. (2008). "A class of mean field interaction models for computer and communication systems." *Performance Evaluation* 65(11–12), 823–838. **DOI:10.1016/j.peva.2008.03.005**

## Population process → ODE recipe

For an LQN with population `N`:

1. State = `x = (x_1, ..., x_K)` where `x_i` = fraction at position `i`, `Σ x_i = 1`
2. For each transition type τ with rate `r_τ(x)` and delta `Δ_τ`:
   - Drift contribution: `r_τ(x) * Δ_τ`
3. `dx/dt = Σ_τ r_τ(x) * Δ_τ`
4. Service: rate = `(1 / demand) * occupancy` (FCFS) or `mult * (1/demand)` (parallel)

`MPP4Lqn/Lqn2MPP/Lqn2MPP.py` implements this for the Wless LQN entity model.

## ODE solver hygiene (`scipy.integrate.solve_ivp`)

```python
from scipy.integrate import solve_ivp
import numpy as np

sol = solve_ivp(
    fun=drift,                # callable (t, x) → dx/dt
    t_span=(0, T),
    y0=x0,
    method='Radau',           # stiff-safe default; alternatives: 'BDF', 'LSODA'
    rtol=1e-8, atol=1e-10,
    dense_output=False,
    max_step=1.0,
)

assert sol.success, sol.message
assert np.all(np.isfinite(sol.y))
```

### Convergence to fixed point

```python
T_long = T * 10
x_inf = sol.y[:, -1]
drift_at_T = drift(T_long, x_inf)
assert np.linalg.norm(drift_at_T) < 1e-6, "did not reach stationary"
```

If not converging: integrate longer, check Jacobian sign, look for sign error in transition encoding.

## Sanity tests (mandatory)

| Setup | Analytical | Fluid ODE fixed point |
|---|---|---|
| M/M/1 (λ=0.5, μ=1) | E[N] = ρ/(1−ρ) = 1 | x_in_system → 1 |
| M/M/c (c=2, λ=1.5, μ=1) | Erlang-C | converge |
| Closed N=10, single station D=1 | E[R] = 10 (saturated) | x_in_queue → 10 |
| Closed N=10, 2 stations equal | balanced (5,5) | x_1 = x_2 = 5 |

If a kernel change breaks one of these: STOP and escalate.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `solve_ivp` returns NaN | Demand = 0 → 1/demand = Inf | Validate demands > 0 upstream |
| Doesn't converge | Sign error in drift, or stiffness | Switch to `Radau`/`BDF`; check Jacobian sign |
| Oscillates | Stiff system with explicit method | Use `Radau` or `BDF` |
| Wrong fixed point | Missing transition or wrong rate | Re-derive on small instance, compare with MVA |

## Constraints

- NEVER cite "converges by Kurtz" without checking Lipschitz + continuous drift
- ALWAYS assert `sol.success` and finiteness after `solve_ivp`
- ALWAYS provide an analytical sanity check on a small instance
- Use stiff-safe method (`Radau`, `BDF`) by default for closed networks
