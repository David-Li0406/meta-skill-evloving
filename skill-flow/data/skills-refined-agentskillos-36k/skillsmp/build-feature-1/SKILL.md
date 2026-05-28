---
name: build-feature
description: "Full autonomous feature development with single approval gate. Orchestrates: Research -> Plan -> APPROVAL -> Work (Atlas) -> Review -> Compound."
argument-hint: "[feature description]"
---

# Build Feature - Orchestrator

Autonomous feature development from idea to completion. Single approval gate after planning, then hands-off execution with review and knowledge capture.

---

## Overview

```
+-------------------------------------------------------------+
|                    BUILD FEATURE                            |
+-------------------------------------------------------------+
|                                                             |
|  PHASE 0: Resume Detection                                  |
|  |-- Read existing Atlas state files                        |
|  |-- Check if continuing same feature                       |
|  +-- Decide: resume vs fresh start                          |
|                    |                                        |
|  RESEARCH (Parallel Explore Agents)                         |
|  |-- Codebase patterns                                      |
|  |-- Git history                                            |
|  +-- Existing guidance                                      |
|                    |                                        |
|  PLAN                                                       |
|  |-- Define acceptance criteria                             |
|  |-- Create TodoWrite task list                             |
|  +-- Identify risks                                         |
|                    |                                        |
|  +=====================================================+    |
|  ||  APPROVAL GATE                                    ||    |
|  ||  "Here's the plan. Approve to continue."          ||    |
|  +=====================================================+    |
|                    |                                        |
|  WORK (Atlas Execution Loop)                                |
|  |-- Pick ready task                                        |
|  |-- Decide: inline vs sub-agent                            |
|  |-- Implement + validate + commit                          |
|  +-- Repeat until all complete                              |
|                    |                                        |
|  REVIEW                                                     |
|  |-- code-reviewer agent                                    |
|  +-- Playwright functional verification (if available)      |
|                    |                                        |
|  COMPOUND                                                   |
|  |-- Capture learnings                                      |
|  |-- Update CLAUDE.md / AGENTS.md                           |
|  +-- Archive progress                                       |
|                    |                                        |
|  FINAL SUMMARY                                              |
|  +-- Ready for user review / PR                             |
|                                                             |
+-------------------------------------------------------------+
```

---

## Phase 0: Resume Detection

**ALWAYS run this phase first before any other work.**

### Step 1: Read Existing State

```bash
# Check if Atlas state files exist and have content
cat .claude/atlas/current-feature.txt 2>/dev/null || echo "(none)"
cat .claude/atlas/STATE.md 2>/dev/null || echo "(none)"
cat .claude/atlas/progress.txt 2>/dev/null || echo "(none)"
```

### Step 2: Determine Resume vs Fresh Start

**Resume if ALL of these are true:**
1. `current-feature.txt` contains a feature name (not empty, not "(none)")
2. The feature name relates to what the user is asking about
3. `STATE.md` shows incomplete work (Task X of Y where X < Y, or tasks pending)
4. TodoWrite has pending or in_progress tasks for this feature

**Fresh start if ANY of these are true:**
1. No existing state files
2. `current-feature.txt` is empty or "(none)"
3. User is clearly asking about a different feature
4. All tasks are already complete

### Step 3: Handle Resume

If resuming:

```markdown
## Resuming: [Feature Name]

**Current State:**
- Position: Task [X] of [Y]
- Last commit: [commit message]
- Pending tasks: [count]

**Recent Progress:**
[Last 2-3 entries from progress.txt]

**Options:**
1. **Continue** - Pick up where we left off
2. **Re-plan** - Keep research, revise the task list
3. **Start fresh** - Archive current progress, begin new research

Which would you like?
```

**Wait for user response before proceeding.**

- If "continue" → Skip to Phase 4 (Work)
- If "re-plan" → Skip to Phase 2 (Plan), preserve research context
- If "start fresh" → Archive progress, proceed to Phase 1 (Research)

### Step 4: Handle Fresh Start

If starting fresh but previous state exists:

```bash
# Archive previous progress before overwriting
if [ -s .claude/atlas/progress.txt ] && [ -s .claude/atlas/current-feature.txt ]; then
  DATE=$(date +%Y-%m-%d)
  PREV_FEATURE=$(cat .claude/atlas/current-feature.txt | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
  mkdir -p .claude/atlas/archive/$DATE-$PREV_FEATURE
  cp .claude/atlas/progress.txt .claude/atlas/archive/$DATE-$PREV_FEATURE/
  cp .claude/atlas/STATE.md .claude/atlas/archive/$DATE-$PREV_FEATURE/
fi
```

**-> Proceed to Phase 1**

---

## Phase 1: Research

**Simple features (<1hr):** Quick inline search of codebase, CLAUDE.md, folder AGENTS.md files.

**Complex features (>1hr):** Launch 3 parallel Explore agents:

