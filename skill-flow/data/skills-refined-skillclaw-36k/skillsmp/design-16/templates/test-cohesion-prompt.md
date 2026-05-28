# Test Cohesion Validation Prompt

## PURPOSE

Ensure all tests for a journey work together as a cohesive suite. This catches:
- Duplicate test function names
- Conflicting fixtures
- Import collisions
- State pollution between tests
- Missing integration test (INV-L009)

## WHEN TO RUN

After `/design test-validate` passes, before `/design run`:

```
Journey → Spec → PRP → Implement → test-validate → test-cohesion → run
                                          ↑              ↑
                                    Individual       Suite-wide
                                    test quality     cohesion
```

## VALIDATION PROCEDURE

### Step 1: Collect All Test Files

```bash
tests_dir="ralph-tests-{journey}"
test_files=$(ls $tests_dir/test_*.py)
```

### Step 2: Check for Duplicate Function Names

```python
import ast
from collections import Counter

all_functions = []
for test_file in test_files:
    tree = ast.parse(open(test_file).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            all_functions.append((test_file, node.name))

# Find duplicates
names = [f[1] for f in all_functions]
duplicates = [name for name, count in Counter(names).items() if count > 1]

if duplicates:
    print("❌ DUPLICATE TEST NAMES:")
    for name in duplicates:
        locs = [f[0] for f in all_functions if f[1] == name]
        print(f"  {name} in: {locs}")
```

### Step 3: Check Fixture Compatibility

```python
# Extract all fixtures used
fixtures_used = set()
fixtures_defined = set()

for test_file in test_files:
    tree = ast.parse(open(test_file).read())
    for node in ast.walk(tree):
        # Check @pytest.fixture decorators
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if hasattr(decorator, 'attr') and decorator.attr == 'fixture':
                    fixtures_defined.add(node.name)
        # Check function parameters (fixtures used)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            for arg in node.args.args:
                fixtures_used.add(arg.arg)

# Check conftest.py
if Path("conftest.py").exists():
    tree = ast.parse(open("conftest.py").read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if hasattr(decorator, 'attr') and decorator.attr == 'fixture':
                    fixtures_defined.add(node.name)

# Find missing fixtures
builtins = {'request', 'tmp_path', 'capsys', 'capfd', 'caplog', 'monkeypatch'}
missing = fixtures_used - fixtures_defined - builtins
if missing:
    print("❌ MISSING FIXTURES:")
    for name in missing:
        print(f"  {name}")
```

### Step 4: Check Import Collisions

```python
all_imports = {}
for test_file in test_files:
    tree = ast.parse(open(test_file).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                key = alias.asname or alias.name
                if key in all_imports and all_imports[key] != alias.name:
                    print(f"❌ IMPORT COLLISION: {key}")
                    print(f"  {all_imports[key]} in {all_imports[key + '_file']}")
                    print(f"  {alias.name} in {test_file}")
                all_imports[key] = alias.name
                all_imports[key + '_file'] = test_file
```

### Step 5: Run Full Suite Collection (Dry Run)

```bash
cd $tests_dir
pytest --collect-only --quiet 2>&1

# Should output:
# <Function test_xxx>
# <Function test_yyy>
# ...
# N tests collected

# If errors → fixture issues or syntax problems
```

### Step 6: Check State Isolation

```python
# Warn if tests modify module-level state
for test_file in test_files:
    content = open(test_file).read()
    if "global " in content:
        print(f"⚠️ WARNING: {test_file} uses 'global' - may cause state pollution")
    if re.search(r"^\w+\s*=", content, re.MULTILINE):
        # Module-level assignment
        print(f"⚠️ WARNING: {test_file} has module-level state")
```

### Step 7: Verify Integration Test Exists (INV-L009)

```bash
if ! ls $tests_dir/test_*integration*.py 2>/dev/null; then
    echo "❌ MISSING: Integration test (INV-L009)"
    echo "   Expected: test_XX_integration.py or test_integration.py"
fi
```

## OUTPUT FORMAT

```
═══════════════════════════════════════════════════════════════
  TEST COHESION CHECK - ralph-tests-J-010
═══════════════════════════════════════════════════════════════

━━━ Test Count ━━━
  Files: 19
  Test functions: 87
  Integration test: ✓ test_16_integration.py

━━━ Duplicate Names ━━━
  ✓ No duplicates found

━━━ Fixture Analysis ━━━
  Fixtures defined: 5 (conftest.py)
  Fixtures used: 8
  ✓ All fixtures available

━━━ Import Analysis ━━━
  ✓ No collisions

━━━ State Isolation ━━━
  ⚠️ test_05.py uses module-level variable (line 15)

━━━ Suite Collection ━━━
  $ pytest --collect-only
  87 tests collected
  ✓ All tests collectable

───────────────────────────────────────────────────────────────
  STATUS: ✓ COHESIVE (1 warning)
  
  Ready for: /design run
───────────────────────────────────────────────────────────────
```

## BLOCKING BEHAVIOR

| Issue | Severity | Action |
|-------|----------|--------|
| Duplicate function names | ❌ BLOCK | Rename tests |
| Missing fixture | ❌ BLOCK | Add to conftest.py |
| Import collision | ❌ BLOCK | Use aliases |
| Collection failure | ❌ BLOCK | Fix syntax/imports |
| Missing integration test | ❌ BLOCK | Add test_integration.py |
| Module-level state | ⚠️ WARN | Review for isolation |

## MANUAL INVOCATION

```bash
/design test-cohesion ./ralph-tests-J-010
```

## QUICK COHESION CHECKLIST

Before running suite:
- [ ] `pytest --collect-only` succeeds?
- [ ] No duplicate test function names?
- [ ] All fixtures defined in conftest.py?
- [ ] Integration test exists (test_*integration*.py)?
- [ ] No module-level mutable state?
