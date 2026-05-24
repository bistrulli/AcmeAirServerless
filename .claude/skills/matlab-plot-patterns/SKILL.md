---
name: matlab-plot-patterns
description: Wless Matlab/Octave plotting patterns - parametric plots from plot_config.json, paper-friendly color palette, exportgraphics to PDF + saveas PNG, Octave fallback. Use when authoring or refactoring plot/*.m.
---

# Matlab/Octave plot patterns (Wless)

## Goal: parametric plots (no hard-coded baselines)

Avoid:
```matlab
boxplot([defconc_data, noconc_data, wlessconc_data, propackconc_data]);   % BAD
xticklabels({'defconc','noconc','wlessconc','propackconc'});
```

Prefer:
```matlab
function plot_overall(run_dir)
    cfg = jsondecode(fileread(fullfile(run_dir, 'plot_config.json')));
    data = readtable(fullfile(run_dir, 'results.csv'));
    figure('Position',[100 100 800 500]); hold on;
    for i = 1:numel(cfg.scenarios)
        s = cfg.scenarios(i);
        rows = strcmp(data.scenario, s.name);
        boxplot(data.billable_s(rows), 'Positions', i, 'Colors', s.color);
    end
    xticks(1:numel(cfg.scenarios));
    xticklabels({cfg.scenarios.label});
    ylabel('Billable time (s)'); xlabel('Scenario'); grid on;
    save_paper_quality(fullfile(run_dir, 'figures', 'overall_billable'));
end
```

## `plot_config.json` (co-located with `results.csv`)

```json
{
  "scenarios": [
    {"name": "noconc",       "label": "No-Conc",   "color": "#1f77b4"},
    {"name": "defconc",      "label": "GCR (80)",  "color": "#ff7f0e"},
    {"name": "propackconc",  "label": "ProPack",   "color": "#2ca02c"},
    {"name": "wlessconc",    "label": "WasteLess", "color": "#d62728"}
  ],
  "yaxis_log": true,
  "title": "Billable time across scenarios"
}
```

## Color palette (color-blind-safe, paper-friendly)

| Use | Hex | matplotlib name |
|---|---|---|
| Baseline 1 | `#1f77b4` | tab:blue |
| Baseline 2 | `#ff7f0e` | tab:orange |
| Baseline 3 | `#2ca02c` | tab:green |
| Our method | `#d62728` | tab:red |
| Annotation | `#7f7f7f` | tab:gray |

## Paper-quality export helper

```matlab
function save_paper_quality(basename_without_ext)
    if exist('OCTAVE_VERSION', 'builtin')
        print(gcf, [basename_without_ext '.pdf'], '-dpdf', '-bestfit', '-painters');
        print(gcf, [basename_without_ext '.png'], '-dpng', '-r300');
    else
        exportgraphics(gcf, [basename_without_ext '.pdf'], 'ContentType','vector');
        exportgraphics(gcf, [basename_without_ext '.png'], 'Resolution', 300);
    end
end
```

Always emit BOTH PDF (paper) AND PNG (slides).

## Octave compatibility

| Matlab feature | Octave fallback |
|---|---|
| `exportgraphics` | `print -dpdf -bestfit` + `print -dpng -r300` |
| `boxplot` | needs `pkg load statistics` |
| `jsondecode` | OK in Octave 5+ |
| `string` type | Octave uses char arrays — be careful with `strcmp` |

Detect at runtime:
```matlab
if exist('OCTAVE_VERSION', 'builtin')
    pkg load statistics
end
```

## Invocation from shell

```bash
# Matlab
matlab -batch "addpath('plot'); plot_overall('results/wless-bench_2026-05-24_14-32')"
# Octave
octave --no-gui --eval "addpath('plot'); plot_overall('results/wless-bench_2026-05-24_14-32')"
```

## Sample-size guardrails

Before drawing a boxplot:
```matlab
n_per_scenario = arrayfun(@(s) sum(strcmp(data.scenario, s.name)), cfg.scenarios);
assert(all(n_per_scenario >= 10), 'sample size < 10 for some scenarios');
```

If you allow `--allow-warnings` mode: change `assert` to `warning(...)`.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Boxplot draws single bar | All scenarios share same x-position | Use `'Positions', i` |
| Colors wrong | Hex → RGB conversion missing in Octave | `hex2rgb` helper or use named colors |
| PDF rasterized | Default renderer | `-painters` flag (Octave) or `'ContentType','vector'` |
| Axes too small | Default figure size | `'Position', [100 100 800 500]` |

## Constraints

- NEVER hard-code scenario names in `plot_*.m`
- NEVER skip PDF export
- ALWAYS check sample size before boxplot (≥10)
- ALWAYS export both PDF + PNG
