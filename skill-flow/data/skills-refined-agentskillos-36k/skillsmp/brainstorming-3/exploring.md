# EXPLORING Phase

The EXPLORING phase gathers context about the project and forms an initial understanding of what needs to be built.

## Purpose

- Understand the current project state
- Read relevant files and documentation
- Check recent git history for context
- Form an initial list of items/topics to discuss

## Process

1. **Check project state:**
   - Read relevant files (code, docs, configs)
   - Check recent commits for context
   - Understand existing architecture

2. **Gather requirements context:**
   - Review any existing specs or requirements
   - Understand stakeholder expectations
   - Identify constraints and dependencies

3. **Form initial item list:**
   - Create a preliminary list of topics to discuss
   - Group related items together
   - Prioritize by importance/dependencies

## Single-Item Mode (EXPLORING)

When `currentItem` is set in collab-state.json:

- Read relevant files based on item description
- Check git history for related changes
- Gather context specific to this item only
- Do NOT expand scope beyond this item

## Exit Criteria

- Context gathered from relevant files
- Initial list of items/topics formed
- Ready to discuss items one at a time

## Checkpoint: Current State Diagram

**REQUIRED** before proceeding to CLARIFYING:

Create a diagram showing the current state relevant to this work:

```
Tool: mcp__mermaid__create_diagram
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "name": "current-state-item-N",
  "content": <flowchart showing existing components/flow>
}
```

Display: "Current state diagram: [previewUrl]"

If the work item doesn't involve architecture/flow (e.g., pure text changes), create a simple diagram showing the file(s) being modified:

```mermaid
graph LR
    A[File: path/to/file.md] --> B[Section being modified]
```

## Transition to CLARIFYING

**Prerequisites:**
- Read relevant files/context
- Formed initial list of items

**Announce:** "I've gathered context. Now let me discuss each item with you one at a time."
