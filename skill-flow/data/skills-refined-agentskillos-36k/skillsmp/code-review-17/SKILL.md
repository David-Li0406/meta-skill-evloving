---
name: code-review
description: Systematic code review and evaluation tool for Python/FastAPI projects. Use when reviewing PRs, evaluating code quality, checking architecture compliance, or providing feedback on implementations. Triggers on "review", "code review", "evaluate", "check code", "PR review", "feedback".
---

# Code Review Guide

## Review Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    Code Review Workflow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Context    →  2. Architecture  →  3. Code Quality           │
│  Understanding     Compliance          Analysis                  │
│                                                                  │
│  4. Security   →  5. Performance   →  6. Testing                │
│  Check             Review              Coverage                  │
│                                                                  │
│  7. Generate Summary & Actionable Feedback                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Review Checklist

### CI Lint & Format (MUST PASS)
- [ ] `black --check` passes (no formatting issues)
- [ ] `ruff check` passes (no lint errors)
- [ ] No unused imports (F401)
- [ ] No unused variables (F841)

```bash
# 코드 작성/수정 후 반드시 실행
black --check <path> && ruff check <path>

# 자동 수정
black <path> && ruff check <path> --fix
```

### Architecture (Clean Architecture)
- [ ] Dependencies point inward (Domain has no external deps)
- [ ] Ports defined as Protocol in correct layer
- [ ] Adapters implement Ports correctly
- [ ] No business logic in controllers
- [ ] DTOs used for API responses (not entities)

### Code Quality
- [ ] Functions are small and focused (<20 lines ideal)
- [ ] Clear naming conventions followed
- [ ] No code duplication (DRY)
- [ ] Proper error handling
- [ ] Type hints present and accurate

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevention (parameterized queries)
- [ ] Authentication/Authorization checks
- [ ] Sensitive data not logged

### Testing
- [ ] Unit tests for business logic
- [ ] Edge cases covered
- [ ] Mocks used appropriately
- [ ] Test names describe behavior

## Review Commands

### Full Review
```
Review this code for:
1. Architecture compliance (Clean Architecture)
2. Code quality issues
3. Security vulnerabilities
4. Performance concerns
5. Test coverage gaps
```

### Focused Reviews
```
# Architecture only
Review architecture compliance for this module.

# Security only
Check this code for security vulnerabilities.

# Performance only
Analyze performance characteristics of this code.
```

## Severity Levels

| Level | Icon | Description | Action |
|-------|------|-------------|--------|
| **Critical** | :x: | Security vulnerability, data loss risk | Must fix before merge |
| **Major** | :warning: | Architecture violation, significant bug | Should fix before merge |
| **Minor** | :bulb: | Code smell, style issue | Consider fixing |
| **Suggestion** | :thought_balloon: | Improvement idea | Optional |

## Reference Files

- **Architecture checklist**: See [architecture-review.md](./references/architecture-review.md)
- **Security checklist**: See [security-review.md](./references/security-review.md)
- **Python best practices**: See [python-review.md](./references/python-review.md)
- **Review templates**: See [review-templates.md](./references/review-templates.md)

## Output Format

```markdown
## Code Review Summary

### Overview
- **Files reviewed**: X
- **Issues found**: X critical, X major, X minor
- **Overall assessment**: [Approve/Request Changes/Comment]

### Critical Issues :x:
1. **[File:Line]** Issue description
   - Impact: ...
   - Fix: ...

### Major Issues :warning:
1. **[File:Line]** Issue description
   - Impact: ...
   - Suggestion: ...

### Minor Issues :bulb:
1. **[File:Line]** Issue description

### Suggestions :thought_balloon:
1. Consider...

### Positive Highlights :star:
1. Good use of...
```

## Eco² Project Standards

This project follows:
- Clean Architecture (see `clean-architecture` skill)
- Python 3.11+ with type hints
- FastAPI async patterns
- Protocol-based interfaces
- CQRS for complex modules
