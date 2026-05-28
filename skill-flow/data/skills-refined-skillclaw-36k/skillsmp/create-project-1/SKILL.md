---
name: create-project
description: Create PARA project notes with validated area connections and PARA philosophy guidance. Ensures projects have clear outcomes, deadlines, and valid area relationships. Use when creating new projects to ensure they follow PARA method correctly.
allowed-tools: AskUserQuestion, mcp__plugin_para-obsidian_para-obsidian__para_create, mcp__plugin_para-obsidian_para-obsidian__para_list_areas, mcp__plugin_para-obsidian_para-obsidian__para_list_projects, mcp__plugin_para-obsidian_para-obsidian__para_template_fields, mcp__plugin_para-obsidian_para-obsidian__para_config
---

# Create Project

Create PARA-compliant project notes with validated area connections through collaborative dialogue.

## Core Philosophy

**From Tiago Forte's PARA Method:**

- **Project** = Has a specific outcome AND deadline. Can be marked "complete."
- **Area** = Standard to maintain. Continuous, no end date.
- **Every project falls within an area** - they're interdependent.
- **Organize by actionability**, not subject matter.

This skill ensures projects are well-defined and properly connected to your life structure.

## Critical Rules

1. **ALWAYS load areas first** - Never suggest areas that don't exist in the vault
2. **NEVER invent connections** - Only offer areas from the loaded list or create new ones
3. **Projects MUST have outcomes** - If no clear outcome, it might be an area instead
4. **Projects MUST have deadlines** - "Ongoing" means it's an area, not a project
5. **Area selection is REQUIRED** - Every project falls within an area
6. **Classification, not invention** - AI classifies into existing categories; user provides facts

## Workflow Overview

```
Phase 0: Load Vault Context (ALWAYS FIRST)
    ↓
Phase 1: Gather Project Intent
    ├── What outcome?
    └── When complete? (validates it's a project)
    ↓
Phase 2: Area Selection (CRITICAL - prevents invalid areas)
    ├── Present numbered list from vault
    ├── User selects OR creates new
    └── NEVER accept free-text area names
    ↓
Phase 3: Confirm & Create
    ├── Present complete proposal
    ├── User approves or adjusts
    └── Create with validated frontmatter
```

---

## Phase 0: Load Vault Context

**ALWAYS fetch vault context before doing anything else:**

```
para_list_areas({ response_format: "json" })
para_list_projects({ response_format: "json" })
```

Store these lists for:
- Area validation in Phase 2
- Detecting duplicate project names
- Understanding user's current structure

**If user provides context in initial message**, still load areas first before responding.

---

## Phase 1: Gather Project Intent

### 1.1 Understand the Outcome

If not provided in initial message, ask:

```
I'll help you create a new project. Let me ask a few questions to ensure it follows the PARA method.

**What outcome do you want to achieve?**
(A project has a specific end result - something you can "complete")
```

**Good outcomes:**
- "Set up Clawdbot for my messaging apps"
- "Migrate database to PostgreSQL"
- "Plan Melanie's birthday trip"

**Bad outcomes (suggest area instead):**
- "Manage my health" → Area: Health
- "Stay on top of finances" → Area: Finance

### 1.2 Confirm Deadline

```
**When should this be complete?**
(PARA projects have deadlines - when will you know this is done?)

Examples: "2025-03-31", "end of Q1", "next month", "by Feb 28"
```

If user says "ongoing" or "no deadline":

```
That sounds more like an **Area** (ongoing responsibility) than a **Project** (specific outcome with deadline).

Would you like to:
1. **Create an area instead** - For ongoing responsibilities
2. **Set a target date** - Even rough estimates help (e.g., "sometime in Q2")
3. **Continue as project** - I'll use a placeholder date you can update later
```

### 1.3 Extract Title

From the outcome, suggest a clear project title:

```
Based on your outcome, I suggest:

**Title:** 🎯 [Clear Action + Object]

Examples:
- Outcome: "Set up Clawdbot" → 🎯 Clawdbot Setup & Integration
- Outcome: "Plan birthday trip" → 🎯 Melanie Birthday Trip 2025
- Outcome: "Migrate database" → 🎯 PostgreSQL Migration

Does this title work, or would you prefer something different?
```

---

## Phase 2: Area Selection

**CRITICAL: This phase prevents the "invalid area" bug.**

### 2.1 Present Valid Areas

Using the areas loaded in Phase 0, present a numbered list:

```
**Which life domain does this project belong to?**

Your existing areas:
1. 🎹 Movie Love
2. 🏠 Property
3. 🏡 Home
4. 🐶 Pet - Muffin
5. 📝 Note Taking
6. 🔧 Dotfiles
7. 🤖 AI Practice

Choose a number, or type "new" to create a new area first.
```

