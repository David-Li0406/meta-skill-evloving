---
name: deepwork-rules
description: Use this skill to create file-change rules that enforce guidelines during AI sessions, automating documentation sync or code review triggers.
---

# deepwork_rules

**Multi-step workflow**: This skill creates file-change rules that enforce guidelines during AI sessions. Use it when automating documentation sync or code review triggers.

> **CRITICAL**: Always invoke steps using the Skill tool. Never copy/paste step instructions directly.

## Overview

This skill manages rules that automatically trigger when certain files change during an AI agent session. Rules help ensure that code changes follow team guidelines, documentation is updated, and architectural decisions are respected.

**Important**: Rules are evaluated at the "Stop" hook, which fires when an agent finishes its turn, including when sub-agents complete their work. Rules are NOT evaluated immediately after each file edit; they batch up and run once at the end of the agent's response cycle.

- **Command action rules**: Execute their command (e.g., `uv sync`) when the agent stops.
- **Prompt action rules**: Display instructions to the agent, blocking until addressed.

Rules are stored as individual markdown files with YAML frontmatter in the `.deepwork/rules/` directory. Each rule file specifies:
- **Detection mode**: trigger/safety, set (bidirectional), or pair (directional).
- **Patterns**: Glob patterns for matching files, with optional variable capture.
- **Action type**: prompt (default) to show instructions, or command to run a shell command.
- **Instructions**: Markdown content describing what the agent should do.

## Available Steps

1. **define** - Creates a rule file that triggers when specified files change. Use this step when setting up documentation sync, code review requirements, or automated commands.

## Execution Instructions

### Step 1: Analyze Intent

Parse any text following `/deepwork_rules` to determine user intent:
- "define" or related terms → start at `deepwork_rules.define`.

### Step 2: Invoke Starting Step

Use the Skill tool to invoke the identified starting step:
```
Skill tool: deepwork_rules.define
```

### Step 3: Continue Workflow Automatically

After each step completes:
1. Check if there's a next step in the sequence.
2. Invoke the next step using the Skill tool.
3. Repeat until the workflow is complete or the user intervenes.

### Handling Ambiguous Intent

If user intent is unclear, use AskUserQuestion to clarify:
- Present available steps as numbered options.
- Let the user select the starting point.

## Guardrails

- Do NOT copy/paste step instructions directly; always use the Skill tool to invoke steps.
- Do NOT skip steps in the workflow unless the user explicitly requests it.
- Do NOT proceed to the next step if the current step's outputs are incomplete.
- Do NOT make assumptions about user intent; ask for clarification when ambiguous.

## Context Files

- Job definition: `.deepwork/jobs/deepwork_rules/job.yml`

## Define Rule

### Objective

Create a new rule file in the `.deepwork/rules/` directory to enforce team guidelines, documentation requirements, or other constraints when specific files change.

### Task

Guide the user through defining a new rule by asking structured questions. **Do not create the rule without first understanding what they want to enforce.**

### Step 1: Understand the Rule Purpose

Start by asking structured questions to understand what the user wants to enforce:
1. **What guideline or constraint should this rule enforce?**
   - What situation triggers the need for action?
   - What files or directories, when changed, should trigger this rule?
2. **What action should be taken?**
   - What should the agent do when the rule triggers?
3. **Are there any "safety" conditions?**
   - Are there files that, if also changed, mean the rule doesn't need to fire?

### Step 2: Choose the Detection Mode

Help the user select the appropriate detection mode:
- **Trigger/Safety Mode**: Fires when trigger patterns match AND no safety patterns match.
- **Set Mode**: Fires when files that should change together don't all change.
- **Pair Mode**: Fires when a trigger file changes but expected files don't.

### Step 3: Define the Patterns

Help the user define glob patterns for files.

### Step 4: Choose the Comparison Mode (Optional)

The `compare_to` field controls what baseline is used when detecting "changed files".

### Step 5: Write the Instructions

Create clear, actionable instructions for what the agent should do when the rule fires.

### Step 6: Create the Rule File

Create a new file in `.deepwork/rules/` with a kebab-case filename.

### Step 7: Verify the Rule

After creating the rule:
1. Check the YAML frontmatter.
2. Test trigger patterns.
3. Review instructions.
4. Check for conflicts.

## Example Rules

### Update Documentation on Config Changes
```markdown
---
name: Update Install Guide on Config Changes
trigger: app/config/**/*
safety: docs/install_guide.md
---
Configuration files have been modified. Please review docs/install_guide.md
and update it if any installation instructions need to change based on the
new configuration.
```

### Security Review for Auth Code
```markdown
---
name: Security Review for Authentication Changes
trigger:
  - src/auth/**/*
  - src/security/**/*
safety:
  - SECURITY.md
  - docs/security_audit.md
---
Authentication or security code has been changed. Please review for hardcoded credentials or secrets.
```

## Required Inputs

**User Parameters** - Gather from user before starting:
- **rule_purpose**: What guideline or constraint should this rule enforce?

## Outputs

**Required outputs**:
- `.deepwork/rules/{rule-name}.md`

## On Completion

1. Verify outputs are created.
2. Inform user: "define complete, outputs: .deepwork/rules/{rule-name}.md".

This skill can be re-run anytime.