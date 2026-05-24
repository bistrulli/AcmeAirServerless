---
description: Regenerate a Matlab/Octave plot from a results.csv with validation. Reads parametric plot_config.json. Emits both PDF (paper) and PNG (slides) into figures/. Requires /audit-data 🟢 first.
---

# /replot <figure-name> [--run-dir <path>] [--expect-scenarios <list>] [--engine matlab|octave]

Invokes `matlab-plot-expert`.

## Args

| Arg | Default | Notes |
|---|---|---|
| `<figure-name>` | (required) | `overall_billable`, `overall_latency`, `zoom_<variant>` |
| `--run-dir` | latest `results/wless-bench_*` | Source CSV |
| `--expect-scenarios` | (none — strict mode) | Comma-sep; fails if missing |
| `--engine` | matlab if installed, else octave | Plot engine |

## Protocol

### 1. Audit
- Run `/audit-data <run-dir>` — must be 🟢 (or 🟡 with `--allow-warnings`)
- 🔴 → STOP

### 2. Resolve plot config
- Default: read `<run-dir>/plot_config.json`
- Fallback: copy `plot/plot_config.default.json` into run-dir and use that

### 3. Invoke engine
```bash
# Matlab
matlab -batch "addpath('plot'); plot_<figure-name>('<run-dir>')"
# Or Octave
octave --no-gui --eval "addpath('plot'); plot_<figure-name>('<run-dir>')"
```

### 4. Validate output
- Both PDF and PNG must exist in `<run-dir>/figures/`
- File size > 5KB (sanity)
- (Optional) `pdfinfo` to check it's not a blank page

### 5. Update repo figures (if user wants paper-canonical)
- If `--update-paper-figures`: copy `<run-dir>/figures/*` to `plot/figures/`
- Otherwise: leave in run-dir only

## Output

```markdown
# /replot report — overall_billable

## Audit: 🟢 (results.csv valid)
## Engine: octave 8.4.0
## Generated:
- results/wless-bench_<run-id>/figures/overall_billable.pdf (12 KB, vector)
- results/wless-bench_<run-id>/figures/overall_billable.png (45 KB, 300 DPI)

## Scenarios plotted (4): defconc, noconc, wlessconc, propackconc

## Next steps
- Review the PDF visually
- If correct: re-run with --update-paper-figures to update plot/figures/
```

## Constraints

- NEVER skip `/audit-data` 🟢 requirement
- NEVER overwrite `plot/figures/` without `--update-paper-figures` flag
- ALWAYS emit both PDF and PNG
- DEFER plot logic edits to `matlab-plot-expert`
