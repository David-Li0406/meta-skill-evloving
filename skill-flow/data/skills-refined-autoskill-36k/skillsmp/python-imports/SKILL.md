---
name: python-imports
description: Python import style guidelines for absolute and relative imports
license: MIT
compatibility: opencode
metadata:
    related_python_guidelines: For general Python development standards, use skill `python-guidelines`
---

# Python Import Style

## What I Do

Provide guidelines for Python import styles with emphasis on absolute imports.

## Import Rules

### Absolute Imports (Recommended)

```python
# ✅ CORRECT - Use absolute imports in regular modules
from module.common.types import TestDesign
from module.consolidate.parsing import parse_p800_raw_results
from package.submodule.utils import helper_function
```

### Relative Imports (Avoid)

```python
# ❌ AVOID - Relative imports in regular modules
from .types import TestDesign
from ..consolidate.parsing import parse_p800_raw_results
```

### Exception: __init__.py Files

```python
# ✅ EXCEPTION - Relative imports allowed in __init__.py only
# Use relative imports when re-exporting from submodules

# In package/__init__.py
from .parsing import parse_data
from .statistics import calculate_stats
from .processing import ProcessResult

# Public API exports
__all__ = ["parse_data", "calculate_stats", "ProcessResult"]
```

## Import Organization

```python
# Standard library imports
import os
import sys
from pathlib import Path
from typing import List, Dict

# Third-party imports
import numpy as np
import pandas as pd
from rich.console import Console

# Local application imports
from package.module import function
from package.module.class_ import ClassName
```

## When to Use Me

Use this skill when:

- Writing import statements
- Organizing module structure
- Refactoring code
- Reviewing imports

## Key Rules

1. **Prefer absolute imports** - More explicit and searchable
2. **Avoid relative imports** - Can be confusing in nested packages
3. **Exception: __init__.py** - Relative imports OK for re-exports
4. **Group by source** - stdlib, third-party, local
5. **No inline imports** - Place all imports at module top

## Rationale

- Absolute imports are explicit about module location
- Easier to search and refactor across codebase
- Prevents ambiguity in nested package structures
- Consistent with project structure documentation
