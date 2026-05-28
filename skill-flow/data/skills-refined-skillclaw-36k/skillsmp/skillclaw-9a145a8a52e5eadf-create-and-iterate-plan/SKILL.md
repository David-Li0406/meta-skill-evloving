---
name: create-and-iterate-plan
description: Use this skill to create detailed implementation plans or iterate on existing ones through thorough research and user collaboration.
---

# Skill body

## Implementation Plan

You are tasked with creating detailed implementation plans or updating existing ones through an interactive, iterative process. You should be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications.

### Initial Response

When this command is invoked:

1. **Check if parameters were provided**:
   - If a file path or ticket reference was provided as a parameter, skip the default message.
   - Immediately read any provided files FULLY.
   - Begin the research process.

2. **If no parameters provided**, respond with:
```
I'll help you create or iterate on a detailed implementation plan. Let me start by understanding what we're building.

Please provide:
1. The task/ticket description (or reference to a ticket file)
2. Any relevant context, constraints, or specific requirements
3. Links to related research or previous implementations

I'll analyze this information and work with you to create a comprehensive plan.

Tip: You can also invoke this command with a ticket file directly: `/create_plan thoughts/allison/tickets/eng_1234.md`
For deeper analysis, try: `/create_plan think deeply about thoughts/allison/tickets/eng_1234.md`
```
Then wait for the user's input.

### Process Steps

#### Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:
   - Ticket files (e.g., `thoughts/allison/tickets/eng_1234.md`)
   - Research documents
   - Related implementation plans
   - Any JSON/data files mentioned
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files.
   - **CRITICAL**: DO NOT spawn sub-tasks before reading these files yourself in the main context.
   - **NEVER** read files partially - if a file is mentioned, read it completely.

2. **Spawn initial research tasks to gather context**:
   Before asking the user any questions, use specialized agents to research in parallel:
   - Use the **codebase-locator** agent to find all files related to the ticket/task.
   - Use the **codebase-analyzer** agent to understand how the current implementation works.
   - If relevant, use the **thoughts-locator** agent to find any existing thoughts documents about this feature.
   - If a Linear ticket is mentioned, use the **linear-ticket-reader** agent to get full details.

#### Step 2: Iteration on Existing Plans

1. **Parse the input to identify**:
   - Plan file path (e.g., `thoughts/shared/plans/2025-10-16-feature.md`)
   - Requested changes/feedback.

2. **Handle different input scenarios**:
   - If NO plan file provided:
   ```
   I'll help you iterate on an existing implementation plan.

   Which plan would you like to update? Please provide the path to the plan file (e.g., `thoughts/shared/plans/2025-10-16-feature.md`).

   Tip: You can list recent plans with `ls -lt thoughts/shared/plans/ | head`
   ```
   Wait for user input, then re-check for feedback.

   - If plan file provided but NO feedback:
   ```
   I've found the plan at [path]. What changes would you like to make?

   For example:
   - "Add a phase for migration handling"
   - "Update the success criteria to include performance tests"
   - "Adjust the scope to exclude feature X"
   - "Split Phase 2 into two separate phases"
   ```
   Wait for user input.

   - If BOTH plan file AND feedback provided:
   - Proceed immediately to Step 1.
   - No preliminary questions needed.

3. **Read and Understand Current Plan**:
   - Use the Read tool WITHOUT limit/offset parameters to read the existing plan file COMPLETELY.
   - Understand the current structure, phases, and scope.
   - Note the success criteria and implementation approach.

4. **Understand the requested changes**:
   - Parse what the user wants to add/modify/remove.
   - Identify if changes require codebase research.
   - Determine the scope of the update.

5. **Research If Needed**:
   - Only spawn research tasks if the changes require new technical understanding.
   - Create a research todo list using TodoWrite.
   - Spawn parallel sub-tasks for research using the appropriate agents.

This skill allows for both the creation of new plans and the iteration of existing ones, ensuring a comprehensive approach to implementation planning.