---
name: validate-syntax
description: >
  L1-L4 語法和結構驗證 - 檢查 Python 語法、AST 結構、縮進格式、命名規範。
  BlueMouse 17-Layer Validation Group 1。
  Triggers: "syntax", "格式檢查", "naming", "PEP8"
allowed-tools:
  - Read
  - Bash
user-invocable: true
context: fork
---

# Validate Syntax Skill (L1-L4)

BlueMouse 17-Layer Validation System - Group 1: 語法和結構驗證

## Two Ways to Use

### 1. AI-Guided Validation
Follow the checklist below to analyze code.

### 2. Script Execution
```bash
python3 .claude/skills/validate-syntax/validator.py myfile.py
python3 .claude/skills/validate-syntax/validator.py --json myfile.py
```

---

# L1-L4 Validation Checklist

## L1: 基本語法檢查

**What**: Code compiles without syntax errors

**How**:
```python
compile(code, '<string>', 'exec')
```

**Pass**: No SyntaxError raised
**Fail**: Report error: `"語法錯誤: {error_message}"`

---

## L2: AST 結構檢查

**What**: Code contains at least one function or class definition

**How**:
```python
tree = ast.parse(code)
has_definition = any(
    isinstance(node, (ast.FunctionDef, ast.ClassDef))
    for node in ast.walk(tree)
)
```

**Pass**: `has_definition == True`
**Fail**: `"缺少函數或類定義"`

---

## L3: 縮進和格式檢查

**What**: Proper indentation format

**Rules**:
1. No tab characters (`\t`) anywhere
2. Leading spaces must be multiples of 4

**How**:
```python
for i, line in enumerate(lines, 1):
    if '\t' in line:
        issues.append(f"Line {i}: 使用 Tab 而非空格")
    leading_spaces = len(line) - len(line.lstrip())
    if leading_spaces % 4 != 0:
        issues.append(f"Line {i}: 縮進不是 4 的倍數")
```

**Pass**: No issues found
**Fail**: `"發現 N 個格式問題"` + list first 3 issues

**Examples**:
```python
# ✅ PASS: 4-space indentation
def foo():
    if True:
        return 1

# ❌ FAIL: Tab character
def foo():
	return 1  # Uses tab

# ❌ FAIL: 2-space indentation
def foo():
  return 1  # 2 spaces, not multiple of 4
```

---

## L4: 命名規範檢查

**What**: PEP 8 naming conventions

**Rules**:
| Type | Convention | Regex |
|------|------------|-------|
| Functions | snake_case | `^[a-z_][a-z0-9_]*$` |
| Classes | PascalCase | `^[A-Z][a-zA-Z0-9]*$` |

**How**:
```python
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
            issues.append(f"函數名 '{node.name}' 不符合 snake_case")
    if isinstance(node, ast.ClassDef):
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
            issues.append(f"類名 '{node.name}' 不符合 PascalCase")
```

**Pass**: All names follow conventions → `"命名符合 PEP 8"`
**Fail**: `"發現 N 個命名問題"` + list issues

**Examples**:
```python
# ✅ PASS
def calculate_total():  # snake_case
    pass

class UserManager:  # PascalCase
    pass

# ❌ FAIL
def CalculateTotal():  # Should be snake_case
    pass

class user_manager:  # Should be PascalCase
    pass
```

---

## Output Format

```
==================================================
L1-L4: 語法和結構驗證
==================================================

Status: ✅ PASSED / ❌ FAILED
Score: X/100 (N/4 layers)

✅/❌ L1: 基本語法檢查 - [message]
✅/❌ L2: AST 結構檢查 - [message]
✅/❌ L3: 縮進和格式檢查 - [message]
✅/❌ L4: 命名規範檢查 - [message]
```

---

## Related Skills

| Skill | Layers |
|-------|--------|
| `/validate-17-layers` | L1-L17 (完整) |
| `/validate-syntax` | **L1-L4** |
| `/validate-signature` | L5-L8 |
| `/validate-dependencies` | L9-L12 |
| `/validate-logic` | L13-L17 |

---

*Part of BlueMouse 17-Layer Validation System*
