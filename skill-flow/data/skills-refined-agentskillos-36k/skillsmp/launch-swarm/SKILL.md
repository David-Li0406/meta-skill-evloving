---
name: launch-swarm
description: Launch a parallel agent swarm to work on beads with a specific label. Spawns agents with correct model, sends bead_swarm template, and confirms execution.
---

> **DEPRECATED:** Use `/swarm-orchestrator` and `pnpm swarm` instead. See `docs/guides/planning-lifecycle.md` for the updated workflow.

# Launch Swarm

Launch multiple Claude Code agents in tmux panes to work on beads in parallel.

## When to use

Use after:
1. `/write-beads` has created the BEADS.md file
2. `/bead-review` has verified the beads
3. `/create-beads` has imported beads into bd

## Prerequisites

- `ntm` (NeoTmux Manager) installed and configured
- Beads exist in bd with the specified label
- At least one bead is in `ready` status (no blockers)

## Workflow

### Step 1: Verify beads are ready

```bash
# Check beads exist with the label
bd list -l <label> --json | jq 'length'

# Check how many are ready (no blocking dependencies)
bd ready -l <label> --json | jq 'length'
```

If no beads are ready, abort - dependencies need to be resolved first.

### Step 2: Kill existing session if present

```bash
tmux kill-session -t mindhive 2>/dev/null || true
```

### Step 3: Spawn agents with correct model

**IMPORTANT:** Always use full model names, not short aliases.

```bash
# Spawn 4 Sonnet 4.5 agents (recommended for most work)
ntm spawn mindhive --cc=4:claude-sonnet-4-5-20250929 --no-user
```

**Note on `--no-user`:** By default, `ntm spawn` creates a user pane (pane 1) plus agent panes. This user pane is a plain shell, not an agent. Using `--no-user` skips the user pane so all panes are agents. This is recommended for swarms because:
- `ntm send --all` won't accidentally send prompts to a shell
- Pane numbering is simpler (all panes are agents)
- No wasted tmux real estate

For complex architectural work, use Opus:
```bash
# Mixed team: 2 Sonnet + 1 Opus
ntm spawn mindhive --cc=2:claude-sonnet-4-5-20250929 --cc=1:claude-opus-4-20250514 --no-user
```

### Model Names Reference

| Model | Full Name | Use Case |
|-------|-----------|----------|
| Sonnet 4.5 | `claude-sonnet-4-5-20250929` | General purpose, fast (recommended) |
| Opus 4.5 | `claude-opus-4-20250514` | Complex reasoning, architecture |

**Warning:** Short aliases (`sonnet`, `opus`) may resolve to older model versions. Always use full model names.

### Step 4: Send bead_swarm template to all panes

```bash
ntm send mindhive --all -t bead_swarm --var label=<label>
```

This sends the bead_swarm template to every agent pane.

### Step 5: Confirm execution in each pane

The template is too long for automatic execution. Press ENTER in each pane:

```bash
# If using --no-user, send to ALL panes (no user pane to skip)
for pane in $(tmux list-panes -t mindhive -F '#{pane_index}'); do
  tmux send-keys -t "mindhive.$pane" Enter
  sleep 0.5
done

# If NOT using --no-user, skip the first pane (user shell)
for pane in $(tmux list-panes -t mindhive -F '#{pane_index}' | tail -n +2); do
  tmux send-keys -t "mindhive.$pane" Enter
  sleep 0.5
done
```

### Step 6: Provide monitoring commands

Output these commands for the user:

```bash
# Watch bead progress
bd list -l <label> --json | jq 'group_by(.status) | map({status: .[0].status, count: length})'

# Check agent activity
ntm activity mindhive

# View specific pane
tmux select-pane -t mindhive.<pane_number>

# Request checkpoint (all agents report status)
ntm mail send mindhive --all "CHECKPOINT: Report your current bead and status"
```

## Error Handling

### "No beads found with label X"
Check the label is correct:
```bash
bd list --json | jq -r '.[].labels[]?' | sort -u
```

### Panes not executing
If agents don't start working, manually check each pane:
- Pane might need ENTER pressed
- Claude Code might not be installed
- Pane might have an error

## Example Session

```
User: /launch-swarm slack-integration

Agent: I'll launch a swarm to work on slack-integration beads.

Step 1: Checking beads...
$ bd list -l slack-integration --json | jq 'length'
19 beads found

$ bd ready -l slack-integration --json | jq 'length'  
5 beads ready to work

Step 2: Killing existing session...
$ tmux kill-session -t mindhive 2>/dev/null || true

Step 3: Spawning agents...
$ ntm spawn mindhive --cc=4:claude-sonnet-4-5-20250929 --no-user
Creating session 'mindhive'... [OK]
Creating 4 pane(s)... [OK]
Launching 4 agent(s)... [OK]

Step 4: Sending template...
$ ntm send mindhive --all -t bead_swarm --var label=slack-integration
Sent to 4 panes

Step 5: Confirming execution...
$ for pane in $(tmux list-panes -t mindhive -F '#{pane_index}'); do
    tmux send-keys -t "mindhive.$pane" Enter
    sleep 0.5
  done
Enter sent to agent panes

Swarm launched! 4 Sonnet 4.5 agents working on 5 ready beads.

Monitor with:
  bd list -l slack-integration --json | jq 'group_by(.status) | map({status: .[0].status, count: length})'
  ntm activity mindhive
```

## Intervention Commands

```bash
# Stop all agents
ntm interrupt mindhive

# Send new instructions to all
ntm mail send mindhive --all "PRIORITY: Stop current work and focus on SCHEMA-01"

# Send to specific pane
ntm send mindhive --pane=2 "Switch to bead mindhive-xyz"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| label | Yes | - | Bead label to filter work |
| agents | No | 4 | Number of agents to spawn |
| model | No | claude-sonnet-4-5-20250929 | Model to use (full name) |
| session | No | mindhive | Tmux session name |

## Related Commands

- `/write-beads` - Create BEADS.md from TDD
- `/create-beads` - Import BEADS.md into bd
- `/bead-review` - QA review of beads

## Reference

See `.ntm/workflows/README.md` for complete documentation on swarm workflows.
