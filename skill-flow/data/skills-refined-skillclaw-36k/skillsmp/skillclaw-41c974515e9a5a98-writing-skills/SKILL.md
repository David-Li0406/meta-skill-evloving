---
name: writing-skills
description: Use this skill when you want to apply Test-Driven Development (TDD) principles to create and document reusable skills for process documentation.
---

# Skill body

## Overview

**Writing skills is Test-Driven Development (TDD) applied to process documentation.**

Skills are stored in `.gemini/skills/` (project-local) or `~/.gemini/skills/` (user-global). You edit skills directly in the project's codebase.

1. **Write Test Cases**: Create pressure scenarios using subagents to define expected behavior.
2. **Watch Tests Fail**: Run the tests to establish baseline behavior without the skill.
3. **Write the Skill**: Document the skill in a SKILL.md file, ensuring it captures the necessary techniques or patterns.
4. **Watch Tests Pass**: Run the tests again to confirm that the agent complies with the skill.
5. **Refactor**: Improve the skill documentation by closing any loopholes while maintaining compliance.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools that help future Agent instances find and apply effective approaches. 

**Skills are:** Reusable techniques, patterns, tools, reference guides  
**Skills are NOT:** Narratives about how you solved a problem once

## When to Create a Skill

**Create when:**

- A technique wasn't intuitively obvious to you.
- You'd reference this again across projects.
- A pattern applies broadly (not project-specific).
- Others would benefit from the documentation.

**Don't create for:**

- One-off solutions.
- Standard practices well-documented elsewhere.
- Project-specific conventions (put in `GEMINI.md`).

## When to Use This Skill

**Situations:**

- When you discover a technique, pattern, or tool worth documenting for reuse.
- When editing existing skills.
- When asked to modify skill documentation.
- When you've written a skill and need to verify it works before deploying.

## TDD Mapping for Skills

| TDD Concept             | Skill Creation                                   |
| ----------------------- | ------------------------------------------------ |
| **Test case**           | Pressure scenario with subagent                  |
| **Production code**     | Skill document (SKILL.md)                        |
| **Test fails (RED)**    | Agent violates rule without skill (baseline)     |
| **Test passes (GREEN)** | Agent complies with skill present                |
| **Refactor**            | Close loopholes while maintaining compliance     |
| **Write test first**    | Run baseline scenario BEFORE writing skill       |
| **Watch it fail**       | Document the expected behavior before implementation |