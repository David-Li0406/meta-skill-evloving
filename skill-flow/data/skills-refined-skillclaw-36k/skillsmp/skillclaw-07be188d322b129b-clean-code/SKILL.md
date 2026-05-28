---
name: clean-code
description: Use this skill when you want to adhere to pragmatic coding standards that emphasize conciseness, clarity, and simplicity in your code.
---

# Clean Code - Pragmatic AI Coding Standards

> **CRITICAL SKILL** - Be **concise, direct, and solution-focused**.

## Core Principles

| Principle     | Rule                                                       |
| ------------- | ---------------------------------------------------------- |
| **SRP**       | Single Responsibility - each function/class does ONE thing |
| **DRY**       | Don't Repeat Yourself - extract duplicates, reuse          |
| **KISS**      | Keep It Simple - simplest solution that works              |
| **YAGNI**     | You Aren't Gonna Need It - don't build unused features     |
| **Boy Scout** | Leave code cleaner than you found it                       |

## Naming Rules

| Element       | Convention                                            |
| ------------- | ----------------------------------------------------- |
| **Variables** | Reveal intent: `userCount` not `n`                    |
| **Functions** | Verb + noun: `getUserById()` not `user()`             |
| **Booleans**  | Question form: `isActive`, `hasPermission`, `canEdit` |
| **Constants** | SCREAMING_SNAKE: `MAX_RETRY_COUNT`                    |

> **Rule:** If you need a comment to explain a name, rename it.

## Function Rules

| Rule                | Description                           |
| ------------------- | ------------------------------------- |
| **Small**           | Max 20 lines, ideally 5-10            |
| **One Thing**       | Does one thing, does it well          |
| **One Level**       | One level of abstraction per function |
| **Few Args**        | Max 3 arguments, prefer 0-2           |
| **No Side Effects** | Don't mutate inputs unexpectedly      |

## Code Structure

| Pattern           | Apply                             |
| ----------------- | --------------------------------- |
| **Guard Clauses** | Early returns for edge cases      |
| **Flat > Nested** | Avoid deep nesting (max 2 levels) |
| **Composition**   | Small functions composed together |
| **Colocation**    | Keep related code close           |

## AI Coding Style

| Situation             | Action                |
| --------------------- | --------------------- |
| User asks for feature | Write it directly     |
| User reports bug      | Fix it, don't explain |
| No clear requirement   | Ask, don't assume     |

## Anti-Patterns (DON'T)

| ❌ Pattern | ✅ Fix |
|-----------|-------|
| Comment every line | Delete obvious comments |
| Helper for one-liner | Inline the code |
| Factory for 2 objects | Direct instantiation |
| utils.ts with 1 function | Put code where used |
| "First we import..." | Just write code |
| Deep nesting | Guard clauses |
| Magic numbers | Named constants |
| God functions | Split by responsibility |

## 🔴 Before Editing ANY File (THINK FIRST!)

**Before changing a file, ask yourself:**

| Question | Why |
|----------|-----|
| **What imports this file?** | They might break if you change the file. |