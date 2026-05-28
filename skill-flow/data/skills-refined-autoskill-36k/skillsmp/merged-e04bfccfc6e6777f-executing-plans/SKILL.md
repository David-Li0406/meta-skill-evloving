---
name: executing-plans
description: Use this skill when a partner provides a complete implementation plan to execute in controlled batches with review checkpoints.
---

# Executing Plans

## Overview

Load a plan, review it critically, execute tasks in batches, and report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan

1. Read the plan file.
2. Review critically - identify any questions or concerns about the plan.
3. If concerns arise, raise them with your human partner before starting.
4. If no concerns, create a TodoWrite and proceed.

### Step 2: Execute Batch

**Default: First 3 tasks**

For each task in the current batch:

1. Mark as in_progress.
2. Follow each step exactly (the plan has bite-sized steps).
3. Run verifications as specified.
4. Mark as completed.

### Step 3: Report

When the batch is complete:

- Show what was implemented.
- Show verification output.
- Say: "Ready for feedback or commit changes?"

### Step 4: Continue

Based on feedback:

- Apply changes if needed.
- Execute the next batch.
- Repeat until complete.

**If user wants to commit changes:**

- Run linting and type checking.
- Commit changes.
- Ask the user if they want to execute the next batch.

### Step 5: Complete Development

After all tasks are complete and verified:

- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- Follow that skill to verify tests, present options, and execute choices.

## When to Stop and Ask for Help

**STOP executing immediately when:**

- You hit a blocker mid-batch (missing dependency, test fails, instruction unclear).
- The plan has critical gaps preventing starting.
- You don't understand an instruction.
- Verification fails repeatedly.

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**

- The partner updates the plan based on your feedback.
- A fundamental approach needs rethinking.

**Don't force through blockers** - stop and ask.

## Remember

- Review the plan critically first.
- Follow plan steps exactly.
- Don't skip verifications.
- Reference skills when the plan says to.
- Between batches: just report and wait.
- Stop when blocked, don't guess.