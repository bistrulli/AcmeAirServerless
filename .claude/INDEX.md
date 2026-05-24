# Wless Claude Code orchestration — INDEX

Quick reference for the agentic pipeline installed in this repo.

---

## Quick start

```
/triage "<your task>"            → classifies + recommends next command
   ↓
/research "<topic>"              → (if literature review needed)
   ↓
/plan "<task>"                   → produces plan/<slug>.md with Codex cross-review
   ↓
/iterate plan/<slug>.md          → autonomous 5-iter loop (or /orchestrate for interactive)
   ↓ (user approves)
git push + gh pr create
```

**Boundary**: agent does LOCAL dev + unit tests (Python + Maven). User runs GCR / SPCL multi-variant experiments.

---

## Inventory

### Agents (21 total)

#### Universal (10)
| Agent | Role |
|---|---|
| [autonomous-orchestrator](agents/autonomous-orchestrator.md) | 5-iter bounded autonomous loop |
| [pipeline-orchestrator](agents/pipeline-orchestrator.md) | Interactive task-by-task execution |
| [bs-detector](agents/bs-detector.md) | LLM anti-pattern auditor (CAT-1..CAT-8) |
| [code-reviewer](agents/code-reviewer.md) | Pre-merge quality/security/perf review |
| [test-engineer](agents/test-engineer.md) | pytest + JUnit design |
| [documentation-writer](agents/documentation-writer.md) | README/CLAUDE.md/REPORT.md/paper |
| [github-issue-manager](agents/github-issue-manager.md) | GitHub Issues CRUD |
| [codex-cross-reviewer](agents/codex-cross-reviewer.md) | Cross-LLM consensus loop |
| [web-researcher](agents/web-researcher.md) | arXiv / Semantic Scholar / GitHub |
| [paper-replicator](agents/paper-replicator.md) | GCR/ProPack/SPCL-sb baselines |

#### Wless-specific (11)
| Agent | Role |
|---|---|
| [wless-experiment-runner](agents/wless-experiment-runner.md) | Local maven orchestrator |
| [maven-serverless-expert](agents/maven-serverless-expert.md) | Quarkus/Spring/Micronaut serverless |
| [server-functions-expert](agents/server-functions-expert.md) | Spring Boot / Tomcat / Quarkus server |
| [spcl-benchmarks-expert](agents/spcl-benchmarks-expert.md) | github.com/spcl/serverless-benchmarks |
| [lqn-model-expert](agents/lqn-model-expert.md) | LQN + MPP4Lqn + DiffLQN |
| [markov-chain-expert](agents/markov-chain-expert.md) | CTMC/DTMC + mean-field/fluid |
| [python-experiment-expert](agents/python-experiment-expert.md) | runexp / extractExpData |
| [matlab-plot-expert](agents/matlab-plot-expert.md) | plot/*.m |
| [locust-workload-expert](agents/locust-workload-expert.md) | Locust + SimpleWorkload |
| [propack-optimizer-expert](agents/propack-optimizer-expert.md) | ProPack + scipy.optimize |
| [local-deploy-expert](agents/local-deploy-expert.md) | mvn lifecycle + port mgmt |

### Skills (12 total)

#### Universal (4)
- [python-pipeline](skills/python-pipeline/SKILL.md)
- [github-issues-workflow](skills/github-issues-workflow/SKILL.md)
- [cross-llm-review](skills/cross-llm-review/SKILL.md)
- [web-research-sources](skills/web-research-sources/SKILL.md)

#### Wless domain (8)
- [maven-serverless-patterns](skills/maven-serverless-patterns/SKILL.md)
- [lqn-modeling-reference](skills/lqn-modeling-reference/SKILL.md)
- [markov-chain-reference](skills/markov-chain-reference/SKILL.md)
- [matlab-plot-patterns](skills/matlab-plot-patterns/SKILL.md)
- [locust-workload-reference](skills/locust-workload-reference/SKILL.md)
- [propack-optimization-reference](skills/propack-optimization-reference/SKILL.md)
- [wless-experiments-catalog](skills/wless-experiments-catalog/SKILL.md)
- [spcl-serverless-benchmarks-reference](skills/spcl-serverless-benchmarks-reference/SKILL.md)

### Commands (16 total)

#### Universal (10)
- [/triage](commands/triage.md) — classify a task
- [/plan](commands/plan.md) — produce reviewed plan
- [/iterate](commands/iterate.md) — autonomous bounded loop
- [/orchestrate](commands/orchestrate.md) — interactive execution
- [/auto](commands/auto.md) — quick path for small tasks
- [/research](commands/research.md) — literature review
- [/document](commands/document.md) — generate / refresh docs
- [/bs-check](commands/bs-check.md) — anti-pattern audit
- [/cross-review](commands/cross-review.md) — Codex consensus loop
- [/issue](commands/issue.md) — GitHub Issues CRUD

#### Wless-specific (6)
- [/wless-bench](commands/wless-bench.md) — local maven benchmark subset
- [/audit-deploy](commands/audit-deploy.md) — maven + port pre-flight
- [/audit-data](commands/audit-data.md) — CSV / RT-file validation
- [/replot](commands/replot.md) — Matlab plot regen with validation
- [/calibrate-demands](commands/calibrate-demands.md) — batched estimeDemands
- [/sb-adapt](commands/sb-adapt.md) — SPCL sb scenario → Wless adapter

---

## Setup checklist (one-time)

- [x] `.claude/` directory created
- [x] `CLAUDE.md` written (project-level)
- [x] `.claude/settings.json` written (permissions + hook)
- [ ] GitHub labels initialized: run `/issue init-labels`
- [ ] JDK 17+ + Maven 3.9+ installed locally
- [ ] Octave or Matlab CLI available (`octave --no-gui` or `matlab -batch`)
- [ ] Codex CLI installed (`codex --help`) — optional; pipeline degrades gracefully if absent
- [ ] `gh` CLI authenticated (`gh auth status`)
- [ ] SPCL serverless-benchmarks cloned locally (referenced by `spcl-benchmarks-expert`)

---

_Generated: 2026-05-24._
