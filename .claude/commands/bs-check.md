---
description: Run BS-detector on a scope. Modes: --diff (uncommitted), --last-commit (HEAD), <file>, --branch (vs main). Reports CAT-1..CAT-8 with severity. Does not modify code.
---

# /bs-check [--diff | --last-commit | --branch | <file>]

Invokes `bs-detector`.

## Modes

| Mode | Scope |
|---|---|
| (none) or `--diff` | `git diff` (uncommitted, staged + unstaged) |
| `--last-commit` | `git show HEAD` |
| `--branch` | `git diff main..HEAD` (whole branch) |
| `<file>` | Just that file |

## Protocol

1. Determine scope (`git diff <mode>` etc.)
2. Invoke `bs-detector` with the diff/files
3. Show report inline (do not auto-fix)
4. If 🔴 critical: highlight and suggest invoking the specialist that owns the area

## Output

```markdown
# BS-check report — <scope>

## Summary
- 🔴 N critical
- 🟡 M warnings
- 🟢 K passes

## Findings
### CAT-X — <name>
**Severity**: 🔴
**File**: `runexp.py:42`
**Issue**: <one sentence>
**Evidence**: <snippet>
**Fix path**: <action>

## Recommendation
- 🔴 findings: invoke <relevant specialist> to remediate, then re-run /bs-check
```

## Constraints

- NEVER auto-fix
- NEVER lower severity
- ALWAYS show file:line and snippet
