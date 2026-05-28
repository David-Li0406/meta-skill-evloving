---
name: author-workflow
description: Create or capture a workflow file for Layton
triggers:
  - create a workflow
  - new workflow
  - add workflow
  - turn this into a workflow
  - save as workflow
  - capture workflow
  - make this repeatable
  - workflow authoring
---

<required_reading>
**Read before starting:**

1. references/workflow-authoring.md - Template and field guide
</required_reading>

## Objective

Help the user create a well-populated workflow file. This workflow handles both:

- **Creating** a new workflow from scratch (guided Q&A)
- **Capturing** a workflow from recent conversation (retrospective extraction)

## Steps

### 1. Determine Mode

Ask the user:

> "I can help you create a workflow file. Which mode?
>
> 1. **Create from scratch** - I'll guide you through defining a new workflow
> 2. **Capture from conversation** - I'll extract a workflow from what we just did
> 3. **Edit existing** - Update a workflow file you already have"

**Wait for response.**

Route based on answer:

- 1 → Continue to "Create Mode" section
- 2 → Continue to "Capture Mode" section
- 3 → Ask which workflow, then read and edit it

---

## Create Mode

### 2a. Understand the Purpose

Ask the user:

> "What workflow do you want to create?
>
> 1. **Name**: What should we call it? (lowercase with hyphens, e.g., 'morning-briefing')
> 2. **Purpose**: What does it accomplish? When would you run it?"

**Wait for response.** Extract `name` and `description`.

### 3a. Define Triggers

Ask the user:

> "What phrases should trigger this workflow? These are things you might say.
>
> Examples for a morning briefing: 'good morning', 'daily standup', 'what should I know'
>
> What 2-5 phrases work for yours?"

**Wait for response.** Extract triggers list.

### 4a. Map the Steps

Guide through steps one at a time:

> "Walk me through what this workflow should do, step by step.
>
> For each step:
>
> - What action? (run a command, query something, synthesize)
> - What data is needed?
> - Any decisions based on results?
>
> Start with step 1..."

**Wait for each step.** Continue until user indicates completion.

### 5a. Identify Adaptations

Ask the user:

> "Should this workflow behave differently based on context?
>
> Examples:
>
> - Morning vs evening
> - Workday vs weekend
> - High vs low workload
>
> Any adaptations?"

**Wait for response.** Extract context rules.

### 6a. Define Success

Ask the user:

> "How do you know this workflow completed successfully?
> What should be true when it's done?"

**Wait for response.** Extract success criteria.

Continue to "Create the File" section.

---

## Capture Mode

### 2b. Review Conversation

Scan recent conversation for:

- **Sequence of actions**: What steps were taken, in what order
- **Commands run**: bash, MCP calls, queries
- **Decisions made**: conditional logic, branching
- **Synthesis**: how information was combined

Present findings:

> "From our conversation, I identified these steps:
>
> 1. {step 1}
> 2. {step 2}
> ...
>
> Is this the process to save? Anything to add or change?"

**Wait for confirmation.**

### 3b. Name and Triggers

If not obvious, ask:

> "What should we call this workflow?
> And what phrases should trigger it?"

**Wait for response.**

Continue to "Create the File" section.

---

## Create the File

### 7. Check for Existing

```bash
layton workflows
```

If workflow name already exists, ask if user wants to overwrite or pick a different name.

### 8. Generate the Workflow File

```bash
layton workflows add <name>
```

This creates a file from `templates/workflow.md`. Edit it to replace the skeleton placeholders with the gathered/captured information.

Reference `references/workflow-authoring.md` for field guidance and optional sections.

### 9. Validate and Confirm

Show the user the created file.

> "Here's the workflow. Does this capture what you wanted?
>
> Want to do a dry-run walkthrough?"

If dry-run:

- Walk through each step
- Show what would happen
- Confirm the flow makes sense

## Context Adaptation

- **If user says "turn this into a workflow"**: Go directly to Capture Mode
- **If user says "create a workflow for X"**: Go directly to Create Mode
- **If process was simple** (2-3 steps): Keep it concise
- **If process was complex**: Consider breaking into phases
- **If steps overlap with existing workflows**: Note and suggest extension

## Success Criteria

- [ ] Workflow file created at `.layton/workflows/<name>.md`
- [ ] All sections populated (not skeleton placeholders)
- [ ] Triggers are natural phrases the user would say
- [ ] Steps are clear enough for AI to follow
- [ ] User confirms the workflow looks correct
