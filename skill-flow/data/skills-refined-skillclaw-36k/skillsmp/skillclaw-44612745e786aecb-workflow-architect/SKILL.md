---
name: workflow-architect
description: Use this skill when you need to design, create, or refine workflows and skills for Antigravity, ensuring optimal structure and integration with existing capabilities.
---

# Skill Body

## Overview
The Workflow Architect skill is designed to help users create and refine workflows and skills within the Antigravity framework. It combines the processes of interviewing users to understand their needs, checking for existing workflows, and proposing optimal structures for new workflows or skills.

## When to Activate
- "Create a workflow for X"
- "I need a slash command that does Y"
- "Help me design an automation for Z"
- "Make a new skill for this process"

## Core Philosophy
1. **Interview First, Write Second** — Understand the goal before coding.
2. **No Duplicates** — Check for existing workflows to avoid redundancy.
3. **Skill-Aware** — Match workflow steps to existing skills.
4. **Pipeline Thinking** — Design workflows that chain logically.

## Steps to Create a Workflow or Skill

### Phase 1: Context Loading
1. **Existing Workflows**: Check for existing workflows in `.agent/workflows/`.
2. **Available Skills**: Review `squads/TEAM.md` for skills that can be invoked.
3. **Pipeline**: Understand the skill flow by reading `squads/PIPELINE.md`.

### Phase 2: Interview (Mandatory)
Ask 3-5 clarifying questions:
1. **Trigger**: What slash command should activate this workflow or skill?
2. **Goal**: What is the desired outcome (artifact, action, state change)?
3. **Mode**: Should it be interactive or autonomous?
4. **Skills**: Which existing skills should be involved?
5. **Overlap**: Does this duplicate any existing workflows or skills?

> **Important**: Do NOT write the workflow or skill until the user answers these questions!

### Phase 3: Design Proposal
Create a brief proposal in markdown format:

```markdown
# Proposed Workflow/Skill: /command-name

## Purpose
[One line description]

## Steps (Draft)
1. [Step 1] — `@skill-name`
2. [Step 2] — Command or action
3. [Step 3] — Output or artifact

## Overlap Check
- Existing workflows: [List any overlaps]
```

### Phase 4: Drafting the SKILL.md
Follow this template for the SKILL.md:
- **Frontmatter**:
  - **name**: lowercase-with-hyphens.
  - **description**: Third-person perspective focusing on utility.
  
- **Body Content**:
  - **Goal**: A summary of the skill’s purpose.
  - **Workflow**: A numbered list of logical steps.
  - **Constraints/Conventions**: Specific rules to follow.
  - **Error Handling**: Instructions for handling failures.

### Phase 5: Automation Protocol
If automation is required:
1. Write the necessary script (e.g., `.sh` or `.py`).
2. Ensure the script is executable (`chmod +x`).
3. In the SKILL.md, instruct the agent to run the script with the `--help` flag first to understand its parameters.

### Phase 6: Deployment
Once the user approves the draft:
1. Create the directory.
2. Write the files.
3. Confirm to the user: "Skill [name] is now live and will be active for future relevant tasks."