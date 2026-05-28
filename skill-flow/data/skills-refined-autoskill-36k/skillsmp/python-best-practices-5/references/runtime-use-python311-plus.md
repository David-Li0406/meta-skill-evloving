---
title: Upgrade to Python 3.11+ for Free Performance
impact: LOW
impactDescription: 10-60% faster with zero code changes
tags: runtime, python311, upgrade, interpreter
---

## Upgrade to Python 3.11+ for Free Performance

Python 3.11 introduced significant interpreter optimizations. Upgrading provides 10-60% performance improvement with no code changes.

**Incorrect (running on Python 3.10):**

```python
# requirements.txt
python_requires = ">=3.10"

# pyproject.toml
[project]
requires-python = ">=3.10"
# Missing 10-60% free performance from newer interpreter
```

**Correct (targeting Python 3.11+):**

```python
# requirements.txt
python_requires = ">=3.11"

# pyproject.toml
[project]
requires-python = ">=3.11"
# Same code runs 10-60% faster with zero changes
```

**Version performance comparison:**

```python
# Same code, different Python versions:
# Python 3.10: 100ms baseline
# Python 3.11: 75ms (25% faster)
# Python 3.12: 70ms (30% faster)
# Python 3.13: 65ms (35% faster, with JIT potential)
```

**Check current version:**

```python
import sys
print(f"Python {sys.version_info.major}.{sys.version_info.minor}")
```

**Migration checklist:**
- Test with target Python version
- Update deprecated stdlib usage
- Check third-party library compatibility

Reference: [What's New in Python 3.11](https://docs.python.org/3/whatsnew/3.11.html)
