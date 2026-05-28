---
name: validate-17-layers
description: >
  BlueMouse 17-Layer Code Validation System - Complete Python code quality validation
  covering syntax, structure, function signatures, dependencies, types, logic, security,
  and performance. Triggers: "validate", "17層驗證", "code quality", "v17"
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
user-invocable: true
context: fork
---

# BlueMouse 17-Layer Validation Skill

Complete code validation system from the BlueMouse AI Safety project. Validates Python code across 17 dimensions.

## Two Ways to Use

### 1. AI-Guided Validation (Recommended)

When user requests code validation, follow the **17-Layer Checklist** below to analyze the code.

### 2. Script Execution

```bash
python3 .claude/skills/validate-17-layers/validator.py myfile.py
python3 .claude/skills/validate-17-layers/validator.py --json myfile.py
```

---

# 17-Layer Validation Checklist

When validating Python code, check ALL 17 layers in order:

## Group 1: L1-L4 語法和結構驗證

### L1: 基本語法檢查
**What**: Code compiles without syntax errors
**How**: `compile(code, '<string>', 'exec')`
**Pass**: No SyntaxError
**Fail**: Report syntax error location and message

### L2: AST 結構檢查
**What**: Code contains function or class definitions
**How**: Parse AST, check for `FunctionDef` or `ClassDef` nodes
**Pass**: At least one function or class defined
**Fail**: "缺少函數或類定義"

### L3: 縮進和格式檢查
**What**: Proper indentation
**How**: Check each line:
- No tab characters (`\t`)
- Leading spaces are multiples of 4
**Pass**: All lines follow rules
**Fail**: Report lines with issues (max 3)

### L4: 命名規範檢查
**What**: PEP 8 naming conventions
**How**:
- Functions: `^[a-z_][a-z0-9_]*$` (snake_case)
- Classes: `^[A-Z][a-zA-Z0-9]*$` (PascalCase)
**Pass**: All names follow conventions
**Fail**: Report non-compliant names

---

## Group 2: L5-L8 函數簽名驗證

### L5: 參數檢查
**What**: Function has parameters (or matches spec if provided)
**How**: Extract function arguments from AST
**Pass**: Has parameters or matches spec
**Fail**: "參數不匹配" with expected vs actual

### L6: 返回值檢查
**What**: Function has explicit return statement
**How**: Check for `ast.Return` nodes in function body
**Pass**: Has at least one `return`
**Fail**: "函數缺少返回值"

### L7: 類型提示檢查
**What**: Type hints coverage ≥80% and has return type
**How**:
```
coverage = params_with_annotations / total_params
passed = coverage >= 0.8 AND has_return_type_hint
```
**Pass**: Coverage ≥80% with return type
**Fail**: "類型提示不足: X%"

### L8: 文檔字符串檢查
**What**: Meaningful docstring (>10 characters)
**How**: `ast.get_docstring(func)`
**Pass**: Docstring length > 10
**Fail**: "缺少或文檔字符串過短"

---

## Group 3: L9-L12 依賴關係驗證

### L9: 導入檢查
**What**: Count import statements
**How**: Count `ast.Import` and `ast.ImportFrom` nodes
**Pass**: Always (informational)
**Output**: "找到 N 個導入語句"

### L10: 標準庫檢查
**What**: Identify stdlib usage
**How**: Match imports against known stdlib:
```
{os, sys, json, re, datetime, typing, asyncio, time, math, hashlib}
```
**Pass**: Always (informational)
**Output**: "精確識別出 N 個標準庫導入"

### L11: 第三方庫檢查
**What**: Identify third-party library usage
**How**: Match imports against common packages:
```
{django, flask, fastapi, requests, numpy, pandas}
```
**Pass**: Always (informational)
**Output**: "使用了 N 個第三方庫"

### L12: 循環依賴檢查
**What**: Detect risky relative imports
**How**: Check `ast.ImportFrom` nodes where `level > 0`
```python
from ..module import x  # level=2, RISKY
from .sibling import y  # level=1, RISKY
```
**Pass**: No relative imports
**Fail**: "檢測到相對導入，可能存在循環依賴風險"

---

## Group 4: L13-L17 類型和邏輯驗證

### L13: 類型一致性檢查
**What**: All functions have ≥70% type hint coverage
**How**: Scan all functions, calculate overall coverage
**Pass**: Coverage ≥70%
**Fail**: "函數類型提示覆蓋率: X%"

