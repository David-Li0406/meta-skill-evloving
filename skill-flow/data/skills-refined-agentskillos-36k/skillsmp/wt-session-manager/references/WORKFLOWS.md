# wt Workflows

Step-by-step workflows with checklists for common wt operations.

---

## Daily Workflow

### Morning Session Start

When starting your hub session:

```
Morning Start Checklist:
- [ ] Run wt to see active workers
- [ ] Check for idle sessions (!! markers)
- [ ] Run bd ready to see available work
- [ ] Decide: resume existing work or spawn new workers
- [ ] Report status to user
```

**Commands:**
```bash
wt                # Active sessions
bd ready          # Available beads
```

**Decision tree:**
- Idle workers? → Check on them first (`wt <name>`)
- Workers making progress? → Let them continue
- Ready beads? → Consider spawning new workers
- All caught up? → Focus on other work

---

### Spawning Multiple Workers

When you have several beads ready:

```
Batch Spawn Checklist:
- [ ] Review ready beads: bd ready
- [ ] Select beads for parallel work
- [ ] Spawn with --no-switch to stay in hub
- [ ] Verify all spawned: wt
- [ ] Start monitoring: wt watch
```

**Commands:**
```bash
bd ready                            # See what's available

wt new project-abc --no-switch      # Spawn first
wt new project-xyz --no-switch      # Spawn second
wt new project-123 --no-switch      # Spawn third

wt                                  # Verify all running
wt watch                            # Monitor progress
```

**Best practices:**
- Use `--no-switch` to spawn multiple without leaving hub
- Don't spawn more than you can monitor
- Consider resource limits (Docker containers, ports)

---

### Checking on Workers

When monitoring shows issues:

```
Worker Check Checklist:
- [ ] Identify problematic session (idle, error)
- [ ] Switch to session: wt <name>
- [ ] Assess situation
- [ ] Provide guidance if stuck
- [ ] Detach: Ctrl-b d
- [ ] Continue monitoring
```

**Signs to check:**
- `!!` marker - Idle too long
- Error status
- No progress on watch

**Commands:**
```bash
wt toast           # Switch to session
# Assess, provide guidance
# Ctrl-b d to detach
```

---

### End of Day

Before closing hub session:

```
End of Day Checklist:
- [ ] Run wt to review all sessions
- [ ] Check for work ready to close
- [ ] Close completed sessions: wt close <name>
- [ ] Note any blocked/stuck sessions
- [ ] Workers persist overnight - they're fine
```

**Note:** Worker sessions survive hub closure. They'll be there tomorrow.

---

## Session Lifecycle Workflows

### Completing a Task

When a worker finishes their bead:

```
Completion Checklist:
- [ ] Ensure all changes committed
- [ ] Run wt done from worker (or wt close from hub)
- [ ] Verify PR created (if pr-review mode)
- [ ] Close session: wt close <name>
- [ ] Verify bead closed: bd show <bead-id>
```

**From worker session:**
```bash
wt status           # Verify which session
wt done             # Submit work
wt close            # Cleanup
```

**From hub:**
```bash
wt close toast      # One command does both
```

---

### Handling Blocked Work

When a worker gets stuck:

```
Blocked Work Checklist:
- [ ] Switch to session: wt <name>
- [ ] Understand the blocker
- [ ] Options:
      a) Provide guidance to unblock
      b) Kill session and update bead: wt kill + bd update
      c) Wait for blocker resolution
- [ ] Document blocker in bead notes
```

**Option A - Provide guidance:**
```bash
wt toast
# Give Claude direction to proceed
# Ctrl-b d
```

**Option B - Kill and track:**
```bash
wt kill toast
bd update project-abc --status blocked --notes "Waiting for API access"
```

**Option C - Leave running:**
Worker will resume when you provide what's needed.

---

### Recovering from Errors

When a session shows error status:

```
Error Recovery Checklist:
- [ ] Switch to session: wt <name>
- [ ] Review error output
- [ ] Decide: fixable or need restart?
- [ ] If fixable: guide Claude
- [ ] If restart needed: wt kill, then wt new
```

