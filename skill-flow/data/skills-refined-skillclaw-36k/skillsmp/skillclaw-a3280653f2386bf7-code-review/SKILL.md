---
name: code-review
description: Use this skill for a systematic and comprehensive code review process that assesses correctness, security, performance, and maintainability.
---

# Code Review Methodology

## When to Use This Skill
- Before reporting implementation completion
- When explicitly asked to review code
- When using the `/review` command
- As an independent audit after code changes

## Review Process Overview

1. **Initial Scan** - Identify all files in scope and understand the changes.
2. **Deep Analysis** - Apply the review methodology across four layers systematically to each file.
3. **Context Evaluation** - Consider surrounding code, project patterns, and existing conventions.
4. **Synthesize Findings** - Compile and report issues based on severity and confidence.

## The 4 Review Layers

### Layer 1: Correctness
- Logic errors and edge cases
- Error handling completeness
- Business rule compliance
- Type safety and null checks

### Layer 2: Security
- Input validation and sanitization
- Authentication and authorization checks
- No hardcoded secrets or API keys
- Injection vulnerability prevention (SQL, XSS, command)

### Layer 3: Performance
- Algorithm efficiency and complexity
- Resource usage and optimization
- Appropriate caching strategies
- No unnecessary re-renders (React/frontend)

### Layer 4: Maintainability
- Adherence to project conventions
- Code organization and clarity
- Documentation completeness
- Complexity management (cyclomatic complexity)

## Severity Classification

| Severity | Criteria | Action Required |
|----------|----------|-----------------|
| Critical | Security vulnerabilities, data loss risks, production-breaking bugs | Must fix before merge |
| Major | Logic errors, missing error handling, performance issues | Should fix before merge |
| Minor | Code style violations, minor inefficiencies, documentation gaps | Nice to fix, can merge |
| Info | Suggestions for improvement, alternative approaches | Comment only |

## Confidence Threshold
**Only report findings with ≥80% confidence.** If uncertain about an issue:
- State the uncertainty explicitly: "Potential issue (70% confidence): ..."
- Suggest investigation rather than assert a problem
- Prefer false negatives over false positives to reduce noise.

## Configuration
Review constraints can be loaded from a project-specific configuration file, allowing for tailored review processes based on project needs.