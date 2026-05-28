# Claude Code Skill for Handoff

A Claude Code skill that guides conversation handoff to a fresh Claude session with context preserved.

## What is This?

This is a [Claude Code](https://claude.com/claude-code) skill - a markdown-based instruction set that teaches Claude AI how to properly hand off a conversation when:
- User requests a handoff
- Context is getting long
- Before ending a work session

## What Does It Provide?

- Structured summary format for preserving context
- Step-by-step handoff procedure
- Integration with `wt handoff` command
- Seamless continuation in fresh session

## Installation

### Prerequisites

1. Install wt CLI:
   ```bash
   go install github.com/badri/wt/cmd/wt@latest
   ```

2. Have [Claude Code](https://claude.com/claude-code) installed

### Install the Skill

#### Option 1: Symlink (Recommended)

```bash
# From the wt repository
cd examples/handoff-skill

# Create symlink in Claude Code skills directory
ln -s "$(pwd)" ~/.claude/skills/handoff
```

#### Option 2: Copy Files

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/handoff

# Copy the skill files
cp -r /path/to/wt/examples/handoff-skill/* ~/.claude/skills/handoff/
```

### Verify Installation

Restart Claude Code, then in a new session, type `/handoff` to invoke the skill.

## Usage

Simply type `/handoff` when you want to hand off the conversation. Claude will:

1. Generate a structured summary of the conversation
2. Execute `wt handoff -m "..."` with the summary
3. Respawn a fresh Claude session with context preserved

## Summary Format

The skill uses a structured summary format:

```
SUMMARY:
- Accomplished: [What was completed]
- Decisions: [Key decisions and rationale]
- Current state: [Where things stand]
- Blockers: [Issues discovered]
- Next steps: [What should happen next]
- Notes: [Additional context]
```

## How It Works

1. You invoke `/handoff`
2. Claude creates a summary of the conversation
3. Claude runs `wt handoff -m "summary..."`
4. `wt` writes context to `~/.config/wt/handoff.md`
5. `wt` respawns Claude with fresh process
6. New Claude reads handoff context and continues

## License

MIT License