**Commands:**
```bash
wt toast                    # Check the error

# If recoverable:
# Guide Claude to fix

# If restart needed:
wt kill toast
wt new project-abc          # Fresh start
```

---

### Abandoning Work

When you need to discard work:

```
Abandon Checklist:
- [ ] Confirm you want to discard changes
- [ ] From worker: wt abandon
- [ ] Bead remains open for future work
- [ ] Consider why - document in bead notes
```

**Commands (from worker):**
```bash
wt abandon          # Prompts for confirmation
```

**Note:** Abandon is for when the approach was wrong. Kill is for when you just need to stop.

---

## Project Management Workflows

### Adding a New Project

When starting work on a new codebase:

```
Project Setup Checklist:
- [ ] Initialize beads in project: bd init (in project dir)
- [ ] Register with wt: wt project add <name> <path>
- [ ] Configure: wt project config <name>
- [ ] Set merge mode, test env, hooks
- [ ] Create first beads: bd create
- [ ] Spawn first worker: wt new <bead>
```

**Commands:**
```bash
cd ~/newproject
bd init                             # Initialize beads

wt project add newproject ~/newproject
wt project config newproject        # Edit config

bd create "Initial setup task"
wt new newproject-xxx
```

---

### Configuring Test Environment

For projects needing Docker/port isolation:

```
Test Env Setup Checklist:
- [ ] Ensure docker-compose.yml uses PORT_OFFSET
- [ ] Configure test_env in project config
- [ ] Set setup command (docker compose up -d)
- [ ] Set teardown command (docker compose down)
- [ ] Optionally set health check
- [ ] Test with: wt new <bead>
```

**docker-compose.yml pattern:**
```yaml
services:
  db:
    ports:
      - "${PORT_OFFSET:-0}5432:5432"
  api:
    ports:
      - "${PORT_OFFSET:-0}3000:3000"
```

**Project config:**
```json
{
  "test_env": {
    "setup": "docker compose up -d",
    "teardown": "docker compose down",
    "port_env": "PORT_OFFSET",
    "health_check": "curl -f http://localhost:${PORT_OFFSET}3000/health"
  }
}
```

---

## Seance Workflows

### Understanding Past Decisions

When you need to know why something was done:

```
Decision Investigation Checklist:
- [ ] List past sessions: wt seance
- [ ] Find relevant session
- [ ] Query: wt seance <name> -p "Why..."
- [ ] Or interactive: wt seance <name>
```

**Commands:**
```bash
wt seance --project supabyoi        # Find sessions

wt seance toast -p "Why did you choose JWT over sessions?"
```

---

### Resuming Abandoned Work

When you need context from an abandoned session:

```
Resume Investigation Checklist:
- [ ] List sessions: wt seance
- [ ] Find the abandoned session
- [ ] Query for context: wt seance <name>
- [ ] Note what was tried
- [ ] Create new bead or update existing
- [ ] Spawn fresh worker with context
```

**Commands:**
```bash
wt seance toast -p "What did you try? What was blocking you?"

# Get context, then:
bd update project-abc --notes "Previous attempt: ..."
wt new project-abc
```

---

## Merge Mode Workflows

### Direct Merge (Solo/Prototype)

For projects where you trust the work:

```
Direct Merge Flow:
1. wt done (or wt close)
2. Branch merges directly to main
3. No PR, no review
4. Immediate integration
```

**Best for:** Solo projects, experiments, trusted changes

---

### PR with Auto-Merge

For projects with CI but no manual review:

```
PR Auto-Merge Flow:
1. wt done
2. PR created with auto-merge enabled
3. CI runs
4. If green, PR auto-merges
5. wt close to cleanup
```

**Best for:** Solo with CI, high test coverage

---

### PR with Review

For team projects or careful changes:

```
PR Review Flow:
1. wt done
2. PR created, awaits review
3. Session stays active for fixes
4. Reviewer may request changes
5. Make fixes in same session
6. git push to update PR
7. PR approved and merged
8. wt close to cleanup
```

**Commands for fixes:**
```bash
wt toast            # Switch back
# Make requested changes
git add . && git commit -m "Address review feedback"
git push
# Ctrl-b d to return to hub
```

**Best for:** Team projects, critical changes, learning
