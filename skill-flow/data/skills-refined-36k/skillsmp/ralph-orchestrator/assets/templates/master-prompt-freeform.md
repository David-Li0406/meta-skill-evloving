# Master Prompt Template: Raw Freeform Mode

<!--
PURPOSE: This template generates the master prompt for raw freeform Ralph loops.
USED BY: ralph-orchestrator skill when neither prd.json nor plan.json exists
VARIABLES: Replace {{placeholders}} with values inferred from the raw prompt

KEY CHARACTERISTICS:
- Single implicit phase (the entire task)
- Inferred success criteria from description
- Minimal tracking (progress.md but no JSON status file)
- Completion promise: TASK COMPLETE
-->

---

# Ralph Loop Task: {{task-name}}

## Your Mission

{{task_description}}

## Completion Criteria

When ALL of the following are true, output exactly: `<promise>TASK COMPLETE</promise>`

{{#each inferred_criteria}}
- [ ] {{this}}
{{/each}}

**CRITICAL**: Do NOT output the completion promise unless ALL criteria are actually met.

---

## CRITICAL INSTRUCTIONS

You are in a Ralph loop. Each iteration, you receive this same prompt. Your memory persists ONLY through files on disk.

### 1. Read State First (EVERY ITERATION)

Before doing ANY work, read:
- `.claude/ralph/{{task-name}}/progress.md` - What you've learned and where you are

### 2. Progress Tracking

After EACH meaningful action, update progress.md:

**Learnings section** (append-only):
```
[Iteration N] <what you learned>
```

**Current State section**:
- Update "Working on" with current focus
- Update "Last verification" with most recent check result

### 3. Work Incrementally

- Break the task into small steps
- Complete one step at a time
- Commit working code frequently
- Document insights in progress.md

### 4. Escape Hatch

**If stuck after 3 attempts**:
1. Document the issue in progress.md
2. Try an alternative approach
3. If still stuck, note the blocker clearly

**Never output the completion promise to escape. That defeats the purpose.**

### 5. Completion Summary

When the task is complete and you're about to output the completion promise, **first output a human-friendly summary**:

```
───────────────────────────────────────
✓ Ralph loop complete!

Total iterations: <N>
───────────────────────────────────────
```

**IMPORTANT:**
- Output this summary ONLY on successful completion
- Do NOT output if stuck or blocked
- Output the summary BEFORE the `<promise>` tag

---

## What To Do Now

1. **Read progress.md** to understand current state
2. **Identify next step** toward completion
3. **Do the work** incrementally
4. **Update progress.md** after each action
5. **Verify** when task seems complete
6. **When ALL criteria met**, output completion summary (see Section 5), then: `<promise>TASK COMPLETE</promise>`

---

## Remember

- READ STATE FIRST every iteration
- NEVER output the completion promise unless it's TRUE
- Work incrementally, commit often
- Your learnings in progress.md help future iterations
