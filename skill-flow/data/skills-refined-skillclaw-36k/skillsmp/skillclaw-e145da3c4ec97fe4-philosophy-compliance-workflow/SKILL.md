---
name: philosophy-compliance-workflow
description: Use this skill when you need to ensure that code and architecture align with core principles of simplicity, modularity, and minimalism through systematic review.
---

# Philosophy Compliance Workflow Skill

## Purpose

This skill facilitates a systematic review process to ensure that all code and architecture align with amplihack's core principles: ruthless simplicity, brick philosophy, and Zen-like minimalism. It validates that implementations serve clear purposes without unnecessary complexity.

## When to Use This Skill

**USE FOR:**
- Architecture reviews before implementation
- Code reviews for philosophy alignment
- Refactoring validation (did we actually simplify?)
- Module design verification
- Pre-merge philosophy checks
- Identifying over-engineering and complexity creep

**AVOID FOR:**
- Functional bug fixes (not philosophy issues)
- Performance optimization alone
- Documentation updates
- Pure syntax/style issues

## Core Philosophy Principles

### The Zen of Simple Code
- Each line serves a clear purpose without embellishment.
- As simple as possible, but no simpler.
- Complex systems from simple, well-defined components.
- Handle what's needed now, not hypothetical futures.

### The Brick Philosophy
- **A brick** = Self-contained module with ONE clear responsibility.
- **A stud** = Public contract (functions, API, data model) others connect to.
- **Regeneratable** = Can be rebuilt from spec without breaking connections.
- **Isolated** = All code, tests, fixtures inside the module's folder.

### Ruthless Simplicity
- Start with the simplest solution that works.
- Add complexity only when justified.
- Question every abstraction.
- Code you don't write has no bugs.

## Review Process

### Step 1: Scope Identification
**Identify what to review:**
- Single module, multiple modules, or full architecture.
- Recent changes or complete codebase.
- Specific complexity concerns or general review.

**Questions to ask:**
- What triggered this review?
- What are the main concerns?
- What's the expected outcome?

### Step 2: Initial Analysis
**Scan the code structure:**
- Module organization and boundaries.
- Public interfaces.