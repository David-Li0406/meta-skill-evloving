# Hub Orchestration Patterns

Advanced patterns for managing multiple workers from the hub session.

---

## The Hub Role

The hub is your **orchestration center**. From here you:
- Groom and prioritize beads
- Spawn and monitor workers
- Provide guidance when workers get stuck
- Complete and cleanup finished work

**Key insight:** The hub doesn't do implementation work. It coordinates work happening in workers.

---

## Pattern: Capacity-Based Spawning

Spawn workers based on available resources, not just available work.

### Resource Considerations

- **CPU/Memory:** Each worker runs Claude + potentially Docker containers
- **Port space:** Each worker uses a PORT_OFFSET (ports X5432, X3000, etc.)
- **Attention capacity:** You can only effectively monitor 3-5 workers
- **Context switches:** More workers = more interruptions

### Recommended Limits

| Scenario | Max Workers |
|----------|-------------|
| Single project, focused work | 2-3 |
| Multiple projects, monitoring | 3-5 |
| Background/overnight | 5+ (less monitoring needed) |

### Pattern

```bash
# Check current capacity
wt                          # How many running?

# Check what's ready
bd ready                    # How many available?

# Spawn up to your limit
wt new project-abc --no-switch
wt new project-xyz --no-switch
# Stop at 3-5
```

---

## Pattern: Priority-Based Triage

When you have more ready beads than worker capacity:

### Triage Criteria

1. **P0 (Critical)** - Spawn immediately
2. **P1 (High)** - Spawn if capacity allows
3. **P2 (Normal)** - Spawn when P0/P1 done
4. **Blockers** - Spawn if they unblock other work

### Pattern

```bash
# Check priorities
bd ready --priority 0       # Critical
bd ready --priority 1       # High

# Spawn critical first
wt new critical-bead-1 --no-switch
wt new critical-bead-2 --no-switch

# Then high priority if capacity
wt new high-priority-bead --no-switch
```

---

## Pattern: Round-Robin Attention

Distribute attention across workers fairly.

### Schedule

Every 30-60 minutes:
1. Run `wt` or `wt watch`
2. Check each session briefly
3. Provide guidance if stuck
4. Move to next

### Pattern

```bash
# Quick check all
wt

# Round-robin through workers
wt toast
# 2 minutes: assess, guide if needed
# Ctrl-b d

wt shadow
# 2 minutes: assess, guide if needed
# Ctrl-b d

wt obsidian
# 2 minutes: assess, guide if needed
# Ctrl-b d

# Back to hub work
```

---

## Pattern: Idle Response Strategy

Different responses based on idle duration and context.

### Idle Duration Response

| Duration | Response |
|----------|----------|
| < 5 min | Normal, probably thinking |
| 5-15 min | Check `wt watch`, may need input |
| 15-30 min | Switch and investigate |
| 30+ min | Likely stuck, needs intervention |

### Investigation Protocol

```bash
wt <name>                   # Switch to idle session

# Assess:
# - Is it waiting for user input?
# - Is it stuck on an error?
# - Is it blocked by external dependency?
# - Did it complete and just didn't signal?

# Respond accordingly:
# - Provide input if waiting
# - Guide through error if stuck
# - Update bead if blocked
# - Close if complete
```

---

## Pattern: Batch Operations

Efficient handling of multiple sessions.

### Batch Spawn

```bash
# Spawn multiple without switching
wt new bead-1 --no-switch
wt new bead-2 --no-switch
wt new bead-3 --no-switch
```

### Batch Close

```bash
# Close multiple completed sessions
wt close toast
wt close shadow
wt close obsidian
```

### Batch Kill (Emergency)

```bash
# Kill all workers (emergency cleanup)
wt kill toast
wt kill shadow
wt kill obsidian
```

---

## Pattern: Project Isolation

Keep workers separated by project when working across codebases.

### Naming Convention

Use project prefix in your mental model:
- `toast` working on `supabyoi-abc`
- `shadow` working on `reddit-saas-xyz`

### Monitoring by Project

```bash
wt ready supabyoi           # Ready beads for supabyoi
wt ready reddit-saas        # Ready beads for reddit-saas

wt                          # Shows project column
```

---

## Pattern: Handoff Between Hub Sessions

Hub sessions may restart (compaction, new terminal). Workers persist.

### Before Hub Restart

```bash
wt                          # Note active workers
# Workers will continue in tmux
```

### After Hub Restart

```bash
# First thing: check workers
wt                          # They're still running

# Check for issues
wt watch                    # Any idle or error?

# Continue orchestration
```

**Key insight:** Workers don't need the hub running. They operate independently in tmux.

---

## Pattern: Escalation Ladder

When a worker can't progress:

### Level 1: Guidance
```bash
wt <name>
# Provide direction, clarify requirements
# Ctrl-b d
```

### Level 2: Unblock
```bash
wt <name>
# Help resolve specific technical blocker
# Maybe run commands, check logs
# Ctrl-b d
```

### Level 3: Reset
```bash
wt kill <name>
bd update <bead> --notes "Resetting: previous approach didn't work"
wt new <bead>
```

### Level 4: Defer
```bash
wt kill <name>
bd update <bead> --status blocked --notes "Waiting for X"
# Work on other beads
```

---

## Pattern: Seance for Context

Use seance to query past sessions for decisions.

### Before Starting Related Work

```bash
# Check what previous sessions learned
wt seance toast -p "What did you try for the auth flow?"
wt seance shadow -p "Why did you choose that approach?"

# Apply learnings to new worker
wt new related-bead
```

### After Unexpected Results

```bash
# Query the session that produced the result
wt seance obsidian -p "Why did you implement it this way?"
```

---

## Pattern: Overnight Workers

Spawning workers that run without supervision.

### Setup

```bash
# Spawn workers for independent work
wt new independent-task-1 --no-switch
wt new independent-task-2 --no-switch

# These should be:
# - Well-defined beads with clear acceptance criteria
# - No external dependencies
# - Unlikely to need human input
```

### Morning Review

```bash
wt                          # Check status
wt watch                    # Any issues?

# Check completed work
wt <name>                   # Review what was done
wt close <name>             # If good, complete it
```

---

## Anti-Patterns

### Don't: Over-spawn

**Problem:** Spawning 10+ workers you can't monitor

**Solution:** Limit to 3-5 active workers

### Don't: Ignore Idle

**Problem:** Leaving workers idle for hours

**Solution:** Regular monitoring, respond within 30 minutes

### Don't: Hub Implementation

**Problem:** Doing implementation work in the hub

**Solution:** Spawn a worker for implementation, keep hub for orchestration

### Don't: Forget to Close

**Problem:** Accumulating finished but unclosed sessions

**Solution:** Close sessions promptly when work is done

### Don't: Skip Seance

**Problem:** Restarting work without checking what past sessions learned

**Solution:** Query seance before related work
