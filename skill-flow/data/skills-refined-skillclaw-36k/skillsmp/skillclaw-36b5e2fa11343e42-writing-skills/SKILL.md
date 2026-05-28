---
name: writing-skills
description: Use this skill for comprehensive guidance on writing, including style guidelines and testing methodologies for skill creation.
---

# Skill body

## Overview

The `writing-skills` skill provides a complete framework for writing, including style guidelines, testing methodologies, and best practices for skill creation. This skill integrates content from previously separate skills to ensure a single source of truth.

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: writing-skills | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: writing-skills | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.

## Key Components

1. **Skill Structure and Formatting**
   - Guidelines for structuring and formatting skills effectively.

2. **Testing Methodology**
   - Detailed methodology for testing skills, including:
     - When to test skills
     - Writing pressure scenarios
     - Pressure types
     - Key elements of good scenarios
     - Testing setup
     - VERIFY GREEN process
     - Plugging holes systematically
     - Re-verification
     - Meta-testing
     - When skill is bulletproof
     - Complete worked examples

3. **Writing Style Guidelines**
   - Voice and tone guidelines
   - Specificity and evidence rules
   - Banned words and phrases
   - LLM pattern avoidance
   - Punctuation and formatting

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

## Migration Notice

This skill consolidates all content from the deprecated `testing-skills-with-subagents` and `writing` skills. For all writing and testing needs, use this skill to avoid confusion and duplication.

## Worked Examples

Refer to the complete worked examples available in the `examples` directory for practical applications of this skill.