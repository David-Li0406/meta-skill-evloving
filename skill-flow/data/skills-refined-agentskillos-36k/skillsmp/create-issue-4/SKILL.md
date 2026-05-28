---
name: create-issue
description: Investigate the root cause of a bug or define requirements for a feature, then produce a well-structured issue ready for your tracker
---

As a Staff Software Engineer, investigate the provided error, bug report, or feature request and produce a well-defined issue document. Focus on thoroughly understanding and documenting the **problem** - solution planning comes later.

Your goal: Create an issue so clear that any developer could understand the problem completely and then plan a solution.

## Investigation Phase

Understand the problem before documenting it:

### For Bugs/Errors

- **Trace the symptom**: Follow code paths, collect logs and stack traces
- **Identify root cause**: What code or condition triggers this?
- **Assess scope**: Isolated or systemic? What's the blast radius?
- **Measure impact**: Users affected, severity, frequency

### For Features/Improvements

- **Map current state**: How does it work today? What's missing?
- **Define the goal**: What user problem does this solve?
- **Note constraints**: Technical, business, or resource limitations

### General

- Explore relevant areas of the codebase
- Check documentation for involved systems
- Look for related issues or past attempts

## Issue Document Structure

```markdown
# [Descriptive Title]

Specific title describing the problem (not the solution).
Bad: "Fix login" | Good: "Login fails silently when SSO session expires mid-authentication"

## Summary

2-3 sentences: What's the problem, who's affected, and why does it matter?

## Problem Description

### Current Behavior
- Observable symptoms
- Error messages or logs (quote relevant excerpts)
- Reproduction steps (for bugs)
- Root cause, if identified

### Expected Behavior
What should happen instead. Be specific.

### Impact
- Who is affected (users, systems, teams)
- Severity (data loss, degraded experience, inconvenience)
- Frequency (constant, intermittent, edge case)

## Context

What a developer needs to understand this problem:
- Relevant code: `[filename.ext:line](path#Lline)`
- Architecture or system components involved
- Dependencies or integrations
- Key constraints

## Scope

### This Issue Addresses
- Specific problem(s) to solve
- Clear boundaries

### Out of Scope
- Related concerns for separate issues

## Acceptance Criteria

How we know this is done:
- [ ] Specific, testable criterion
- [ ] Another measurable outcome
- [ ] Relevant tests pass

Keep criteria focused on **outcomes**, not implementation details.

## Additional Context

- Related issues or PRs
- Customer reports or support tickets
- Screenshots, logs, or examples

---
**Signals:**
- Severity: [Low | Medium | High | Critical]
- Complexity Estimate: [Small | Medium | Large | XL]
```

## Quality Checklist

Before finalizing:

- [ ] Problem is clear: Could a developer explain this to someone else?
- [ ] Evidence-based: Symptoms and root cause supported by code/logs?
- [ ] Properly scoped: One cohesive problem, not multiple issues bundled?
- [ ] Impact articulated: The "why it matters" is explicit?
- [ ] Testable criteria: Each acceptance criterion is unambiguous?
- [ ] No premature solutioning: Describes the problem, not a predetermined fix?

## Principles

**Focus on the problem.** Define *what* needs solving and *why*.

**Capture context.** Include enough detail that someone unfamiliar can understand without asking questions.

**Be evidence-driven.** Reference specific code, quote actual errors, cite real data.

**Scope ruthlessly.** A focused issue gets solved. A sprawling issue becomes backlog.

## Output

Save as `issue-brief-problem-description.md` in the appropriate location (project root, `.github/issues/`, or as specified).
