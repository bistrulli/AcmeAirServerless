---
description: Codex cross-review loop (max 5 iterations) on a plan / code diff / paper artifact. Degrades to Claude self-review if codex-cli unavailable.
---

# /cross-review <artifact-file> [--checklist plan|code|paper]

Invokes `codex-cross-reviewer`.

## Protocol

### 1. Tooling check
```bash
codex --help 2>/dev/null && echo "AVAILABLE" || echo "FALLBACK: claude-self-review"
```

### 2. Snapshot
- `mkdir -p results/codex_review/<run-id>/`
- Copy artifact to `iter_1_artifact.md`

### 3. Loop (max 5)
- Generate prompt from `--checklist` template (plan/code/paper)
- Invoke Codex (or fallback)
- Parse verdict JSON: `{verdict: APPROVE|APPROVE_WITH_CHANGES|REJECT, findings: [...], summary: ...}`
- Save to `iter_k_review.md`
- If APPROVE → break
- If APPROVE_WITH_CHANGES → apply requested edits via Claude, re-snapshot, next iter
- If REJECT → Claude refines, next iter

### 4. Final verdict
- Write `results/codex_review/<run-id>/final_verdict.md`
- Show user

## Checklist templates

### `--checklist plan`
1. Completeness (atomic sub-tasks, verifiable)
2. Novelty (vs ProPack, GCR default, SPCL-sb default)
3. Methodology (LQN/Markov soundness, reproducibility)
4. Feasibility (local-only, time)
5. Baseline coverage
6. Boundary compliance (no GCR/AWS/Azure)

### `--checklist code`
1. Correctness (logic, edge cases)
2. Tests (coverage, sanity vs analytical)
3. Style (CLAUDE.md §8)
4. Performance (vectorization, ODE tolerance)
5. Security (input validation, no creds, no cloud CLIs)

### `--checklist paper`
1. Clarity (claims, contributions)
2. Math (LQN/Markov notation, theorems)
3. Reproducibility (code link, seed, HASHES)
4. Citations (DOI-verified)
5. Narrative (motivation, novelty, limitations)

## Output artifacts

```
results/codex_review/<run-id>/
├── audit.md
├── iter_1_{artifact,prompt,review}.md
├── ...
└── final_verdict.md
```

## Constraints

- NEVER auto-merge changes the user did not approve
- ALWAYS save prompt + raw review for audit
- ALWAYS log fallback if codex unavailable
