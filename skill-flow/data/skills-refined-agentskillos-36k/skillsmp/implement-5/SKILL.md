---
name: implement
description: Execute all tasks from task breakdown to build feature according to plan
---

# Implement - Execute Implementation

## Overview

Execute all tasks from the task breakdown to build the feature according to the implementation plan.

**Announce at start:** "I'm using the implement skill to execute the implementation plan."

## When to Use

- After creating task breakdown (`SpecKit/tasks`)
- When ready to start implementation
- When all prerequisites are in place

## Prerequisites

- ✅ Project constitution (`SpecKit/constitution`)
- ✅ Functional specification (`SpecKit/specify`)
- ✅ Technical plan (`SpecKit/plan`)
- ✅ Task breakdown (`SpecKit/tasks`)

## The Process

### Step 1: Validate Prerequisites

1. Check that all required files exist:
   - `.specify/memory/constitution.md`
   - `specs/<feature-id>/spec.md`
   - `specs/<feature-id>/plan.md`
   - `specs/<feature-id>/tasks.md`

2. Verify required tools are installed:
   - Swift (for Swift StateTree project)
   - Testing frameworks
   - Build tools

### Step 2: Parse Task Breakdown

1. Read `specs/<feature-id>/tasks.md`
2. Parse tasks in order
3. Identify dependencies
4. Identify parallelizable tasks

### Step 3: Execute Tasks

For each task:

1. **Check Dependencies**
   - Ensure all dependency tasks are complete
   - Wait if dependencies not ready

2. **Execute Task Steps**
   - Follow steps exactly as specified
   - Create/modify files as indicated
   - Run tests as specified

3. **Verify Completion**
   - Run verification commands
   - Check test results
   - Validate checkpoint criteria

4. **Handle Errors**
   - If error occurs, stop and report
   - Don't proceed until error resolved
   - Ask for help if blocked

### Step 4: Parallel Execution

For tasks marked `[P]`:
- Can execute in parallel if dependencies met
- Still verify each task independently
- Report completion of parallel batch

### Step 5: Checkpoints

After each user story phase:
- Run checkpoint validation
- Report progress
- Wait for feedback if needed

### Step 6: Complete Implementation

After all tasks complete:
- Run full test suite
- Verify all checkpoints passed
- Report completion
- Use `Superpowers/finishing-a-development-branch` for final steps

## Example Usage

```
/speckit.implement
```

The skill will:
1. Validate prerequisites
2. Parse task breakdown
3. Execute tasks in order
4. Handle dependencies
5. Run parallel tasks when possible
6. Verify checkpoints
7. Report progress

## Key Principles

- **Follow plan exactly**: Don't deviate from task breakdown
- **Respect dependencies**: Don't skip dependency checks
- **Verify each step**: Run tests and validations
- **Stop on errors**: Don't proceed with errors
- **Report progress**: Keep user informed

## Error Handling

**When to Stop:**
- Missing dependencies
- Test failures
- Build errors
- Unclear instructions
- Blocked by external factors

**What to Do:**
- Stop immediately
- Report error clearly
- Ask for clarification
- Don't guess or work around

## Integration with Other Skills

- **Before**: Use `SpecKit/tasks` to create task breakdown
- **During**: Use `Superpowers/test-driven-development` for TDD
- **After**: Use `Superpowers/finishing-a-development-branch` for completion
- **Alternative**: Use `Superpowers/executing-plans` for batch execution with checkpoints

## Difference from Superpowers/executing-plans

- **SpecKit/implement**: Execute all tasks automatically
- **Superpowers/executing-plans**: Batch execution with checkpoints and review

Choose based on:
- **SpecKit/implement**: When tasks are well-defined and can run automatically
- **Superpowers/executing-plans**: When you want batch review and feedback

## Project-Specific Notes

For Swift StateTree project:
- Use Swift Testing framework (not XCTest)
- Run `swift test` to verify tests
- Use `swift build` to verify compilation
- Follow project guidelines from `AGENTS.md`
- Code comments must be in English
