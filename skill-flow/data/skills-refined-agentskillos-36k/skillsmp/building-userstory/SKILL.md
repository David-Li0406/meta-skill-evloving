---
name: building-userstory
description: Interactive Q&A to build UserStory.md from user input. Use when the user wants to create a user story document or start the assisted workflow.
---

# User Story Builder

Interactively builds `docs/UserStory.md` through structured Q&A with the user.

## Purpose

Guides users through creating a user story document that can be transformed into PRD.md using the `generating-prd-from-userstory` skill.

## Workflow

1. **Check for existing UserStory.md**
   - If exists, ask user if they want to rebuild (backup as `docs/UserStory.md.bak`)

2. **Ask structured questions** using AskUserQuestion tool for each template section:
   - Project name
   - Problem statement
   - Target users
   - Value proposition
   - User stories (use "As a [role], I want to [action] so that [benefit]" format)
   - Success criteria
   - Constraints
   - Out of scope

3. **Generate UserStory.md**
   - Read template from `ralph/templates/userstory.md.template`
   - Replace placeholders with user responses
   - Write to `docs/UserStory.md`

4. **Suggest next step**: `make ralph_prd` to generate PRD.md

## Template

See `ralph/templates/userstory.md.template` for structure and placeholders.

## Usage

```bash
make ralph_userstory
```
