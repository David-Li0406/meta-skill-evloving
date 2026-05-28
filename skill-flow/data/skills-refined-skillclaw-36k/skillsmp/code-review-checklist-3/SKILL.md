---
name: code-review-checklist
description: "Meta" skill for self-review, planning complex features, and identifying tech debt.
---

# Code Review & Planning

## When to use this skill
- Before starting a complex coding task ("Planning Mode").
- Before submitting work / marking a task as done.
- When the user asks for a code review.

## 1. Planning Checklist
- [ ] **Context**: Do I understand the *why*? Is this the right problem to solve?
- [ ] **Dependencies**: Am I adding new libraries? Are they necessary?
- [ ] **Edge Cases**: What happens if input is null? If network fails?

## 2. Code Review Checklist (Self-Correction)
- [ ] **Readability**: Can a junior dev understand this?
- [ ] **Performance**: Any N+1 queries? Loop inside loops?
- [ ] **Security**: Inputs validated? SQL injected?
- [ ] **Tests**: Did I break existing tests? Did I add new ones?

## 3. Tech Debt
- If you see ugly code but can't fix it now, leave a `TODO:` comment.
- Propose refactoring as a separate task, don't scope creep.
