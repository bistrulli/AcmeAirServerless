---
description: Produce a reviewed plan/<slug>.md for a Wless task. Parallel expert consultation, Codex cross-review (max 5 iter), GitHub issue creation, user approval gate before /iterate.
---

# /plan <task description>

Produces `plan/<slug>.md` ready to drive `/iterate`.

## 8 phases

### A. Triage (inline)
- `git status` + `git log --oneline -5`
- Classify (mirror `/triage` logic)
- Decide which experts to consult

### B. Context load
- `cat CLAUDE.md` (sections 1, 3, 8, 10)
- `cat` of files the task most likely touches (≤ 5 files)
- Recent commits on relevant paths

### C. Web research (optional)
- If task involves novel theory or external tool: call `/research <topic>` first
- Otherwise skip

### D. Parallel expert consultation (KEY PHASE — single message, multiple Task calls)
- Identify 3–5 relevant agents from CLAUDE.md inventory
- Invoke each in parallel via Task tool with the same task description
- Each returns a design memo (≤ 400 words): approach, risks, files to touch

Example agents to invoke for an LQN-touching task:
- `lqn-model-expert` (entity model + estimation)
- `markov-chain-expert` (fluid model theory)
- `python-experiment-expert` (runexp integration)
- `test-engineer` (sanity vs M/M/c)

### E. Synthesis → `plan/<YYYY-MM-DD>-<slug>.md`

Template:
```markdown
# Plan: <title>

**Date**: 2026-MM-DD
**Slug**: <slug>
**Size**: medium
**Domain**: lqn + maven

## Goal
<1-paragraph what + why>

## Out of scope
- Anything requiring GCR deployment (user-driven only)
- <other explicit exclusions>

## Approach
<approach summary, with citations to expert memos>

## Sub-tasks (iter:1)
- [ ] [agent:lqn-model-expert] [area:lqn] Add Cauchy demand support in MPP4Lqn/entity/Activity.py
- [ ] [agent:python-experiment-expert] [area:python] Wire --distribution=cauchy in estimeDemands.py
- [ ] [agent:test-engineer] [area:lqn] Add sanity test vs M/M/c with Cauchy think-time
- [ ] [agent:documentation-writer] [area:docs] Update CLAUDE.md §3 + README

## Sub-tasks (iter:2 — provisional)
- [ ] Refine fit if iter:1 sanity test fails
- [ ] Update plot config if needed

## Verification
- Sanity: M/M/c with Cauchy think-time vs Pollaczek-Khinchine
- Smoke: `python runexp.py --target local --variants Acmeair_0 --scenarios wlessconc --seed 42`
- BS-check pre-commit each task

## Risks
- R1: Cauchy heavy tail breaks demand estimator (median may help vs mean)
- R2: Solver tolerance too tight for heavy-tailed → may need atol relax

## Acceptance
- All sub-tasks closed
- Sanity test passes within 2% of Pollaczek-Khinchine
- Codex cross-review APPROVE on final diff
```

### F. Codex cross-review (loop, max 5 iter)
- Call `/cross-review plan/<slug>.md --checklist plan`
- Apply APPROVE_WITH_CHANGES feedback; loop until APPROVE or 5 iter

### G. GitHub issue creation
- Call `/issue create-plan <slug> "<title>"` → parent issue
- For each sub-task: `/issue create-subtask <parent-id> "<title>" <agent> <area>`
- Set labels: `type:plan`, `iter:1`, `status:in-review`

### H. Approval gate (USER)
Show the user:
- Path to `plan/<slug>.md`
- Issue numbers created
- Cross-review verdict + iteration count
- Recommended next command: `/iterate plan/<slug>.md`

**Wait for user "yes"** before any execution starts.

## Constraints

- NEVER skip Phase D (parallel experts)
- NEVER write a plan that violates the no-GCR boundary
- ALWAYS get APPROVE from cross-review or exit with explicit "MAX_ITER, please review"
- ALWAYS create GitHub issues (or fallback markdown) — single source of truth
