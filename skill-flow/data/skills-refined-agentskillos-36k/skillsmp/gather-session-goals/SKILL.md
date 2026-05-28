---
name: gather-session-goals
description: Collect and classify work items at the start of a collab session. Invoked by collab skill after creating a new session.
user-invocable: false
model: opus
allowed-tools: mcp__plugin_mermaid-collab_mermaid__*, Read
---

# Gather Session Goals

## Overview

Collect and classify work items at the start of a collab session through iterative questioning.

**Invoked by:** collab skill after creating a new session

**Returns to:** collab skill (which manages the work item loop)

## Collab Session Required

Before proceeding, check for active collab session:

1. Check if `.collab/` directory exists
2. Check if any session folders exist within
3. If no session found:
   ```
   No active collab session found.

   Use /collab to start a session first.
   ```
   **STOP** - do not proceed with this skill.

4. If multiple sessions exist, check `COLLAB_SESSION_PATH` env var or ask user which session.

## The Process

### Step 1: Open Question

Ask the user: **"What do you want to accomplish this session?"**

Store the initial response. Parse any items mentioned and add them to the work items list with type = "unknown".

### Step 2: Anything Else Loop

After parsing the initial response:

1. Infer type for each item from context:
   - Contains "setup", "install", "configure", "organize", "clean up", "docker", "deploy" → type = "task"
   - Contains "fix", "bug", "broken", "error", "crash", "fail" → type = "bugfix"
   - Contains "add", "new", "create", "implement", "build", "refactor", "clean", "simplify", "restructure", "investigate", "explore", "spike" → type = "code"
   - Otherwise → type = "unknown"

2. Ask: **"Anything else?"**

3. If user provides more items:
   - Parse and infer types
   - Repeat from step 2

4. If user says no/done/that's it:
   - Proceed to Step 3

### Step 3: Classify Unknown Items

For each item still marked as type = "unknown":

Ask: **"What type is '[item title]'?"**
```
1. code
2. bugfix
3. task
```

Set the item type based on user response.

### Step 4: Present Summary

Display the work items for confirmation:

```
Here are the work items for this session:

1. [bugfix] Fix login redirect issue
2. [code] Add user authentication
3. [code] Clean up database layer

Does this list look correct?

1. Yes
2. Add more
3. Remove item
4. Edit item
```

**Handle user responses:**
- **1 (Yes)** - Proceed to Step 5
- **2 (Add more)** - Return to Step 2
- **3 (Remove)** - Ask which item to remove, remove it, return to Step 4
- **4 (Edit)** - Ask which item to edit, update it, return to Step 4

### Step 5: Write to Design Doc

**Before writing, output:** "Writing work items to design doc..."

1. Read current design doc:
   Tool: mcp__mermaid__get_document
   Args: { "project": "<cwd>", "session": "<session>", "id": "design" }

2. Parse existing content and locate "## Work Items" section

3. Build new Work Items content:
   FOR each work_item in confirmed_list:
     ADD markdown block:
       ### Item {N}: {title}
       **Type:** {type}
       **Status:** pending
       **Problem/Goal:**

       **Approach:**

       **Root Cause:** (only if type is bugfix)

       **Success Criteria:**

       **Decisions:**

       ---

4. Replace "## Work Items" section with new content

5. Write updated design doc:
   Tool: mcp__mermaid__update_document
   Args: { "project": "<cwd>", "session": "<session>", "id": "design", "content": "<updated-full-content>" }

**Note:** Full update is appropriate here because we're writing an entire new Work Items section.
For subsequent edits (e.g., updating a single item), prefer `patch_document` instead.

After writing, display:

```
Work items written to design doc. Returning to collab workflow.
```

Return control to the collab skill.

## Key Constraints

- **One question at a time** - Never batch multiple questions together
- **Don't skip classification** - Every item must have a type before proceeding
- **Must get explicit confirmation** - User must approve the list before writing to design doc

## Contract

**Preconditions:**
- Collab session exists
- Design doc exists (may be empty template)

**Postconditions:**
- Design doc contains `## Work Items` section
- At least one work item defined
- All items have `Status: pending`
- User has confirmed the list

**Side effects:**
- Writes to design doc
- Does NOT modify collab-state.json (collab skill handles that)

## Browser-Based Questions

When a collab session is active, prefer `render_ui` for user interactions.

**For item type classification:**
```
Tool: mcp__mermaid__render_ui
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "ui": {
    "type": "Card",
    "props": { "title": "Classify item" },
    "children": [
      { "type": "Markdown", "props": { "content": "What type is **[item title]**?" } },
      {
        "type": "RadioGroup",
        "props": {
          "name": "type",
          "options": [
            { "value": "code", "label": "Code (feature, refactor, investigation)" },
            { "value": "bugfix", "label": "Bugfix (fix, error, crash)" },
            { "value": "task", "label": "Task (setup, config, organization)" }
          ]
        }
      }
    ],
    "actions": [{ "id": "classify", "label": "Continue", "primary": true }]
  },
  "blocking": true
}
```

**For work items list confirmation:**
```
Tool: mcp__mermaid__render_ui
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "ui": {
    "type": "Card",
    "props": { "title": "Confirm work items" },
    "children": [
      { "type": "Markdown", "props": { "content": "[markdown list of items]" } },
      {
        "type": "RadioGroup",
        "props": {
          "name": "action",
          "options": [
            { "value": "yes", "label": "Yes, this is correct" },
            { "value": "add", "label": "Add more items" },
            { "value": "remove", "label": "Remove an item" },
            { "value": "edit", "label": "Edit an item" }
          ]
        }
      }
    ],
    "actions": [{ "id": "confirm", "label": "Continue", "primary": true }]
  },
  "blocking": true
}
```

## Integration

**Called by:**
- **collab** skill - After session creation

**Returns to:**
- **collab** skill - To start the work item loop
