---
name: code-review
description: Use this skill when you need to provide concise and focused code reviews that match the complexity of the task requirements, ensuring code quality and security.
---

# Code Review

Delivers **focused, streamlined** code reviews matching stated task requirements exactly. No over-analysis.

## Python Standards

Refer to `docs/python-best-practices.md` for comprehensive Python guidelines.

## Workflow

1. **Read task requirements** to understand expected scope.
2. **Check `make validate`** passes before detailed review.
3. **Match review depth** to task complexity (simple vs complex).
4. **Validate requirements** - does implementation match task scope exactly?
5. **Issue focused feedback** with specific file paths and line numbers.

## Review Strategy

**Simple Tasks (100-200 lines)**: Focus on security, compliance, requirements match, and basic quality.

**Complex Tasks (500+ lines)**: Include architecture, performance, and comprehensive testing in addition to the above.

**Always**: Use existing project patterns and conduct the review immediately after implementation.

## Review Checklist

**Security & Compliance**:

- [ ] No security vulnerabilities (injection, XSS, etc.)
- [ ] Follows @AGENTS.md mandatory requirements
- [ ] Passes `make validate`

**Requirements Match**:

- [ ] Implements exactly what was requested
- [ ] No over-engineering or scope creep
- [ ] Appropriate complexity level

**Code Quality**:

- [ ] Follows project patterns in `src/`
- [ ] Proper type hints and docstrings
- [ ] Tests cover stated functionality

## Output Standards

**Simple Tasks**: Provide feedback on CRITICAL issues only and clear approval when requirements are met.

**Complex Tasks**: Include CRITICAL/WARNINGS/SUGGESTIONS with specific fixes.

**All reviews**: Ensure they are concise, streamlined, and avoid unnecessary complexity analysis.