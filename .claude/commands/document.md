---
description: Generate or refresh Wless documentation. Targets: readme, claude, manual-replicate, report (per-run), paper (section <name>).
---

# /document <target> [--audience dev|user|reviewer]

Invokes `documentation-writer`.

## Targets

| Target | File | Trigger |
|---|---|---|
| `readme` | `README.md` | Public-facing changes |
| `claude` | `CLAUDE.md` | Pipeline / agent / convention updates |
| `manual-replicate` | `Manual/ReplicabilityGuide.md` | Reproducibility regression |
| `report <run-dir>` | `results/<run-dir>/REPORT.md` | Post-experiment |
| `paper section-<id>` | `paper/section-<id>.md` | Paper revision |

## Protocol

### 1. Read current state
- Existing file (if any)
- Related code (cross-check claims)
- Git log of relevant paths (cite recent changes)

### 2. Audience tailoring
- `--audience dev`: terse, code-pointers, assume Java + Python + LQN literacy
- `--audience user`: step-by-step, prerequisites stated, copy-paste commands
- `--audience reviewer`: emphasize novelty, baselines, reproducibility

### 3. Write
- Active voice
- `file_path:line_number` for code references
- Tables for comparisons
- Code blocks with explicit prompts (`$ ` shell, `>>> ` Python REPL)

### 4. Cross-check
- For each numeric claim: link to CSV
- For each citation: ensure DOI/arXiv via `web-researcher`
- For each "supported feature": grep for a test

### 5. Update timestamps
- `CLAUDE.md` `_Last updated_` line
- `REPORT.md` header

## Output

Show user:
- Diff against existing file
- New / changed sections
- Citations added (with verification status)

## Constraints

- NEVER copy-paste a function body — link to source
- NEVER claim "supported" without a runnable example
- NEVER skip the cross-check step
