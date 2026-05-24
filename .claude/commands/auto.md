---
description: Fast-path for small Wless tasks (trivial / small). No formal plan, no issue creation. Aborts if scope grows >3 files or touches LQN demand / pom.xml / SPCL sb wrappers — those go through /plan.
---

# /auto <task description>

Inline minimal pipeline for low-risk changes.

## Protocol

### 1. Bound check
- Estimate scope (Read + Grep)
- If touches:
  - `> 3 files` → ABORT, recommend `/plan`
  - `pom.xml` or `Acmeair_variants/*/Entry/` → ABORT, recommend `/audit-deploy` + `/plan`
  - `MPP4Lqn/`, `lqnmodel_*.lqn.py`, `estimeDemands.py` → ABORT, recommend `/plan`
  - `plot/*.m` baseline list → ABORT, recommend `/audit-data` + `/replot`
  - SPCL sb wrapping → ABORT, recommend `/sb-adapt`
  - gcloud/aws/az reference → REFUSE (boundary)
- Otherwise proceed

### 2. Implementation (inline)
- Make the minimal change (Edit / Write)
- No drive-by refactors

### 3. `bs-detector` quick scan on diff
- 🔴 → revert, escalate
- 🟡 → log + continue
- 🟢 → continue

### 4. Targeted test
- Python: `pytest -k <relevant>`
- Maven: `mvn -pl <module> test -q -Dtest=<Class>`
- Skip only if test infra absent — note it in the response

### 5. `code-reviewer` quick pass
- Show verdict
- If APPROVE → commit; if REJECT → escalate

### 6. Commit
- `git add <files>` (specific, not `-A`)
- Message: `<scope>: <imperative summary>`
- Commit and show the SHA

## Aborts (escalation paths)

| Abort reason | Recommendation |
|---|---|
| > 3 files | `/plan` |
| Grammar/numerical/LQN demand | `/plan` after `/calibrate-demands` |
| Maven pom change | `/plan` after `/audit-deploy` |
| Plot logic change | `/plan` after `/audit-data` |
| SPCL sb | `/sb-adapt` then `/plan` |
| gcloud/aws/az | REFUSE — boundary violation |

## Constraints

- NEVER push (user pushes manually)
- NEVER skip the bound check
- NEVER bypass `bs-detector`
