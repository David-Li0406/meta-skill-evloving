---
name: code-review
description: Perform automated code reviews with best practices, security checks, and refactoring suggestions. Use when reviewing code, checking for vulnerabilities, or analyzing code quality.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review Skill

Perform comprehensive code reviews following industry best practices.

## 1. Security Review

Check for OWASP Top 10 vulnerabilities:

**SQL Injection:**
```bash
# Search for SQL injection risks
grep -r "execute.*\+" . --include="*.py" --include="*.js" --include="*.php"
grep -r "query.*\+" . --include="*.py" --include="*.js"
grep -r "SELECT.*%" . --include="*.py"
```

**XSS (Cross-Site Scripting):**
```bash
# Check for unescaped output
grep -r "innerHTML\s*=" . --include="*.js" --include="*.jsx"
grep -r "dangerouslySetInnerHTML" . --include="*.jsx" --include="*.tsx"
grep -r "render_template_string" . --include="*.py"
```

**Command Injection:**
```bash
# Check for command injection
grep -r "exec\|eval\|system\|shell_exec" . --include="*.py" --include="*.js" --include="*.php"
grep -r "os\.system\|subprocess\.call" . --include="*.py"
grep -r "child_process\.exec" . --include="*.js"
```

**Hardcoded Secrets:**
```bash
# Find potential secrets
grep -r "password\s*=\s*['\"]" . --include="*.py" --include="*.js" --include="*.java"
grep -r "api_key\s*=\s*['\"]" . --include="*.py" --include="*.js"
grep -r "secret\s*=\s*['\"]" . --include="*.py" --include="*.js"
grep -r "Bearer\s\+[A-Za-z0-9]" . --include="*.py" --include="*.js"
```

**Insecure Deserialization:**
```bash
# Check for insecure deserialization
grep -r "pickle\.loads\|yaml\.load\|eval\|exec" . --include="*.py"
grep -r "JSON\.parse.*localStorage" . --include="*.js"
grep -r "unserialize" . --include="*.php"
```

## 2. Code Quality Review

**Complexity Analysis:**
```bash
# Find long functions (potential complexity issues)
grep -n "def \|function " . -r --include="*.py" --include="*.js" | while read line; do
    echo "$line"
done

# Find files with too many lines
find . -name "*.py" -o -name "*.js" | xargs wc -l | sort -rn | head -20
```

**Code Smells:**
```bash
# Find duplicate code patterns
# God classes (too many methods)
grep -c "def \|function " **/*.py **/*.js

# Long parameter lists
grep "def.*,.*,.*,.*,.*," . -r --include="*.py"
grep "function.*,.*,.*,.*,.*," . -r --include="*.js"

# Magic numbers
grep -r "\s[0-9]\{3,\}" . --include="*.py" --include="*.js" | grep -v "test"
```

**Naming Conventions:**
```bash
# Check naming conventions
# Python: snake_case for functions
grep "def [A-Z]" . -r --include="*.py"

# JavaScript: camelCase for functions
grep "function [a-z_]" . -r --include="*.js"

# Constants should be UPPER_CASE
grep "const [a-z]" . -r --include="*.js" --include="*.ts"
```

## 3. Best Practices Review

**Error Handling:**
```bash
# Find bare except clauses (Python)
grep -r "except:" . --include="*.py"

# Find empty catch blocks (JavaScript)
grep -A2 "catch\s*(" . -r --include="*.js" | grep -A1 "{\s*}"

# Find TODO/FIXME comments
grep -r "TODO\|FIXME\|HACK\|XXX" . --include="*.py" --include="*.js" --include="*.java"
```

**Resource Management:**
```bash
# Find files opened without 'with' statement (Python)
grep -r "open(" . --include="*.py" | grep -v "with"

# Find potential memory leaks
grep -r "addEventListener" . --include="*.js" | grep -v "removeEventListener"
```

**Documentation:**
```bash
# Find functions without docstrings (Python)
grep -B1 "def " . -r --include="*.py" | grep -v '"""' | grep -v "'''" | grep -v "#"

# Find exported functions without JSDoc (JavaScript)
grep "export function" . -r --include="*.js" | grep -B3 -v "/\*\*"
```

## 4. Performance Review

**N+1 Query Problems:**
```bash
# Find potential N+1 queries
grep -r "for.*in\|forEach" . --include="*.py" --include="*.js" -A5 | grep "query\|find\|get"
```

