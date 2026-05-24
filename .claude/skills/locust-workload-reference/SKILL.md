---
name: locust-workload-reference
description: Locust 2.x patterns for Wless workload generation — HttpUser class, wait_time distributions (exponential / constant / Pareto), per-user seeded RNG, custom RT file listener, CSV export. Use when editing SimpleWorkload.py.
---

# Locust workload reference (Wless)

## Locust 2.x essentials

- `HttpUser`: a virtual user that issues HTTP requests
- `@task(weight)`: a request method
- `wait_time`: think-time between tasks (callable or `constant_pacing(...)`)
- `--headless`: run without web UI
- `--csv`: write per-endpoint and time-series CSVs

## Standard wait-time distributions

| Distribution | Use case | Code |
|---|---|---|
| Exponential (mean=1s) | Closed-network LQN baseline | `wait_time = lambda self: random.expovariate(1.0)` |
| Constant pacing (1 req/s) | Open-network λ comparison | `from locust import constant_pacing; wait_time = constant_pacing(1.0)` |
| Pareto (α=1.5) | Heavy-tailed SLA stress | `wait_time = lambda self: max(0.05, np.random.pareto(1.5)+0.1)` |
| Lognormal | Real-world web | `wait_time = lambda self: np.random.lognormal(0, 0.5)` |

## Per-user seeded RNG (CRITICAL for reproducibility)

```python
import os, random, time
from locust import HttpUser, task, events

SEED = int(os.environ.get("WLESS_SEED", "42"))
RT_FILE = os.environ.get("WLESS_RT_FILE", "rt.txt")

class AcmeairUser(HttpUser):
    def on_start(self):
        self._rng = random.Random(SEED + id(self))   # per-user determinism

    wait_time = lambda self: self._rng.expovariate(1.0)

    @task(1)
    def auth(self):
        with self.client.get("/auth", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"HTTP {resp.status_code}")
```

## Custom RT file listener

```python
@events.request.add_listener
def _record_rt(request_type, name, response_time, response_length, exception, **kwargs):
    if exception is None:
        with open(RT_FILE, "a") as f:
            f.write(f"{time.time()},{name},{response_time:.3f}\n")
```

## Invocation

```bash
WLESS_SEED=42 \
WLESS_RT_FILE=results/wless-bench_${RUN_ID}/Acmeair_0/defconc/defconcrt.txt \
locust -f Acmeair_variants/Acmeair_0/clientEntry/SimpleWorkload.py \
       --headless \
       --users 50 --spawn-rate 5 --run-time 60s \
       --host http://localhost:8080 \
       --csv results/wless-bench_${RUN_ID}/Acmeair_0/defconc/loc
```

## CSV outputs

| File | Content |
|---|---|
| `loc_stats.csv` | Per-endpoint aggregate (median, P95, max, RPS) |
| `loc_stats_history.csv` | Time series (every 2s) |
| `loc_failures.csv` | Failures |
| `loc_exceptions.csv` | Python exceptions during run |
| `<scenario>rt.txt` (custom) | Per-request timestamp + RT — consumed by `extractExpData.py` |

## Profiles (presets)

```python
# Profile: warmup_then_steady
# 20s ramp-up, 60s steady, no further variation
def get_profile(name):
    return {
      "warmup_then_steady": ("--users", "50", "--spawn-rate", "2.5", "--run-time", "80s"),
      "burst":              ("--users", "200", "--spawn-rate", "50", "--run-time", "30s"),
      "soak":               ("--users", "50", "--spawn-rate", "5", "--run-time", "600s"),
    }[name]
```

## Tuning for local maven serverless

- Start small (`--users 10 --spawn-rate 2`); watch CPU
- If CPU >80% on locust+function: lower users or run on separate machine
- Locust + Quarkus + Locust on same machine = noisy results; document in REPORT.md
- Always include 30–60s warmup (Locust ramp + steady)

## Validation post-run

- `wc -l <scenario>rt.txt` > 0
- Mean RT from `<scenario>rt.txt` matches `loc_stats.csv` median (within 5%)
- No "Connection refused" in `loc_failures.csv`

## Constraints

- ALWAYS seed via `WLESS_SEED` env var (default 42)
- ALWAYS write custom RT file in addition to `--csv`
- NEVER use `time.sleep()` inside a `@task` — use `wait_time`
- NEVER share `random` module across users — use per-user `self._rng`
