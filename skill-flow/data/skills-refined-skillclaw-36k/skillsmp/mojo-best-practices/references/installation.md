# Mojo Installation Guide

Install Mojo using pixi (recommended), uv, pip, or conda. Choose **stable** for production or **nightly** for latest features.

> **Note:** Version numbers in this file are updated via `scripts/update-versions.py`. The source of truth is `metadata.json`.

## Version Check

```bash
mojo --version                   # Direct check
pixi list | grep mojo            # In pixi environment
```

**Current versions:** Stable v25.7 (Mojo 0.25.7) | Nightly v26.2 (Mojo 0.26.2)

---

## Pixi (Recommended)

Pixi manages both Python and native dependencies in a reproducible environment.

### Nightly

```bash
# New project
pixi init my-project \
  -c https://conda.modular.com/max-nightly/ -c conda-forge \
  && cd my-project
pixi add mojo
pixi shell

# Existing project - add to pixi.toml channels first:
# [workspace]
# channels = ["https://conda.modular.com/max-nightly/", "conda-forge"]
pixi add mojo
```

### Stable (v25.7)

```bash
# New project
pixi init my-project \
  -c https://conda.modular.com/max/ -c conda-forge \
  && cd my-project
pixi add "mojo==0.25.7"
pixi shell

# Existing project
pixi add "mojo==0.25.7"
```

---

## uv

uv is a fast Python package manager. Good for Python-only workflows.

### Nightly

```bash
uv init my-project && cd my-project
uv venv && source .venv/bin/activate
uv pip install mojo \
  --index-url https://dl.modular.com/public/nightly/python/simple/ \
  --prerelease allow
```

### Stable

```bash
uv init my-project && cd my-project
uv venv && source .venv/bin/activate
uv pip install mojo \
  --extra-index-url https://modular.gateway.scarf.sh/simple/
```

---

## pip

Standard Python package manager.

### Nightly

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --pre mojo \
  --index-url https://dl.modular.com/public/nightly/python/simple/
```

### Stable

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install mojo \
  --extra-index-url https://modular.gateway.scarf.sh/simple/
```

---

## Conda

For conda/mamba users.

### Nightly

```bash
conda install -c conda-forge \
  -c https://conda.modular.com/max-nightly/ mojo
```

### Stable (v25.7)

```bash
conda install -c conda-forge \
  -c https://conda.modular.com/max/ "mojo==0.25.7"
```

---

## Version Alignment with MAX

If using MAX with custom Mojo kernels, versions must match:

```bash
# Check alignment
pip show modular | grep Version   # e.g., 26.2.0
mojo --version                    # Must match major.minor (e.g., 0.26.2)
```

Mismatched versions cause kernel compilation failures. Always use the same channel (stable or nightly) for both.

---

## Quick Reference

| Method | Nightly | Stable |
|--------|---------|--------|
| pixi | `pixi add mojo` | `pixi add "mojo==0.25.7"` |
| uv | `uv pip install mojo --index-url https://dl.modular.com/public/nightly/python/simple/ --prerelease allow` | `uv pip install mojo --extra-index-url https://modular.gateway.scarf.sh/simple/` |
| pip | `pip install --pre mojo --index-url https://dl.modular.com/public/nightly/python/simple/` | `pip install mojo --extra-index-url https://modular.gateway.scarf.sh/simple/` |
| conda | `conda install -c conda-forge -c https://conda.modular.com/max-nightly/ mojo` | `conda install -c conda-forge -c https://conda.modular.com/max/ "mojo==0.25.7"` |

---

## References

- [Mojo Installation Guide](https://docs.modular.com/mojo/manual/install)
- [Mojo Stable Docs](https://docs.modular.com/stable/mojo/)
- [Mojo Nightly Docs](https://docs.modular.com/mojo/)
