---
name: testing-skills-with-subagents
description: Use this skill when creating or editing skills to verify their functionality under pressure and ensure they resist rationalization, applying the RED-GREEN-REFACTOR cycle to process documentation.
---

# Testing Skills With Subagents

## Overview

**Testing skills is just TDD applied to process documentation.**

You run scenarios without the skill (RED - watch agent fail), write the skill addressing those failures (GREEN - watch agent comply), then close loopholes (REFACTOR - stay compliant).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill prevents the right failures.

**REQUIRED BACKGROUND:** You MUST understand test-driven development (TDD) before using this skill. This skill provides specific test formats (pressure scenarios, rationalization tables).

**Complete worked example:** See examples/CLAUDE_MD_TESTING.md for a full test campaign testing CLAUDE.md documentation variants.

## When to Use

Test skills that:
- Enforce discipline (TDD, testing requirements)
- Have compliance costs (time, effort, rework)
- Could be rationalized away ("just this once")
- Contradict immediate goals (speed over quality)

Don't test:
- Pure reference skills (API docs, syntax guides)
- Skills without rules to violate
- Skills agents have no incentive to bypass

## TDD Mapping for Skill Testing

| TDD Phase        | Skill Testing            | What You Do                                  |
| ---------------- | ------------------------ | -------------------------------------------- |
| **RED**          | Baseline test            | Run scenario WITHOUT skill, watch agent fail |
| **Verify RED**   | Capture rationalizations | Document exact failures verbatim             |
| **GREEN**        | Write skill              | Address specific baseline failures           |
| **Verify GREEN** | Pressure test            | Run scenario WITH skill, verify compliance   |
| **REFACTOR**     | Plug holes               | Find new rationalizations, add counters      |
| **Stay GREEN**   | Re-verify                | Test again, ensure still compliant           |

## RED Phase: Baseline Testing (Watch It Fail)

**Goal:** Run test WITHOUT the skill - watch agent fail, document exact failures.

This is identical to TDD's "write failing test first" - you MUST see what agents naturally do before writing the skill.

**Process:**

- [ ] **Create pressure scenarios** (3+ combined pressures)
- [ ] **Run WITHOUT skill** - give agents realistic tasks