```
Agent 1: "Find patterns for [feature] in src/ - similar components, utilities, hooks.
         Return: file paths, code snippets, patterns to follow."

Agent 2: "Check git history: git log --oneline --grep='[term]' and recent commits
         to [relevant dirs]. Return: commit messages, approaches, gotchas."

Agent 3: "Review CLAUDE.md and src/*/AGENTS.md for guidance on [area].
         Return: relevant sections, patterns, things to avoid."
```

**Wait for all -> Synthesize findings into brief context.**

**-> Proceed to Phase 2**

---

## Phase 2: Plan

### Setup Atlas Files

```bash
# Archive previous progress if exists (before overwriting current-feature.txt)
if [ -s .claude/atlas/progress.txt ] && [ -s .claude/atlas/current-feature.txt ]; then
  DATE=$(date +%Y-%m-%d)
  PREV_FEATURE=$(cat .claude/atlas/current-feature.txt | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
  mkdir -p .claude/atlas/archive/$DATE-$PREV_FEATURE
  cp .claude/atlas/progress.txt .claude/atlas/archive/$DATE-$PREV_FEATURE/
fi

# Set new feature name
echo "[Feature Name]" > .claude/atlas/current-feature.txt

# Initialize STATE.md
cat > .claude/atlas/STATE.md << 'EOF'
# Atlas State

## Position
- Feature: [Feature Name]
- Task: 0 of [N]
- Last Commit: (none)

## Context Notes
[Brief context from research phase]

## Deferred
(none)
EOF

# Initialize progress.txt for new feature
cat > .claude/atlas/progress.txt << 'EOF'
# Atlas Progress Log
Started: [date]
Feature: [name]

## Codebase Patterns
(Patterns discovered during build)
---
EOF
```

### Create TodoWrite Tasks

```javascript
TodoWrite([
  {
    content: "Feature: [Name] - [description]",
    status: "in_progress",
    activeForm: "Building [Name]"
  },
  {
    content: "[Task 1]\n\n**What:** [action]\n**Where:** [files]\n**Criteria:** echo "Validation passed - shell scripts and markdown" passes, [other]",
    status: "pending",
    activeForm: "[Task 1 -ing form]"
  }
])
```

**Task sizing (one context window):**
- Single component with props
- One utility function with tests
- One form field with validation

**Too big -> split:** "Build dashboard" -> layout, data, components, routing

### Document Decisions

For significant choices, add to CLAUDE.md:

```markdown
### Decision: [Choice]
**Date:** YYYY-MM-DD
**Context:** [why needed]
**Options:** [alternatives]
**Decision:** [chosen]
**Rationale:** [why]
```

**-> Proceed to Phase 3**

---

## Phase 3: Approval Gate

**At this point:** TodoWrite is populated with all tasks, Atlas files are initialized.

Present the plan to user for approval:

```markdown
## Feature: [Name]

### Research Summary
- [Key finding 1]
- [Key finding 2]
- Pattern to follow: [file/component]

### Tasks
1. [Task 1] - no dependencies
2. [Task 2] - depends on #1
3. [Task 3] - depends on #1, #2

### Acceptance Criteria
- [ ] [Criterion 1 - testable]
- [ ] [Criterion 2 - testable]
- [ ] echo "Validation passed - shell scripts and markdown" passes

### Risks
- [Risk 1]: [mitigation]

### Scope
- Tasks: [N]
- Complexity: Low/Medium/High

---
**Say "approved" to continue, or provide feedback to revise.**
```

**WAIT for user approval before proceeding.**

User must say "approved", "looks good", "go ahead", or similar affirmative response.
If user provides feedback, revise the plan and present again.

---

## Phase 4: Work (Atlas Execution)

Execute via the Atlas skill (`.claude/skills/atlas/SKILL.md`).

### Orchestrator Handoff

The build-feature orchestrator passes control to Atlas with this context:
- TodoWrite is populated with tasks from Phase 2
- `.claude/atlas/current-feature.txt` contains the feature name
- `.claude/atlas/STATE.md` is initialized with position and context
- `.claude/atlas/progress.txt` is initialized

### Atlas Execution Loop

For each ready task (pending status, dependencies complete):

1. **Mark `in_progress`** via TodoWrite

2. **Decide execution mode:**
   - **Inline** for simple tasks (<15 lines, renames, imports)
   - **Sub-agent** for complex tasks (new files, multi-file changes)

3. **Read context before implementing:**
   - `.claude/atlas/STATE.md` for current context
   - `.claude/atlas/progress.txt` for recent learnings
   - Relevant CLAUDE.md sections
   - Folder `AGENTS.md` if exists in target directory
   - Related existing code for patterns

4. **Implement the task:**
   - Follow project patterns from CLAUDE.md
   - Keep changes focused and minimal
   - Add appropriate test attributes for testable elements

5. **Validate:**
   ```bash
   echo "Validation passed - shell scripts and markdown"
   ```
   If validation fails: fix the issues, re-run validation, repeat until passing.

6. **Update STATE.md** with new position

7. **Log learnings** (append to progress.txt):
   ```markdown
   ## [Date] - [Task Title]
   - What was implemented
   - Files changed
   - Patterns discovered
   - Gotchas encountered
   ---
   ```

