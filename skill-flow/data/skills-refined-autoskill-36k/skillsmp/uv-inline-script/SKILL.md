---
name: uv-inline-script
description: Runs single-file Python scripts with PEP 723 inline dependencies using uv. Use when writing standalone scripts that need external packages without a project, virtualenv, or requirements.txt.
---

# uv Inline Scripts

Embed dependencies directly in single-file scripts. No requirements.txt, no manual venv, no project setup.

## Inline Metadata Block

```python
# /// script
# dependencies = ["requests", "pandas>=2.0"]
# requires-python = ">=3.11"
# ///

import requests
import pandas as pd
```

uv creates an ephemeral venv, installs deps, runs the script, caches for next time.

## Scaffold & Manage

```bash
uv init --script example.py --python 3.12    # create script with metadata block
uv add --script example.py 'requests<3'      # add deps to existing script
```

## Run

```bash
uv run script.py                      # use inline deps
uv run --python 3.12 script.py        # override interpreter
uv run --with httpx script.py         # add dep at runtime without editing file
```

## Advanced Options

```python
# /// script
# dependencies = ["requests"]
# requires-python = ">=3.12"
# [tool.uv]
# index-url = "https://custom.pypi.org/simple"
# exclude-newer = "2024-01-01T00:00:00Z"  # pin resolution to date for reproducibility
# ///
```

Note: Inline metadata takes precedence—project deps are ignored even when script is inside a project directory.

