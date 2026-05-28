---
name: planning
description:
  Create plans, summaries, analysis, or outlines. Use when asked to investigate,
  plan, or avoid code changes
---

# Planning Protocol

Applies when asked to plan or not make code changes

## Core Rules

- Be concise, no storytelling
- Work with facts only, no assumptions
- Read files, docs, search internet, analyze deeply before answering
- Prefer thorough investigation over fast imprecise plans

## Written Plans (when saving to file)

Format:

- 80 char line limit
- Proper MD: spacing, titles, bullets, indentation

Requirements:

- Deterministic, unambiguous, idempotent
- Atomic steps, clearly defined
- No optional steps or alternatives (ask for clarification instead)
- Any agent without context should be able to follow it

## Executing Plans

- Follow each step exactly as defined
- Refuse to start if any step is ambiguous or non-deterministic
- Ask for clarification, don't improvise
