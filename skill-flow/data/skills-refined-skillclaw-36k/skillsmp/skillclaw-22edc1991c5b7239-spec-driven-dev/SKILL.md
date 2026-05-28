---
name: spec-driven-dev
description: Use this skill when you need to guide the specification-driven development (SDD) workflow, ensuring changes are planned, documented, and approved before implementation.
---

# Specification-Driven Development Guide

## Purpose

This skill guides you through the Specification-Driven Development (SDD) process, ensuring that changes are planned, documented, and approved before implementation.

## Quick Reference

### SDD Workflow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│     Proposal  │───▶│     Review    │───▶│     Implementation │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                                               ▼
                    ┌──────────────┐    ┌──────────────┐
                    │     Archive   │◀───│     Validate   │
                    └──────────────┘    └──────────────┘
```

### Workflow Stages

| Stage      | Description                          | Output            |
|------------|--------------------------------------|-------------------|
| **Proposal**   | Define the change and its rationale | `proposal.md`     |
| **Review**     | Stakeholder approval                 | Approval record    |
| **Implementation** | Execute the approved specification | Code, tests, documentation |
| **Validation**  | Confirm implementation meets specification | Test results      |
| **Archive**     | Close and archive                   | Archived specification and links |

### Core Principles

| Principle         | Description                                      |
|-------------------|--------------------------------------------------|
| **Specification First** | No changes should be made without an approved specification. |
| **Tool Priority** | Use SDD tools when available.                    |
| **Methodology > Tools** | SDD can operate with any tools or manual processes. |

### Exceptions to "Specification First"

- Emergency fixes (restore service first, document later)
- Minor changes (typos, comments, formatting adjustments)

## Proposal Template

```markdown
# [SPEC-ID] Feature Title

## Summary
Briefly describe the proposed change.

## Motivation
Why is this change needed? What problem does it solve?

## Detailed Design
Technical solution, affected components, data flow.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies
List dependencies on other specifications or external systems.

## Risks
Potential risks and mitigation strategies.
```

## Detailed Guide

For complete standards, refer to:
- [Specification-Driven Development Standards](../../../core/spec-driven-development.md)

### AI Optimization Format (Token Saving)

AI assistants can use YAML format files to reduce token usage:
- Basic standard: `ai/standards/spec-driven-development.ai.yaml`

## Integration with Other Standards

### Integration with Commit Messages

Reference specification ID in commit messages:

```
feat(auth): implement login feature

Implements SPEC-001 login functionality with OAuth2 support.

Refs: SPEC-001
```

### Integration with Check-in Standards

Before submitting code for specifications:

- [ ] Specification is approved
- [ ] Implementation meets specification
- [ ] Tests cover acceptance criteria
- [ ] PR references specification ID

### Integration with Code Review

Reviewers should verify:

- [ ] Changes comply with the approved specification
- [ ] No scope creep beyond the specification
- [ ] Specification acceptance criteria are met

## Examples

### ✅ Good Practice

```markdown
# SPEC-001 Add OAuth2 Login

## Summary
Add Google OAuth2 login to allow users to log in with their Google accounts.

## Motivation
- Reduce friction for new user registrations
- Avoid storing passwords to enhance security

## Acceptance Criteria
- [ ] Users can click the "Log in with Google" button
- [ ] New users are automatically registered
- [ ] Existing users can link their Google accounts
```

### ❌ Poor Practice

```markdown
# Add Login

Add login functionality.
```
- Missing specification ID
- No motivation provided
- No acceptance criteria listed

## Common SDD Tools

| Tool | Description | Command Example |
|------|-------------|-----------------|