### 2.2 Handle User Selection

| Response | Action |
|----------|--------|
| Number (e.g., `7`) | Use that area: `[[🤖 AI Practice]]` |
| `new` / `create new` | Go to Phase 2.3 (Create Area Sub-flow) |
| Area name verbatim | Match against list, use if found |
| Invalid input | Re-prompt with numbered list |

**NEVER allow:**
- Free-text area entry that could create broken wikilinks
- Accepting areas not in the loaded list without explicit creation

### 2.3 Create Area Sub-flow (if "new")

```
**Creating a new area first...**

Areas are ongoing life responsibilities (no end date). Examples:
- 🏡 Home - Household maintenance and improvements
- 💼 Career - Professional development and work
- 🏃 Health - Physical and mental wellness

**What responsibility or life domain is this?**
```

After user provides name:

```
para_create({
  template: "area",
  title: "[User's area name]",
  dest: "02 Areas",
  response_format: "json"
})
```

Then continue with project creation using the new area.

---

## Phase 3: Confirm & Create

### 3.1 Present Complete Proposal

```
## Project Proposal

**Title:** 🎯 [Title from Phase 1.3]
**Outcome:** [Clear outcome statement]
**Deadline:** [Date from Phase 1.2]
**Area:** [[Area from Phase 2]]
**Status:** planning

### Generated Sections
- **Why This Matters:** [Generated from context - problem it solves, why now]
- **Tasks:** [First actionable steps to get started]

---

**Ready to create?** (yes / tell me what to change)
```

### 3.2 Handle Response

| Response | Action |
|----------|--------|
| `yes` / `y` / `looks good` | Create immediately |
| Specific feedback | Adjust and re-present OR apply and create |
| `cancel` / `no` | Abort gracefully |

### 3.3 Create Project Note

```
para_create({
  template: "project",
  title: "[Validated title]",
  dest: "01 Projects",
  args: {
    "Status (planning/active/on-hold/completed)": "planning",
    "Target completion date (YYYY-MM-DD)": "[Validated date]",
    "Area": "[Validated area from Phase 2]"  // Note: template wraps in [[]]
  },
  content: {
    "Why This Matters": "[Generated content - problem it solves, why now]",
    "Tasks": "- [ ] [First suggested task]\n- [ ] [Second task if applicable]"
  },
  response_format: "json"
})
```

### 3.4 Confirm Creation

```
Created: 🎯 [Project Title].md → 01 Projects
Linked to: [[Area Name]]

Would you like to:
1. **Add initial tasks** - Break down the first steps
2. **Link resources** - Connect existing notes
3. **Done** - Project is ready to go
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No areas exist | Offer to create first area before project |
| Duplicate project name | Suggest alternative or confirm overwrite |
| Invalid date format | Re-prompt with examples |
| Area creation fails | Show error, retry area creation |
| Project creation fails | Show error, don't lose user's input |

---

## Example Interaction

```
User: /para-obsidian:create-project

AI: I'll help you create a new project. First, let me load your vault structure.

    Your areas:
    1. 🎹 Movie Love
    2. 🏠 Property
    3. 🏡 Home
    4. 🐶 Pet - Muffin
    5. 📝 Note Taking
    6. 🔧 Dotfiles
    7. 🤖 AI Practice

    What outcome do you want to achieve?

User: Set up Clawdbot for my messaging apps

AI: Great! When do you need this done by?

User: End of February

AI: Which area does this project fall under?

    Looking at your areas, I'd suggest:
    - 🤖 AI Practice (since Clawdbot is AI-related)

    Choose a number (1-7), or type "new" to create a new area.

User: 7

AI: ## Project Proposal

    **Title:** 🎯 Clawdbot Setup & Integration
    **Outcome:** Set up Clawdbot for messaging apps
    **Deadline:** 2025-02-28
    **Area:** [[🤖 AI Practice]]
    **Status:** planning

    ### Generated Sections
    - **Why This Matters:** Enables AI-assisted messaging across apps.
      This automates responses and saves time on routine conversations.
    - **Tasks:**
      - [ ] Research Clawdbot setup requirements
      - [ ] Install and configure Clawdbot
      - [ ] Connect to primary messaging apps
      - [ ] Test and validate working

    ---

    **Ready to create?** (yes / tell me what to change)

User: yes

AI: Created: 🎯 Clawdbot Setup & Integration.md → 01 Projects
    Linked to: [[🤖 AI Practice]]

    Would you like to add initial tasks or link resources?
```

---

## PARA Philosophy Reference

See `./references/para-philosophy.md` for deeper explanation of:
- Project vs Area distinction
- The "three questions" pattern
- How projects and areas feed each other
- Common classification mistakes