### L14: 邏輯完整性檢查
**What**: Code has control flow structures
**How**: Check for `ast.If`, `ast.For`, `ast.While`
**Pass**: Always (informational)
**Output**: "邏輯結構完整" or "邏輯結構簡單"

### L15: 錯誤處理檢查 ⚠️ ANTI-PATTERN DETECTION
**What**: No empty try-except blocks
**How**: Find `ast.Try` nodes, check handlers:
```python
# ❌ FAIL: Empty handler
except:
    pass

# ❌ FAIL: Only pass
except Exception as e:
    pass

# ✅ PASS: Actual handling
except Exception as e:
    logger.error(e)
    raise
```
**Pass**: Has try-except AND no empty/pass-only handlers
**Fail**: "發現 N 個空的或只有 pass 的錯誤處理塊 (Anti-pattern)"

### L16: 安全性檢查 🔒 SECURITY SCAN
**What**: No dangerous functions or hardcoded secrets
**How**:
1. Dangerous functions:
   - `eval()` - arbitrary code execution
   - `exec()` - arbitrary code execution
   - `pickle` - deserialization vulnerability
2. Hardcoded secrets (regex):
   - `api_key\s*=\s*[\'"][^\s*]{10,}[\'"]`
   - `password\s*=\s*[\'"][^\s*]{8,}[\'"]`
**Pass**: No dangerous functions AND no hardcoded secrets
**Fail**: "發現 N 個潛在安全性問題" with list

### L17: 性能檢查 ⚡ COMPLEXITY ANALYSIS
**What**: No deeply nested loops (≥3 levels)
**How**: Calculate maximum loop nesting depth
```python
# ❌ FAIL: 3-level nesting
for i in range(n):      # Level 1
    for j in range(n):  # Level 2
        for k in range(n):  # Level 3 - TOO DEEP
            pass

# ✅ PASS: 2-level nesting
for i in range(n):      # Level 1
    for j in range(n):  # Level 2
        pass
```
**Pass**: max_depth < 3
**Fail**: "檢測到過深的循環嵌套 (Depth: N)，建議優化算法"

---

## Output Format

When reporting results, use this format:

```
============================================================
BlueMouse 17-Layer Validation Report
============================================================

Status: ✅ PASSED / ❌ FAILED
Quality Score: X/100
Layers Passed: N/17

------------------------------------------------------------
Layer Results:
------------------------------------------------------------

L1-L4: 語法和結構:
  ✅/❌ L1: 基本語法檢查 - [message]
  ✅/❌ L2: AST 結構檢查 - [message]
  ✅/❌ L3: 縮進和格式檢查 - [message]
  ✅/❌ L4: 命名規範檢查 - [message]

L5-L8: 函數簽名:
  ✅/❌ L5: 參數檢查 - [message]
  ✅/❌ L6: 返回值檢查 - [message]
  ✅/❌ L7: 類型提示檢查 - [message]
  ✅/❌ L8: 文檔字符串檢查 - [message]

L9-L12: 依賴關係:
  ✅/❌ L9: 導入檢查 - [message]
  ✅/❌ L10: 標準庫檢查 - [message]
  ✅/❌ L11: 第三方庫檢查 - [message]
  ✅/❌ L12: 循環依賴檢查 - [message]

L13-L17: 類型和邏輯:
  ✅/❌ L13: 類型一致性檢查 - [message]
  ✅/❌ L14: 邏輯完整性檢查 - [message]
  ✅/❌ L15: 錯誤處理檢查 - [message]
  ✅/❌ L16: 安全性檢查 - [message]
  ✅/❌ L17: 性能檢查 - [message]

Suggestions (top 5 failed layers):
  1. [L#] ([name]): [message]
  ...
============================================================
```

## Quality Score Calculation

```
quality_score = (passed_layers / 17) * 100
```

---

## Related Skills

| Skill | Layers | 用途 |
|-------|--------|------|
| `/validate-17-layers` | L1-L17 | 完整驗證 |
| `/validate-syntax` | L1-L4 | 語法和結構 |
| `/validate-signature` | L5-L8 | 函數簽名 |
| `/validate-dependencies` | L9-L12 | 依賴關係 |
| `/validate-logic` | L13-L17 | 類型和邏輯 |

---

*Part of BlueMouse v6.6 AI Safety Layer*
