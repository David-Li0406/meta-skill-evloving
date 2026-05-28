---
name: code-review
description: Use this skill for systematic code review and quality assessment across multiple layers, ensuring correctness, security, performance, and maintainability.
---

# Code Review Methodology

## Overview
This skill provides a structured approach to code review, focusing on four key layers: Correctness, Security, Performance, and Style & Maintainability. It includes severity classification and confidence thresholds for reporting findings.

## When to Use This Skill
- Before reporting implementation completion
- When explicitly asked to review code
- When using the `/review` command
- As an independent audit after code changes

## The 4 Review Layers

### Layer 1: Correctness
- Logic errors and edge cases
- Error handling completeness
- Type safety and null checks
- Algorithm correctness
- Business rule compliance

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

## Severity Classification

| Severity | Criteria | Action Required |
|----------|----------|-----------------|
| Critical | Security vulnerabilities, crashes, data loss, corruption | Must fix before merge |
| Major | Bugs, performance issues, missing error handling | Should fix |
| Minor | Code smells, maintainability issues, test gaps | Nice to fix |
| Info | Suggestions for improvement | Comment only |

## Confidence Threshold
**Only report findings with ≥80% confidence.** If uncertain about an issue, state the uncertainty explicitly and suggest investigation rather than assert a problem.

## Review Process

1. **Initial Scan** - Identify all files in scope and understand the change.
2. **Deep Analysis** - Apply all 4 layers systematically to each file.
3. **Context Evaluation** - Consider surrounding code, project patterns, and existing conventions.
4. **Synthesize Findings** - Group by severity, deduplicate, and prioritize.

## Output Format
Structure your review as follows:
1. **Files Reviewed** - List all files analyzed.
2. **Overall Assessment** - APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION.
3. **Summary** - 2-3 sentence overview.
4. **Critical Issues** - With file:line references.
5. **Major Issues** - With file:line references.
6. **Minor Issues** - With file:line references.
7. **Positive Observations** - What's done well (always include at least one).

## Review Checklists

### Security Review Checklist
- All user inputs validated?
- SQL injection prevention?
- XSS prevention?
- Auth checks on all protected routes?
- Sensitive data encrypted?

### Code Quality Checklist
- Variable names descriptive?
- Functions single-purpose?
- DRY principle followed?
- All error cases handled?
- New code has tests?

## Review Feedback Patterns

### Constructive Feedback Template
- **What**: Describe the issue clearly.
- **Why**: Explain why it's a problem.
- **How**: Suggest a solution or alternative.
- **Severity**: Classify the severity.

### Feedback Tone Guidelines
- Focus on the code, not the person.
- Acknowledge good patterns when seen.
- Provide actionable suggestions.

## Review Metrics

### Quality Score Calculation
- Categories: Correctness, Security, Maintainability, Performance.
- Base score: 100, with deductions for issues.

## Integration
### Used By Agents
- **Primary Users**: Quality reviewers.
- **Secondary Users**: Code developers for self-review, deliverable evaluators for quality assessment.