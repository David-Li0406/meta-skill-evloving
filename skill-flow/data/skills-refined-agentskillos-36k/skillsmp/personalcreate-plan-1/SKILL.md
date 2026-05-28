---
name: personal:create-plan
description: >
  Create detailed implementation plans through interactive, iterative collaboration.
  Use when the user asks for a technical plan or implementation strategy.
---

# Implementation Plan

You are tasked with creating detailed implementation plans through an interactive, iterative process. You should be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications.

## Initial Response

If the user has not provided a ticket, file path, or detailed request yet, respond with:
```
I'll help you create a detailed implementation plan. Let me start by understanding what we're building.

Please provide:
1. The task/ticket description (or reference to a ticket file)
2. Any relevant context, constraints, or specific requirements
3. Links to related research or previous implementations

I'll analyze this information and work with you to create a comprehensive plan.
```

Then wait for the user's input.

## Process Steps

### Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:
   - Ticket files (e.g., `path/to/ticket.md`)
   - Research documents
   - Related implementation plans
   - Any JSON/data files mentioned
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: DO NOT spawn sub-tasks before reading these files yourself in the main context
   - **NEVER** read files partially - if a file is mentioned, read it completely

2. **Spawn initial research tasks to gather context**:
   Before asking the user any questions, use specialized agents to research in parallel:

   - Use the `personal:codebase-locator` agent to find all files related to the ticket/task
   - Use the `personal:codebase-analyzer` agent to understand how the current implementation works

   These agents will:
   - Find relevant source files, configs, and tests
   - Identify the specific directories to focus on
   - Trace data flow and key functions
   - Return detailed explanations with file:line references

3. **Read all files identified by research tasks**:
   - After research tasks complete, read ALL files they identified as relevant
   - Read them FULLY into the main context
   - This ensures you have complete understanding before proceeding

4. **Analyze and verify understanding**:
   - Cross-reference the ticket requirements with actual code
   - Identify any discrepancies or misunderstandings
   - Note assumptions that need verification
   - Determine true scope based on codebase reality

5. **Present informed understanding and focused questions**:
   ```
   Based on the ticket and my research of the codebase, I understand we need to [accurate summary].

   I've found that:
   - [Current implementation detail with file:line reference]
   - [Relevant pattern or constraint discovered]
   - [Potential complexity or edge case identified]

   Questions that my research couldn't answer:
   - [Specific technical question that requires human judgment]
   - [Business logic clarification]
   - [Design preference that affects implementation]
   ```

   Only ask questions that you genuinely cannot answer through code investigation.

### Step 2: Research & Discovery

After getting initial clarifications:

1. **If the user corrects any misunderstanding**:
   - DO NOT just accept the correction
   - Spawn new research tasks to verify the correct information
   - Read the specific files/directories they mention
   - Only proceed once you've verified the facts yourself

2. **Create a research todo list** using TodoWrite to track exploration tasks

3. **Spawn parallel sub-tasks for comprehensive research**:
   - Create multiple Task agents to research different aspects concurrently
   - Use the right agent for each type of research:

   **For deeper investigation:**
   - `personal:codebase-locator` - To find more specific files (e.g., "find all files that handle [specific component]")
   - `personal:codebase-analyzer` - To understand implementation details (e.g., "analyze how [system] works")
   - `personal:codebase-pattern-finder` - To find similar features we can model after

   Each agent knows how to:
   - Find the right files and code patterns
   - Identify conventions and patterns to follow
   - Look for integration points and dependencies
   - Return specific file:line references
   - Find tests and examples

3. **Wait for ALL sub-tasks to complete** before proceeding

4. **Present findings and design options**:
   ```
   Based on my research, here's what I found:

   **Current State:**
   - [Key discovery about existing code]
   - [Pattern or convention to follow]

   **Design Options:**
   1. [Option A] - [pros/cons]
   2. [Option B] - [pros/cons]

   **Open Questions:**
   - [Technical uncertainty]
   - [Design decision needed]

   Which approach aligns best with your vision?
   ```

### Step 3: Plan Structure Development

Once aligned on approach:

1. **Create initial plan outline**:
   ```
   Here's my proposed plan structure:

   ## Overview
   [1-2 sentence summary]

   ## Implementation Phases:
   1. [Phase name] - [what it accomplishes]
   2. [Phase name] - [what it accomplishes]
   3. [Phase name] - [what it accomplishes]

   Does this phasing make sense? Should I adjust the order or granularity?
   ```

2. **Get feedback on structure** before writing details

### Step 4: Detailed Plan Writing

After structure approval:

1. **Gather plan metadata**:
   - Run the `~/bin/spec-metadata` script to capture date, branch, and commit

2. **Write the plan** to `.coding-agent/plans/YYYY-MM-DD-ENG-XXXX-description.md`
   - Format: `YYYY-MM-DD-ENG-XXXX-description.md` where:
     - YYYY-MM-DD is today's date
     - ENG-XXXX is the ticket number (omit if no ticket)
     - description is a brief kebab-case description
   - Examples:
     - With ticket: `2025-01-08-ENG-1478-parent-child-tracking.md`
     - Without ticket: `2025-01-08-improve-error-handling.md`

3. **Use this template structure**:

````markdown
# [Feature/Task Name] Implementation Plan

## Overview

[Brief description of what we're implementing]

## Plan Metadata

- Date: [from `~/bin/spec-metadata`]
- Git Commit: [from `~/bin/spec-metadata`]
- Branch: [from `~/bin/spec-metadata`]
- Repository: [from `~/bin/spec-metadata`]

## Motivation

[Why are we doing this? What problem are we solving? What triggered this work?]

### Relevant Artifacts
<!-- Links that provide context - these will be included in the PR description -->
- [Ticket](url)
- [Failed CI / Error logs / Slack thread / Design doc](url)
- [Related PR or previous work](url)

## Current State Analysis

[What exists today? What are the current pain points or limitations?]

## Requirements

[List explicit requirements, constraints, or acceptance criteria]

## Non-Goals

[Explicitly list what this work will NOT include]

## Proposed Approach

[High-level design of the solution, including key decisions and tradeoffs]

### Alternatives Considered

- [Alternative A] - [Why rejected]
- [Alternative B] - [Why rejected]

## Implementation Plan

### Phase 1: [Name]
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Phase 2: [Name]
- [ ] Task 1
- [ ] Task 2

### Phase 3: [Name]
- [ ] Task 1

## Testing Strategy

### Automated Verification
- [ ] `command to run`
- [ ] `another command`

### Manual Verification
- [ ] Step 1
- [ ] Step 2

## Test Results

| Test | Status | Output |
| --- | --- | --- |
| `command to run` | ⏳ Pending | |
| `another command` | ⏳ Pending | |

## Rollout Plan

[If applicable, how will this be deployed? Are there feature flags?]

## Risks & Mitigations

- [Risk] - [Mitigation]

## Open Questions

- [Question that needs clarification]
````

### Step 5: Review and Iterate

1. **Present the full plan** to the user
2. **Ask for explicit approval** before implementation
3. **Revise** based on feedback until approved

## Quality Bar

Your output should feel like a design doc that could be handed to a team for implementation. Be precise, thorough, and grounded in the actual codebase.
