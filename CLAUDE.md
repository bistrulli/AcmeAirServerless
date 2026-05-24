# WasteLess (Wless) — Project-level Claude instructions

This file is the entry point for Claude Code when working in this repository. It encodes goal, conventions, agent inventory, and workflow for Wless-specific work.

---

## 1. Project goal

**WasteLess (Wless)** is an **Optimal Resource Provisioner for second-generation serverless applications**. Given a serverless function (originally targeted at Google Cloud Run, now generalized to local Maven-based deployments and to the SPCL `serverless-benchmarks` suite), Wless computes the **optimal concurrency / thread-pool / vCPU allocation** that minimizes billable-time cost subject to a P95 latency SLA.

**Core ideas**:
- Build a **Layered Queueing Network (LQN)** model of the application from observation traces (Prometheus span metrics or generated workload).
- Convert the LQN into a **Mean-Field / Markov-chain fluid model** (MPP4Lqn) and solve it (ODE integration).
- Use the analytical model to predict latency/throughput at varying concurrency and pick the optimum.
- Compare against baselines: **no-concurrency**, **GCR-default (80)**, **ProPack** (empirical Pareto cost-latency), and now **SPCL serverless-benchmarks** baseline runs.

## 2. Novelty (research positioning)

1. **Model-Driven Engineering + LQN**: closed-form thread-pool sizing for serverless functions.
2. **Local-first observation-based modelling** (journal extension, in `wless_local_model_brainstorm.md`): per-function model built from Prometheus span metrics instead of hand-crafted global LQN.
3. **Portability across deployment targets**: same provisioner logic now works on local Maven serverless functions and on SPCL serverless-benchmarks workloads.

**Comparison baselines**: GCR default, no-concurrency, ProPack (Pareto), SPCL serverless-benchmarks default config.

## 3. Pipeline overview

```
serverless-function source (Java/Maven or Python)
   ↓ (local deploy via maven OR sb-runner)
deployed function instance + Locust workload generator
   ↓ (observe)
trace data (response times, billable time, span metrics)
   ↓ (estimeDemands.py per function)
LQN demand vector  →  MPP4Lqn.Lqn2MPP  →  ODE system
   ↓ (solve)
predicted (concurrency → latency, billable) curve
   ↓ (optimize)
optimal concurrency vector → deploy.sh / update.sh
   ↓ (validate)
Locust workload re-run → results.csv → plot/*.m → figures/*.pdf
```

## 4. Agentic pipeline (Claude Code)

Entry point: `/triage <task>` → `/research <topic>` (if needed) → `/plan <task>` → `/iterate plan/<slug>.md` with Codex cross-review (max 5 iterations) and BS-check pre-commit. For deployment/data/replot changes there are pre-flight gates (`/audit-deploy`, `/audit-data`, `/replot`).

**Important boundary**: The agent develops and **unit-tests locally** (Python + Maven). It does NOT execute multi-variant Google Cloud Run experiments — those remain the user's responsibility. The agent orchestrates code, validates artifacts, and reports.

See `.claude/commands/` for the full command catalog and `.claude/agents/` for specialist roles.

## 5. Sub-agents inventory (21 total)

### Universal (10)
- `autonomous-orchestrator` — 5-iteration bounded autonomous loop
- `pipeline-orchestrator` — interactive task-by-task orchestration with approval gates
- `bs-detector` — LLM anti-pattern auditor (8 categories, last is Wless-specific)
- `code-reviewer` — pre-merge quality/security/perf review
- `test-engineer` — pytest + JUnit (Maven) design (unit, property, sanity vs analytical)
- `documentation-writer` — README, CLAUDE.md, REPORT.md, paper sections
- `github-issue-manager` — CRUD on GitHub Issues with canonical labels
- `codex-cross-reviewer` — cross-LLM consensus via `codex-cli` (max 5 iter)
- `web-researcher` — arXiv / Semantic Scholar / GitHub deep read with citation verification
- `paper-replicator` — replicates baselines (ProPack, GCR default, SPCL-sb default) for benchmarking

