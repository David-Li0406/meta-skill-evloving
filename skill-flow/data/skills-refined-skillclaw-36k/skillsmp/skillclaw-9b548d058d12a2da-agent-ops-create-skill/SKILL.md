---
name: agent-ops-create-skill
description: Use this skill when you want to create new AgentOps skills through an interactive interview process, supporting both from-scratch and clone modes with tiered complexity.
---

# Create Skill Workflow

## Purpose

Guide users through creating new AgentOps skills with consistent structure and quality. This process reduces friction for skill ecosystem growth while enforcing standards.

## Mode Selection

Present mode options at the start:

| Mode | Description | Use When |
|------|-------------|----------|
| **A) From scratch** | Start with a blank template | Creating entirely new capability |
| **B) Clone existing** | Use an existing skill as a base | New skill similar to an existing one |

### Clone Mode Procedure

1. List available skills from `.github/skills/`
2. User selects one to clone
3. Read that skill's SKILL.md as a base
4. Interview focuses on what to change/customize

## Complexity Tiers

After mode selection, assess complexity:

| Tier | Questions | Criteria |
|------|-----------|----------|
| **Simple** | 5 | Single procedure, minimal dependencies, clear scope |
| **Complex** | 10+ | Multiple procedures, decision trees, error handling, many dependencies |

### Complexity Assessment Questions

Ask the user:
1. "Does this skill have a single main procedure, or multiple branching paths?"
2. "Does it need to invoke other skills or handle errors specially?"

**If answers suggest simple** → Simple tier (5 questions)  
**If answers suggest complex** → Complex tier (10+ questions)

---

## Interview Questions

### Simple Tier (5 Questions)

Use `agent-ops-interview` skill for one-question-at-a-time flow.

| # | Question | Field | Validation |
|---|----------|-------|------------|
| 1 | "What should this skill be called? (use kebab-case, e.g., `my-custom-skill`)" | `name` | Kebab-case, unique in `.github/skills/`. **Must NOT start with `agent-ops-`** (reserved for bundled assets). |
| 2 | "Describe in one sentence what this skill does:" | `description` | Non-empty, < 200 chars |
| 3 | "What is the main procedure? Describe the step-by-step workflow:" | Procedure section | Non-empty |
| 4 | "What state files does it read and write? (e.g., focus.md, issues/*)" | `state_files` | Valid file paths or patterns |
| 5 | "Should this skill have an accompanying prompt file for slash command usage? (yes/no)" | `create_prompt` | Boolean - if yes, generate `.github/prompts/{name}.prompt.md` |