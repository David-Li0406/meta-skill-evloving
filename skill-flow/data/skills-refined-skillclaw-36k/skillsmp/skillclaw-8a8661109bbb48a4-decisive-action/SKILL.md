---
name: decisive-action
description: Use this skill when you need guidance on whether to ask clarifying questions or proceed autonomously in decision-making scenarios.
---

# Decisive Action

Guidance on when to ask clarifying questions versus proceeding autonomously.

## Core Principle

Ask questions only when ambiguity would **materially impair correctness** or capacity to fulfill the request precisely.

## When to Ask (High Impact Ambiguity)

### Always Ask For

| Scenario                      | Why                              | Example                              |
| ----------------------------- | -------------------------------- | ------------------------------------ |
| **Destructive Operations**    | Irreversible, high cost of error | "Delete which files?"                |
| **Multiple Valid Approaches** | Materially different tradeoffs   | "Add index vs cache vs denormalize?" |
| **Security-Critical**         | Wrong choice = vulnerability     | "Which auth method?"                 |
| **Data Migration**            | Data loss risk                   | "Preserve or transform?"             |
| **Breaking Changes**          | Affects downstream users         | "Deprecate or remove?"               |

### Ask Threshold Checklist

Before asking, verify:
- [ ] >30% chance of wrong interpretation
- [ ] Error cost > correction cost
- [ ] No clear standard approach exists
- [ ] User context doesn't clarify intent

## When to Proceed Without Asking

### Default to Action For

| Scenario                     | Why                  | Assumption               |
| ---------------------------- | -------------------- | ------------------------ |
| **Standard Approach Exists** | Industry convention  | Use conventional pattern |
| **Easily Reversible**        | Low cost of error    | Can undo via git/backup  |
| **Clear from Context**       | Intent is obvious    | Proceed with stated goal |
| **User Can Review**          | PR/dry-run available | Changes are inspectable  |

### Proceed Threshold Checklist

Proceed without asking if:
- [ ] Standard/obvious solution exists
- [ ] Easily reversible (git, backup)
- [ ] User can review before finalize
- [ ] Context makes intent clear
- [ ] Error cost < interruption cost

## Decision Matrix

| Reversibility | Ambiguity | Action |
|---------------|-----------|--------|
| Reversible    | Low       | **Proceed** |
| Reversible    | High      | **Proceed** with preview |
| Irreversible  | Low       | **Proceed** with confirmation |
| Irreversible  | High      | **Ask** |

## Safety Mechanisms

### Before Proceeding Autonomously

1. **Dry-run/Preview**: Show proposed action before executing.
2. **Backup First**: Create git branch, backup directory.
3. **Clarify Intent**: Ensure understanding of the request before acting.