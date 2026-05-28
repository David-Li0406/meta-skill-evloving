---
name: ralph-orchestrator
description: Build structured prompts for Ralph loops with TDD guidance, progress tracking, verification steps, and escape hatches. Invoke when starting a Ralph-based development task, creating orchestrated iteration loops, or converting PRDs to executable Ralph prompts. Wraps the official ralph-loop plugin to maximize loop success rates through careful prompt engineering and persistent state management.
---

# Ralph Orchestrator

Build structured, scaffolded prompts for Ralph loops that maximize success rates through:
- **Progress tracking**: Persistent learnings that survive iterations
- **Context health**: When to commit, summarize, or archive
- **TDD workflow**: Test-first development patterns
- **Escape hatches**: Recovery when stuck
- **Verification**: Automatic and manual verification steps

## Core Concept

Ralph loops succeed when Claude has:
1. **Clear completion criteria** - Unambiguous signal for when to output the completion promise
2. **Progress visibility** - Ability to see what worked/failed in previous iterations
3. **Incremental goals** - Small, achievable steps that build momentum
4. **Recovery paths** - What to do when stuck

This skill builds prompts that embed all these elements.

## How Ralph Works

The official `ralph-loop` plugin creates a self-referential feedback loop:
1. Your prompt is fed to Claude
2. Claude works on the task
3. Claude tries to exit
4. Stop hook intercepts exit and re-feeds the SAME prompt
5. Repeat until completion promise is detected or max iterations reached

**Key insight**: The prompt never changes between iterations. Claude's "memory" comes from:
- Files on disk (progress.md, AGENTS.md, prd.json, your code)
- Git history
- Test results

This skill builds prompts that leverage these persistence mechanisms.

---

## Workflow

### Phase 1: Understand the Input

Determine input mode from the invocation context:

**PRD Mode** (if `.claude/ralph/<task-name>/prd.json` exists):
- Read the prd.json file
- Extract stories, success criteria, verification method
- Extract integrations array (if present) for available tools
- Identify which stories are already passing (`"passes": true`)
- Determine next story to work on
- Completion promise: `<promise>ALL STORIES PASS</promise>`

**Plan Mode** (if `.claude/ralph/<task-name>/plan.json` exists):
- Read the plan.json file
- Extract phases, goal, success criteria, verification method
- Extract integrations array (if present) for available tools
- Identify which phases are already complete (`"complete": true`)
- Determine next phase to work on
- Completion promise: `<promise>ALL PHASES COMPLETE</promise>`

**Raw Freeform Mode** (if neither PRD nor plan exists):
- Parse the provided prompt text
- Infer success criteria from the description
- Create implicit single-phase structure
- Completion promise: `<promise>TASK COMPLETE</promise>`

### Phase 2: Initialize Working Files

Ensure working files exist in `.claude/ralph/<task-name>/`:

**progress.md** - Create from template if not exists:
- Read `assets/templates/progress_template.md`
- Fill in task name, timestamp, mode, first story ID
- Write to `.claude/ralph/<task-name>/progress.md`

**AGENTS.md** - Create from template if not exists:
- Read `assets/templates/agents_template.md`
- Fill in task name, timestamp, problem statement
- Write to `.claude/ralph/<task-name>/AGENTS.md`

### Phase 3: Build the Master Prompt

The master prompt is fed to Claude each iteration. It must be:
- **Self-contained**: All necessary context included
- **State-aware**: References progress files Claude should read
- **Action-oriented**: Clear next steps
- **Bounded**: Knows when to stop

**Load and populate the appropriate template based on mode:**

| Mode | Template | Completion Promise |
|------|----------|-------------------|
| PRD | `assets/templates/master-prompt-prd.md` | `ALL STORIES PASS` |
| Plan | `assets/templates/master-prompt-plan.md` | `ALL PHASES COMPLETE` |
| Freeform | `assets/templates/master-prompt-freeform.md` | `TASK COMPLETE` |

**For Plan Mode**, also check `task_type` in plan.json:
- `"implementation"` (default): Use TDD workflow sections
- `"documentation"`: Use Research/Writing workflow sections
- `"investigation"`: Use Investigation workflow sections

The templates use Handlebars-style placeholders (`{{variable}}`, `{{#each}}`, `{{#if}}`) that should be replaced with actual values from the JSON files.

### Phase 4: Return the Built Prompt

Output the complete master prompt ready for the /ralph command:

```
Master prompt built for Ralph loop.

**Summary**:
- Task: <task-name>
- Mode: <prd|plan|freeform>
- Stories/Phases: <count> (<passing/complete> done, <blocked> blocked)
- Current focus: <first incomplete item>
- Completion promise: "<promise>"

**Working files**:
- .claude/ralph/<task-name>/progress.md
- .claude/ralph/<task-name>/AGENTS.md
- .claude/ralph/<task-name>/prd.json or plan.json
- ./CLAUDE.md (project root - for project-wide patterns)

Ready to invoke ralph-loop with this prompt.
```

---

## Key Principles

### 1. The Prompt is the Contract

Everything Claude needs to succeed must be in the prompt. The prompt is fed fresh each iteration - Claude doesn't remember previous iterations except through:
- Files on disk (progress.md, AGENTS.md, prd.json, code files)
- Git history
- Test results

### 2. Progress Files are Memory

Since Ralph loops re-feed the same prompt, persistent files are how Claude "remembers":
- **progress.md**: Append-only learnings, current state, iteration history
- **AGENTS.md**: Task-specific patterns and architectural decisions
- **CLAUDE.md**: Project-wide conventions (promoted from AGENTS.md)
- **prd.json/plan.json**: Story/phase completion status

### 3. Small Stories Beat Big Stories

Stories should be completable in 1-3 iterations. If a story takes more than 5 iterations:
- It's too big - should have been broken down
- There's a blocker - use escape hatch

### 4. Verification is Essential

Every story must have a verification method. Without it, Claude can't objectively know when it's done. Prefer automated verification (tests, type checks) over manual.

### 5. Escape Hatches Prevent Infinite Loops

When stuck, Claude should:
1. Document the issue thoroughly
2. Try an alternative approach
3. Mark as blocked and move on
4. NEVER lie about completion

---

## References

Load these for detailed guidance:

- **references/prompt-patterns.md** - Best practices for prompt writing
- **references/story-sizing.md** - How to size user stories for Ralph
- **references/escape-hatches.md** - Detailed recovery patterns

---

## Integration with ralph-loop

This skill builds the prompt; the actual looping is handled by the official `ralph-loop` plugin:

```bash
/ralph-loop "<master-prompt>" --max-iterations <N> --completion-promise "<promise>"
```

The stop hook in ralph-loop:
- Intercepts Claude's exit attempts
- Re-feeds the same prompt
- Detects completion promise to exit loop
- Respects max-iterations limit

Our progress.md, AGENTS.md, and prd.json/plan.json provide the persistent context that makes each iteration productive.
