---
name: debugging
description: Systematic debugging approach for finding and fixing bugs
triggers:
  - "(?i)debug"
  - "(?i)bug"
  - "(?i)not working"
  - "(?i)broken"
  - "(?i)error"
  - "(?i)fix.*issue"
---

# Debugging Skill

When this skill is loaded, follow a systematic debugging approach:

## Debugging Process

### 1. Reproduce the Issue
- Get exact steps to reproduce
- Identify the expected vs actual behavior
- Note any error messages verbatim

### 2. Gather Context
- Read relevant code files
- Check recent changes (git log)
- Look for similar issues/patterns

### 3. Form Hypotheses
List potential causes in order of likelihood:
- Most common: typos, logic errors, wrong variable
- Medium: async/timing issues, state bugs
- Less common: library bugs, environment issues

### 4. Test Hypotheses
- Add logging/print statements
- Run tests in isolation
- Use debugger if available
- Check with minimal reproduction

### 5. Verify the Fix
- Ensure the original issue is resolved
- Check for regressions
- Run existing tests
- Consider edge cases

## Debugging Commands

```bash
# Check recent changes
git log --oneline -10

# Search for related code
grep -r "function_name" .

# Run specific test
pytest tests/test_file.py::test_name -v
```

## Common Patterns

- **Undefined errors**: Check imports and variable scope
- **Type errors**: Verify data types at boundaries
- **Async bugs**: Look for missing await, race conditions
- **State bugs**: Check initialization order
