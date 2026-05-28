---
name: with-codex
description: Use this skill when you want to collaborate with OpenAI Codex CLI alongside Claude Code for second opinions, validation, and collaborative problem-solving.
---

# With Codex - Claude and Codex Collaboration

This skill enables collaboration between Claude Code and OpenAI Codex CLI for second opinions, validation, and collaborative problem-solving.

## CRITICAL REQUIREMENT

**Claude Code MUST be running inside a tmux session for this skill to work.**

If not in tmux, inform the user:
"このスキルを使用するには、tmuxセッション内でClaude Codeを起動する必要があります。以下のコマンドを実行してください:

```bash
tmux new-session -s claude
claude
```

## Environment Requirements

- WSL (Ubuntu) with tmux installed
- OpenAI Codex CLI installed and authenticated in WSL
- Claude Code running inside a tmux session
- Skill scripts at: `~/.claude/skills/with-codex/scripts/`

## Standard Workflow (MUST FOLLOW)

When this skill is triggered, ALWAYS execute these steps in order:

### Step 1: Setup - Split pane and start Codex

```bash
~/.claude/skills/with-codex/scripts/codex-manager.sh setup
```

This splits the current tmux pane:
- Left pane: Claude Code (current)
- Right pane: Codex CLI (newly created, with dark background)

### Step 2: Claude performs its own analysis first

Analyze the user's request independently before querying Codex.

### Step 3: Send the same prompt to Codex

```bash
~/.claude/skills/with-codex/scripts/codex-manager.sh send "YOUR_PROMPT_HERE"
```

Replace `YOUR_PROMPT_HERE` with the actual question/task from the user.

### Step 4: Wait for Codex response

```bash
~/.claude/skills/with-codex/scripts/codex-manager.sh wait 60
```

Wait up to 60 seconds for Codex to complete its response.

### Step 5: Capture Codex output

```bash
~/.claude/skills/with-codex/scripts/codex-manager.sh capture 200
```

Capture the last 200 lines of Codex's output.

### Step 6: Present combined results

Present results in this format:

```markdown
## Claude's Analysis
[Your independent analysis]

## Codex's Analysis
[Captured response from Codex]

## Synthesis
- **Agreement**: [Points where both AIs agree]
- **Differences**: [Alternative perspectives from Codex]
- **Recommendation**: [Best combined approach]
```

### Step 7: Cleanup

Perform any necessary cleanup when the conversation ends or the user requests it.