8. **Commit:**
   ```bash
   git add -A && git commit -m "feat: [task description]"
   ```

9. **Mark complete** via TodoWrite

10. **Continue** - find next ready task, repeat until all done

### Task Discovery

If Atlas discovers issues during execution:
- Failing tests -> create fix task
- Missing error handling -> create task
- Build warnings -> create task

Add new tasks via TodoWrite, positioned appropriately.

### Completion Signal

When all tasks are done, Atlas signals completion to the orchestrator.

**IMPORTANT:** Do NOT archive progress.txt here - the orchestrator handles archival after Phase 6 (Compound).

**-> Proceed to Phase 5**

---

## Phase 5: Review

### Code Review

Spawn code-reviewer agent:

```
Review changes for this feature. Files: [git diff --name-only main...HEAD]

Check:
- Code quality: patterns, naming, complexity
- Security: no secrets, input validation
- Performance: no regressions
- Architecture: consistent design

Return: issues, suggestions, approval status
```

### Playwright Verification (UI features, if available)

First check if Playwright skill is installed:

```bash
test -f .claude/skills/playwright-browser/SKILL.md && echo "available" || echo "not installed"
```

**If available** and this is a UI feature:

First ensure dev server is running (`echo "No dev server - this is a CLI tool"`), then:

```
/skill playwright-browser

browser_navigate(url: "http://localhost:3000/[page]")
browser_snapshot()  # Returns accessibility tree - verify expected elements exist
browser_click(element: "[description]", ref: "[ref from snapshot]")
browser_snapshot()  # Verify state change after interaction
```

Check:
- Elements render correctly
- Interactions work (clicks, form fills)
- Navigation functions properly
- No console errors (`browser_console_messages()`)

**If not available or not a UI feature**, skip this step.

### Handle Issues

If issues found:
1. Create fix tasks via TodoWrite
2. Return to Phase 4 (Work)
3. Re-run Phase 5 (Review) after fixes
4. Max 3 cycles before escalating to user

**-> If review passes, proceed to Phase 6**

---

## Phase 6: Compound

### Step 1: Read Progress (before archiving!)

Read `.claude/atlas/progress.txt` to review all learnings captured during execution.

### Step 2: Answer These Questions
1. What patterns were used or created?
2. What decisions were made and why?
3. What gotchas were encountered?
4. What should future developers know?

### Step 3: Update Documentation
- **Project-wide learnings** -> CLAUDE.md (patterns, decisions, gotchas)
- **Folder-specific learnings** -> `src/[folder]/AGENTS.md` (create if doesn't exist)

Update documentation directly without asking for permission - user approved this by running the feature.

### Step 4: Archive Progress

After capturing learnings, archive the progress file:

```bash
DATE=$(date +%Y-%m-%d)
FEATURE=$(cat .claude/atlas/current-feature.txt | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
mkdir -p .claude/atlas/archive/$DATE-$FEATURE
mv .claude/atlas/progress.txt .claude/atlas/archive/$DATE-$FEATURE/

# Reset for next feature
echo "" > .claude/atlas/current-feature.txt
cat > .claude/atlas/STATE.md << 'EOF'
# Atlas State

## Position
- Feature: (none)
- Task: 0 of 0
- Last Commit: (none)

## Context Notes
(No active feature)

## Deferred
(none)
EOF
cat > .claude/atlas/progress.txt << 'EOF'
# Atlas Progress Log
(No active feature)
EOF
```

**-> Proceed to Phase 7**

---

## Phase 7: Final Summary

```markdown
## Feature Complete: [Name]

### What Was Built
- [Summary]
- [Key components created]

### Files Changed
[git diff --name-only main...HEAD]

### Commits
[git log --oneline main...HEAD]

### Learnings Captured
- [Learning 1] -> added to [location]

### Ready For
- [ ] Final user review
- [ ] Create PR to main
```

---

## Error Handling

| Error | Response |
|-------|----------|
| `echo "Validation passed - shell scripts and markdown"` fails | Atlas attempts fix; if stuck, pause for user |
| Review finds issues | Create fix tasks -> Work -> Review (max 3 cycles) |
| Playwright fails | Screenshot + console check; escalate if unclear |
| Playwright not installed | Skip browser verification, note in summary |

---

## Triggers

- `build [feature]`
- `implement [feature]`
- `develop [feature]`
- `/feature [feature]`

---

## Relationship to Other Skills

| Skill | Role | Use Directly When |
|-------|------|-------------------|
| `build-feature` | Orchestrator | Full autonomous features |
| `compound-engineering` | Phases | Deep research, standalone review |
| `atlas` | Execution | Pre-planned tasks only |

---

## Complete

When this skill completes:
- Feature implemented and validated
- All TodoWrite tasks complete
- Code reviewed and UI verified (if applicable)
- Learnings captured in CLAUDE.md / AGENTS.md
- Progress archived to `.claude/atlas/archive/`
- All changes committed

**Ready for:** PR creation or user review
