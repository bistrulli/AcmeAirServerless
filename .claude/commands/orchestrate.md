---
description: Execute a Wless plan interactively, task-by-task, with explicit approval gates between phases. Use for novel / high-risk work where you want full control. Slower than /iterate but safer.
---

# /orchestrate plan/<slug>.md [--no-cross-review]

Interactive execution. Invokes `pipeline-orchestrator`.

## Protocol

### Phase 0 — Context (show user)
```bash
cat plan/<slug>.md
git status
git log --oneline -5
gh issue list --label "type:plan" --state open
```
- List sub-tasks
- **GATE**: user "go" / "abort"

### Phase 1 — Setup
1. Branch creation (if needed)
2. Pre-flight: `/audit-deploy`, `/audit-data`, `/calibrate-demands`, or `spcl-benchmarks-expert` check (as plan scope dictates)
3. **GATE**: user acks pre-flight output

### Phase 2 — Per-task loop
For each sub-task:
1. Show task + assigned specialist
2. **GATE**: user "go" / "skip" / "abort"
3. Invoke specialist
4. Run `bs-detector` — show report
5. Run targeted tests (`pytest -k <name>` or `mvn -pl <module> test`)
6. Show `git diff --stat`
7. **GATE**: user confirms commit message + commit
8. (Optional `--no-cross-review`) skip Codex per-task; otherwise prompt user
9. Update issue label
10. Loop

### Phase 3 — Finalize
1. Full diff review (`git diff main..HEAD`)
2. Full Python + Maven test on touched modules
3. (Optional) `paper-replicator` if benchmark scope
4. **GATE**: user approves final report
5. Compose push command — user runs it

## Flags

- `--no-cross-review` — skip Codex per-task (still runs final cross-review unless that's also off)

## Difference vs /iterate

| Aspect | /orchestrate (this) | /iterate |
|---|---|---|
| Pace | Step-by-step | Fire-and-forget |
| Gates | Many | One (final push) |
| Cross-review | Optional | Mandatory |
| Use when | High risk / novel | Well-scoped feature |

## Constraints

- NEVER proceed without explicit user "go" at each gate
- NEVER batch multiple commits without showing each
- ALWAYS show actual commands before running
- Same DENY list (no gcloud/aws/az/kubectl/helm)
