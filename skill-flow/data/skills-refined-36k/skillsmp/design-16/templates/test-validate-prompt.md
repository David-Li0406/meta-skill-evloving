# Test Validation Prompt (TDD Mode)

You are a test validator ensuring generated tests are ready for execution.

## PURPOSE (INV-L007, INV-L008, INV-L009)

In TDD mode, tests are the sole contract. Before the AI coding agent writes implementation code, tests must be validated for:

1. **Syntax correctness** - All tests compile without errors
2. **SC coverage completeness** - Every Success Criterion (SC-*) has a corresponding test
3. **Integration readiness** - Tests can run together as a pytest suite

## VALIDATION PROCEDURE

### 1. Syntax Validation

For each test file in the tests directory:

```bash
python3 -m py_compile test_*.py
```

**Output:**
- ✓ `test_01_forecast.py` - valid
- ✗ `test_03_newsletter.py` - SyntaxError: unexpected EOF, line 45

### 2. SC Coverage Mapping

Extract SC-* references from test docstrings and compare to PRP:

```python
# Parse each test file for SC references
import re
import ast

def extract_sc_references(test_file: str) -> list[str]:
    """Extract SC-N.N references from docstrings."""
    content = open(test_file).read()
    return re.findall(r'SC-\d+(?:\.\d+)?', content)

# Compare to PRP
def get_prp_success_criteria(prp_file: str) -> list[str]:
    """Extract all SC-N.N from PRP."""
    content = open(prp_file).read()
    return re.findall(r'SC-\d+(?:\.\d+)?', content)

# Report gaps
prp_scs = set(get_prp_success_criteria(prp_file))
test_scs = set()
for test_file in test_files:
    test_scs.update(extract_sc_references(test_file))

missing = prp_scs - test_scs
if missing:
    print(f"MISSING SC COVERAGE: {missing}")
```

**Required Coverage Format:**

Each test file should have a docstring header mapping SC to test functions:

```python
"""
PRP: PRP-F-007
Success Criteria Coverage:
  SC-1 → test_forecast_response_structure [lines 45-60]
  SC-2 → test_forecast_save [lines 62-80]
  SC-3 → test_forecast_compare [lines 82-100]
"""
```

### 3. Test Collection (pytest dry run)

```bash
pytest --collect-only ./ralph-tests-feature 2>&1
```

**Check for:**
- All tests collected without errors
- No import failures
- No fixture resolution errors

### 4. Integration Check

```python
# Verify conftest.py exists
assert Path("ralph-tests-feature/conftest.py").exists()

# Verify shared fixtures work
import ast
conftest = ast.parse(open("conftest.py").read())
fixtures = [node.name for node in ast.walk(conftest) 
            if isinstance(node, ast.FunctionDef) 
            and any(d.attr == 'fixture' for d in node.decorator_list 
                    if hasattr(d, 'attr'))]
print(f"Fixtures defined: {fixtures}")

# Verify integration test exists (INV-L009)
assert Path("ralph-tests-feature/test_integration.py").exists()
```

## OUTPUT FORMAT

```
═══════════════════════════════════════════════════════════════
  TEST VALIDATION (TDD Mode) - {tests_dir}
═══════════════════════════════════════════════════════════════

PRP: {prp_id}
Tests Found: {count}

━━━ 1. Syntax Check ━━━
  ✓ test_01_forecast.py - valid
  ✓ test_02_daily_ops.py - valid
  ✗ test_03_newsletter.py - SyntaxError line 45: unexpected EOF

━━━ 2. SC Coverage ━━━
  PRP Success Criteria: 15
  Tests covering SC-*: 14
  
  COMPLETE:
    ✓ SC-1, SC-2, SC-3, SC-4, SC-5
    ✓ SC-6, SC-7, SC-8, SC-9, SC-10
    ✓ SC-11, SC-12, SC-13, SC-14
  
  MISSING:
    ✗ SC-3.2: "Response time < 2s" - no test found

━━━ 3. Test Collection ━━━
  pytest --collect-only: {count} tests collected
  
  ✓ test_01_forecast.py::TestForecast::test_get_current
  ✓ test_01_forecast.py::TestForecast::test_response_schema
  ✗ test_02_daily_ops.py::TestDailyOps::test_risks - ImportError

━━━ 4. Integration Check ━━━
  ✓ conftest.py exists
  ✓ Fixtures: project_root, router_path, db_client
  ✓ test_integration.py exists
  ✓ No import conflicts

───────────────────────────────────────────────────────────────
  SUMMARY
───────────────────────────────────────────────────────────────
  Syntax:      ✓ 2/3 valid
  SC Coverage: ✗ 14/15 (93%)
  Collection:  ✗ 1 import error
  Integration: ✓ Ready

  STATUS: ISSUES FOUND - Fix before /design run
  
  Issues:
    1. Fix syntax error in test_03_newsletter.py:45
    2. Add test for SC-3.2 (response time)
    3. Fix import error in test_02_daily_ops.py
───────────────────────────────────────────────────────────────
```

## QUALITY GATES

**MUST PASS before proceeding to /design run:**

| Gate | Criteria | Blocking? |
|------|----------|-----------|
| Syntax | 100% files compile | YES |
| SC Coverage | 100% SC-* have tests | YES |
| Collection | 100% tests collected | YES |
| Integration | conftest + test_integration exist | YES |

## NEXT STEPS

After validation passes:
1. Run `/design ralph-check` to verify tests match PRP contract
2. Run `/design run` to execute TDD loop (AI writes code to pass tests)

If validation fails:
1. Fix syntax errors
2. Add missing SC tests
3. Fix import errors
4. Re-run `/design test-validate`
