---
name: architecture-decision-records
description: Use this skill when you need to document significant architectural decisions with comprehensive context, rationale, and alternatives in a structured format.
---

# Architecture Decision Records (ADR) - Writing Guide

This skill provides guidance for creating high-quality Architecture Decision Records (ADRs) that document significant technical decisions made during a project's development.

## What is an ADR?

An Architecture Decision Record captures:
- **What** decision was made
- **Why** it was made (problem context)
- **How** it's implemented (with code examples)
- **Trade-offs** (what was gained/lost)
- **Alternatives** considered

## When to Write an ADR

Write an ADR when making decisions that:
1. **Impact the entire system** (e.g., database choice, framework selection)
2. **Are difficult to reverse** (e.g., monorepo structure)
3. **Involve significant trade-offs** (e.g., choosing between architectural patterns)
4. **Set architectural patterns** (e.g., error handling, authentication)
5. **Require future context** (e.g., rationale for technology choices)

### Examples of ADR-Worthy Decisions
- Choosing a database design
- Selecting a framework for development
- Defining a deployment strategy

### Examples of Non-ADR Decisions
- Adding a new field to an entity
- Refactoring a component
- Fixing a bug

## ADR Format and Structure

### File Naming Convention
```
docs/architecture-decisions/adr-NNN-kebab-case-title.md
```
- **NNN**: Zero-padded 3-digit number (001, 002, etc.)
- **kebab-case-title**: Descriptive, lowercase, hyphen-separated

### Document Structure

Every ADR follows this structure:

```markdown
# ADR-NNN: Title (Clear, Concise Description)

**Date:** YYYY-MM-DD
**Status:** Accepted | Proposed | Deprecated | Superseded
**Context:** One-line summary of when/why this decision was needed

---

## Problem

[Description of the problem that led to the decision]

## Decision

[Description of the decision made]

## Consequences

[Description of the consequences of the decision]
```

## Prerequisites

Before creating an ADR, ensure you have:
1. Reviewed existing upstream artifacts (BRD, PRD)
2. Followed shared standards and templates
3. Validated the decision against existing technology stacks

Use this skill to ensure that your architectural decisions are well-documented and easily traceable for future reference.