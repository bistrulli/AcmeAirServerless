---
description: GitHub Issues CRUD for Wless plans + sub-tasks. Subcommands - init-labels, create-plan, create-subtask, promote, close. Falls back to markdown-only tracking in plan/ if gh auth fails.
---

# /issue <subcommand> [args]

Invokes `github-issue-manager`.

## Subcommands

### `init-labels`
Creates canonical label taxonomy (idempotent via `gh label create --force`):
- `type:` plan, subtask, blocker, research, bug
- `iter:` 1, 2, 3, 4, 5
- `status:` in-review, blocked, ready
- `area:` lqn, maven, matlab, sb, propack, workload, python, docs
- `agent:` one per agent in `.claude/agents/` (auto-discovered)

### `create-plan <slug> <title>`
- Creates parent issue
- Labels: `type:plan`, `iter:1`, `status:in-review`
- Body links to `plan/<slug>.md`

### `create-subtask <parent-id> <title> <agent-name> <area>`
- Child issue
- Labels: `type:subtask`, `iter:1`, `agent:<name>`, `area:<area>`
- Body: `Refs #<parent-id>`

### `promote <id>`
- Move from `iter:k` to `iter:k+1`

### `close <id> <commit-sha>`
- Close with comment "Done in `<sha>`"

### `list [--iter k] [--status s]`
- Wraps `gh issue list`

## Fallback (no gh)

Writes markdown checklist into `plan/<slug>.md`:
```markdown
## Sub-tasks
- [ ] [iter:1] [agent:lqn-model-expert] [area:lqn] Add Cauchy demand support
```

`autonomous-orchestrator` polls these checkboxes instead.

## Constraints

- ALWAYS `--force` on label create
- NEVER delete labels without user approval
- NEVER post non-canonical comments without approval
