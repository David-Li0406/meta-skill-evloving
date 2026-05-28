---
name: code-review
description: Self-review code changes before commit to ensure quality
---

# Code Review Skill

This skill performs automated self-review of code changes before committing to ensure code quality and catch potential issues.

## Purpose

Ensure code changes meet quality standards before commit by performing automated checks and analysis.

## When to Use

- Before final commit of any code changes
- After implementing fixes (GREEN phase of TDD)
- When preparing PR for human review

## Checks Performed

### 1. Code Style & Patterns
- Code follows project-specific patterns and conventions
- Consistent naming conventions (camelCase, snake_case, etc.)
- Proper import organization
- No unused imports or variables

### 2. Static Analysis
- No linting errors (`eslint`, `flake8`, `biome`, etc.)
- No type errors (`mypy`, `tsc`, etc.)
- No security vulnerabilities (basic patterns)

### 3. Test Coverage
- All modified code has corresponding tests
- New functionality includes test cases
- Edge cases are considered

### 4. Code Quality
- No hardcoded secrets or sensitive data
- Proper error handling
- No console.log/print statements in production code
- Functions are reasonably sized

### 5. Documentation
- Public functions have docstrings/comments
- Complex logic is documented
- README updated if needed

## Process

1. **Identify Changed Files**
   - Compare against the base branch
   - List all modified, added, deleted files

2. **Run Project Linters**
   - Execute project-specific lint commands
   - Report any errors or warnings

3. **Type Check** (if applicable)
   - Run TypeScript/mypy/other type checkers
   - Report type errors

4. **Security Scan**
   - Check for hardcoded secrets
   - Check for common security anti-patterns

5. **Generate Report**
   - List all issues found
   - Categorize by severity (error, warning, info)

## Output Format

```json
{
  "status": "pass|fail",
  "files_reviewed": 5,
  "issues": [
    {
      "file": "src/auth.ts",
      "line": 45,
      "severity": "error",
      "category": "linting",
      "message": "Missing semicolon"
    }
  ],
  "summary": {
    "errors": 0,
    "warnings": 2,
    "info": 1
  },
  "recommendation": "Ready to commit" | "Fix errors before committing"
}
```

## Important

- NEVER skip this review step
- If any errors are found, they MUST be fixed before commit
- Warnings should be addressed if time permits
- If review cannot be completed, report the blocker