**Inefficient Algorithms:**
```bash
# Nested loops (potential O(n²))
grep -r "for.*in" . --include="*.py" --include="*.js" -A3 | grep "for.*in"

# Multiple database calls in loops
grep -r "for\|while" . --include="*.py" --include="*.js" -A5 | grep "query\|execute\|find"
```

**Large File Operations:**
```bash
# Check for files read entirely into memory
grep -r "read()\|readlines()\|readFile" . --include="*.py" --include="*.js"
```

## 5. Dependency Review

**Outdated Dependencies:**
```bash
# Check for outdated npm packages
npm outdated

# Check for Python package updates
pip list --outdated

# Security vulnerabilities
npm audit
pip-audit
```

**Unused Imports:**
```bash
# Python unused imports
grep -r "^import\|^from" . --include="*.py" | cut -d: -f2 | sort | uniq

# JavaScript unused imports
grep -r "^import" . --include="*.js" --include="*.jsx" | cut -d: -f2 | sort | uniq
```

## 6. Testing Coverage

**Missing Tests:**
```bash
# Find source files without corresponding test files
for file in src/**/*.py; do
    testfile="tests/test_$(basename $file)"
    [ ! -f "$testfile" ] && echo "Missing test: $testfile for $file"
done

# Find functions without tests
grep "def test_" tests/ -r | cut -d: -f2 | sort
```

**Test Quality:**
```bash
# Find tests without assertions
grep -r "def test_" . --include="test_*.py" -A10 | grep -v "assert"

# Find disabled tests
grep -r "@skip\|@unittest.skip\|test.skip" . --include="*.py" --include="*.js"
```

## 7. Code Review Checklist

When reviewing code, check:

**Functionality:**
- Does the code do what it's supposed to do?
- Are edge cases handled?
- Is error handling appropriate?

**Security:**
- No SQL injection vulnerabilities
- No XSS vulnerabilities
- No hardcoded secrets
- Input validation present
- Output encoding applied

**Performance:**
- No N+1 query problems
- Efficient algorithms used
- Proper indexing on database queries
- No unnecessary loops or operations

**Maintainability:**
- Code is readable and well-organized
- Proper naming conventions
- Adequate comments and documentation
- Functions are small and focused
- DRY principle followed

**Testing:**
- Unit tests present
- Tests cover edge cases
- Tests are maintainable
- Good test coverage

**Dependencies:**
- No unnecessary dependencies
- Dependencies are up to date
- No known vulnerabilities

## 8. Automated Code Review Tools

**Python:**
```bash
# Linting
pylint src/
flake8 src/
black --check src/

# Security
bandit -r src/
safety check

# Complexity
radon cc src/ -a
radon mi src/
```

**JavaScript:**
```bash
# Linting
eslint .
prettier --check .

# Security
npm audit
snyk test

# Complexity
npx complexity-report src/
```

**Type Checking:**
```bash
# Python
mypy src/

# TypeScript
tsc --noEmit

# JavaScript (with JSDoc)
npx typescript --allowJs --checkJs --noEmit src/**/*.js
```

## 9. Review Report Format

Provide feedback in this structure:

```markdown
# Code Review Report

## Summary
- Files reviewed: X
- Critical issues: X
- Warnings: X
- Suggestions: X

## Critical Issues
1. [File:Line] Security: SQL Injection risk in user input
2. [File:Line] Security: Hardcoded API key

## Warnings
1. [File:Line] Performance: N+1 query in loop
2. [File:Line] Code Quality: Function too complex (CC: 15)

## Suggestions
1. [File:Line] Consider extracting method for better readability
2. [File:Line] Add error handling for edge case

## Positive Observations
- Good test coverage
- Well-documented functions
- Proper error handling
```

## 10. Common Review Patterns

**Python Specific:**
```bash
# Check for mutable default arguments
grep "def.*=\[\]" . -r --include="*.py"
grep "def.*={}" . -r --include="*.py"

# Check for string concatenation in loops
grep -A5 "for.*in" . -r --include="*.py" | grep "+="
```

**JavaScript Specific:**
```bash
# Check for var instead of let/const
grep "\svar\s" . -r --include="*.js"

# Check for == instead of ===
grep "==\|!=" . -r --include="*.js" | grep -v "===" | grep -v "!=="

# Check for missing 'use strict'
head -5 src/**/*.js | grep -L "use strict"
```

## When to Use This Skill

Use `/code-review` when:
- Reviewing pull requests
- Conducting security audits
- Checking code quality before deployment
- Onboarding new code into a project
- Performing pre-commit reviews
- Analyzing legacy code
- Preparing for code refactoring

The skill will analyze code and provide actionable feedback on security, quality, performance, and best practices.
