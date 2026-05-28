---
name: first-run-plugins
description: On first run after claudesync setup, offer to install recommended plugins
triggers:
  - CLAUDESYNC_FIRST_RUN=true in hook output
---

# First-Run Plugin Recommendations

When you detect `CLAUDESYNC_FIRST_RUN=true` in the session start output, show the user how to install recommended plugins using the `/plugin` command.

## Trigger

The `first-run-plugins.sh` hook outputs `CLAUDESYNC_FIRST_RUN=true` when the flag file exists at `~/.claude/.claudesync-first-run`.

## Action

**Always ask before installing.** Show the user the commands and let them choose whether to install or skip.

### Implementation Steps

1. **Show welcome message with plugin recommendation**:

```
Welcome to claudesync!

I recommend the **compound-engineering** plugin for advanced workflows,
code review skills, and planning tools.

**Quick install** (run these commands in terminal):
```bash
claude plugin marketplace add https://github.com/EveryInc/every-marketplace
claude plugin install compound-engineering
```

**Or use the plugin manager UI**: Run `/plugin` to browse and install interactively.

Would you like me to install it now, or skip for now?
```

2. **Use AskUserQuestion** to let user choose:
   - "Install it" - run the two CLI commands above
   - "Skip for now" - continue without installing

3. **After showing the recommendation**, delete the flag file:
   ```bash
   rm ~/.claude/.claudesync-first-run
   touch ~/.claude/.claudesync-first-run.done
   ```

## Example Interaction

```
Welcome to claudesync!

I noticed this is your first session after setup. I recommend installing
the **compound-engineering** plugin for advanced workflows and planning tools.

**Quick install** (run in terminal):
  claude plugin marketplace add https://github.com/EveryInc/every-marketplace
  claude plugin install compound-engineering

Or run `/plugin` to browse and install via the UI.

[Install it] [Skip for now]
```

## Updike MCP Servers Check

After handling the plugin recommendation, also check if the updike repository is set up:

```bash
# Check if updike repo exists
ls ~/updike/mcp-servers/social-api/src/index.ts 2>/dev/null
```

**If missing**, show:
```
The Updike MCP servers require the ~/updike repository.

Would you like me to set it up?
```

**If user agrees**, run:
```bash
git clone https://github.com/Folly-Partners/updike.git ~/updike
cd ~/updike/mcp-servers/webflow && npm install && npm run build
```

**Also check if webflow needs building** (for existing repos):
```bash
ls ~/updike/mcp-servers/webflow/dist/index.js 2>/dev/null
```

If the repo exists but webflow isn't built, offer to build it:
```bash
cd ~/updike/mcp-servers/webflow && npm install && npm run build
```

## Notes

- **Always ask first** - never install without user consent
- Only show this recommendation once (delete flag after showing)
- The `.done` file prevents showing again
- Keep it simple - just recommend compound-engineering for now
