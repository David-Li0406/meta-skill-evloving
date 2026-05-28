---
name: ralph-loop
description: Start Ralph Loop in current session
detection_patterns:
  - "start ralph loop"
  - "ralph loop"
  - "execute plan at"
  - "work through the plan"
  - "implement the plan"
  - "run the plan"
  - "iterate on"
  - "keep working until"
auto_invoke: false
---

# Ralph Loop Skill

Start an iterative development loop that prevents the session from ending until the task is complete.

## Detection Patterns

This skill activates when the user says things like:
- "start ralph loop for building the API"
- "execute plan at plans/active/my-feature/"
- "work through the plan"
- "implement the plan tasks"
- "keep working until the tests pass"

## Behavior

When activated:

1. **Parse the request** to determine:
   - Is this plan mode (references a plan path)?
   - Is this simple mode (just a task description)?

2. **Initialize the loop**:
   ```bash
   # For plan mode
   .claude/scripts/setup-ralph-loop.sh --plan <path> --max-iterations 50

   # For simple mode
   .claude/scripts/setup-ralph-loop.sh "<task>" --max-iterations 20
   ```

3. **Start working**:
   - In plan mode: Read plan files, start on first incomplete task
   - In simple mode: Start working on the described task

4. **Continue iterating**:
   - The stop hook will prevent exit until completion
   - In simple mode: Output `<promise>DONE</promise>` when complete
   - In plan mode: Acceptance criteria checked automatically

## Example Invocations

**Plan mode**:
```
User: "execute plan at plans/active/add-authentication/"
Claude: [Initializes Ralph Loop in plan mode, reads plan, starts working]
```

**Simple mode**:
```
User: "start ralph loop for refactoring the database layer"
Claude: [Initializes Ralph Loop in simple mode, starts refactoring]
```

## Notes

- Use `/cancel-ralph` to stop early
- State stored in `.claude/ralph-loop.local.md`
- Stop hook: `.claude/hooks/stop.sh`
