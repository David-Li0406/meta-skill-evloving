# Claude Code Skill for wt

A Claude Code skill that teaches Claude how to use wt (worktree session manager) effectively for orchestrating parallel development sessions from the hub.

## What is This?

This is a [Claude Code](https://claude.com/claude-code) skill - a markdown-based instruction set that teaches Claude AI how to manage wt sessions. It focuses on **hub operations** - spawning workers, monitoring progress, and completing work across multiple parallel sessions.

## What Does It Provide?

**Main skill file:**
- Hub/Worker architecture understanding
- Session lifecycle management
- When to use wt vs direct work
- Core command reference
- Common orchestration patterns

**Reference documentation:**
- `references/CLI_REFERENCE.md` - Complete command reference with all flags
- `references/WORKFLOWS.md` - Step-by-step workflows with checklists
- `references/HUB_PATTERNS.md` - Advanced hub orchestration patterns

## Why is This Useful?

The skill helps Claude understand:

1. **When to use wt** - Not every task needs isolation. The skill teaches when worktree sessions add value vs overhead.

2. **How to orchestrate** - Managing multiple workers, monitoring progress, handling idle sessions.

3. **Session lifecycle** - Spawning, monitoring, completing, and cleaning up sessions properly.

4. **Integration with beads** - How wt and bd work together for bead-driven development.

## Installation

### Prerequisites

1. Install wt CLI:
   ```bash
   go install github.com/badri/wt/cmd/wt@latest
   ```

2. Install beads CLI (wt depends on beads):
   ```bash
   curl -sSL https://raw.githubusercontent.com/steveyegge/beads/main/install.sh | bash
   ```

3. Have [Claude Code](https://claude.com/claude-code) installed

### Install the Skill

#### Option 1: Symlink (Recommended)

```bash
# From the wt repository
cd examples/claude-code-skill

# Create symlink in Claude Code skills directory
ln -s "$(pwd)" ~/.claude/skills/wt
```

#### Option 2: Copy Files

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/wt

# Copy the skill files
cp -r /path/to/wt/examples/claude-code-skill/* ~/.claude/skills/wt/
```

### Verify Installation

Restart Claude Code, then in a new session, ask:

```
Do you have the wt skill installed?
```

Claude should confirm it has access to the wt skill and can help with worktree session management.

## How It Works

Claude Code automatically loads skills from `~/.claude/skills/`. When this skill is installed:

1. Claude gets the core orchestration patterns from `SKILL.md` immediately
2. Claude can read reference docs when it needs detailed information
3. The skill uses progressive disclosure - quick reference in SKILL.md, details in references/

## Usage Examples

Once installed, Claude will automatically:

- Check for active workers at session start
- Suggest spawning workers for ready beads
- Monitor and report on worker status
- Guide you through completing and closing sessions

You can also explicitly ask Claude to use wt:

```
Spawn workers for these ready beads
```

```
Check on my active workers
```

```
Close the toast session - it's done
```

## Relationship to beads

wt is designed to work with beads (bd):

- **beads** tracks what needs to be done (issues, dependencies)
- **wt** manages isolated sessions for doing the work

The workflow:
1. `bd ready` - See what beads are ready for work
2. `wt new <bead>` - Spawn isolated worker for a bead
3. Worker completes the bead
4. `wt close` - Cleanup and close the bead

## Philosophy

**One bead = one session = one worktree**

Each worker session is:
- Isolated (own git worktree, branch, test environment)
- Persistent (survives hub session restarts)
- Focused (works on exactly one bead)

The hub orchestrates but doesn't implement. Implementation happens in workers.

## Contributing

Found ways to improve the skill? Contributions welcome!

## License

MIT License
