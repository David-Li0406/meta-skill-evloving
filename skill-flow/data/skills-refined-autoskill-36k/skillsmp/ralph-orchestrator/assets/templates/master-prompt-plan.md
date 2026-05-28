# Master Prompt Template: Plan Mode

<!--
PURPOSE: This template generates the master prompt for Plan-based Ralph loops.
USED BY: ralph-orchestrator skill when plan.json exists (created via /ralph-freeform)
VARIABLES: Replace {{placeholders}} with actual values from plan.json

KEY DIFFERENCES FROM PRD MODE:
- Phases instead of stories (larger chunks of work)
- Simpler structure (2-5 phases vs 5+ user stories)
- Goal-focused with phases to achieve it
- Completion promise: ALL PHASES COMPLETE

TASK TYPE HANDLING:
- Check plan.json task_type field
- "implementation" (default): Use TDD workflow (Section 4a)
- "documentation": Use Research/Writing workflow (Section 4b)
- "investigation": Use Investigation workflow (Section 4c)
-->

---

# Ralph Loop Task: {{task-name}}

## Your Mission

{{goal}}

## Completion Criteria

When ALL of the following are true, output exactly: `<promise>ALL PHASES COMPLETE</promise>`

{{#each success_criteria}}
- [ ] {{this}}
{{/each}}

**CRITICAL**: Do NOT output the completion promise unless ALL criteria are actually met. The loop will continue until you output this exact text or max iterations is reached.

---

## CRITICAL INSTRUCTIONS

You are in a Ralph loop. Each iteration, you receive this same prompt. Your memory persists ONLY through files on disk. Follow these instructions exactly.

### 1. Read State First (EVERY ITERATION)

Before doing ANY work, read these files to understand current state:

- `.claude/ralph/{{task-name}}/progress.md` - What you've learned, where you are, what iteration you're on
- `.claude/ralph/{{task-name}}/AGENTS.md` - Persistent patterns and architectural decisions
- `.claude/ralph/{{task-name}}/plan.json` - Current phase status (which phases are complete)

**DO NOT** start working until you've read these files. They contain your memory from previous iterations.

### 1b. Available Integrations

{{#if integrations}}
You have access to these integrations for this task:

{{#each integrations}}
- **{{name}}** ({{type}}): {{usage}}
  - Tools: {{tools}}
{{/each}}

Use these integrations when relevant to the current phase.
{{else}}
No additional integrations configured for this task.
{{/if}}

{{#if input_sources}}
### 1c. Input Sources

Read and analyze these materials:
{{#each input_sources}}
- {{this}}
{{/each}}

Reference these throughout your analysis phases.
{{/if}}

### 2. Progress Tracking (MANDATORY)

After EACH meaningful action, update `.claude/ralph/{{task-name}}/progress.md`:

**Learnings section** (append-only):
```
[Iteration N] <what you learned>
```

**Current State section**:
- Update "Working on" with current focus
- Update "Current Phase" with active phase ID
- Update "Last verification" with most recent check result
- Increment "Attempts on current issue" if retrying same problem

**Phase Status section**:
- Check off phases as they complete: `- [x] P1: Phase name`

**Iteration History section**:
- Add brief entry for this iteration

### 3. Context Health

{{#if task_type_implementation}}
**Commit frequently**:
- After each passing test
- After each working feature
- Use descriptive commit messages
- This creates recovery points
{{/if}}

{{#if task_type_documentation}}
**Save drafts**:
- Write intermediate outputs to working directory
- Document analysis findings as you go
{{/if}}

{{#if task_type_investigation}}
**Save artifacts**:
- Logs, screenshots, traces to working directory
- Document each hypothesis test result
{{/if}}

**Summarize on milestones**:
- When completing a phase, add insights to AGENTS.md
- Document patterns discovered, architectural decisions
- Keep AGENTS.md as distilled knowledge

**Archive if progress.md grows large**:
- If > 300 lines, move old iterations to progress_archive.md
- Keep active iteration history manageable

### 4. Workflow

{{#if task_type_implementation}}
<!-- Section 4a: TDD Workflow (for implementation tasks) -->

For each phase:

1. **Write test FIRST**
   - Define what success looks like in code
   - Test should be specific and focused

2. **Run test - confirm it FAILS**
   - This proves the test is valid
   - If it passes, test may be wrong

3. **Implement minimal code**
   - Just enough to make test pass
   - Don't over-engineer

4. **Run test - confirm it PASSES**
   - If fails, debug and fix
   - Update progress.md with learnings

5. **Refactor if needed**
   - Clean up while tests still pass
   - Run tests after refactoring

6. **Commit and document**
   - Commit working code
   - Update progress.md
   - Update AGENTS.md if pattern discovered
{{/if}}

{{#if task_type_documentation}}
<!-- Section 4b: Research/Writing Workflow (for documentation tasks) -->

For each phase:

1. **Gather information first**
   - Read all relevant input sources
   - Take notes on key findings
   - Identify gaps or questions

2. **Analyze before writing**
   - Synthesize information across sources
   - Form conclusions or recommendations
   - Note assumptions being made

3. **Draft incrementally**
   - Write section by section
   - Reference source material
   - Keep deliverable focused on audience needs

4. **Review against criteria**
   - Check all required sections present
   - Verify claims are supported
   - Ensure clarity and completeness
{{/if}}

{{#if task_type_investigation}}
<!-- Section 4c: Investigation Workflow (for debugging/analysis tasks) -->

For each phase:

1. **Observe first**
   - Reproduce the issue if possible
   - Gather logs, traces, evidence
   - Document exact symptoms

2. **Form hypotheses**
   - List possible causes
   - Rank by likelihood
   - Identify how to test each

3. **Test hypotheses systematically**
   - One hypothesis at a time
   - Document results of each test
   - Update likelihood based on evidence

4. **Confirm root cause**
   - Gather definitive evidence
   - Document the failure mode
   - Identify when/why it started

5. **Document findings**
   - Write investigation report
   - Include evidence and reasoning
   - Recommend fix if in scope
{{/if}}

### 5. Verification Steps

{{verification_description}}

Run verification after completing each phase:
- **Method**: {{verification_method}}
{{#if verification_command}}- **Command**: `{{verification_command}}`{{/if}}
- **If verification fails**: Note in progress.md, attempt fix, re-verify

### 6. Escape Hatches

**If stuck after 3 attempts on the same issue**:

1. **Document the issue** in progress.md:
   ```
   ### Blocked: <issue description>
   - Attempted: <what you tried>
   - Error: <exact error message>
   - Hypothesis: <why it might be failing>
   ```

2. **Try ONE alternative approach**:
   - Different method or strategy
   - Simplified implementation
   - Ask if requirement can be relaxed

3. **If still stuck after alternative**:
   - Add to "Blocked Phases" section in progress.md
   - Move to NEXT phase (don't spin forever)

4. **If ALL phases are blocked**:
   - Create comprehensive summary in progress.md
   - List all blockers and what was attempted
   - Do NOT output false completion promise
   - The loop will continue until max iterations

**Never output the completion promise to escape a difficult situation. That defeats the purpose of the loop.**

### 7. Project CLAUDE.md Updates

After completing a phase, check if any learnings should be promoted to the project-level CLAUDE.md:

**Promote to CLAUDE.md when:**
- Discovered a project-wide convention (naming, structure, patterns)
- Found a command or workflow that applies beyond this task
- Identified a gotcha that future tasks should know about
- Established an architectural decision affecting the whole project

**Do NOT promote:**
- Task-specific implementation details
- Temporary workarounds
- Learnings only relevant to this task

### 8. Completion Summary

When ALL phases are complete and you're about to output the completion promise, **first output a human-friendly summary** of the loop execution:

```
───────────────────────────────────────
✓ Ralph loop complete!

Total iterations: <N>
  • P1 (<phase name>): <X> iterations
  • P2 (<phase name>): <Y> iterations
  • ...

All phases complete.
───────────────────────────────────────
```

**How to calculate iterations per phase:**
- Read the Iteration History section in progress.md
- Count how many iterations focused on each phase
- Sum to get total iterations

**IMPORTANT:**
- Output this summary ONLY on successful completion
- Do NOT output if using escape hatches or if phases are blocked
- Output the summary BEFORE the `<promise>` tag

---

## Phases

{{#each phases}}
### {{id}}: {{name}}
{{#if complete}}✅ COMPLETE{{/if}}

**Steps**:
{{#each steps}}
- [ ] {{this}}
{{/each}}

**Verify**: {{verification}}

{{#if notes}}**Notes**: {{notes}}{{/if}}

---
{{/each}}

## Current Focus: {{current_phase_id}}

Work on the first non-complete phase listed above.

---

## What To Do Now

{{#if task_type_implementation}}
1. **Read state files** - progress.md, AGENTS.md, plan.json, and ./CLAUDE.md
2. **Identify current iteration** from progress.md
3. **Determine current phase** - first non-complete phase
4. **Check attempt count** - if 3+ attempts on same issue, use escape hatch
5. **Work through current phase steps** using TDD workflow
6. **Update progress.md** after each action
7. **Run verification** when phase seems complete
8. **Update plan.json** when phase passes: `"complete": true`
9. **Update AGENTS.md** with task-specific patterns discovered
10. **Promote to CLAUDE.md** any project-wide conventions discovered
11. **Commit working code** with descriptive message
12. **Move to next phase** until all complete
13. **When ALL phases complete**, output completion summary (see Section 8), then: `<promise>ALL PHASES COMPLETE</promise>`
{{/if}}

{{#if task_type_documentation}}
1. **Read state files** - progress.md, AGENTS.md, plan.json
2. **Identify current iteration** from progress.md
3. **Determine current phase** - first non-complete phase
4. **If analysis phase**: Read input sources, take notes, form findings
5. **If drafting phase**: Write sections of deliverable
6. **Update progress.md** after each meaningful action
7. **Save work** - write drafts to .claude/ralph/{{task-name}}/ directory
8. **Run verification** when phase seems complete (check against criteria)
9. **Update plan.json** when phase passes: `"complete": true`
10. **Move to next phase** until all complete
11. **When ALL phases complete**, output completion summary (see Section 8), then: `<promise>ALL PHASES COMPLETE</promise>`
{{/if}}

{{#if task_type_investigation}}
1. **Read state files** - progress.md, AGENTS.md, plan.json
2. **Identify current iteration** from progress.md
3. **Determine current phase** - first non-complete phase
4. **If reproduce phase**: Attempt to trigger the issue, capture evidence
5. **If hypothesis phase**: Test one hypothesis, document results
6. **If root cause phase**: Confirm with evidence, document findings
7. **Update progress.md** after each test or finding
8. **Save artifacts** - logs, screenshots, traces to working directory
9. **Update plan.json** when phase passes: `"complete": true`
10. **Move to next phase** until all complete
11. **When ALL phases complete**, output completion summary (see Section 8), then: `<promise>ALL PHASES COMPLETE</promise>`
{{/if}}

---

## Remember

- You are in a LOOP - your work from previous iterations is in the files
- READ STATE FIRST every iteration (progress.md, AGENTS.md, plan.json, CLAUDE.md)
- NEVER output the completion promise unless it's TRUE
- Document progress always
- If stuck 3 times, use escape hatch - don't spin forever
- Progress through phases methodically
- Your learnings in progress.md help future iterations avoid mistakes
- Promote project-wide patterns to CLAUDE.md, keep task-specific in AGENTS.md
