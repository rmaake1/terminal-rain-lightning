# Convert to proper package layout + fix sound paths + reinstall

## Context

The upstream PR (sound effects) was already merged. `pipx install` produced a broken install because `pyproject.toml` had no package declaration, so setuptools auto-discovery emitted a wheel with no Python code (only dist-info). Additionally the PR hardcoded `"sounds/rain.mp3"` as a CWD-relative path, so sound would only work when running from the repo directory.

The fix: convert the single-file module to a package (`terminal_rain_lightning/`), bundle the sounds inside it, resolve paths via `importlib.resources`, and declare everything in `pyproject.toml`.

**Current state (already staged, not yet committed):**
- `terminal_rain_lightning.py` → `terminal_rain_lightning/__init__.py`
- `sounds/rain.mp3` → `terminal_rain_lightning/sounds/rain.mp3`
- `sounds/thunder.mp3` → `terminal_rain_lightning/sounds/thunder.mp3`

## Steps

### 1. Fix sound-path resolution in `terminal_rain_lightning/__init__.py`

Add to the imports at the top:
```python
from importlib.resources import files as _res_files
```

Add two module-level constants after the existing `THUNDER_COOLDOWN` line:
```python
_RAIN_SOUND = str(_res_files(__package__) / "sounds" / "rain.mp3")
_THUNDER_SOUND = str(_res_files(__package__) / "sounds" / "thunder.mp3")
```

In `play_rain_sound()` (line 221), replace `"sounds/rain.mp3"` → `_RAIN_SOUND`.  
In `play_thunder_sound()` (line 236), replace `"sounds/thunder.mp3"` → `_THUNDER_SOUND`.

### 2. Update `pyproject.toml`

- Bump `requires-python` to `">=3.9"` (`importlib.resources.files` was added in 3.9)
- Remove 3.6/3.7/3.8 classifiers
- Add package discovery + package-data sections:

```toml
[tool.setuptools.packages.find]
where = ["."]

[tool.setuptools.package-data]
terminal_rain_lightning = ["sounds/*.mp3"]
```

### 3. Commit

```
git add terminal_rain_lightning/ pyproject.toml
git commit -m "Convert to package layout; bundle sounds via importlib.resources"
```

### 4. Reinstall

```
pipx install --force .
```

### 5. Smoke-test

```
terminal-rain --help
```

Confirm `--no-sound`, `--rain-color`, `--lightning-color` all appear.

## Files modified

- `terminal_rain_lightning/__init__.py` — import + 2 constants + 2 path substitutions
- `pyproject.toml` — `requires-python`, classifiers, `[tool.setuptools.*]` sections

## Verification

- `terminal-rain --help` exits 0 and shows all three flags
- Sound works from any working directory (not just the repo root)
