---
description: Execute a Wless plan autonomously via a bounded 5-iteration loop. Coordinates specialists, runs BS-check + tests each iteration, integrates Codex cross-review, manages GitHub issue lifecycle. Final commit/push requires explicit user approval. Local-only (no GCR/AWS/Azure).
---

# /iterate plan/<slug>.md

Drives a reviewed plan to completion with minimal user intervention.

## Protocol (5 phases)

### Phase 0 — Read context
```bash
cat plan/<slug>.md
git status
gh issue list --label "type:plan" --state open
gh issue list --label "iter:1" --state open
codex --help 2>/dev/null || echo "DEGRADE: claude-self-review"
```

### Phase 1 — Setup
1. Branch: `git checkout -b feat/<slug>`
2. Run-id: `RUN_ID=$(date +%Y-%m-%d_%H-%M-%S)`
3. Output dir: `mkdir -p results/orchestrate_$RUN_ID/`
4. Pre-flight gates (based on plan scope):
   - If `pom.xml` / `Acmeair_variants/*/Entry/` touched → `/audit-deploy <variant>`
   - If `plot/*.m` / figures touched → `/audit-data <variant>`
   - If LQN demand files touched → `/calibrate-demands <variant>`
   - If SPCL sb wrapping touched → `spcl-benchmarks-expert` pin/sanity
   - If gate fails (🔴): STOP, escalate

### Phase 2 — Main loop (k = 1..5)

Invoke `autonomous-orchestrator` with the plan.

#### A. COLLECT
Work queue from issues `iter:k` (or plan checkboxes).

#### B. EXECUTE per sub-task
- Invoke specialist (`agent:*` label)
- Run `bs-detector` on diff
  - 🔴 → revert; requeue
  - 🟡 → log; continue
  - 🟢 → proceed
- Run tests:
  - Python: `pytest tests/<module>/ -q`
  - Maven: `mvn -pl <module> test -q`
  - Test failure → revert; requeue
- Stage + commit with `Refs #<subtask-issue>` (no push)

#### C. REVIEW
- Bundle diff: `results/orchestrate_$RUN_ID/iter_${k}_artifact.md`
- `codex-cross-reviewer` with `checklist=code`, max_iter=5
- Verdict APPROVE → continue; APPROVE_WITH_CHANGES → apply; REJECT → revert

#### D. RECONCILE
- Move open subtasks `iter:k` → `iter:k+1`
- Close completed: `gh issue close <id> --comment "Done in <SHA>"`
- Write `iter_${k}_summary.md`

#### E. GATE
- All closed → SUCCESS
- 3 consecutive REJECT → FAILURE
- k = 5 → MAX_ITER_REACHED

### Phase 3 — Finalize
1. `bs-detector` full branch diff
2. Final `codex-cross-reviewer` cumulative artifact
3. Tests: `pytest -v` + `mvn test -q` on touched modules
4. Re-run pre-flight gates regression
5. Write `final_report.md`

### Phase 4 — USER APPROVAL
Show:
- Final report summary
- `git diff --stat main..HEAD`
- Test results
- Per-iter verdicts
- Open vs closed sub-tasks

Compose:
```bash
git push origin feat/<slug>
gh pr create --title "<title>" --body "$(cat results/orchestrate_$RUN_ID/final_report.md)"
```

**Wait for user "yes" before executing.**

## Output structure

```
results/orchestrate_<run_id>/
├── audit.md
├── iter_1_{artifact,review,summary}.md
├── iter_2_*.md
├── ...
├── codex_review/iter_*_{artifact,prompt,review}.md
└── final_report.md
```

## Failure modes

| Mode | Trigger | Action |
|---|---|---|
| FAILURE | 3 consecutive REJECT | Save state, escalate with audit |
| MAX_ITER_REACHED | k = 5, sub-tasks open | Save state, ask user: continue manual, or scope cut |
| GATE_FAIL | `/audit-*` returns 🔴 | STOP before Phase 2 |
| INTERRUPTED | User Ctrl-C | Preserve branch, write partial `final_report.md` |
| BOUNDARY_VIOLATION | gcloud/aws/az detected | REJECT diff, escalate |

## Difference vs /orchestrate

| Aspect | `/iterate` (this) | `/orchestrate` (interactive) |
|---|---|---|
| Approval gates | Only at Phase 4 | Multiple per task |
| Cross-review | Mandatory each iter | Optional |
| Pace | Fire-and-forget | Step-by-step |
| Use when | Plan well-defined | High-risk, novel |

## Constraints

- NEVER push without Phase 4 user approval
- NEVER bypass `bs-detector` / `code-reviewer`
- ALWAYS commit incrementally (no big-bang at loop end)
- ALWAYS update issue labels in lockstep with commits
- ALWAYS write `final_report.md` even on FAILURE/MAX_ITER
- NEVER invoke `gcloud`/`aws`/`az`/`kubectl`/`helm`
