---
name: validate-code
description: Use this skill to validate Python code for syntax, dependencies, and function signatures.
---

# Validate Code Skill (L1-L12)

BlueMouse 17-Layer Validation System

## Two Ways to Use

### 1. AI-Guided Validation
Follow the checklist below to analyze code.

### 2. Script Execution
```bash
python3 .claude/skills/validate-code/validator.py myfile.py
python3 .claude/skills/validate-code/validator.py --verbose myfile.py
```

---

# Validation Checklist

## L1: Basic Syntax Check

**What**: Code compiles without syntax errors.

**How**:
```python
compile(code, '<string>', 'exec')
```

**Pass**: No SyntaxError raised.  
**Fail**: Report error: `"Syntax error: {error_message}"`

---

## L2: AST Structure Check

**What**: Code contains at least one function or class definition.

**How**:
```python
tree = ast.parse(code)
has_definition = any(
    isinstance(node, (ast.FunctionDef, ast.ClassDef))
    for node in ast.walk(tree)
)
```

**Pass**: `has_definition == True`  
**Fail**: `"Missing function or class definition"`

---

## L3: Indentation and Formatting Check

**What**: Proper indentation format.

**Rules**:
1. No tab characters (`\t`) anywhere.
2. Leading spaces must be multiples of 4.

**How**:
```python
for i, line in enumerate(lines, 1):
    if '\t' in line:
        issues.append(f"Line {i}: Uses tab instead of spaces")
    leading_spaces = len(line) - len(line.lstrip())
    if leading_spaces % 4 != 0:
        issues.append(f"Line {i}: Indentation is not a multiple of 4")
```

**Pass**: No issues found.  
**Fail**: `"Found N formatting issues"` + list first 3 issues.

---

## L4: Naming Convention Check

**What**: PEP 8 naming conventions.

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
            issues.append(f"Function name '{node.name}' does not follow snake_case")
    if isinstance(node, ast.ClassDef):
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
            issues.append(f"Class name '{node.name}' does not follow PascalCase")
```

**Pass**: All names follow conventions → `"Naming conforms to PEP 8"`  
**Fail**: `"Found N naming issues"` + list issues.

---

## L5: Parameter Check

**What**: Function has parameters (or matches spec if provided).

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
- With spec: `"Parameters match specification"`
- Without spec: `"Function has N parameters"`

**Fail**: `"Parameter mismatch: expected {expected}, actual {actual}"`

---

## L6: Return Value Check

**What**: Function has explicit `return` statement.

**How**:
```python
has_return = any(
    isinstance(node, ast.Return)
    for node in ast.walk(func)
)
```

**Pass**: `"Function has return value"`  
**Fail**: `"Function missing return value"`

---

## L7: Type Hint Check

**What**: Type hints coverage ≥80% AND has return type annotation.

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

**Pass**: `"Type hint coverage: {coverage}%"`  
**Fail**: `"Insufficient type hints: {coverage}%"`

---

## L8: Docstring Check

**What**: Function has meaningful docstring (>10 characters).

**How**:
```python
docstring = ast.get_docstring(func)
passed = docstring and len(docstring) > 10
```

**Pass**: `"Has complete docstring ({length} characters)"`  
**Fail**: `"Missing or docstring too short"`

---

## L9: Import Check (Informational)

**What**: Count import statements in code.

**How**:
```python
imports = [
    node for node in ast.walk(tree)
    if isinstance(node, (ast.Import, ast.ImportFrom))
]
```

**Output**: `"Found N import statements"`  
**Pass**: Always (informational only).

---

## L10: Standard Library Check (Informational)

**What**: Identify Python standard library usage.

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

**Output**: `"Accurately identified N standard library imports"`  
**Pass**: Always (informational only).

---

## L11: Third-Party Library Check (Informational)

**What**: Identify common third-party library usage.

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
- Found: `"Used N third-party libraries"`
- None: `"No third-party libraries used"`

**Pass**: Always (informational only).

---

## L12: Circular Dependency Check ⚠️

**What**: Detect risky relative imports that may cause circular dependencies.

**How**:
```python
for node in ast.walk(tree):
    if isinstance(node, ast.ImportFrom) and node.level > 0:
        has_relative = True
```

**Pass**: No relative imports → `"Passed (no risky relative imports detected)"`  
**Fail**: `"Detected relative imports, potential circular dependency risk"`

---

## Output Format

```
==================================================
L1-L12: Code Validation
==================================================

Status: ✅ PASSED / ❌ FAILED
Score: X/100 (N/12 layers)

✅/❌ L1: Basic Syntax Check - [message]
✅/❌ L2: AST Structure Check - [message]
✅/❌ L3: Indentation and Formatting Check - [message]
✅/❌ L4: Naming Convention Check - [message]
✅/❌ L5: Parameter Check - [message]
✅/❌ L6: Return Value Check - [message]
✅/❌ L7: Type Hint Check - [message]
✅/❌ L8: Docstring Check - [message]
✅ L9: Import Check - Found N import statements
✅ L10: Standard Library Check - Accurately identified N standard library imports
✅ L11: Third-Party Library Check - Used N third-party libraries
✅/❌ L12: Circular Dependency Check - [message]
```

---

## Related Skills

| Skill | Layers |
|-------|--------|
| `/validate-17-layers` | L1-L17 (Complete) |
| `/validate-syntax` | **L1-L4** |
| `/validate-signature` | **L5-L8** |
| `/validate-dependencies` | **L9-L12** |
| `/validate-logic` | L13-L17 |

---

*Part of BlueMouse 17-Layer Validation System*