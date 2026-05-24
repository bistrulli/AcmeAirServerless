---
description: Adapt a SPCL serverless-benchmarks scenario into the Wless pipeline. Pins upstream SHA, generates a wrapper variant in Acmeair_variants/sb_<id>/, emits LQN model skeleton, Locust profile, and SB_ADAPTATION.md.
---

# /sb-adapt <benchmark-id> [--sb-root ~/git/serverless-benchmarks] [--lang python|nodejs]

Invokes `spcl-benchmarks-expert` + `lqn-model-expert` + `locust-workload-expert`.

## Args

| Arg | Default | Notes |
|---|---|---|
| `<benchmark-id>` | (required) | e.g., `110.dynamic-html`, `120.uploader`, `210.thumbnailer` |
| `--sb-root` | `~/git/serverless-benchmarks` | Local SeBS clone |
| `--lang` | `python` | SeBS language wrapper to use |

## Protocol

### 1. Pin upstream
```bash
cd <sb-root>
git rev-parse HEAD > /Users/emilio-imt/git/Wless/docs/research-notes/sb-pin-$(date +%Y-%m-%d)-<benchmark-id>.md
```

If SeBS not cloned: tell user to `git clone https://github.com/spcl/serverless-benchmarks <sb-root>`.

### 2. Sanity-run upstream locally
```bash
cd <sb-root>
./sebs.py local invoke <benchmark-id> --config config/example.json
```
- 🔴 if fails (likely Docker / Minio not running) — instruct user

### 3. Wrap as Wless variant
Create `Acmeair_variants/sb_<id>/`:
- `<langEntry>/` directory with `function.py` (or `.js`) copied + thin Wless adapter
- `pom.xml` if Java (rare for SeBS — usually Python)
- `application.properties` (if applicable)
- `lqnmodel_<id>.lqn.py` (skeleton: 1 task, 1 entry per function)
- `clientEntry/SimpleWorkload.py` (Locust pointing at the local SeBS endpoint or invocation loop)

### 4. Demand calibration sketch
- Run 10 SeBS invocations (seed=42) locally → record mean `time`
- Pre-populate `lqnmodel_<id>.lqn/optSol.csv` with this demand
- Call `/calibrate-demands sb_<id>` to refine

### 5. Document
Write `Acmeair_variants/sb_<id>/SB_ADAPTATION.md`:
```markdown
# SeBS adaptation: <benchmark-id>
- Upstream SHA: <sha>
- Upstream version: <release>
- Language: <lang>
- Wless scenarios mapped: defconc, noconc, wlessconc, propackconc
- Deviations from upstream defaults: <list>
- Sanity run (10 invocations, seed=42): mean=Xms, P95=Yms
- LQN structure: 1 task `T_<func>`, 1 entry `<func>`, demand=Xms
- Locust profile: <endpoint or invocation>
```

### 6. Verify
- `/audit-deploy sb_<id>` (if Java) or smoke `python function.py < input.json`
- `/wless-bench sb_<id> --scenarios defconc --duration 10s` (smoke)

## Output

```markdown
# /sb-adapt report — 110.dynamic-html

## Pin: SeBS @ <SHA> (<date>)
## Upstream sanity: 🟢 (1.2s mean across 5 invocations)

## Created
- Acmeair_variants/sb_110.dynamic-html/pythonEntry/function.py
- Acmeair_variants/sb_110.dynamic-html/lqnmodel_110.dynamic-html.lqn.py
- Acmeair_variants/sb_110.dynamic-html/clientEntry/SimpleWorkload.py
- Acmeair_variants/sb_110.dynamic-html/SB_ADAPTATION.md

## Next steps
1. `/calibrate-demands sb_110.dynamic-html` (refine demand)
2. `/wless-bench sb_110.dynamic-html --scenarios defconc,wlessconc --duration 30s`
3. `/replot overall --run-dir results/wless-bench_<run-id>`
```

## Constraints

- NEVER modify `<sb-root>/benchmarks/` — always wrap
- NEVER run SeBS `aws`/`azure`/`gcf` deployment — local only
- ALWAYS pin SHA in `docs/research-notes/`
- ALWAYS hand off LQN refinement to `lqn-model-expert`
