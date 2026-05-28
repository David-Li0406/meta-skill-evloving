---
name: code-review
description: Comprehensive code review methodology. 4 layers (Correctness, Security, Performance, Style), severity classification, 80% confidence threshold.
---

# Code Review Skill

## TL;DR

Systematic code review across 4 layers with severity classification. Only report findings with ≥80% confidence. Include file:line references for all issues.

---

## The 4 Review Layers

### Layer 1: Correctness
- Logic errors and edge cases
- Error handling completeness
- Type safety and null checks
- Algorithm correctness
- Off-by-one errors

### Layer 2: Security
- No hardcoded secrets or API keys
- Input validation and sanitization
- Injection vulnerability prevention (SQL, XSS, command)
- Authentication and authorization checks
- Sensitive data not logged
- OWASP Top 10 awareness

### Layer 3: Performance
- No N+1 query patterns
- Appropriate caching strategies
- No unnecessary re-renders (React/frontend)
- Lazy loading where appropriate
- Memory leak prevention
- Algorithmic complexity concerns

### Layer 4: Style & Maintainability
- Adherence to project conventions
- Code duplication (DRY violations)
- Complexity management (cyclomatic complexity)
- Documentation completeness
- Test coverage gaps

---

## Severity Classification

| Severity | Icon | Criteria | Action Required |
|----------|------|----------|-----------------|
| Critical | 🔴 | Security vulnerabilities, crashes, data loss | Must fix before merge |
| Major | 🟠 | Bugs, performance issues, missing error handling | Should fix |
| Minor | 🟡 | Code smells, maintainability issues, test gaps | Nice to fix |
| Nitpick | 🟢 | Style preferences, naming suggestions | Optional |

---

## Confidence Threshold

**Only report findings with ≥80% confidence.**

If uncertain about an issue:
- State the uncertainty explicitly: "Potential issue (70% confidence): ..."
- Suggest investigation rather than assert a problem
- Prefer false negatives over false positives (reduce noise)

---

## Review Process

1. **Initial Scan** - Identify all files in scope, understand the change
2. **Deep Analysis** - Apply all 4 layers systematically to each file
3. **Context Evaluation** - Consider surrounding code, project patterns
4. **Philosophy Check** - Verify against code-philosophy (5 Laws) if applicable
5. **Synthesize Findings** - Group by severity, deduplicate, prioritize

---

## Output Format

```markdown
**Files Reviewed:** [list all files]

**Overall Assessment:** APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION

**Summary:** [2-3 sentence overview]

### 🔴 Critical Issues
[List with file:line references, or "None"]

### 🟠 Major Issues
[List with file:line references, or "None"]

### 🟡 Minor Issues
[List with file:line references, or "None"]

### 🟢 Positive Observations
[What's done well - always include at least one]

### Philosophy Compliance
- Early Exit: [PASS|FAIL|N/A]
- Parse Don't Validate: [PASS|FAIL|N/A]
- Atomic Predictability: [PASS|FAIL|N/A]
- Fail Fast: [PASS|FAIL|N/A]
- Intentional Naming: [PASS|FAIL|N/A]
```

---

## What NOT to Do

- Do NOT report low-confidence findings as definite issues
- Do NOT provide vague feedback without file:line references
- Do NOT skip any of the 4 layers
- Do NOT forget to note positive observations
- Do NOT modify any files during review
