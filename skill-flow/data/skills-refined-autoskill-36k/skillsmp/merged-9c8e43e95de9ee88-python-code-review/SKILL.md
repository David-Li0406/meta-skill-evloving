---
name: python-code-review
description: Use this skill when performing a comprehensive review of Python code for quality, security, performance, and best practices.
---

# Python Code Review

## Instructions

When reviewing Python code, follow this comprehensive review format:

1. **Read target files** from the provided arguments.
2. **Check each dimension** listed below.
3. **Report findings** with severity and location.
4. **Suggest fixes** with code examples.

## Review Dimensions

### 1. Strengths Section (✅)
Identify and highlight what's working well:
- Good code organization and structure
- Proper use of Python idioms and patterns
- Clear documentation (docstrings, comments)
- Appropriate error handling
- Good naming conventions
- Proper use of language features

### 2. Issues & Concerns Section (⚠️)
Categorize issues by severity:

**Critical Bugs:**
- Runtime errors (ZeroDivisionError, IndexError, etc.)
- Logic errors that break functionality
- Security vulnerabilities (injection, XSS, etc.)
- Reference specific line numbers using format: `filename:line_number`

**Recommendations:**
- Code quality improvements
- Better error handling
- Edge case handling
- Performance optimizations
- Code maintainability issues

### 3. Type Safety
**Check for:**
- Missing type hints on function parameters and return types
- Use of `Any` without justification
- Legacy typing imports (`List`, `Dict`, `Optional`, `Union`)
- Missing Protocol definitions for duck typing
- Incorrect use of TypeVar, Generic, or ParamSpec

### 4. Error Handling
**Check for:**
- Bare `except:` or `except Exception:`
- Swallowed exceptions (catch and ignore)
- Missing context in re-raised exceptions
- Non-specific exception types

### 5. Security
**Check for:**
- SQL queries with string formatting (injection risk)
- `subprocess.run(..., shell=True)` with user input
- Hardcoded credentials or API keys
- `eval()` or `exec()` with external input
- Missing input validation

### 6. Performance
**Check for:**
- List membership checks instead of sets (`in list` vs `in set`)
- String concatenation in loops
- Repeated function calls that could be cached
- N+1 query patterns

### 7. Modern Patterns
**Check for:**
- Legacy typing imports when builtin generics available
- Missing walrus operator opportunities
- If/elif chains that should be match-case

### 8. Code Structure
**Check for:**
- Functions longer than 50 lines
- Classes with too many responsibilities
- Deep nesting (more than 3 levels)
- Circular imports
- Dead code (unreachable or unused)

### 9. Documentation
**Check for:**
- Public functions without docstrings
- Outdated docstrings (don't match signature)
- Missing type information in docstrings when types unclear

## Review Checklist

Always check for:
- [ ] Division by zero or similar runtime errors
- [ ] Empty collection handling (lists, dicts, etc.)
- [ ] Input validation and sanitization
- [ ] Exception handling completeness
- [ ] Resource management (file handles, connections)
- [ ] Security vulnerabilities (OWASP Top 10)
- [ ] Type correctness and potential type errors
- [ ] Function side effects and purity
- [ ] Code duplication and DRY principle
- [ ] Naming clarity and consistency

## Report Format

For each finding, report:

````text
## [SEVERITY] [Category]: [Brief Description]

**Location**: `file.py:123` in `function_name`

**Issue**: Detailed explanation of the problem.

**Fix**:
```python
# Suggested fix with code example
````

**Impact**: Why this matters (security, performance, reliability).

````

## Summary Format

End the review with:

```text
## Review Summary

**Files Reviewed**: [count]
**Total Findings**: [count]

| Severity | Count |
|----------|-------|
| Critical | X     |
| High     | X     |
| Medium   | X     |
| Low      | X     |

**Top Issues**:
1. [Most important issue]
2. [Second most important issue]
3. [Third most important issue]

**Recommendation**: [APPROVE / REQUEST CHANGES / BLOCK]
```

## References

- [OWASP Python Security](https://owasp.org/www-project-web-security-testing-guide/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)