### Wless-domain (11)
- `wless-experiment-runner` — orchestrates LOCAL experiments (maven deploy + Locust + extract) on the developer machine
- `maven-serverless-expert` — Java/Maven serverless function authoring, packaging, local deploy, JUnit
- `server-functions-expert` — traditional long-running server functions (Spring Boot, Tomcat, Quarkus): wiring, pooling, JVM tuning
- `spcl-benchmarks-expert` — deep knowledge of github.com/spcl/serverless-benchmarks: structure, runner, deployments, configs
- `lqn-model-expert` — LQN theory (Layered Queueing Networks), MPP4Lqn internals, demand estimation, DiffLQN solver
- `markov-chain-expert` — discrete/continuous-time Markov chains, mean-field / fluid approximation, ODE derivation, stationary analysis
- `python-experiment-expert` — `runexp.py`, `extractExpData.py`, ProPack glue, JSON/CSV processing
- `matlab-plot-expert` — `plot/*.m`, parametric plot regeneration, PDF/PNG export
- `locust-workload-expert` — `SimpleWorkload.py`, Locust patterns, distribution generation, metrics export
- `propack-optimizer-expert` — `ProPack/propack.py`, scipy.optimize, Pareto curve fitting
- `local-deploy-expert` — local maven `package` + `mvn spring-boot:run` / `mvn quarkus:dev` lifecycle; port management; teardown

## 6. Skills inventory (12 total)

### Universal (4)
- `python-pipeline` — project conventions, venv, type hints, pytest, reproducibility
- `github-issues-workflow` — canonical labels, commit refs, fallback markdown-only
- `cross-llm-review` — Claude ↔ Codex consensus protocol
- `web-research-sources` — verified academic source catalog (arXiv, Semantic Scholar, etc.)

### Wless domain (8)
- `maven-serverless-patterns` — pom.xml archetypes for serverless (quarkus, micronaut, spring-cloud-function), local run, JUnit
- `lqn-modeling-reference` — verified LQN definitions, MPP4Lqn entity catalog, demand estimation formulae
- `markov-chain-reference` — CTMC / DTMC formulae, mean-field convergence, ODE derivation from population processes
- `matlab-plot-patterns` — parametric plot templates, color palettes, paper-ready PDF export
- `locust-workload-reference` — load profiles, exponential / heavy-tail arrivals, custom metrics CSV
- `propack-optimization-reference` — Pareto/multi-objective formulation, scipy.optimize idioms
- `wless-experiments-catalog` — `Acmeair_variants/` map, scenario taxonomy (defconc, noconc, wlessconc, propackconc)
- `spcl-serverless-benchmarks-reference` — SPCL sb structure, runner, deployments (local + AWS/Azure/GCF), benchmark catalog

## 7. Commands inventory (16 total)

### Universal (10)
- `/triage <task>` — classify task, recommend next command
- `/plan <task>` — produce reviewed plan with parallel expert consultation + Codex cross-review
- `/iterate plan/<file>` — autonomous bounded loop (max 5 iterations)
- `/orchestrate plan/<file>` — interactive task-by-task execution
- `/auto <task>` — small/medium task without formal plan
- `/research <topic>` — deep web research → `docs/research-notes/`
- `/document <target>` — generate / refresh documentation
- `/bs-check [scope]` — run BS-detector on diff / last commit / file
- `/cross-review <artifact>` — Codex consensus loop
- `/issue <subcommand>` — GitHub Issues CRUD (init-labels, create-plan, ...)

### Wless-domain (6)
- `/wless-bench [variant-range]` — run local maven benchmark subset with retry/parallelism; agent never executes GCR
- `/audit-deploy [variant]` — pre-flight maven build, JVM check, port availability, deploy.sh sanity
- `/audit-data [variant]` — validate CSV / response-time files / LQN demands before plot pipeline
- `/replot [figure]` — regenerate Matlab plot from CSV with data validation
- `/calibrate-demands [variant]` — batched estimeDemands run with sanity checks (demands > 0, no NaN)
- `/sb-adapt [benchmark]` — adapt SPCL serverless-benchmarks scenario into the Wless pipeline (wraps function + emits LQN model skeleton + workload)

## 8. Conventions

### Code style (Python)
- Source: top-level scripts (`runexp.py`, `extractExpData.py`) and module dirs (`MPP4Lqn/`, `ProPack/`)
- Use `python3` directly (no venv assumed; deps in `requirements.txt`)
- Type hints on **new** code (existing code is type-hint-free; do not retrofit blindly)
- Errors: explicit `raise` with informative message — never silent `except Exception: pass`
- Subprocess: always list-form, never shell=True with user input
- Seeds: any use of `numpy.random` MUST take a seed parameter for reproducibility

### Code style (Java / Maven serverless)
- Source: `Acmeair_variants/Acmeair_*/<MSname>Entry/` (one Maven module per microservice)
- JDK 17+ (LTS), Maven 3.9+
- Quarkus / Spring Cloud Function / Micronaut as serverless container (per variant)
- JUnit 5 (`jupiter`) for unit tests; AssertJ for fluent assertions
- Logging: SLF4J + Logback; never `System.out.println` in production code
- Local deploy: `mvn package` then `mvn quarkus:dev` (or `java -jar target/*.jar`); NEVER `gcloud` from the agent

