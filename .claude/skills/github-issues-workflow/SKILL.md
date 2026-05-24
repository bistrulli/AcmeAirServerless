---
name: github-issues-workflow
description: Wless GitHub Issues lifecycle — canonical labels, commit references, fallback markdown-only tracking in plan/<slug>.md. Use during /plan, /iterate, and when triaging external bug reports.
---

# Wless GitHub Issues workflow

## Label taxonomy (canonical)

| Prefix | Values | Color | Meaning |
|---|---|---|---|
| `type:` | plan, subtask, blocker, research, bug | varies | Issue kind |
| `iter:` | 1, 2, 3, 4, 5 | `#c2e0c6` | Iteration within a plan (drives `/iterate` loop) |
| `status:` | in-review, blocked, ready | varies | Workflow state |
| `agent:` | <agent-name> | per agent | Recommended owner |
| `area:` | lqn, maven, matlab, sb, propack, workload, python, docs | varies | Scope |

## Init labels (one-time)

```bash
# Type
gh label create "type:plan"     --color "0e8a16" --force
gh label create "type:subtask"  --color "1d76db" --force
gh label create "type:blocker"  --color "b60205" --force
gh label create "type:research" --color "fbca04" --force
gh label create "type:bug"      --color "d93f0b" --force
# Iter
for k in 1 2 3 4 5; do gh label create "iter:$k" --color "c2e0c6" --force; done
# Status
gh label create "status:in-review" --color "fef2c0" --force
gh label create "status:blocked"   --color "e99695" --force
gh label create "status:ready"     --color "bfd4f2" --force
# Area
gh label create "area:lqn"      --color "5319e7" --force
gh label create "area:maven"    --color "cccc00" --force
gh label create "area:matlab"   --color "f9d0c4" --force
gh label create "area:sb"       --color "c5def5" --force
gh label create "area:propack"  --color "0052cc" --force
gh label create "area:workload" --color "bfdadc" --force
gh label create "area:python"   --color "306998" --force
gh label create "area:docs"     --color "ffffff" --force
# Agent labels (generate from .claude/agents/*.md filenames)
for f in .claude/agents/*.md; do
    name=$(basename "$f" .md)
    gh label create "agent:$name" --color "ededed" --force
done
```

## Commit message conventions

Format: `<scope>: <imperative summary>` (≤ 72 chars)

Scopes:
- `lqn:` — LQN model, demands, MPP4Lqn
- `maven:` — pom.xml, serverless function code
- `python:` — runexp, extractExpData, glue
- `matlab:` — plot/*.m
- `sb:` — SPCL serverless-benchmarks adapter
- `propack:` — ProPack/
- `workload:` — Locust, SimpleWorkload
- `docs:` — docs, README, CLAUDE.md
- `tests:` — test-only changes
- `infra:` — .claude/, .gitignore, settings

Reference issues: `Refs #N` (related), `Fixes #N` (closes on merge).

Examples:
```
lqn: enforce demand>0 in estimeDemands; refs #42
maven: migrate MSauthEntry from Spring to Quarkus; fixes #51
sb: pin SeBS at 2c1f3a4 for 110.dynamic-html adapter; refs #60
```

## Plan → Issue mapping

For a plan `plan/2026-05-24-add-cauchy-lqn.md`:

1. **Parent**:
   - Title: same as plan
   - Labels: `type:plan`, `iter:1`, `status:in-review`
   - Body: `Plan: plan/2026-05-24-add-cauchy-lqn.md`

2. **Each sub-task** in plan → child issue:
   - Title: from sub-task line
   - Labels: `type:subtask`, `iter:1`, `agent:<name>`, `area:<area>`
   - Body: `Refs #<parent-id>`

## Fallback (no gh)

If `gh auth status` fails, write markdown checklist into `plan/<slug>.md`:

```markdown
## Sub-tasks
- [ ] [iter:1] [agent:lqn-model-expert] [area:lqn] Add Cauchy demand support in MPP4Lqn/entity/Activity.py
- [ ] [iter:1] [agent:python-experiment-expert] [area:python] Wire --distribution=cauchy in estimeDemands.py
```

`autonomous-orchestrator` polls these checkboxes. Mark `- [x]` on commit.

## Constraints

- ALWAYS `--force` on label create (idempotent)
- NEVER post comments other than "Done in <sha>" without approval
- NEVER delete labels or close issues without user confirmation (outside automatic close-on-completion)
