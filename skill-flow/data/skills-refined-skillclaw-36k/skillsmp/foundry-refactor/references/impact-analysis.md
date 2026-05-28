# Impact Analysis

**NEVER refactor without understanding impact first.**

## LSP-Enhanced Impact Analysis

```
# Get all references to the symbol
references = findReferences(file="src/module.py", symbol="OldClassName", line=10, character=6)

# Analyze results:
- Total reference count
- Unique files affected
- Reference types (import, call, type annotation, assignment)
- Test files vs production files
```

## Impact Report Format

Present to user before proceeding:

```markdown
## Refactoring Impact: Rename OldClassName -> NewClassName

**Total References:** 47 across 12 files

**By Category:**
- Imports: 12 files
- Class instantiation: 8 locations
- Type annotations: 15 locations
- Inheritance: 2 locations

**Files Affected:**
- src/auth/service.py (8 refs)
- src/api/handlers.py (12 refs)
- tests/test_auth.py (15 refs)
- ... (9 more files)

**Risk Assessment:** MEDIUM
- All references in controlled codebase
- Good test coverage (15 test refs)

Proceed? [Execute] [Dry Run] [Cancel]
```

## Fallback Impact Analysis

If LSP unavailable:

```
Use Grep to find references:
Grep(pattern="OldClassName", path="src/", output_mode="content")

WARNING: Grep-based analysis may include false positives (comments, strings).
Review each match before proceeding.
```
