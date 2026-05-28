# context and handoff

managing long sessions, pausing, and resuming.

## context management

### persistence layers

| layer | survives session? | purpose |
|-------|-------------------|---------|
| TodoWrite | no | in-session visibility |
| agents plan | yes | artifacts, notes |
| git commits | yes | permanent progress |
| plan.md | yes | summary, next steps |

### keeping context clean

during long work:

1. **commit frequently**: git is persistent memory
2. **update TodoWrite**: single source of truth for progress
3. **write to plan artifacts**: notes, decisions, blockers

```bash
# check plan directory
ls ~/.agents/plans/{project}/{date}-{slug}/

# update notes
echo "## Progress\n- completed X\n- blocked on Y" >> plan.md
```

### when context feels heavy

signs:
- responses getting slower
- repeating information
- losing track of earlier decisions

actions:
1. commit all current work
2. update plan.md with current state
3. consider pausing and resuming

## pausing work

when you need to stop mid-task:

### 1. commit current state

```bash
git add -A
git commit -m "WIP: [current state description]"
```

### 2. update plan artifact

```markdown
# plan.md

## current state
- phase 3 of 5: implementation
- completed: auth middleware, route guards
- in progress: user permissions
- blocked: none

## next steps
1. finish user permissions helper
2. add tests for permission checks
3. integrate with existing routes

## notes
- using pattern from arbor/auth
- decided to use middleware approach (see commit abc123)
```

### 3. summarize TodoWrite state

copy current todos to plan.md if important.

### 4. push to remote

```bash
git push
```

## resuming work

when starting again:

### 1. check plan directory

```bash
cat ~/.agents/plans/{project}/{date}-{slug}/plan.md
```

### 2. check git state

```bash
git log --oneline -10
git status
git diff HEAD~3 --stat
```

### 3. understand current state

```bash
outline --diff=HEAD~5
layer .
```

### 4. reinitialize TodoWrite

create todos matching where you left off.

### 5. continue from next step

resume flywheel from current position.

## session handoff

when handing off to a new session (or new operator):

### prepare handoff artifact

```markdown
# handoff: {task name}

## context
[brief project description]
[what we're trying to accomplish]

## current state
[phase N of M]
[what's done]
[what's in progress]

## key decisions made
- [decision 1]: [rationale]
- [decision 2]: [rationale]

## blockers / open questions
- [blocker 1]
- [question 1]

## files touched
- `path/to/file1.ts` - [what changed]
- `path/to/file2.ts` - [what changed]

## next steps
1. [step 1]
2. [step 2]
3. [step 3]

## verification
```bash
verify --format=summary
pnpm lint
pnpm build
```
```

### handoff location

save to: `~/.agents/plans/{project}/{date}-{slug}/handoff.md`

## context limits

### when approaching limits

signs:
- tool calls failing
- responses truncated
- obvious context loss

actions:
1. **immediately commit**: preserve work
2. **write handoff**: capture state
3. **pause session**: start fresh

### proactive context management

- summarize completed phases (don't keep full history)
- reference commits instead of repeating code
- use plan.md for persistent notes

## anti-patterns

- **losing work**: not committing before context fills
- **no handoff artifact**: impossible to resume
- **keeping everything in context**: summarize and reference instead
- **not using git**: losing persistent memory
- **TodoWrite as only tracking**: it doesn't survive sessions
