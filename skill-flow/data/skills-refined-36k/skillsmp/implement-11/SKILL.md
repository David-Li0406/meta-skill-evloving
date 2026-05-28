---
name: implement
description: Execute tasks from a feature spec one at a time, updating living documentation as you go. Use after /interview to implement the planned feature.
---

# Implement - Task Execution

This skill executes tasks from a feature specification, one task at a time, while maintaining living documentation.

## Overview

Use `/implement <feature-name>` after running `/interview` to:
1. Work through tasks one at a time
2. Update progress in tasks.json (set `passes: true`)
3. Update specs if implementation deviates from the plan
4. Keep documentation as the source of truth

**Usage:**
```
/implement my-feature          # Interactive mode
/implement my-feature --all    # Autonomous mode (all tasks)
```

**Modes:**
- Default - Interactive: asks after each task
- `--all` - Autonomous: completes all remaining tasks without stopping
- For fully automated execution without human in the loop, run `ralph -f <feature-name> [-n <iterations>]` instead (default: 30 iterations)

## Instructions

### Step 1: Read the Tasks File

The user provides the feature name as an argument:
```
/implement my-feature
```

The tasks file is always located at `specs/<feature-name>/tasks.json`.

1. Read `specs/<feature-name>/tasks.json`
2. Parse the JSON structure to access the tasks array
3. If you need additional context for a task, look in the same folder for:
   - `specs/<feature-name>/spec.md` - the PRD (what and why)
   - `specs/<feature-name>/plan.md` - the technical implementation (how)
4. Only read spec.md/plan.md when needed - each task's `context` field should contain enough information for most cases

**Important:** All three files (`spec.md`, `plan.md`, `tasks.json`) are **living documents** and the **source of truth**. Update them as you implement to reflect the actual state of the feature.

### Step 2: Identify Next Task

Read `tasks.json` and find the first task with `"passes": false`.

If all tasks have `passes: true`, inform the user and ask if there's anything else to do.

### Step 3: Execute ONE Task

**Important: Only work on ONE task at a time.**

For the current task, use its structured fields:
- `title` - What needs to be done
- `context` - Relevant details from spec/plan
- `files` - Expected files to create or modify
- `success` - Verifiable success criteria
- `steps` - Verification steps to confirm completion

**Execution workflow:**

1. **Read the context** - Use the task's `context` field and review `files` to understand scope
2. **Reference the specs** - Check spec.md and plan.md for additional context if needed
3. **Implement** - Write the code AND write tests for the functionality
4. **Run linting** - Run the lint command from plan.md (e.g., `npm run lint`). Fix any issues.
5. **Verify success criteria** - Execute the `steps` and confirm the `success` criteria. The task is NOT complete until all steps pass.
6. **Update tasks.json** - Only set `passes: true` after linting passes AND verification passes

**Do NOT mark a task complete if:**
- Linting fails
- Tests are failing
- The verification steps show errors
- Success criteria are not met

If verification or linting fails, fix the issue and verify again before marking complete.

### Step 4: Update Documentation

After completing the task:

#### Always do:
- Set `"passes": true` for the completed task in tasks.json

#### Only if you deviated from the original plan:
- Add a note to the task's `learnings` array explaining what you did differently and why
- Update `plan.md` with the actual approach taken
- Update `spec.md` if requirements changed

**Don't add learnings if you followed the plan as written.**

**Example task after completion with deviation:**
```json
{
  "id": 3,
  "title": "Create API endpoint for user data",
  "category": "backend",
  "context": "Use REST per plan.md",
  "files": ["src/api/users.ts"],
  "success": "GET /api/users returns 200 with user list",
  "steps": ["Run npm test -- users.test.ts", "curl localhost:3000/api/users"],
  "passes": true,
  "learnings": [
    "Changed from REST to GraphQL because existing codebase uses GraphQL",
    "Updated plan.md accordingly"
  ]
}
```

### Step 5: Confirm and Continue

After completing a task:

1. Briefly summarize what was done
2. Show the updated task status (e.g., "3/7 tasks complete")
3. Provide a concise "How to test" - tell the user how they can manually verify it works (e.g., "Run `npm start` and visit /login to see the new form" or "Call `curl localhost:3000/api/users` to test the endpoint")

**If interactive mode (default):**
Use `AskUserQuestion` tool with:
- Question: "Continue to the next task?"
- Header: "Next"
- Options:
  - Label: "Yes" / Description: "Continue to the next task"
  - Label: "No" / Description: "Stop here, I'll continue later"

**If autonomous mode (`--all`):**
- Briefly report progress
- Immediately continue to the next task
- Only stop if blocked or all tasks complete

### Living Documentation Rules

**The specs folder is the source of truth.** Only update them when you deviate from the original plan.

