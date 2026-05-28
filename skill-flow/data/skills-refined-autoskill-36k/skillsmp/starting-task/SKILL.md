---
name: starting-task
description: Use when starting a work session or when user asks to begin working on a beads task. Handles task selection, branch management, and context display. Use after /clear, at session start, or when switching tasks.
---

# Flow: Start Task

<STOP-AND-READ>

## ⛔ BEFORE DOING ANYTHING

**READ this ENTIRE skill FIRST. Do NOT run any commands yet.**

**Violation check — if ANY of these are true, STOP and apologize:**
- [ ] I already ran `bd ready` → VIOLATION. Apologize, start over.
- [ ] I already ran `bd list` → VIOLATION. Apologize, start over.
- [ ] I already ran `bd show` → VIOLATION. Apologize, start over.
- [ ] I said "Let me wait for content to load" → About to violate. STOP.
- [ ] I'm "preparing" or "getting ready" → About to violate. STOP.

**If you checked any box: Tell the user you violated the skill, apologize, and start over from Step 1 below.**

**Required action NOW:**
1. Read this entire skill (don't skim)
2. Create TodoWrite checklist from the steps
3. ONLY THEN execute Step 1

</STOP-AND-READ>

## Overview

**Core principle:** Consultation over assumption.

This skill guides starting work on beads tasks through explicit consultation steps. Users choose tasks, see context first, and decide on branch strategy - even when choices seem "obvious."

## 🚨 CRITICAL: Follow This Exact Process

**Step 1 - Run the tree builder script:**
```bash
bd graph --all --json | python3 <skill-base-dir>/scripts/bd-tree.py
```

The script outputs a properly formatted hierarchical tree. Example output:
```
1. [E] StatusKit (claude-tools-5dl) | P1 · in_progress | #statuskit
   ├─ 1.1 [T] Distribution (claude-tools-5dl.1) | P2 · open | #statuskit
   ├─ 1.2 [F] Git module (claude-tools-c7b) | P2 · open | #statuskit
   └─ 1.3 [F] Beads module (claude-tools-5d1) | P2 · open | #statuskit
```

**Script options:**
- `-s "term"` — filter by search term
- `-n 10` — limit to first N root tasks
- `--collapse` — show only roots with child count `[+N]`

**For task selection:**
- ✅ Use plain text output (allows user to type `1.2` or `1.1.1`)
- ❌ DO NOT use `AskUserQuestion` tool (cannot handle hierarchical numbers)

## Quick Reference

| Step | Action | Key Point |
|------|--------|-----------|
| 0. Detect | Check agent-deck, worktree context | Environment awareness |
| 1. Tree | `bd graph --all --json \| python3 <skill-base-dir>/scripts/bd-tree.py` | Script builds tree |
| 2. Select | Let user choose by number/ID | User agency |
| 3. Show | Display in box format | Context BEFORE commitment |
| 4. Branch | Check branch type | Generic vs Feature |
| 5. Search | Find existing branches | Reuse before create |
| 6. Ask | RECOMMEND or NEUTRAL | Tone matters |
| 6.5. Worktree | Ask: here OR worktree | Parallel work option |
| 7. Update | `bd update` | Only after confirmation |
| 8. Create | `git checkout -b` | If requested (skip if worktree) |

**Branch Tone Guide:**
- Generic (main/master/develop) → **RECOMMEND** creating feature branch
- Feature → **NEUTRAL** ask to continue or create new

## Workflow

Follow these steps **in order**. Do not skip steps.

### 0. Environment Detection

**Run at skill start to detect available tools and context:**

```bash
# Check if agent-deck is available
command -v agent-deck >/dev/null 2>&1 && echo "HAS_AGENT_DECK=true" || echo "HAS_AGENT_DECK=false"

# Check if already in a worktree
pwd | grep -q "\.worktrees/" && echo "IN_WORKTREE=true" || echo "IN_WORKTREE=false"
```

Store these values for use in Step 6.5.

### 1. Build and Display Task Tree

**Run the tree builder script:**
```bash
bd graph --all --json | python3 <skill-base-dir>/scripts/bd-tree.py
```

The script handles:
- Parsing JSON and building parent-child relationships
- Filtering (shows open/in_progress, hides closed/blocked)
- Sorting (in_progress → open → deferred, then by priority)
- Hierarchical numbering (`1.`, `1.1`, `1.2`)
- Tree connectors (`├─`, `└─`)

**Script options:**
- `bd graph --all --json | python3 <skill-base-dir>/scripts/bd-tree.py -s "search"` — filter by term
- `bd graph --all --json | python3 <skill-base-dir>/scripts/bd-tree.py --collapse` — show roots only with `[+N]`

**If script shows no tasks:**
```
Нет доступных задач для работы.

Причины:
- Все задачи закрыты
- Все открытые задачи заблокированы
- Все задачи отложены (deferred)

Что вы хотите сделать?
1. bd blocked - посмотреть заблокированные задачи
2. bd list --status=deferred - посмотреть отложенные
3. new - создать новую задачу
```

**✓ Validation Checkpoint:**
- [ ] I ran the script (not bd ready/list/show directly)
- [ ] I'm asking for selection with PLAIN TEXT (not AskUserQuestion tool)

### 2. Get User's Task Selection

User can select by:
- **Hierarchical number:** `1`, `1.2`, `1.1.2`
- **Task ID:** `claude-tools-c7b`
- **Create new:** `new` or `create`

Map selection to task ID and proceed.

### 3. Show Task Description FIRST

**Before any actions**, display task in detailed box format:

```
┌─ [Type] Title ────────────────────────────────────────────┐
│ ID: <task-id>                                             │
│ Priority: <priority>  Status: <status>  Type: <type>      │
│ Labels: #label1 #label2                                   │
├───────────────────────────────────────────────────────────┤
│ DESCRIPTION                                               │
│ <full task description>                                   │
│                                                            │
├───────────────────────────────────────────────────────────┤
│ LINKS                                                      │
│ Design: docs/plans/...                                    │
│ Plan: docs/plans/...                                      │
│                                                            │
├───────────────────────────────────────────────────────────┤
│ DEPENDENCIES                                              │
│ Depends on:                                               │
│   → claude-tools-xxx: Some task (closed)                  │
│                                                            │
│ Blocks:                                                   │
│   → claude-tools-yyy: Another task (open)                 │
└───────────────────────────────────────────────────────────┘
```

**Include sections only if present:**
- Metadata (always)
- Description (if present)
- Links (if description contains `Design:` or `Plan:` lines)
- Dependencies (if present)

**If task is already in_progress:**
```
┌─ [F] Git module ──────────────────────────────────────────┐
│ ⚠️  Задача уже в работе (in_progress)                     │
│                                                            │
│ ID: claude-tools-c7b                                      │
...
```

**User needs context BEFORE committing to task.**

### 4. Check Git Branch

```bash
git branch --show-current
```

Identify branch type:
- **Generic:** main, master, develop, trunk
- **Feature:** anything else

### 5. Search for Existing Branches

**Search for branches containing the task ID:**
```bash
git branch -a | grep -E "(fix|chore|feature)/{task-id}"
```

This searches both local and remote (origin) branches, filtering for branches that match our naming convention (prefix + full task-id).

**Filter results:**
- Remove `remotes/origin/HEAD` entries
- Extract branch names (strip `remotes/origin/` prefix)
- Deduplicate (if same branch exists locally and remotely, prefer local)

**If matching branches found:**
- Present options to checkout existing branch OR create new one
- If multiple branches found, show all options
- Include branch names and location (local/remote) in the suggestion

**If no matching branches found:**
- Proceed to create new branch with appropriate prefix

**Determine branch prefix from task type:**
- bug → `fix/`
- chore → `chore/`
- feature → `feature/`
- task → `feature/`
- epic → `feature/` (epics use feature prefix)
- **Unknown type:** default to `feature/` and warn user

**Generate brief name:**
- Take 2-3 key words from task title
- Convert to lowercase
- Replace spaces with hyphens
- Example: "Fix authentication timeout" → "authentication-timeout"

**Final format:** `{prefix}{task-id}-{brief-name}`

Examples:
- bug task `claude-tools-abc` "Fix login error" → `fix/claude-tools-abc-login-error`
- feature task `claude-tools-xyz` "Add dark mode" → `feature/claude-tools-xyz-dark-mode`
- chore task `claude-tools-123` "Update dependencies" → `chore/claude-tools-123-update-dependencies`

### 6. Ask About Branch (with appropriate tone)

**Three scenarios to handle:**

#### Scenario A: Existing Branches Found

**If one branch found:**

> "Found existing branch for this task: `{branch-name}` (local/remote)
>
> Would you like to:
> 1. Checkout existing branch: `{branch-name}`
> 2. Create new branch: `{prefix}{task-id}-{brief-name}`"

**If multiple branches found:**

> "Found multiple branches for this task:
> - `{branch-1}` (local)
> - `{branch-2}` (remote)
>
> Would you like to:
> 1. Checkout: `{branch-1}` (most recent/local preferred)
> 2. Checkout: `{branch-2}`
> 3. Create new branch: `{prefix}{task-id}-{brief-name}`"

**Why prioritize existing:** Avoid duplicate branches, continue existing work.

**Priority for multiple branches:**
- Prefer local over remote (faster checkout)
- Prefer branches matching current task type prefix
- Show most recent first (by commit date)

#### Scenario B: No Existing Branches + Generic Branch → RECOMMEND

Use strong, specific recommendation:

> "You're currently on `{branch}` (main development branch). **I recommend creating a separate branch** for this work to keep main clean and make it easier to create PRs later.
>
> Would you like me to create branch `{prefix}{task-id}-{brief-name}`?"

**Why recommend:** Generic branches should stay stable.

#### Scenario C: No Existing Branches + Feature Branch → NEUTRAL

Use neutral, informational tone:

> "You're currently on feature branch `{branch}`.
>
> Would you like to continue work on this branch, or create a new branch `{prefix}{task-id}-{brief-name}`?"

**Why neutral:** User might be working on related features, or might want isolation - don't assume.

### 6.5. Ask About Worktree (Parallel Work Option)

**After user confirms branch choice, ask how to open it:**

**Skip this step if:**
- `IN_WORKTREE=true` (already in worktree, don't nest)
- User explicitly said "checkout here" or similar

**Check if worktree already exists:**
```bash
git worktree list | grep "{branch-name}"
```

#### If Worktree Already Exists

**With agent-deck:**
```bash
agent-deck session list | grep "{branch-name}"
```
- Session exists → "Сессия уже существует. Переключитесь в agent-deck TUI (Ctrl+j/k)."
- No session → "Worktree есть. Создать сессию agent-deck?" → `agent-deck add "$(pwd)" -t "{task-title}"` (without --worktree)

**Without agent-deck:**
> "Worktree уже существует: `.worktrees/{branch-name-sanitized}/`
> Откройте в новом терминале:
> ```
> cd .worktrees/{branch-name-sanitized} && claude
> ```"

Skip to Step 7.

#### If No Existing Worktree

**With agent-deck (`HAS_AGENT_DECK=true`):**

> "Как открыть ветку `{branch-name}`?
>
> 1. Здесь (обычный checkout)
> 2. В новой сессии agent-deck с worktree"

**Without agent-deck (`HAS_AGENT_DECK=false`):**

> "Как открыть ветку `{branch-name}`?
>
> 1. Здесь (обычный checkout)
> 2. В worktree (для параллельной работы)"

#### Execution Based on Choice

**Option 1 (checkout here):**
- Proceed to Step 7, then Step 8 (normal checkout)

**Option 2 with agent-deck:**
```bash
agent-deck add "$(pwd)" -t "{task-title}" --worktree {branch-name}
```
- Proceed to Step 7 (update beads status)
- **Skip Step 8** (branch created by agent-deck)
- Tell user: "Создана сессия `{task-title}` с worktree. Переключитесь в agent-deck TUI."

**Option 2 without agent-deck:**
- Invoke `superpowers:using-git-worktrees` skill with branch name
- Proceed to Step 7 (update beads status)
- **Skip Step 8** (branch created by worktree skill)
- Tell user the worktree path and how to open it

**If agent-deck command fails:**
> "agent-deck недоступен или вернул ошибку. Создаю worktree через git..."

Then invoke `superpowers:using-git-worktrees` as fallback.

### 7. Update Task Status

**Only after user confirms everything:**
```bash
bd update <task-id> --status=in_progress
```

Or if user is claiming:
```bash
bd update <task-id> --claim
```

### 8. Create or Checkout Branch (if requested)

**If user chose existing branch:**
```bash
git checkout <existing-branch-name>
```

Or if remote branch:
```bash
git checkout -b <local-branch-name> origin/<remote-branch-name>
```

**If user chose to create new branch:**
```bash
git checkout -b <prefix><task-id>-<brief-name>
```

Follow user's preference from step 6.

## Red Flags - STOP

If you're thinking any of these, STOP and follow the workflow:

**Skill loading violations (MOST CRITICAL):**
- "Let me wait for content to load" → Content IS loaded. Read it NOW.
- "I'll prepare while reading" → NO. Read FIRST, act SECOND.
- "Let me get the task list" → STOP. Did you read the skill? Run the script.

**Command violations:**
- "bd ready is good enough" → Use the script
- "I'll build the tree myself" → Script does this. Don't reinvent.
- "I'll format differently" → Script output is the correct format

**Tool violations:**
- "AskUserQuestion is more user-friendly"
- "Structured UI is better than plain text"

**Workflow violations:**
- "Creating a feature branch is obviously right"
- "User said they're in a hurry"
- "I'll choose a good task for them"
- "Description can go in summary at the end"

**Branch naming violations:**
- "No need to search existing branches"
- "I'll skip the prefix for simple tasks"
- "feature/ works for all task types"

**Worktree violations:**
- "Step 6.5 is optional, I'll skip it"
- "User didn't mention worktree so skip Step 6.5"
- "User said yes to branch, going straight to checkout"
- "Already in worktree, I'll create nested worktree"

**All of these mean: Go back to CRITICAL section. Follow exact process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Let me wait for content to load" | Content IS loaded. Read the skill NOW. |
| "I'll get the task list while reading" | NO. Read skill FIRST. Commands come AFTER. |
| "bd ready is a quick way to see tasks" | Wrong. Use the script: `bd graph --all --json \| python3 <skill-base-dir>/scripts/bd-tree.py` |
| "I'll build the tree myself" | Script does this correctly. Don't reinvent. |
| "AskUserQuestion is more user-friendly" | Can't handle hierarchical numbers (1.2, 1.1.1). Use plain text. |
| "Creating branch is obviously right" | Right for this user, this time? Ask. |
| "User said they're in a hurry" | Consultation is part of the service, not overhead. |
| "I'll choose a good task for them" | User agency matters. Show options, let them choose. |
| "No existing branches to search" | Always search. Prevents duplicate branches. |
| "I can skip prefix for simple tasks" | All branches need prefixes. Consistent naming matters. |
| "feature/ works for everything" | Wrong. Use fix/ for bugs, chore/ for chores. |
| "Step 6.5 is optional" | "Optional" means conditional on context, not skippable. Always evaluate. |
| "User didn't ask for worktree" | Step 6.5 OFFERS the option. User doesn't need to ask first. |
| "User said yes to branch, proceed to checkout" | Stop at 6.5. Offer worktree option BEFORE checkout. |
| "I'll create worktree inside worktree" | Never nest worktrees. Check IN_WORKTREE first. |

## Examples

### ❌ BAD: Assumes and acts

```
User: "start the git module task"
Agent: I've created branch claude-tools-c7b and marked the task in_progress.
       [shows task details in summary]
```

**Problems:**
- Created branch without asking
- No recommendation (generic branch)
- Description shown after actions
- No user choice

### ✅ GOOD: Consults before acting

```
User: "start the git module task"
Agent: Доступные задачи:

       1. [E] StatusKit (claude-tools-5dl) | P1 · in_progress | #statuskit
          ├─ 1.1 [T] Distribution (claude-tools-5dl.1) | P2 · open | #statuskit
          ├─ 1.2 [F] Git module (claude-tools-c7b) | P2 · open | #statuskit
          └─ 1.3 [F] Beads module (claude-tools-5d1) | P2 · open | #statuskit

       2. [F] External feature (claude-tools-xyz) | P2 · open

       Выберите задачу (по номеру или ID), или введите 'new' для создания новой:

User: 1.2

Agent: ┌─ [F] Git module ──────────────────────────────────────────┐
       │ ID: claude-tools-c7b                                      │
       │ Priority: P2  Status: open  Type: feature                 │
       │ Labels: #statuskit #python                                │
       ├───────────────────────────────────────────────────────────┤
       │ DESCRIPTION                                               │
       │ Create module that displays:                             │
       │ - Current directory (project name)                        │
       │ - Branch and its status                                   │
       │ - Number of changes (staged/unstaged)                     │
       │ - Hash and age of last commit                             │
       ├───────────────────────────────────────────────────────────┤
       │ DEPENDENCIES                                              │
       │ Depends on:                                               │
       │   → claude-tools-5dl: StatusKit (in_progress)             │
       └───────────────────────────────────────────────────────────┘

       You're currently on `master` (main development branch).
       I recommend creating a feature branch for this work to keep
       master clean and make it easier to create PRs later.

       Would you like me to create branch `feature/claude-tools-c7b-git-module`?
```

**Correct because:**
- Shows hierarchical tree first
- Lets user select by number
- Shows full context in box format
- Searches for existing branches first
- Uses correct prefix (feature/ for feature type)
- Uses full format: prefix + task-id + brief-name
- Recommends (not creates) for generic branch
- Gives user choice
- Uses appropriate tone

### ✅ GOOD: Existing branch found

```
User: "start bug task claude-tools-abc"
Agent: [shows task description box for bug task]

       Found multiple branches for this task:
       - `fix/claude-tools-abc-login-error` (local)
       - `fix/claude-tools-abc-auth-fix` (remote)

       Would you like to:
       1. Checkout: `fix/claude-tools-abc-login-error` (local preferred)
       2. Checkout: `fix/claude-tools-abc-auth-fix`
       3. Create new branch: `fix/claude-tools-abc-authentication-timeout`
```

**Correct because:**
- Searched with proper grep pattern (only matching our convention)
- Presents existing branches with location (local/remote)
- Shows local branch first (priority)
- Still offers option to create new
- Uses correct prefix (fix/ for bug type)
- Deduplicated branches (no duplicates if same branch exists locally and remotely)

### ❌ BAD: Time pressure bypass

```
User: "start git module, I'm in a hurry"
Agent: [creates branch immediately without asking]
```

**Problem:** "In a hurry" is not a reason to skip consultation.

### ✅ GOOD: Consults despite pressure

```
User: "start git module, I'm in a hurry"
Agent: [shows task description]

       You're on `master`. I recommend creating a feature branch.

       Quick question: Should I create branch `claude-tools-c7b`?
       (Takes 2 seconds)
```

**Correct because:**
- Acknowledges hurry (quick question)
- Still consults
- Follows workflow

## Edge Cases

### When Task Already in_progress

If task status is already `in_progress`:
1. Show warning in task display box: `⚠️  Задача уже в работе (in_progress)`
2. Still show full description (user might not remember)
3. Still check branch and ask
4. Don't update status (already correct)

### When No Tasks Available

If filtering leaves no tasks to show:
```
Нет доступных задач для работы.

Причины:
- Все задачи закрыты
- Все открытые задачи заблокированы
- Все задачи отложены (deferred)

Что вы хотите сделать?
1. bd blocked - посмотреть заблокированные задачи
2. bd list --status=deferred - посмотреть отложенные
3. new - создать новую задачу

Ваш выбор:
```

### When Search Found Nothing

If search argument provided but no matches found:
```
Поиск "<search-term>" не нашел задач.

Доступные задачи:
[show full tree without filter]

Выберите задачу (по номеру или ID), или введите 'new' для создания новой:
```

### When Multiple Graphs Exist

If `bd graph --all --json` returns multiple graphs:
- Merge all graphs into one tree
- Use sequential root numbering across all graphs
- Example: Graph 1 roots = `1.`, `2.`, Graph 2 roots = `3.`, `4.`

### When User Already in Worktree

If `IN_WORKTREE=true` (detected in Step 0):
- **Do NOT offer to create another worktree** (avoid nesting)
- At Step 6.5, show only:
  ```
  Вы уже в worktree. Продолжить работу здесь или переключиться на другую ветку?

  1. Продолжить здесь (checkout в текущем worktree)
  2. Переключиться на другую ветку
  ```
- If user wants different worktree, suggest: "Вернитесь в основной проект и запустите /flow:start оттуда"

### When Worktree Already Exists for Branch

If `git worktree list | grep "{branch-name}"` returns result:
- **Do NOT create duplicate worktree**
- Show existing worktree path
- With agent-deck: check for existing session, offer to create session if none
- Without agent-deck: tell user to open existing worktree manually

### When agent-deck Command Fails

If `agent-deck add` returns non-zero exit code:
1. Log the error (don't hide it)
2. Inform user: "agent-deck недоступен или вернул ошибку"
3. **Fallback:** invoke `superpowers:using-git-worktrees` instead
4. Continue workflow normally

## The Bottom Line

Always follow the workflow. Consultation is not overhead - it's the service.

Show context first, let users choose, recommend appropriately, then act.
