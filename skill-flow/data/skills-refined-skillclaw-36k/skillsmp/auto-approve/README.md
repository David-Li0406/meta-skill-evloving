# Auto-Approve

A PermissionRequest hook for Claude Code that uses Haiku to auto-approve routine operations.

## The Problem

Claude Code asks for permission frequently. You either:
- Click "approve" repeatedly (breaks flow)
- Use dangerous skip-permissions flags (unsafe)

## The Solution

Auto-approve uses Haiku as a security reviewer. It:
- Instantly approves safe, read-only tools
- Instantly approves patterns you've configured
- Asks Haiku about everything else
- Caches approvals permanently
- **Never auto-denies** - you always have final say

## Installation

1. Install the skill:
```bash
npx skills add jakehower/agent-toolkit/skills/auto-approve
```

2. Run the skill to set up the hook:
```
/auto-approve
```

## Usage

After installation, the hook runs automatically on every permission request.

### Managing Config

Run `/auto-approve` anytime to:
- View current configuration
- Add patterns to always allow or always ask
- Review audit log and suggested patterns
- Clear cache
- Update or uninstall

### Config Files

| File | Purpose |
|------|---------|
| `~/.claude/auto-approve/config.md` | Global settings |
| `.claude/auto-approve.md` | Project-specific settings |

### Example Config

```markdown
## Safe Tools
- Read
- Glob
- Grep

## Always Allow
- npm test
- git push origin feature-

## Always Ask
- rm -rf
- git push origin main

## Custom Rules
- Always approve writes to src/ and test/
```

## How It Works

```
Permission Request
       |
       v
  Safe Tool? ----yes----> ALLOW
       |
       no
       v
  Always Allow? ----yes----> ALLOW
       |
       no
       v
  Always Ask? ----yes----> ASK USER
       |
       no
       v
  Cached? ----yes----> ALLOW
       |
       no
       v
  Ask Haiku
       |
       +--> approve --> ALLOW (cache it)
       |
       +--> ask/unsure --> ASK USER
```

### Pattern Matching

- **Safe Tools**: Exact match on tool name (e.g., `Read`, `Glob`)
- **Always Allow/Ask**: Substring match on `tool_name:tool_input` (e.g., `npm test` matches any Bash command containing "npm test")
- **Custom Rules**: Passed to Haiku as additional context for decisions

## Requirements

- Claude Code CLI (`claude` command)
- `jq` for JSON parsing
- `curl` for updates

## License

MIT
