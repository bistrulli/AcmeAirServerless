---
name: lqn-modeling-reference
description: Verified LQN (Layered Queueing Network) reference — entity model (processor, task, entry, activity, call), demand estimation formulae, MPP4Lqn package map, DiffLQN invocation. Use when authoring LQN models, debugging estimeDemands, or extending MPP4Lqn.
---

# LQN modeling reference (Wless)

## LQN entity model (cheat sheet)

| Entity | Role | Key attributes |
|---|---|---|
| **Processor** (`P`) | Physical CPU pool | `multiplicity` (cores) |
| **Task** (`T`) | Software server | `multiplicity` (threads), `scheduling` (FCFS/inf/ref) |
| **Entry** (`E`) | Named service of a task | `host-demand` (CPU time) |
| **Activity** (`A`) | Sub-step inside an entry | `demand`, optional `call` |
| **Call** | Between entries | sync (`->`) or async (`~>`) |

## Scheduling disciplines

| Code | Meaning | When |
|---|---|---|
| `fcfs` | First-come-first-served (queueing) | Default for software tasks |
| `inf` | Infinite-server (no contention) | Reference task or pure delay |
| `ref` | Reference task (closed-class population) | Locust users in Wless |

## Wless-specific mapping

```
Locust users (N=50)             →  Reference task  T_client, mult=50
clientEntry HTTP call            →  Call ->  to first MS entry
Maven serverless function (mult=k thread pool) → Task T_MSname, mult=k
Function entry method            →  Entry MSname (host-demand from estimeDemands)
Downstream HTTP / DB call        →  Call ->  to next task entry
```

## Demand estimation (`estimeDemands.py`)

For each observed entry `E`:

```
demand(E) = observed_RT(E) − Σ observed_RT(call_i)
              for each call_i from E to a downstream entry
```

### Validation (MANDATORY before passing to solver)

```python
assert all(d > 0 for d in demands.values()), \
    f"negative demand: {[(k,v) for k,v in demands.items() if v<=0]}"
assert all(np.isfinite(d) for d in demands.values()), "NaN/Inf in demands"
assert all(d < observed_total_rt[entry] for entry, d in demands.items()), \
    "demand exceeds observed RT (impossible)"
```

If any fails: trace is corrupt OR call graph is wrong OR warmup was insufficient. NEVER silently `nan_to_num`.

## MPP4Lqn package map

```
MPP4Lqn/
├── entity/
│   ├── Processor.py
│   ├── Task.py             ← multiplicity, scheduling
│   ├── Entry.py            ← host-demand
│   ├── Activity.py         ← demand + optional call
│   ├── Call.py             ← sync/async
│   └── Lqn.py              ← container + builder API
├── Lqn2MPP/
│   └── Lqn2MPP.py          ← LQN → ODE generator
├── transducers/            ← encoders/decoders LQN XML ↔ Python
└── solver/                 ← DiffLQN (Java) wrapper
```

## Python builder pattern (`lqnmodel_<N>.lqn.py`)

```python
from MPP4Lqn.entity import Lqn, Processor, Task, Entry, Activity, Call

lqn = Lqn()

proc_cpu = Processor("CPU", multiplicity=8)

t_client = Task("T_client", multiplicity=50, scheduling="ref", processor=proc_cpu)
t_auth   = Task("T_MSauth",  multiplicity=80, scheduling="fcfs", processor=proc_cpu)

e_client = Entry("clientEntry", host_demand=0.0, task=t_client)
e_auth   = Entry("MSauth",      host_demand=0.5, task=t_auth)

e_client.add_call(Call(target=e_auth, count=1, sync=True))

lqn.add(proc_cpu, t_client, t_auth, e_client, e_auth)
lqn.write("model.lqn")
```

`model.lqn` is GENERATED — never hand-edit.

## DiffLQN solver invocation

```bash
java -jar tools/DiffLQN.jar model.lqn --output optSol.csv
```

Outputs `(concurrency, throughput, RT, threads_opt)` per task.

## Sanity tests (use as test fixtures)

| Setup | Analytical | LQN solver |
|---|---|---|
| M/M/1: 1 task `inf` ref, 1 task fcfs mult=1, demand D, λ → fluid | E[R] = D/(1-ρ), ρ=λD | ±1% |
| M/M/c: c=2, demand D, λ | Erlang-C | ±2% |
| Closed N=1, tandem D1+D2 | E[R] = D1+D2 | ±1% |
| Bottleneck N→∞ | X → 1/max(D) | converge |

## Wless contribution: thread-pool sizing

```
For task T (entries E_1..E_k), closed pop N:
  for m in 1..N:
    solve LQN with T.multiplicity = m
    if RT(T) <= SLA:
      cost(m) = m * cpu_per_thread
      track smallest m with cost(m) minimal
  m* = wlessconc
```

`wlessconc` baseline vs `defconc=80`, `noconc=1`, `propackconc` (Pareto).

## Constraints

- NEVER hand-edit `model.lqn` (regenerate from `.lqn.py`)
- NEVER suppress `demand < 0` with `abs()` or `max(0, ...)`
- ALWAYS include time unit (ms vs s) in the builder
- Solver runtime grows with task × multiplicity space — limit for large variants