1. **tasks.json** - Always set `passes: true` as you complete tasks.
   - Only add to the `learnings` array if you did something differently than planned.
   - Learnings are useful context for subsequent tasks and future reference.
2. **plan.md** - Only update if technical approach changed:
   - User requests a different approach
   - You discover a better solution during implementation
   - Original approach doesn't work as expected
3. **spec.md** - Only update if requirements changed:
   - User changes their mind about a feature
   - Scope changes (features added/removed)

**Key principle:** If you followed the plan, just mark `passes: true`. If you deviated, add learnings and update docs so they reflect reality.

### Task Execution Principles

1. **Self-contained** - Each task should be completable independently
2. **Non-colliding** - Tasks shouldn't conflict with each other
3. **Testable in isolation** - Each task can be verified without completing other tasks
4. **Verify before checking** - Run the verification command and confirm success criteria pass before marking complete
5. **Atomic commits** - Consider committing after each task (if appropriate)

### Handling Issues

**If a task is blocked:**
- Don't set `passes: true`
- Add a note to `learnings` explaining the blocker
- Ask user how to proceed

**If a task needs to change:**
- Discuss with user
- Update the task fields in tasks.json (title, context, files, success, steps)
- Update related specs if needed

**If you discover new tasks:**
- Add them to the `tasks` array in tasks.json with `passes: false`
- Assign the next available `id`
- Place them in logical order
- Add a note in `learnings` of the current task explaining why new tasks were added

### Example Session

```
User: /implement user-auth

Agent: [Reads specs/user-auth/tasks.json]
Agent: "Found 5 tasks. Starting with Task 1: Set up auth middleware."
Agent: [Implements the task + writes tests]
Agent: [Runs npm run lint - passes]
Agent: [Runs verification steps from task - passes]
Agent: "Linting and tests pass. Marking Task 1 complete."
Agent: [Updates tasks.json - sets passes: true for Task 1]
Agent: "Completed Task 1. (1/5)
        How to test: Run `npm start`, then `curl -H 'Authorization: Bearer <token>' localhost:3000/api/protected` - should return 200."
Agent: [Uses AskUserQuestion: "Continue to the next task?" Yes/No]

User: [Selects "Yes"]

Agent: [Implements Task 2]
Agent: [Needs more context, reads plan.md from same folder]
Agent: [Runs verification - tests fail]
Agent: "Tests failing. Fixing issue..."
Agent: [Fixes the issue]
Agent: [Runs verification again - tests pass]
Agent: "Note: Changed JWT library from plan due to security advisory."
Agent: [Updates tasks.json - sets passes: true and adds learning, updates plan.md]
Agent: "Completed Task 2. (2/5)"
Agent: [Uses AskUserQuestion: "Continue to the next task?" Yes/No]

... continues until all tasks done ...

Agent: "All tasks complete! Feature implementation finished."
```

## Command Variations

- `/implement <feature-name>` - Interactive mode (asks after each task)
- `/implement <feature-name> --all` - Autonomous mode (completes all tasks)
- `ralph -f <feature-name> [-n <iterations>]` - Fully automated (no human in the loop, default: 30 iterations)

Examples:
```
/implement user-auth
/implement shopping-cart --all
ralph -f shopping-cart
ralph -f user-auth -n 15
```

### Interactive Mode (default)
After each task, use `AskUserQuestion` tool:
- Question: "Continue to the next task?"
- Options: "Yes" or "No"

### Autonomous Mode (`--all`)
- Continue through all tasks without asking
- Still update documentation after each task
- Still report progress (briefly) after each task
- Stop if a task fails or is blocked
- At the end, summarize all completed tasks

## Important Notes

- ONE task at a time - no skipping ahead
- Always update tasks.json as you go (set `passes: true`, add `learnings` if needed)
- Specs are living documents - keep them accurate
- If unsure about something, ask the user
- Commit after tasks when appropriate (respect user's git preferences)

## tasks.json Structure Reference

```json
{
  "featureName": "<feature-name>",
  "description": "Living document. Update passes/learnings as tasks complete.",
  "tasks": [
    {
      "id": 1,
      "title": "<clear action>",
      "category": "<backend|frontend|database|config|test|docs>",
      "context": "<relevant details from spec/plan>",
      "files": ["<file1>", "<file2>"],
      "success": "<verifiable criteria>",
      "steps": ["<verification step 1>", "<verification step 2>"],
      "passes": false,
      "learnings": []
    }
  ]
}
```

**Fields:**
- `id` - Task identifier (1, 2, 3...)
- `title` - Clear, actionable task name
- `category` - Type of work (backend, frontend, database, config, test, docs)
- `context` - Relevant details needed to complete the task
- `files` - Expected files to create or modify
- `success` - Verifiable success criteria
- `steps` - Ordered verification steps
- `passes` - `false` when pending, `true` when completed
- `learnings` - Notes about decisions, deviations, or useful context (added after completion)
