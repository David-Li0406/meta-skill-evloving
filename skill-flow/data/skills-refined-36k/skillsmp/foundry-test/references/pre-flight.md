# Pre-Flight Diagnostics

Detailed LSP-based pre-flight diagnostics for catching import issues before running tests.

## Symbol Resolution Check

Verify test files can resolve their imports using LSP:

```
# Get test file structure
symbols = documentSymbol(file="tests/test_auth.py")

# For key imports, verify targets exist
definition = goToDefinition(file="tests/test_auth.py", symbol="AuthService", line=5)

if definition not found:
    Report: "Import AuthService cannot be resolved - likely import error"
```

## Pre-Flight Report Format

Generate a diagnostic report before running tests:

```markdown
## Pre-Flight Diagnostics

| Test File | Status |
|-----------|--------|
| tests/test_auth.py | OK - all imports resolve |
| tests/test_user.py | WARNING - cannot resolve 'UserService' (line 5) |
| tests/test_api.py | OK |

**Issues Found:** 1 unresolved import
**Recommendation:** Fix import in test_user.py before running full suite

Proceed? [Fix First] [Run Anyway]
```

## LSP Operations Reference

| Operation | Purpose | Example |
|-----------|---------|---------|
| `documentSymbol()` | Get all symbols in file | Find test functions, imports |
| `goToDefinition()` | Verify import resolves | Check if imported class exists |
| `findReferences()` | Find all usages | Trace how a fixture is used |
