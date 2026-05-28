# LSP Integration Patterns

LSP (Language Server Protocol) provides structural code intelligence that complements the AI-powered MCP fidelity review. Use LSP for fast, deterministic checks; use MCP for semantic analysis.

## Pre-Review Structural Verification

Before running the expensive AI review, verify structural requirements exist:

**Symbol existence check:**
```python
# Get all symbols in implementation file
symbols = LSP(operation="documentSymbol", filePath="src/auth/service.py", line=1, character=1)

# Expected from spec: class AuthService with methods login(), logout(), refresh_token()
expected_symbols = ["AuthService", "login", "logout", "refresh_token"]

# Compare and identify gaps
# Missing symbols indicate incomplete implementation - no need for AI review yet
```

**Cross-file symbol search:**
```python
# Find implementations across codebase
results = LSP(operation="workspaceSymbol", filePath="src/auth/service.py", line=1, character=1)
# Search for "AuthService" in results to verify it exists somewhere
```

**Quick structural report format:**
```markdown
## Structural Pre-Check: phase-1

| Task | File | Expected Symbols | Status |
|------|------|------------------|--------|
| task-1-1 | src/auth/service.py | AuthService, login, logout | All present |
| task-1-2 | src/auth/validator.py | TokenValidator, validate | MISSING: validate |
| task-1-3 | src/auth/session.py | SessionManager | Present + 1 extra |

**Issues Found:** 1 missing symbol, 1 unexpected symbol
**Recommendation:** Review task-1-2 before full fidelity review
```

## During-Review Type Analysis

When analyzing deviations, use LSP to get precise type information:

```python
# Get type info and documentation for a symbol
hover_info = LSP(operation="hover", filePath="src/auth/service.py", line=45, character=15)

# Useful for understanding:
# - Return types that differ from spec
# - Parameter types that don't match
# - Missing type annotations
```

## Post-Review Deviation Investigation

After MCP identifies deviations, use LSP to understand impact:

**Trace deviation origins:**
```python
# Find where a deviated symbol is defined
definition = LSP(operation="goToDefinition", filePath="src/auth/service.py", line=45, character=10)
# May reveal the deviation originated in a dependency
```

**Assess blast radius:**
```python
# Find all references to deviated code
refs = LSP(operation="findReferences", filePath="src/auth/service.py", line=45, character=10)
# High reference count = high impact deviation
```

**Understand call patterns:**
```python
# What calls this deviated function?
incoming = LSP(operation="incomingCalls", filePath="src/auth/service.py", line=45, character=10)
# Reveals which parts of codebase depend on deviated behavior

# What does this function call?
outgoing = LSP(operation="outgoingCalls", filePath="src/auth/service.py", line=45, character=10)
# Reveals if deviation propagates to other functions
```

## Symbol-to-Spec Mapping

For systematic verification, map spec requirements to LSP operations:

| Spec Requirement | LSP Operation | What to Check |
|------------------|---------------|---------------|
| "Create class X" | `documentSymbol` | Class exists in file |
| "Add method Y to X" | `documentSymbol` | Method exists under class |
| "X should call Y" | `outgoingCalls` | Call relationship exists |
| "Y should be used by Z" | `incomingCalls` | Usage relationship exists |
| "X defined in file F" | `goToDefinition` | Definition location matches |

## Fallback Handling

LSP may be unavailable for some file types or configurations:

```python
# Attempt LSP check
symbols = LSP(operation="documentSymbol", filePath=task.file_path, line=1, character=1)

if symbols.error or not symbols.result:
    # LSP unavailable for this file type
    # Skip structural pre-check, proceed directly to MCP fidelity review
    # Log: "LSP unavailable for {file_path}, skipping structural pre-check"
else:
    # Run structural verification
    # Then proceed to MCP fidelity review
```

**Common LSP-unavailable scenarios:**
- Configuration files (JSON, YAML, TOML)
- Shell scripts without language server
- Unsupported languages
- Files outside project root
