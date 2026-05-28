---
name: TmuxSubagentCreation
description: Create Claude Code subagents via tmux automation of the /agents TUI command. USE WHEN tmux subagent, tmux agent, /agents automation, automated agent creation via TUI, spawn subagent via tmux.
---

# TmuxSubagentCreation

Create Claude Code subagents via tmux automation of the /agents TUI command

---

# TmuxSubagentCreation

Create Claude Code subagents programmatically by automating the interactive `/agents` TUI via tmux.

## When to Use

- Need to create a subagent without manual TUI interaction
- Want to use Claude's "Generate with Claude" feature programmatically
- Building agents that need their own skills preloaded

## Prerequisites

- `tmux` installed (`brew install tmux` if needed)
- `claude` CLI available

## Step-by-Step Process

### 1. Start Claude Code in tmux

```bash
# Kill any existing session
tmux kill-session -t cc 2>/dev/null || true

# Start new detached session with Claude Code
tmux new-session -d -s cc -x 120 -y 30 'claude'

# Wait for startup
sleep 4

# Verify it started
tmux capture-pane -t cc -p
```

### 2. Navigate to /agents

```bash
# Type the command
tmux send-keys -t cc '/agents' Enter

# Wait for menu to load
sleep 2

# Capture screen to verify
tmux capture-pane -t cc -p
```

### 3. Select "Create new agent"

```bash
# Press Enter (already highlighted)
tmux send-keys -t cc Enter
sleep 2
```

### 4. Choose Location

```bash
# Options: Project (.claude/agents/) or Personal (~/.claude/agents/)
# Use Down arrow to navigate, Enter to select
tmux send-keys -t cc Down Enter  # Select Personal
sleep 2
```

### 5. Choose Creation Method

```bash
# Select "Generate with Claude (recommended)"
tmux send-keys -t cc Enter
sleep 2
```

### 6. Enter Agent Description

```bash
# Type comprehensive description
DESCRIPTION="Your detailed agent description here..."
tmux send-keys -t cc "$DESCRIPTION"
tmux send-keys -t cc Enter

# Wait for generation (can take 10-20 seconds)
sleep 15
```

### 7. Configure Tools, Model, Color

```bash
# Tools - Enter to continue with defaults (all tools)
tmux send-keys -t cc Enter
sleep 2

# Model - Enter for Sonnet (recommended)
tmux send-keys -t cc Enter
sleep 2

# Color - Enter for automatic
tmux send-keys -t cc Enter
sleep 2
```

### 8. Save the Agent

```bash
# Press Enter or 's' to save
tmux send-keys -t cc Enter
sleep 2

# Verify creation
tmux capture-pane -t cc -p
```

### 9. Cleanup

```bash
# Exit agents menu
tmux send-keys -t cc Escape
sleep 1

# Exit claude
tmux send-keys -t cc '/exit' Enter
sleep 2

# Kill session
tmux kill-session -t cc
```

## Adding Skills to Subagents

Subagents can have skills preloaded via the `skills` YAML frontmatter field:

```yaml
---
name: my-agent
description: Agent description
model: sonnet
skills:
  - SkillName
  - AnotherSkill
---

System prompt here...
```

Skills are injected into the subagent's context at startup. Subagents do NOT inherit parent skills - list them explicitly.

## Creating Skills for Subagents

If the subagent needs a custom skill, spawn the skill-writer agent:

```
Task(
  subagent_type: "skill-writer",
  description: "Create skill for subagent",
  prompt: "operation: create
name: SkillName
summary: What it does
triggers: trigger1, trigger2
content: |
  Full skill content here..."
)
```

Then reference it in the subagent's frontmatter.

## Key tmux Commands Reference

| Command | Purpose |
|---------|---------|
| `tmux send-keys -t cc 'text' Enter` | Type text and press enter |
| `tmux send-keys -t cc Enter` | Press enter |
| `tmux send-keys -t cc Escape` | Press escape |
| `tmux send-keys -t cc Down` | Arrow down |
| `tmux send-keys -t cc Up` | Arrow up |
| `tmux send-keys -t cc Tab` | Press tab |
| `tmux capture-pane -t cc -p` | Read current screen |

## Troubleshooting

**Agent saved to wrong location**: Check working directory. If Claude started in `~/.claude`, a "project" agent saves to `~/.claude/.claude/agents/`. Move file to correct location:
```bash
mv ~/.claude/.claude/agents/agent-name.md ~/.claude/agents/
```

**Screen capture shows nothing**: Increase sleep times - Claude Code may need more time to start or respond.

**Generation takes too long**: The "Generate with Claude" feature can take 15-30 seconds. Use longer sleep after description submission.

