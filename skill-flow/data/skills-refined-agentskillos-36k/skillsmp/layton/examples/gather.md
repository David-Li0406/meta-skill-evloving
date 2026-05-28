---
name: gather
description: Aggregate data from all configured skills into a unified view
triggers:
  - gather data
  - collect skill data
  - aggregate skills
  - what's happening across my tools
---

## Objective

Read all skill files from `.layton/skills/`, execute their documented commands, and aggregate the results into a unified view. This workflow is a building block for other workflows like morning-briefing and focus-suggestion.

## Steps

### 1. List Configured Skills

Get the list of configured skills:

```bash
layton skills
```

If no skills are configured, suggest running `layton skills --discover` and `layton skills add <name>`.

### 2. Iterate Over Skill Files

For each skill in `.layton/skills/`:

1. **Read the skill file** to understand:
   - `## Commands` section: what to execute
   - `## What to Extract` section: what information matters
   - `## Key Metrics` section: important numbers to surface

2. **Execute commands** from the Commands section:
   - Run each command from the repo root
   - Capture stdout and stderr
   - Note exit codes

3. **Extract key information** using the guidance from "What to Extract":
   - Look for the specific data points mentioned
   - Parse structured output (JSON if available)
   - Handle missing or error states gracefully

### 3. Handle Failures Gracefully

When a skill command fails:

- Note the failure in results (don't stop gathering)
- Include the error message for context
- Continue with remaining skills
- Flag skills with errors in final summary

### 4. Aggregate Results

Organize gathered data by skill:

```text
Gathered Data
=============

## GTD
- Inbox: 3 items
- Next Actions: 12 tasks
- Waiting For: 5 items
- Status: OK

## Beads
- Watching: 8 items
- Focus: "Implement skill integration"
- Status: OK

## <Other Skills>
...
```

## Context Adaptation

- **If a skill has no commands**: Skip it but note in output
- **If all commands fail for a skill**: Mark as "unavailable" but continue
- **If JSON output available**: Prefer structured data over text parsing
- **If gathering takes too long**: Report partial results with note

## Success Criteria

- All configured skills are queried
- Failures don't stop the gather process
- Results are organized by skill name
- Key metrics extracted per skill file guidance
- Errors are clearly noted but don't crash the workflow
