---
name: plan-work
description: Break down an issue or task into concrete implementation steps with file locations, code changes, and acceptance criteria
---

As a Staff Software Engineer, produce a detailed implementation plan for the given issue. Prioritize long-term correctness, maintainability, and idiomatic solutions over quick fixes.

## Investigation Phase

Before designing a solution:

- **Verify understanding**: Confirm the problem statement and root cause
- **Map the implementation surface**: Identify files, functions, and data flows involved
- **Study patterns**: How does the codebase handle similar cases?
- **Check runtime behavior**: Gather logs, queries, or API responses as needed
- **Note constraints**: Performance, compatibility, security requirements

## Plan Structure

### Summary

1-3 sentences: What's the problem, and the high-level fix approach.

### Root Cause Analysis

- What's happening and why (with evidence)
- Sequence of events or data flow leading to the issue
- Key code references: `[filename.ext:line](path#Lline)`

### Solution Design

Address the root cause directly - no workarounds:

- Follow **idiomatic patterns** for the language/framework
- Respect **separation of concerns** - logic belongs in the appropriate layer
- Consider **idempotency** and **graceful degradation** for distributed systems
- Flag **breaking changes** clearly for developer confirmation

**Alternatives Considered**: Document rejected approaches and why.

### Files to Modify

List each file with:

- Path and line reference
- Brief description of the change (1-2 sentences)
- Concise code snippet only if essential

### Implementation Steps

Numbered, actionable steps. Keep code examples minimal - show the essential change, not surrounding context.

### Verification

**Automated Testing:**

- Specific test commands to run
- New test cases needed (describe intent, not full implementations)

**Manual/Staging Verification:**

- Steps to validate in a running environment
- Log queries or monitoring checks
- Expected behavior vs. previous behavior

**Post-Deployment:**

- Deployment sequence if order matters
- Rollback criteria and procedure
- Monitoring queries for regressions

## Quality Checklist

Before finalizing:

- [ ] Follows idiomatic patterns for the language/framework?
- [ ] Addresses root cause, not just symptoms?
- [ ] Handles concurrent/distributed edge cases?
- [ ] Handles error cases appropriately?
- [ ] Is this the simplest solution that solves the problem?
- [ ] Breaking changes called out for developer confirmation?
- [ ] No injection, auth bypass, or data exposure risks?

## Principles

**Prioritize**: Long-term correctness > backward compatibility > implementation speed

**Avoid**:

- Leaking internal details across layer boundaries
- Over-engineering (extra config, abstractions, or features not requested)
- Ignoring existing codebase patterns
- Large code blocks - summarize or show only the essential diff
