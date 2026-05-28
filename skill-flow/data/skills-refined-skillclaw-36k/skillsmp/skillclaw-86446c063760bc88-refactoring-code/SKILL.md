---
name: refactoring-code
description: Use this skill when you need to improve code structure while preserving behavior, ensuring that tests verify functionality throughout the process.
---

# Refactoring Code

You are following a systematic refactoring methodology that improves code quality, maintainability, and simplicity while **preserving existing behavior**.

**Core Principle:** Refactoring changes structure, not functionality. Safety and clarity are more important than elegance.

## The Iron Law

```
BEHAVIOR MUST BE PRESERVED
Tests must verify behavior, not implementation
```

If you change what the code does (not just how it does it), you're not refactoring—you're rewriting.

## Prerequisites

- Access to the codebase for pattern research
- **Behavior-driven tests** that verify current functionality
- Understanding of project conventions

## Core Responsibilities

1. **Simplify Complex Code** - Break down complex functions, reduce nesting, improve readability.
2. **Extract Patterns** - Identify and extract reusable components, hooks, utilities.
3. **Eliminate Duplication** - Apply DRY principles while avoiding premature abstraction.
4. **Improve Type Safety** - Strengthen TypeScript usage, eliminate `any` types when possible.
5. **Performance Optimization** - Identify unnecessary re-renders, optimize data structures.
6. **Align with Standards** - Ensure code follows project patterns and conventions.

## The Five-Phase Refactoring Process

You MUST complete each phase before proceeding to the next.

Copy this checklist and track your progress:

```
Refactoring Progress:
- [ ] Phase 1: Understand Current Behavior
  - [ ] Read existing code thoroughly
  - [ ] Check usage across the codebase
  - [ ] Document current behavior
- [ ] Phase 2: Verify Test Coverage (CRITICAL)
  - [ ] Behavior-driven tests exist and pass
  - [ ] Tests cover main workflows and edge cases
  - [ ] Tests don't depend on implementation details
- [ ] Phase 3: Identify Issues
  - [ ] Issues documented with locations
  - [ ] Issues categorized by type and severity
  - [ ] Root cause understood for each issue
- [ ] Phase 4: Plan Refactoring
  - [ ] Broken into small, verifiable steps
  - [ ] Each step has verification criteria
  - [ ] Dependencies between steps identified
- [ ] Phase 5: Execute & Verify
  - [ ] All planned changes implemented
  - [ ] All tests pass
  - [ ] No new type errors or warnings
  - [ ] Behavior verified unchanged
```