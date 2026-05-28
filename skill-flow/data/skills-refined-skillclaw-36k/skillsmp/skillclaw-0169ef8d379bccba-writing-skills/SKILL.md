---
name: writing-skills
description: Use this skill when creating new skills, editing existing skills, or verifying skills work before deployment by applying TDD principles to process documentation.
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.** 

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand test-driven development (TDD) before using this skill. This skill adapts TDD to documentation.

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious to you.
- You'd reference this again across projects.
- Pattern applies broadly (not project-specific).
- Others would benefit.

**Never create for:**
- One-off solutions.
- Standard practices documented elsewhere.
- Project-specific conventions (use CLAUDE.md).

## TDD Mapping for Skills

| TDD Concept             | Skill Creation                                   |
|-------------------------|--------------------------------------------------|
| **Test case**           | Pressure scenario with subagent                  |
| **Production code**     | Skill document (SKILL.md)                        |
| **Test fails (RED)**    | Agent violates rule without skill (baseline)     |
| **Test passes (GREEN)** | Agent complies with skill present                 |
| **Refactor**            | Close loopholes while maintaining compliance      |
| **Write test first**    | Run baseline scenario BEFORE writing skill       |
| **Watch it fail**       | Document exact rationalizations agent uses       |
| **Minimal code**        | Write skill addressing those specific violations   |
| **Watch it pass**       | Verify agent now complies                        |
| **Refactor cycle**      | Find new rationalizations → plug → re-verify     |

## Quick Reference

| Phase  | Action                          | Verify                          |
|--------|---------------------------------|---------------------------------|
| **RED**| Create pressure scenarios       | Document baseline failures       |
| **RED**| Run WITHOUT skill               | Agent violates rule             |
| **GREEN**| Write minimal skill           | Addresses baseline failures      |
| **GREEN**| Run WITH skill                | Agent now complies              |
| **REFACTOR**| Find new rationalizations   | Agent still complies            |
| **REFACTOR**| Add explicit counters       | Bulletproof against excuses     |
| **DEPLOY**| Commit and optionally PR     | Skill ready for use             |

## Common Mistakes

- Failing to run baseline tests before writing skills.
- Creating skills for one-off solutions or project-specific conventions.
- Not documenting rationalizations used by agents.

**Iron Law:** No skill without a failing test first. This applies to both new skills and edits.