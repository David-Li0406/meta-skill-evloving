---
name: uv
description: Use when managing Python dependencies, running scripts, or working in Python projects. Triggers on pip install, dependency management, virtual environments, or running Python scripts.
---

# Package Management with uv

Use `uv` exclusively for all Python dependency management. Never use `pip`, `pip-tools`, or `poetry` directly.

## Project Dependencies

```bash
# Add or upgrade
uv add <package>

# Remove
uv remove <package>

# Reinstall from lock file
uv sync
```

## Scripts

Run scripts with proper dependencies:

```bash
uv run script.py
```

### Inline Script Metadata

Scripts can declare dependencies inline:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "pandas",
# ]
# ///

import requests
import pandas as pd
# ...
```

### Managing Script Dependencies

```bash
# Add dependency to script
uv add package-name --script script.py

# Remove from script
uv remove package-name --script script.py

# Sync script dependencies
uv sync --script script.py
```

## Quick Reference

| Task | Command |
|------|---------|
| Add package | `uv add <pkg>` |
| Remove package | `uv remove <pkg>` |
| Sync from lock | `uv sync` |
| Run script | `uv run script.py` |
| Add to script | `uv add <pkg> --script script.py` |
