# Master Prompt Template: PRD Mode

<!--
PURPOSE: This template generates the master prompt for PRD-based Ralph loops.
USED BY: ralph-orchestrator skill when prd.json exists
VARIABLES: Replace {{placeholders}} with actual values from prd.json

The master prompt is fed to Claude each iteration of the Ralph loop.
Claude's memory persists through files on disk, not the prompt itself.
-->

---

# Ralph Loop Task: {{task-name}}

## Your Mission

{{problem_statement}}

## Completion Criteria

When ALL of the following are true, output exactly: `<promise>ALL STORIES PASS</promise>`

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
- `.claude/ralph/{{task-name}}/prd.json` - Current story status (which stories pass)

**DO NOT** start working until you've read these files. They contain your memory from previous iterations.

### 1b. Available Integrations

{{#if integrations}}
You have access to these integrations for this task:

{{#each integrations}}
- **{{name}}** ({{type}}): {{usage}}
  - Tools: {{tools}}
{{/each}}

Use these integrations when relevant to the current story.
{{else}}
No additional integrations configured for this task.
{{/if}}

### 2. Progress Tracking (MANDATORY)

After EACH meaningful action, update `.claude/ralph/{{task-name}}/progress.md`:

**Learnings section** (append-only):
```
[Iteration N] <what you learned>
```
Example:
```
[Iteration 3] Database requires await on pool.connect() before queries
[Iteration 4] Test file must be named *.test.ts to be discovered
```

**Current State section**:
- Update "Working on" with current focus
- Update "Current Story" with active story ID
- Update "Last verification" with most recent test/check result
- Increment "Attempts on current issue" if retrying same problem

**Story Status section**:
- Check off stories as they pass: `- [x] US-001: Create endpoint`

**Iteration History section**:
- Add brief entry for this iteration

### 3. Context Health

**Commit frequently**:
- After each passing test
- After each working feature
- Use descriptive commit messages
- This creates recovery points

**Summarize on milestones**:
- When completing a story, add insights to AGENTS.md
- Document patterns discovered, architectural decisions
- Keep AGENTS.md as distilled knowledge

**Archive if progress.md grows large**:
- If > 300 lines, move old iterations to progress_archive.md
- Keep active iteration history manageable

### 4. TDD Workflow

For each story or feature:

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

### 5. Verification Steps

{{verification_description}}

Run verification after implementing each story:
- **Command**: `{{verification_command}}`
- **Expected result**: All tests pass / type check succeeds
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
   - Different library or method
   - Simplified implementation
   - Ask if requirement can be relaxed

3. **If still stuck after alternative**:
   - Mark story as BLOCKED in prd.json: `"blocked": true, "blocked_reason": "..."`
   - Add to "Blocked Stories" section in progress.md
   - Move to NEXT story (don't spin forever)

4. **If ALL stories are blocked**:
   - Create comprehensive summary in progress.md
   - List all blockers and what was attempted
   - Do NOT output false completion promise
   - The loop will continue until max iterations

**Never output the completion promise to escape a difficult situation. That defeats the purpose of the loop.**

### 7. Project CLAUDE.md Updates

After completing a story, check if any learnings should be promoted to the project-level CLAUDE.md:

**Promote to CLAUDE.md when:**
- Discovered a project-wide convention (naming, structure, patterns)
- Found a command or workflow that applies beyond this task
- Identified a gotcha that future tasks should know about
- Established an architectural decision affecting the whole project

**Do NOT promote:**
- Task-specific implementation details
- Temporary workarounds
- Learnings only relevant to this feature

**Update format:**
Append to CLAUDE.md under a "## Discovered Patterns" or relevant existing section:
```
## Discovered Patterns

### <Category>
- <pattern description> (discovered during {{task-name}})
```

**Location:**
- Read: `./CLAUDE.md` (project root)
- Write: Append new patterns, never remove existing content

**Relationship to AGENTS.md:**
- AGENTS.md = Task-specific patterns (stays in `.claude/ralph/{{task-name}}/`)
- CLAUDE.md = Project-wide conventions (promoted from AGENTS.md)

### 8. Completion Summary

When ALL stories pass and you're about to output the completion promise, **first output a human-friendly summary** of the loop execution:

```
───────────────────────────────────────
✓ Ralph loop complete!

Total iterations: <N>
  • US-001 (<story title>): <X> iterations
  • US-002 (<story title>): <Y> iterations
  • ...

All stories pass.
───────────────────────────────────────
```

**How to calculate iterations per story:**
- Read the Iteration History section in progress.md
- Count how many iterations focused on each story
- Sum to get total iterations

**IMPORTANT:**
- Output this summary ONLY on successful completion
- Do NOT output if using escape hatches or if stories are blocked
- Output the summary BEFORE the `<promise>` tag

---

## User Stories

{{#each stories}}
### {{id}}: {{title}}
{{#if passes}}✅ PASSING{{/if}}
{{#if blocked}}🚫 BLOCKED: {{blocked_reason}}{{/if}}

**Description**: {{description}}

**Acceptance Criteria**:
{{#each acceptance_criteria}}
- [ ] {{this}}
{{/each}}

**Verification**: {{verification}}

---
{{/each}}

## Current Focus: {{current_story_id}}

Work on the first non-passing, non-blocked story listed above.

---

## What To Do Now

1. **Read state files** - progress.md, AGENTS.md, prd.json, and ./CLAUDE.md
2. **Identify current iteration** from progress.md
3. **Determine current story** - first non-passing, non-blocked story
4. **Check attempt count** - if 3+ attempts on same issue, use escape hatch
5. **Follow TDD workflow** for current story
6. **Update progress.md** after each action
7. **Run verification** when story seems complete
8. **Update prd.json** when story passes: `"passes": true`
9. **Update AGENTS.md** with task-specific patterns discovered
10. **Promote to CLAUDE.md** any project-wide conventions discovered
11. **Commit working code** with descriptive message
12. **Move to next story** until all pass
13. **When ALL criteria met**, output completion summary (see Section 8), then: `<promise>ALL STORIES PASS</promise>`

---

## Remember

- You are in a LOOP - your work from previous iterations is in the files
- READ STATE FIRST every iteration (progress.md, AGENTS.md, prd.json, CLAUDE.md)
- NEVER output the completion promise unless it's TRUE
- Commit often, document always
- If stuck 3 times, use escape hatch - don't spin forever
- Progress through stories methodically
- Your learnings in progress.md help future iterations avoid mistakes
- Promote project-wide patterns to CLAUDE.md, keep task-specific in AGENTS.md
