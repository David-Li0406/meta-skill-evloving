---
name: using-skills
description: Use this skill when starting any conversation to ensure mandatory workflows for finding and using skills are followed, including invoking relevant skills before any task.
---

# Skill body

## MANDATORY FIRST RESPONSE PROTOCOL

Before responding to ANY user message, complete this checklist:

1. **List available skills mentally.**
2. **Ask yourself:** "Does ANY skill match this request?"
3. **If yes:** Use the `Skill` tool to load the skill file.
4. **Announce which skill you're using** with the format: 
   ```
   🔧 Using Skill: [Skill Name] | [brief purpose based on context]
   ```
5. **Follow the skill exactly.**

**Responding WITHOUT completing this checklist = automatic failure.**

## Critical Rules

1. **Follow mandatory workflows.** Always check for relevant skills before ANY task.
2. **Execute skills with the Skill tool.** Never rely on memory or previous knowledge of skills.
3. **If a skill applies to your task, you MUST use it.** This is not negotiable.

## Skills with Checklists

If a skill has a checklist, YOU MUST create TodoWrite todos for EACH item.

**Don't:**
- Work through checklist mentally.
- Skip creating todos "to save time."
- Batch multiple items into one todo.
- Mark complete without doing them.

**Why:** Checklists without TodoWrite tracking lead to missed steps. The overhead of TodoWrite is minimal compared to the cost of missing steps.

## Common Rationalizations That Mean You're About To Fail

If you catch yourself thinking ANY of these thoughts, STOP. You are rationalizing. Check for and use the skill.

- "This is just a simple question" → WRONG. Questions are tasks. Check for skills.
- "I can check files quickly" → WRONG. Files don't have conversation context. Check for skills.
- "Let me gather information first" → WRONG. Skills tell you HOW to gather information. Check for skills.
- "This doesn't need a formal skill" → WRONG. If a skill exists for it, use it.
- "I remember this skill" → WRONG. Skills evolve. Run the current version.
- "This doesn't count as a task" → WRONG. If you're taking action, it's a task. Check for skills.
- "The skill is overkill for this" → WRONG. Skills exist because simple things can become complex. Use it.
- "I'll just do this one thing first" → WRONG. Check for skills BEFORE doing anything.

**Why:** Skills document proven techniques that save time and prevent mistakes. Not using available skills means repeating solved problems and making known errors.