---
name: cross-llm-review
description: Protocol for Claude ↔ OpenAI Codex cross-review of Wless artifacts (plan / code / paper). Bounded loop max 5 iterations. Degrades to Claude self-review (fresh subagent) if codex-cli unavailable. Used by /plan and /iterate.
---

# Cross-LLM review protocol

## Tooling check

```bash
codex --help 2>/dev/null \
  && echo "codex-cli: AVAILABLE" \
  || echo "codex-cli: NOT_AVAILABLE — falling back to Claude self-review"
```

Record in `results/codex_review/<run-id>/audit.md`.

## Checklist templates

### `plan` checklist
1. **Completeness** — atomic, verifiable sub-tasks?
2. **Novelty** — explains what's NEW vs ProPack, GCR default, SPCL-sb default?
3. **Methodology** — LQN / Markov / queueing soundness; reproducible?
4. **Feasibility** — realistic given local-only execution?
5. **Baseline coverage** — defconc, noconc, propackconc, sb-default where applicable?
6. **Boundary** — respects no-GCR/AWS/Azure for the agent?

### `code` checklist
1. **Correctness** — logic, edge cases, error handling
2. **Tests** — coverage, sanity vs analytical, determinism (seeded)
3. **Style** — CLAUDE.md §8 (Python type hints, Java SLF4J, Matlab parametric)
4. **Performance** — vectorization, ODE tolerance, no I/O in hot paths
5. **Security** — input validation, no credentials, no `gcloud`/`aws`/`az`

### `paper` checklist
1. **Clarity** — claims, contributions, scope statement
2. **Math** — LQN / Markov notation, theorem statements
3. **Reproducibility** — code link, seed, version, HASHES
4. **Citations** — every reference DOI- or arXiv-verified
5. **Narrative** — motivation, novelty, limitations

## Bounded loop (max 5 iter)

```
artifact_v1 = read(<artifact>)
for k in 1..5:
    snapshot → results/codex_review/<run-id>/iter_k_artifact.md
    prompt = template_for(checklist, artifact_vk)
    save → iter_k_prompt.md
    review = run codex_or_fallback(prompt)
    save → iter_k_review.md
    verdict = parse_json(review)
    if verdict == APPROVE: break
    if verdict == APPROVE_WITH_CHANGES: merge + next iter
    if verdict == REJECT: refine via Claude (orchestrator decides) + next iter
write → results/codex_review/<run-id>/final_verdict.md
```

## Codex invocation template

```bash
codex exec --quiet --json <<'EOF'
You are reviewing a Wless artifact. Apply the <plan|code|paper> checklist.
Output ONLY this JSON:
{
  "verdict": "APPROVE" | "APPROVE_WITH_CHANGES" | "REJECT",
  "findings": [{"severity": "low"|"med"|"high", "criterion": "...", "note": "..."}],
  "summary": "..."
}

ARTIFACT:
---
<paste artifact content>
---
EOF
```

If JSON parse fails: log raw, treat as `APPROVE_WITH_CHANGES` with raw text as finding.

## Fallback (codex unavailable)

Spawn fresh Claude Task with this system prompt:
> You are a SECOND reviewer (NOT the original author). Apply the <checklist> rubric. Be skeptical. Cross-check claims against the actual files referenced. Output the same JSON described above.

Log `DEGRADE: claude-self-review` in `audit.md`.

## Output structure

```
results/codex_review/<run-id>/
├── audit.md
├── iter_1_artifact.md
├── iter_1_prompt.md
├── iter_1_review.md
├── iter_2_*.md
├── ...
└── final_verdict.md
```

## Constraints

- ALWAYS save prompt + raw review for audit
- ALWAYS log fallback if codex unavailable
- NEVER auto-merge changes the user did not approve
- NEVER skip the loop (always at least one iteration)