### Matlab style
- Source: `plot/*.m`
- Parametric over scenario list (no hard-coded baselines); read CSV path from `config.json` co-located with run dir
- Save PDF (`exportgraphics`) AND PNG (`saveas`) for paper + slides

### LQN / model style
- LQN sources: `Acmeair_variants/Acmeair_*/lqnmodel_*.lqn.py` (Python description) — never hand-edit generated `model.lqn`
- Demand estimation: `estimeDemands.py` per variant; output `optSol.csv`
- ALWAYS validate `demands > 0` and `no NaN` before passing to solver

### Commit messages
- Format: `<scope>: <imperative summary>` (e.g., `lqn: enforce demand>0 in estimeDemands`)
- Reference issues with `Refs #N` or `Fixes #N`
- Co-Authored-By tag added by tooling (do not hand-write)

### Reproducibility (local experiments)
- Output directory: `results/<scenario>_<run_id>/` with `run_id = YYYY-MM-DD_HH-MM-SS`
- Required artifacts: `REPORT.md`, `results.csv`, `config.json`, `HASHES.txt` (SHA256 of inputs)
- Seed propagation: pass `--seed N` through and log it in `config.json`

## 9. GitHub repository

- Remote: configured via `git remote get-url origin`
- Labels: initialize via `/issue init-labels` (canonical set: type:plan/subtask/blocker/research, iter:1..5, status:in-review/blocked, agent:<name>, area:lqn|maven|matlab|sb|propack|workload)
- Issue tracking: enabled via `github-issue-manager`. If `gh auth` fails, system falls back to markdown-only tracking in `plan/`.

## 10. Risk register

| ID | Risk | Mitigation |
|----|------|-----------|
| R1 | Agent attempts to deploy to GCR (cost/blast radius) | `/wless-bench` and all commands restrict to `mvn` + `localhost`; `bs-detector` CAT-8 flags any `gcloud` invocation |
| R2 | LQN solver gets NaN/Inf demands | `/calibrate-demands` validates `demands > 0`, `no NaN`; `lqn-model-expert` audits |
| R3 | Local port collision during maven serverless run | `local-deploy-expert` enforces port discovery + teardown on abort |
| R4 | Matlab plot regen produces wrong figure (silent baseline change) | `/replot` requires `--expect-scenarios` flag matching the CSV header |
| R5 | Hallucinated paper citations | `web-researcher` requires DOI/arXiv ID verification |
| R6 | SPCL sb adapter drifts from upstream | `spcl-benchmarks-expert` pins git SHA and emits compatibility note |
| R7 | Markov-chain / mean-field claim without reference | `markov-chain-expert` cites Kurtz '70 / Le Boudec / Benaïm-Le Boudec by DOI |

## 11. Modes of work (explicit)

- **One decision at a time** — present options with pro/contro and wait for user choice
- **Test-driven** — sanity check vs analytical ground truth (M/M/1, M/M/c, single-class closed network) before claiming success
- **Epistemic honesty** — say "I don't know" or "verify this" rather than confabulate metrics or citations
- **Real brainstorming** — disagree if you see a flaw, surface alternatives, do not blindly comply
- **Local-only execution** — never invoke `gcloud`, `aws`, `az` from any agent or command

## 12. Quick-start workflow examples

### A. Bug fix (small)
```
/triage "Fix off-by-one in extractExpData P95 calculation"
  → categoria: small
/auto "Fix off-by-one in extractExpData P95 calculation"
```

### B. New feature (medium-large)
```
/triage "Add SPCL '110.dynamic-html' benchmark to Wless pipeline"
  → categoria: medium, sb-touching
/research "SPCL serverless-benchmarks 110.dynamic-html structure"
/plan "Adapt 110.dynamic-html for Wless"
  → plan/2026-MM-DD-sb-dynamic-html.md (+ Codex cross-review)
/iterate plan/2026-MM-DD-sb-dynamic-html.md
```

### C. Maven serverless change
```
/triage "Migrate MSauthEntry from Spring to Quarkus"
  → categoria: large, maven-touching
/audit-deploy MSauthEntry             (pre-flight)
/plan "Migrate MSauthEntry to Quarkus"
/iterate plan/2026-MM-DD-quarkus-auth.md
/audit-deploy MSauthEntry             (regression)
```

### D. Plot regeneration
```
/audit-data Acmeair_0
/replot overall --expect-scenarios defconc,noconc,wlessconc,propackconc
```

### E. LQN demand recalibration
```
/calibrate-demands Acmeair_0..Acmeair_5
```

---

_Last updated: 2026-05-24._
