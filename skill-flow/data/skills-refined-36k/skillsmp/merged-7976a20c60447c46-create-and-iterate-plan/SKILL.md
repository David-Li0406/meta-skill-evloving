---
name: create-and-iterate-plan
description: Use this skill to create and iterate on detailed implementation plans through thorough research and user collaboration.
---

# Implementation Plan

You are tasked with creating and iterating on detailed implementation plans through an interactive, iterative process. You should be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications.

## Initial Response

When this command is invoked:

1. **Check if parameters were provided**:
   - If a file path or ticket reference was provided, skip the default message and read the provided files fully to begin the research process.
   - If no parameters are provided, respond with:
   ```
   I'll help you create or iterate on a detailed implementation plan. Please provide:
   1. The task/ticket description (or reference to a ticket file)
   2. Any relevant context, constraints, or specific requirements
   3. Links to related research or previous implementations
   ```

## Process Steps

### Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:
   - Ticket files (e.g., `thoughts/allison/tickets/eng_1234.md`)
   - Research documents
   - Related implementation plans
   - Any JSON/data files mentioned
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files.

2. **Spawn initial research tasks to gather context**:
   - Use specialized agents to research in parallel:
     - **codebase-locator** to find all files related to the ticket/task.
     - **codebase-analyzer** to understand how the current implementation works.
     - **thoughts-locator** to find any existing thoughts documents about this feature.
     - **linear-ticket-reader** for full details if a Linear ticket is mentioned.

3. **Read all files identified by research tasks**:
   - After research tasks complete, read ALL files they identified as relevant.

4. **Analyze and verify understanding**:
   - Cross-reference the ticket requirements with actual code.
   - Identify any discrepancies or misunderstandings.

5. **Present informed understanding and focused questions**:
   ```
   Based on the ticket and my research, I understand we need to [accurate summary].
   Questions that my research couldn't answer:
   - [Specific technical question]
   ```

### Step 2: Research & Discovery

1. **If the user corrects any misunderstanding**:
   - Spawn new research tasks to verify the correct information.

2. **Create a research todo list** using TodoWrite to track exploration tasks.

3. **Spawn parallel sub-tasks for comprehensive research**:
   - Use the right agent for each type of research:
     - **codebase-pattern-finder** for similar features.
     - **thoughts-analyzer** for key insights from relevant documents.

4. **Wait for ALL sub-tasks to complete** before proceeding.

5. **Present findings and design options**:
   ```
   Based on my research, here's what I found:
   **Current State:**
   - [Key discovery]
   **Design Options:**
   1. [Option A] - [pros/cons]
   ```

### Step 3: Plan Structure Development

1. **Create initial plan outline**:
   ```
   Here's my proposed plan structure:
   ## Overview
   [1-2 sentence summary]
   ## Implementation Phases:
   1. [Phase name] - [what it accomplishes]
   ```

2. **Get feedback on structure** before writing details.

### Step 4: Detailed Plan Writing

1. **Write the plan** to `thoughts/shared/plans/YYYY-MM-DD-ENG-XXXX-description.md`.
2. **Use this template structure**:
````markdown
# [Feature/Task Name] Implementation Plan

## Overview
[Brief description]

## Current State Analysis
[What exists now]

## Desired End State
[A Specification of the desired end state]

## Implementation Approach
[High-level strategy]

## Phase 1: [Descriptive Name]
### Overview
[What this phase accomplishes]
### Changes Required:
#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]
### Success Criteria:
#### Automated Verification:
- [ ] Migration applies cleanly
#### Manual Verification:
- [ ] Feature works as expected
````

### Step 5: Sync and Review

1. **Sync the thoughts directory** to ensure the plan is properly indexed.
2. **Present the draft plan location**:
   ```
   I've created the initial implementation plan at:
   `thoughts/shared/plans/YYYY-MM-DD-ENG-XXXX-description.md`
   ```

3. **Iterate based on feedback** until the user is satisfied.

### Step 6: Iterate on Existing Plans

1. **Read the existing plan file COMPLETELY** if the user provides a plan for iteration.
2. **Understand the requested changes** and determine if they require codebase research.
3. **Make focused, precise edits** to the existing plan, maintaining the existing structure.
4. **Present the changes made**:
   ```
   I've updated the plan at `thoughts/shared/plans/[filename].md`
   Changes made:
   - [Specific change 1]
   ```

## Important Guidelines

1. **Be Skeptical**: Question vague requirements and verify with code.
2. **Be Interactive**: Confirm understanding before making changes.
3. **Be Thorough**: Read all context files COMPLETELY before planning.
4. **Track Progress**: Use TodoWrite to track planning tasks.

## Success Criteria Guidelines

1. **Automated Verification**: Commands that can be run.
2. **Manual Verification**: UI/UX functionality and performance under real conditions.

## Example Interaction Flow

```
User: /create_plan
Assistant: I'll help you create a detailed implementation plan...
User: We need to add parent-child tracking for Claude sub-tasks. See thoughts/allison/tickets/eng_1478.md
Assistant: Let me read that ticket file completely first...
```