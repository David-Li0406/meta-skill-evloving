---
name: aico-pm-brainstorming
description: Use this skill when you need to guide users through structured dialogue to transform vague ideas into clear, actionable product concepts, especially when requirements are unclear or incomplete.
---

# Skill body

## ⚠️ CRITICAL RULES - READ FIRST

1. **READ CONSTITUTION**: Always read `docs/reference/pm/constitution.md` first for product context.
2. **ONE QUESTION AT A TIME**: Never ask multiple questions in one message.
3. **USE MULTIPLE CHOICE**: Prefer AskUserQuestion tool with 2-4 options.

## Language Configuration

Before generating any content, check `aico.json` in project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Check context**: Scan `docs/reference/pm/` for existing product context.
2. **Understand problem**: Ask clarifying questions one at a time.
3. **Explore alternatives**: Propose 2-3 approaches with trade-offs.
4. **Validate concept**: Present ideas in small sections (200-300 words), confirm each.
5. **Document outcome**: Save validated concept for next steps.

## Core Pattern

| Phase      | Action                                 | Output            |
| ---------- | -------------------------------------- | ----------------- |
| Understand | Ask clarifying questions one at a time | Problem statement |
| Explore    | Propose 2-3 approaches with trade-offs | Selected approach |
| Validate   | Present concept in small sections      | Validated concept |

## Key Rules

- ALWAYS ask ONE question per message - never overwhelm with multiple questions.
- MUST prefer multiple choice over open-ended questions when possible.
- ALWAYS explore 2-3 alternative approaches before settling on one.
- Present ideas incrementally in 200-300 word sections, confirm each before continuing.

## Question Examples

- "What problem are you trying to solve for users?"
- "Who is the primary user for this feature?"
- "What does success look like? (A) metric improvement (B) user satisfaction (C) both."

## Common Mistakes

- ❌ Ask multiple questions at once → ✅ One question per message.
- ❌ Jump to solutions immediately → ✅ Understand problem first.
- ❌ Skip alternatives → ✅ Always explore 2-3 approaches.