---
name: domain-expert
description: Guardian of the 'Holy Trinity' (Business Plan, System Arch, Artie Persona). Use when validating features against core rules.
---

# Domain Expert

Guardian of the OlyBars "Holy Trinity" and specialized domain knowledge.

## When to use this skill

- Use this before implementing any major feature to ensure it aligns with the "Mission".
- This is helpful for validating gamification logic (points, decay).
- Use this when writing copy for "Artie" to ensure persona consistency.

## How to use it

### 1. The Holy Trinity Check

Before coding, ask:

1.  **Business Plan**: Does this feature require manual entry by a busy bar owner? (If yes -> REJECT).
2.  **System Arch**: Does this violate the "No Binge Gamification" rule? (If yes -> REJECT).
3.  **Artie Persona**: Is Artie acting like a "Bot" or a "Spirit"? (Must be Spirit).

### 2. Knowledge Graph & Lore

- Use the **`getLoreContext`** tool to retrieve official project facts before answering business questions.
- Consult `docs/knowledge/core/business_plan.md` for Roadmap priorities.
- Consult `docs/knowledge/core/system_architecture.md` for Point Logic.
- **Hierarchy of Truth**: Trinity Rules > Skills > Knowledge Base > Code.

### 3. Compliance

- Strictly follow WSLCB (Liquor Control) rules. No "Free Shots", no "Chug" contests.
