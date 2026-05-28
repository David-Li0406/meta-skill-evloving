---
name: code-review
description: "Review code changes for correctness, security, tests, and architecture; use for code review or PR review requests (trigger keywords: code review, review changes, PR review, security review)."
---

# Code Review

## What this skill does
- Reviews diffs or files for bugs, security risks, maintainability, and architecture alignment.
- Prioritizes high-severity issues and missing tests over style nitpicks.
- Adapts to repository patterns and local guidance (e.g., CLAUDE.md) when present.

## When to use it
- Trigger phrases: "code review", "PR review", "review changes", "security review".
- Use after writing or modifying code, before merge, or when asked to approve/request changes.

## Step-by-step workflow
1) Identify scope: diff, files, commit, or PR; confirm intent and expected behavior.
2) Review changed code first, then open surrounding context only when needed.
3) Scan for critical risks: correctness, security, data loss, auth/authz, injection, secrets, crypto misuse.
4) Check architecture alignment and dependency boundaries; note any layering violations.
5) Evaluate error handling, logging, resource cleanup, and edge cases.
6) Assess code quality and maintainability: clarity, naming, abstraction level, duplication, complexity, and dependency changes; note SOLID issues only when material.
7) Check tests and coverage gaps; call out missing or brittle tests.
8) Flag performance issues only when evidence exists; avoid speculative optimizations.
9) Write actionable feedback with file references and minimal fix guidance.
10) Summarize remaining risks and verification steps.

## Expected outputs / formatting
- Findings ordered by severity with file paths.
- Short rationale and concrete fix suggestions for each issue.
- Call out security items with optional CWE/OWASP references when applicable.
- Missing tests called out explicitly.
- Brief change summary only after findings.
- Keep feedback pragmatic; avoid theoretical or stylistic nitpicks.

## Example prompts
- "Do a code review of the staged changes."
- "Review this PR for security and correctness issues."
- "Check these files for architecture violations."
- "Review the code you just generated and call out risks."
