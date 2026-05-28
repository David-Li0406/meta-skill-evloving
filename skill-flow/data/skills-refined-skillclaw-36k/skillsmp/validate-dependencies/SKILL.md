---
name: validate-dependencies
description: >
  L9-L12 依賴關係驗證 - 檢查導入語句、標準庫、第三方庫、循環依賴。
  BlueMouse 17-Layer Validation Group 3。
  Triggers: "dependencies", "imports", "依賴檢查", "circular"
allowed-tools:
  - Read
  - Bash
  - Grep
user-invocable: true
context: fork
---

# Validate Dependencies Skill (L9-L12)

BlueMouse 17-Layer Validation System - Group 3: 依賴關係驗證

## Two Ways to Use

### 1. AI-Guided Validation
Follow the checklist below to analyze code.

### 2. Script Execution
```bash
python3 .claude/skills/validate-dependencies/validator.py myfile.py
python3 .claude/skills/validate-dependencies/validator.py --verbose myfile.py
```

---

# L9-L12 Validation Checklist

## L9: 導入檢查 (Informational)

**What**: Count import statements in code

**How**:
```python
imports = [
    node for node in ast.walk(tree)
    if isinstance(node, (ast.Import, ast.ImportFrom))
]
```

**Output**: `"找到 N 個導入語句"`
**Pass**: Always (informational only)

---

## L10: 標準庫檢查 (Informational)

**What**: Identify Python standard library usage

**Known Stdlib**:
```python
stdlib = {
    'os', 'sys', 'json', 're', 'datetime', 'typing',
    'asyncio', 'time', 'math', 'hashlib', 'collections',
    'functools', 'itertools', 'pathlib', 'subprocess',
    'threading', 'multiprocessing', 'logging', 'unittest',
    'argparse', 'copy', 'io', 'tempfile'
}
```

**How**:
```python
import_names = []
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for n in node.names:
            import_names.append(n.name.split('.')[0])
    elif isinstance(node, ast.ImportFrom):
        if node.module:
            import_names.append(node.module.split('.')[0])

used = [name for name in import_names if name in stdlib]
```

**Output**: `"精確識別出 N 個標準庫導入"`
**Pass**: Always (informational only)

---

## L11: 第三方庫檢查 (Informational)

**What**: Identify common third-party library usage

**Known Third-Party**:
```python
third_party = {
    'django', 'flask', 'fastapi', 'requests', 'numpy',
    'pandas', 'pytest', 'aiohttp', 'sqlalchemy', 'pydantic',
    'httpx', 'redis', 'celery', 'boto3', 'tensorflow',
    'torch', 'scikit-learn'
}
```

**How**:
```python
used = []
for module in third_party:
    if f"import {module}" in code or f"from {module}" in code:
        used.append(module)
```

**Output**:
- Found: `"使用了 N 個第三方庫"`
- None: `"未使用第三方庫"`

**Pass**: Always (informational only)

---

## L12: 循環依賴檢查 ⚠️

**What**: Detect risky relative imports that may cause circular dependencies

**How**:
```python
for node in ast.walk(tree):
    if isinstance(node, ast.ImportFrom) and node.level > 0:
        has_relative = True
```

**Import Level Explanation**:
| Code | Level | Risk |
|------|-------|------|
| `import os` | 0 | ✅ Safe |
| `from module import x` | 0 | ✅ Safe |
| `from .sibling import x` | 1 | ⚠️ Risky |
| `from ..parent import x` | 2 | ⚠️ Risky |

**Pass**: No relative imports → `"通過 (未檢測到危險的相對導入)"`
**Fail**: `"檢測到相對導入，可能存在循環依賴風險"`

**Examples**:
```python
# ✅ PASS: Absolute imports only
import os
from package.module import func
from typing import Dict

# ❌ FAIL: Relative imports
from .sibling import helper  # level=1
from ..parent import config  # level=2
```

**Why Relative Imports Are Risky**:
```
project/
├── package_a/
│   └── module_a.py  # from ..package_b import func_b
└── package_b/
    └── module_b.py  # from ..package_a import func_a
                     # ❌ Circular dependency!
```

---

## Output Format

```
==================================================
L9-L12: 依賴關係驗證
==================================================

Status: ✅ PASSED / ❌ FAILED
Score: X/100 (N/4 layers)

✅ L9: 導入檢查 - 找到 N 個導入語句
✅ L10: 標準庫檢查 - 精確識別出 N 個標準庫導入
✅ L11: 第三方庫檢查 - 使用了 N 個第三方庫
✅/❌ L12: 循環依賴檢查 - [message]

[Verbose mode shows detected libraries]
```

---

## Related Skills

| Skill | Layers |
|-------|--------|
| `/validate-17-layers` | L1-L17 (完整) |
| `/validate-syntax` | L1-L4 |
| `/validate-signature` | L5-L8 |
| `/validate-dependencies` | **L9-L12** |
| `/validate-logic` | L13-L17 |

---

*Part of BlueMouse 17-Layer Validation System*
