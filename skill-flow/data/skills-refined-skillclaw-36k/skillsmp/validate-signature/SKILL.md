---
name: validate-signature
description: >
  L5-L8 函數簽名驗證 - 檢查參數、返回值、類型提示、文檔字符串。
  BlueMouse 17-Layer Validation Group 2。
  Triggers: "signature", "參數檢查", "type hints", "docstring"
allowed-tools:
  - Read
  - Bash
user-invocable: true
context: fork
---

# Validate Signature Skill (L5-L8)

BlueMouse 17-Layer Validation System - Group 2: 函數簽名驗證

## Two Ways to Use

### 1. AI-Guided Validation
Follow the checklist below to analyze code.

### 2. Script Execution
```bash
python3 .claude/skills/validate-signature/validator.py myfile.py
python3 .claude/skills/validate-signature/validator.py --spec spec.json myfile.py
```

---

# L5-L8 Validation Checklist

## L5: 參數檢查

**What**: Function has parameters (or matches spec if provided)

**How**:
```python
func = functions[0]  # Check first function
actual_params = set(arg.arg for arg in func.args.args)

if spec and 'inputs' in spec:
    expected_params = set(spec['inputs'])
    passed = expected_params == actual_params
else:
    passed = True  # No spec, just report count
```

**Pass**:
- With spec: `"參數與規格匹配"`
- Without spec: `"函數有 N 個參數"`

**Fail**: `"參數不匹配: 期望 {expected}, 實際 {actual}"`

---

## L6: 返回值檢查

**What**: Function has explicit `return` statement

**How**:
```python
has_return = any(
    isinstance(node, ast.Return)
    for node in ast.walk(func)
)
```

**Pass**: `"函數有返回值"`
**Fail**: `"函數缺少返回值"`

**Examples**:
```python
# ✅ PASS
def process(data):
    return data * 2

# ❌ FAIL
def process(data):
    print(data)  # No return
```

---

## L7: 類型提示檢查

**What**: Type hints coverage ≥80% AND has return type annotation

**How**:
```python
params_with_hints = sum(1 for arg in func.args.args if arg.annotation)
total_params = len(func.args.args)
has_return_hint = func.returns is not None

if total_params > 0:
    coverage = params_with_hints / total_params
else:
    coverage = 1.0 if has_return_hint else 0.0

passed = coverage >= 0.8 and has_return_hint
```

**Pass**: `"類型提示覆蓋率: {coverage}%"`
**Fail**: `"類型提示不足: {coverage}%"`

**Coverage Examples**:
| Params | Annotated | Coverage | Return Type | Result |
|--------|-----------|----------|-------------|--------|
| 5 | 5 | 100% | ✅ | ✅ PASS |
| 5 | 4 | 80% | ✅ | ✅ PASS |
| 5 | 3 | 60% | ✅ | ❌ FAIL |
| 5 | 5 | 100% | ❌ | ❌ FAIL |

**Examples**:
```python
# ✅ PASS: 100% coverage + return type
def process(data: list, count: int) -> dict:
    return {}

# ❌ FAIL: Missing return type
def process(data: list, count: int):
    return {}

# ❌ FAIL: <80% coverage
def process(data, count: int) -> dict:  # 50%
    return {}
```

---

## L8: 文檔字符串檢查

**What**: Function has meaningful docstring (>10 characters)

**How**:
```python
docstring = ast.get_docstring(func)
passed = docstring and len(docstring) > 10
```

**Pass**: `"有完整文檔字符串 ({length} 字符)"`
**Fail**: `"缺少或文檔字符串過短"`

**Examples**:
```python
# ✅ PASS: >10 characters
def process(data):
    """Process input data and return results."""
    return data

# ❌ FAIL: Too short (≤10 chars)
def process(data):
    """Process"""
    return data

# ❌ FAIL: No docstring
def process(data):
    return data
```

---

## Output Format

```
==================================================
L5-L8: 函數簽名驗證
==================================================

Status: ✅ PASSED / ❌ FAILED
Score: X/100 (N/4 layers)

✅/❌ L5: 參數檢查 - [message]
✅/❌ L6: 返回值檢查 - [message]
✅/❌ L7: 類型提示檢查 - [message]
✅/❌ L8: 文檔字符串檢查 - [message]
```

---

## Related Skills

| Skill | Layers |
|-------|--------|
| `/validate-17-layers` | L1-L17 (完整) |
| `/validate-syntax` | L1-L4 |
| `/validate-signature` | **L5-L8** |
| `/validate-dependencies` | L9-L12 |
| `/validate-logic` | L13-L17 |

---

*Part of BlueMouse 17-Layer Validation System*
