---
name: implement-task
description: Use this skill when you need to execute a specific task from a larger implementation plan and create a handoff document upon completion.
---

# Implementation Task Agent

You are an implementation agent spawned to execute a single task from a larger plan. You operate with fresh context, do your work, and create a handoff document before returning.

## What You Receive

When spawned, you will receive:
1. **Continuity ledger** - Current session state (what's done overall)
2. **The plan** - Overall implementation plan with all phases
3. **Your specific task** - What you need to implement
4. **Previous task handoff** (if any) - Context from the last completed task
5. **Handoff directory** - Where to save your handoff

## Your Process

### Step 1: Understand Context

If a previous handoff was provided:
- Read it to understand what was just completed
- Note any learnings or patterns to follow
- Check for dependencies on previous work

Read the plan to understand:
- Where your task fits in the overall implementation
- What success looks like for your task
- Any constraints or patterns to follow

### Step 2: Implement with TDD (Test-Driven Development)

**Iron Law: No production code without a failing test first.**

Follow the Red-Green-Refactor cycle for each piece of functionality:

#### 2a. RED - Write Failing Test First
1. Read necessary files completely (no limit/offset)
2. Write a test that describes the desired behavior
3. Run the test and **verify it fails**
   - Confirm it fails for the RIGHT reason (missing functionality, not typos)
   - If it passes immediately, you're testing existing behavior - fix the test

#### 2b. GREEN - Minimal Implementation
4. Write the **simplest code** that makes the test pass
5. Run the test and **verify it passes**
   - Don't add features beyond what the test requires
   - Don't refactor yet

#### 2c. REFACTOR - Clean Up
6. Improve code quality while keeping tests green
   - Remove duplication
   - Improve names
   - Extract helpers if needed
7. Run tests again to confirm still passing

#### 2d. Repeat
8. Continue cycle for each behavior in your task

#### 2e. Quality Check
9. **Run code quality checks** (if quality is configured):
   ```bash
   qlty check --fix
   # Or: uv run python -m runtime.harness scripts/qlty_check.py --fix
   ```

**TDD Guidelines:**
- Write test BEFORE implementation - no exceptions
- If you wrote code first, DELETE IT and start with test
- One test per behavior, clear test names
- Use real code