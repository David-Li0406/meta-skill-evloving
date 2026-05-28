# Lane: Recovery

Detailed reference for the Recovery lane in Kyora Agent OS. This lane handles continuation of unfinished work in a new session.

## Entry Conditions

Start in Recovery when:

- A new session continues an unfinished task
- Previous session ended mid-task (token/time limit)
- Partial completion exists in the repo

## Why Recovery Exists

New sessions suffer from "session amnesia" — the agent loses context about:

- What was the original objective
- What's already done vs what remains
- What assumptions were made
- What gates are pending

Recovery lane reconstructs this context before continuing.

## Owner

- **Primary**: Orchestrator (for routing) or previous lane owner
- **Supporting**: Previous implementer (via handoff packet)

## Outputs (Required)

**Recovery/Resume Packet** — This is MANDATORY before continuing any implementation.

## Definition of Done

- Objective reconstructed from available evidence
- Current state identified (done vs remaining)
- Next smallest verifiable step is clear
- Any pending gates re-confirmed

## Recovery Protocol (Step-by-Step)

### Step 1: Reconstruct Objective

Sources to check (in order):

1. Previous handoff packets (if any)
2. Recent git commits/changes
3. TODO.md or plan files
4. Test outputs (what passed/failed)
5. User prompt history (if available)

### Step 2: Identify What's Done

Check:

- `git status` / `git diff` — uncommitted changes
- `git log --oneline -10` — recent commits
- Test results — what's passing now
- Build status — is it currently broken

### Step 3: Identify What Remains

From the original task packet or plan:

- List remaining phases/steps
- Note any blockers or failing tests
- Identify pending PO gates

### Step 4: Re-Assert Context

Before continuing:

- Confirm acceptance criteria still apply
- Verify no external changes invalidated prior work
- Check if SSOT instructions have changed

### Step 5: Continue with Next Smallest Step

- Start with the smallest verifiable action
- Run validation after the step
- Create a phase handoff packet when phase completes

## Tool Allowlist

| Tool | When to Use |
|------|-------------|
| `read` | Read plan files, handoff packets |
| `search` | Find related code changes |
| `get_changed_files` | See uncommitted changes |
| `run_in_terminal` | Run `git log`, `git status`, test commands |

**Note**: Recovery is primarily read + git inspection. Edit only after packet is created.

## Output Format: Recovery Packet

```
RECOVERY PACKET

Goal (1 sentence):
-

Last known lane:
-

What's already done (based on git changes/tests):
-

What's broken / failing (if any):
-

Next smallest verifiable step:
-

Commands to run first:
-

Pending PO gates:
-

Assumptions to re-confirm:
-
```

## Common Failure Modes

| Failure | Prevention |
|---------|------------|
| Jumping straight to implementation | ALWAYS create Recovery Packet first |
| Wrong assumptions about prior state | Verify with git and tests |
| Missing context from previous session | Check all evidence sources |
| Skipping re-confirmation | Verify acceptance criteria still valid |
| Fixing unrelated issues | Stay focused on original objective |

## Validation Commands

Run these first to understand current state:

```bash
# Check git state
git status
git log --oneline -10
git diff --stat

# Check build state
make test.quick       # Backend unit tests
make portal.check     # Portal lint/typecheck

# If portal, check for errors
make portal.build
```

## When to Escalate

Escalate to PO if:

- Original objective is unclear even after reconstruction
- Significant external changes invalidated prior work
- Pending gates cannot be resolved
- Unfinished work may conflict with newer changes
