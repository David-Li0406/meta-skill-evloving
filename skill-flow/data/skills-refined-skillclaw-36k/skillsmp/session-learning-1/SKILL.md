---
name: session-learning
description: This skill should be used when the user asks about "session learning", "learn from session", "improve future sessions", "session reflection", "session metrics", "session analysis", "/session-reflect", "req learning", "learning updates", "rollback learning", or wants to understand how Claude Code can get smarter over time by learning from sessions.
git_hash: uncommitted
---

# Session Learning Guide

The session learning system helps Claude Code improve over time by analyzing your sessions and suggesting updates to memories, skills, and commands.

## Quick Start

### Enable Session Learning

Add to your `.claude/requirements.yaml` or `.claude/requirements.local.yaml`:

```yaml
hooks:
  session_learning:
    enabled: true
    prompt_on_stop: true  # Prompts for review when ending session
```

### Review a Session

```bash
/session-reflect          # Full analysis with recommendations
/session-reflect quick    # Quick summary statistics
/session-reflect analyze-only  # Analysis without applying changes
```

### Manage Learning

```bash
req learning stats        # Show learning statistics
req learning list         # List recent updates
req learning rollback 3   # Undo update #3
req learning disable      # Disable learning for this project
```

## How It Works

### 1. Data Collection

During your session, the framework collects metrics:
- **Tool usage**: Which tools you use, how often, which files
- **Requirement flow**: What gets blocked, how long to satisfy
- **Errors**: What errors occur and how they're resolved
- **Skills/Agents**: Which skills and agents you run

Metrics are stored in `.git/requirements/sessions/<session_id>.json`.

### 2. Pattern Analysis

When you run `/session-reflect`, the session-analyzer agent looks for:
- **Workflow patterns**: Common sequences, TDD cycles, etc.
- **Friction points**: High time-to-satisfy, repeated blocks
- **Knowledge gaps**: Repeated lookups, error patterns
- **Automation opportunities**: Manual steps that could be automated

### 3. Recommendations

Based on analysis, the system suggests:
- **Memory updates**: Add project conventions to Serena memories
- **Skill updates**: Improve trigger patterns
- **Command updates**: Add frequently used arguments

Each recommendation has a confidence score (0-1).

### 4. User Approval

You review and select which recommendations to apply. All changes are:
- Recorded in `.git/requirements/learning_history.json`
- Rollback-capable via `req learning rollback`
- Version-controlled (memories in `.serena/memories/`)

## Configuration Options

```yaml
hooks:
  session_learning:
    enabled: true         # Enable the learning system
    prompt_on_stop: true  # Show review prompt when session ends
    min_tool_uses: 5      # Minimum activity before prompting
    max_recommendations: 5    # Max recommendations per session
    confidence_threshold: 0.7 # Only show high-confidence items
    update_targets:
      - memories          # .serena/memories/ files
      - skills            # Plugin skill files
      - commands          # Plugin command files
```

## Example Session Flow

```
1. You work normally through a session...

2. When ending the session, Stop hook prompts:
   "Session had 47 tool uses. Review for learning?
    Run /session-reflect to analyze and improve future sessions."

3. You run /session-reflect

4. Analyzer detects patterns:
   - TDD Workflow (HIGH confidence)
   - Repeated ADR lookup (MEDIUM confidence)
   - Useful command pattern (MEDIUM confidence)

5. You select which to apply

6. Updates are written with version tracking:
   - .serena/memories/workflow-patterns.md (appended)
   - .serena/memories/frequently-referenced.md (created)

7. Next session benefits from these learnings
```

## Best Practices

1. **Run at end of productive sessions** - More data = better patterns
2. **Use `analyze-only` first** - Preview before committing
3. **Review confidence scores** - Higher = more reliable
4. **Check learning stats** - Track what's been learned over time
5. **Rollback if needed** - `req learning rollback` reverses mistakes

## Troubleshooting

### No session metrics found

```bash
# Check if metrics directory exists
ls -la .git/requirements/sessions/

# Sessions are collected automatically when framework is enabled
# Run some commands first, then try again
```

### Learning not prompting at session end

Check configuration:
```yaml
hooks:
  session_learning:
    enabled: true        # Must be true
    prompt_on_stop: true # Must be true
    min_tool_uses: 5     # Session must have at least this many tool uses
```

### Rollback not available

Some updates (like creates) don't have previous content to restore.
Use git to restore:
```bash
git checkout -- .serena/memories/filename.md
```

## Related Commands

| Command | Description |
|---------|-------------|
| `/session-reflect` | Analyze session and apply learning |
| `req learning stats` | Show learning statistics |
| `req learning list` | List recent updates |
| `req learning rollback <id>` | Undo a specific update |
| `req learning disable` | Disable learning for project |
