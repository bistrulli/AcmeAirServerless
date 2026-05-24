---
name: python-pipeline
description: Wless Python project conventions — environment, dependencies, type hints, error handling, pytest, reproducibility (seed, hashes, REPORT.md). Use when modifying or creating any .py file in runexp.py, extractExpData.py, MPP4Lqn/, ProPack/, tests/.
---

# Wless Python pipeline conventions

## Environment

- **Python**: 3.9+ (existing code is 3.9-compatible; new code may use 3.10+ features if pinned in requirements.txt)
- **Package manager**: pip + `requirements.txt`
- **No venv assumed**: invoke `python3 runexp.py` directly

## Dependencies (pinned in `requirements.txt`)

Current set (verify before adding):
```
numpy>=1.21
pandas>=1.3
scipy>=1.7
matplotlib>=3.5
locust>=2.15
Jinja2>=3.0
pygnuplot
```

Add a dependency: pin version, justify in commit, update both `requirements.txt` and `CLAUDE.md` if user-facing.

## Project layout

```
runexp.py                          ← experiment driver
extractExpData.py                  ← post-processor
MPP4Lqn/                           ← LQN ↔ MPP toolkit
├── entity/                        ← Lqn object model
├── Lqn2MPP/                       ← ODE generator
└── transducers/
ProPack/
└── propack.py                     ← Pareto optimizer baseline
Acmeair_variants/Acmeair_<N>/      ← per-variant: maven serverless function + Locust client
tests/                             ← pytest (mirror module path)
plot/                              ← Matlab/Octave
```

## Code style

### Type hints
- **New** code: yes (Python 3.9 typing — `list[int]` requires `from __future__ import annotations`)
- **Existing** code: do not retrofit blindly; add when touching nearby

### Error handling
```python
# Good
if demand <= 0:
    raise ValueError(f"non-positive demand {demand} for entry {entry.name}")

# Bad (silent fallback)
try:
    ...
except Exception:
    pass

# Bad (mask)
return np.nan_to_num(demand)
```

### Imports
```python
# stdlib
import json
from pathlib import Path

# third-party
import numpy as np
import pandas as pd

# local
from MPP4Lqn.entity import Task, Entry
```

### Subprocess
```python
subprocess.run(
    ["mvn", "-pl", module, "package", "-DskipTests"],
    cwd=base_dir, capture_output=True, text=True,
    timeout=600, check=False,
)
```
List form, explicit `timeout`, never `shell=True` with user input.

### Naming
- `snake_case` for functions / variables
- `PascalCase` for classes
- `UPPER_CASE` for constants

## Testing

### Layout
```
tests/
├── test_runexp.py
├── MPP4Lqn/
│   ├── test_Lqn2MPP.py
│   └── test_entity.py
├── ProPack/
│   └── test_propack.py
└── conftest.py
```

### pytest idioms
```python
import pytest

@pytest.mark.parametrize("n,expected", [(1, 1), (10, 10)])
def test_X(n, expected):
    assert foo(n) == expected

@pytest.mark.slow
def test_full_pipeline():
    ...

@pytest.fixture
def lqn_mm1():
    return Lqn().with_task(Task("S", mult=1)).with_entry(Entry("E", demand=1.0))
```

### Coverage
- New code: ≥ 80%
- LQN solver + ProPack: ≥ 90% (numerical kernel)
- Run: `pytest --cov=MPP4Lqn --cov-report=term-missing`

### Sanity tests (HIGHEST VALUE)
Always include at least ONE test vs analytical for new numerical code:
- M/M/1: E[R] = 1/(μ−λ)
- M/M/c: Erlang-C formula
- Closed N=1: E[R] = D

## Reproducibility

### Seeds
```python
import numpy as np
rng = np.random.default_rng(seed)  # not global np.random
```
Always pass `seed` explicitly. Log in `config.json`.

### Output dirs
- `results/<scenario>_<run_id>/` with `run_id = YYYY-MM-DD_HH-MM-SS`
- Required artifacts: `REPORT.md`, `results.csv`, `config.json`, `HASHES.txt`

### HASHES.txt
```bash
shasum -a 256 inputs/*.csv > HASHES.txt
```

### REPORT.md skeleton
```markdown
# Setup
- git SHA: <sha>
- Python: 3.9.18
- JDK: 17.0.9, Maven 3.9.6
- Seed: 42

# Config
<paste config.json>

# Results
<summary table>

# Sanity (vs analytical)
<M/M/c or N/A>

# Files
<list with SHA256>

# Reproduce
$ python runexp.py --target local --seed 42 --variants Acmeair_0
```

## Anti-patterns

- ❌ Wildcard imports (`from foo import *`)
- ❌ Dynamic code execution on user input — use `json.loads` or `ast.literal_eval` for data
- ❌ Subprocess with `shell=True` on user input
- ❌ Bare `except:` / `except Exception: pass`
- ❌ Global random state without `default_rng(seed)`
- ❌ Hard-coded variant paths (use parameters)

## Constraints

- ALWAYS pin dependency versions
- ALWAYS pass seeds and timeout
- NEVER silent fallback on numerical errors
