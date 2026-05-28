---
name: bug_hunter
description: Deep security and bug audit, checking for null pointers, exception handling uncertainties, type safety, and race conditions.
---

# Bug Hunter Skill

**Goal**: Fix existing bugs and prevent potential crashes (Defensive Programming).

## Instructions

Perform a "Deep Security Review" on the code.

### 1. Focus Areas

- **Null/Undefined**: Check property access chains. Missing optional chaining or null checks?
- **Exception Handling**: Empty `catch` blocks? Uncaught Promise rejections?
- **Type Safety**: (If TS/Static) Misuse of `any` or dangerous casts.
- **Race Conditions**: Async operation state management issues.
- **Resource Leaks**: Event listeners or timers not cleared on destruction.

### 2. Reporting

For each issue found, provide:

1. **Problem Description**
2. **Risk Level** (High/Medium/Low)
3. **Fixed Code Snippet** (Using defensive programming style)
