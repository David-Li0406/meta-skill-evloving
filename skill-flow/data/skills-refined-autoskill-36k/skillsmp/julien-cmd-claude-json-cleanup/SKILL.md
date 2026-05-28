---
name: julien-cmd-claude-json-cleanup
description: "Clean up oversized ~/.claude.json file to prevent token limit errors. Use when Read tool fails with 'exceeds maximum allowed tokens' or to maintain Claude config performance."
license: Apache-2.0
metadata:
  author: "Julien"
  version: "1.0.0"
  category: "maintenance"
  last_updated: "2026-01"
triggers:
  # Keywords
  - "claude.json"
  - "claude json"
  - "token limit"
  # Action phrases
  - "cleanup claude"
  - "nettoyer claude"
  - "clean config"
  - "reduce config size"
  - "claude config cleanup"
  - "settings cleanup"
  - "shrink claude config"
  - "réduire la taille de claude"
  # Problem phrases
  - "exceeds maximum"
  - "file too large"
  - "fichier trop gros"
  - "claude.json trop gros"
  - "can't read claude.json"
  - "token limit exceeded"
  - "25000 tokens"
  - "config file too big"
---

# Claude JSON Cleanup

Manage and clean up oversized `~/.claude.json` configuration files.

## Observability

**First**: Display activation message:
```
🔧 Skill "julien-cmd-claude-json-cleanup" activated
```

## Problem

The `~/.claude.json` file stores Claude Code configuration including:
- Project settings per directory
- MCP server configurations
- Conversation memory references
- Session data

Over time, this file can exceed the 25,000 token limit, causing errors like:
```
Error: File content (26095 tokens) exceeds maximum allowed tokens (25000)
```

## Quick Command

Run the cleanup script:

```bash
node ~/.claude/scripts/cleanup-claude-json.js
```

Or from marketplace:

```bash
node "$HOME/OneDrive/Coding/_Projets de code/2025.11 Claude Code MarketPlace/skills/julien-cmd-claude-json-cleanup/scripts/cleanup-claude-json.js"
```

## What It Does

The script automatically:
1. **Creates backup** → `~/.claude.json.backup`
2. **Removes stale projects** → Entries for deleted directories
3. **Cleans github paths** → Non-existent repo references
4. **Reports savings** → Before/after size and token estimates

## Manual Analysis

If you need to investigate further:

```bash
# Check file size
wc -c ~/.claude.json

# Analyze sections by size
node -e "
const fs = require('fs');
const os = require('os');
const d = JSON.parse(fs.readFileSync(os.homedir() + '/.claude.json'));
Object.entries(d).forEach(([k, v]) => {
    const size = JSON.stringify(v).length;
    const type = Array.isArray(v) ? 'array' : typeof v;
    if (type === 'object') console.log(k + ': ' + Object.keys(v).length + ' entries (' + size + ' bytes)');
    else if (type === 'array') console.log(k + ': ' + v.length + ' items (' + size + ' bytes)');
});
"
```

## Restoring Backup

If something goes wrong:

```bash
cp ~/.claude.json.backup ~/.claude.json
```

## Troubleshooting

### Script fails with "ENOENT"
```bash
# File doesn't exist - this is normal for fresh installs
ls ~/.claude.json || echo "No config file yet"
```

### Script fails with "EACCES"
```bash
# Permission issue - check file ownership
ls -la ~/.claude.json
# Fix permissions if needed
chmod 644 ~/.claude.json
```

### File still too large after cleanup
If projects are all valid but file is still > 25,000 tokens:
1. Check `mcpServers` section - remove unused servers
2. Check `skillUsage` section - can be cleared safely
3. Consider moving rarely-used MCP configs to `.mcp.json` per-project

### Restore from backup
```bash
cp ~/.claude.json.backup ~/.claude.json
```

## Prevention

Add to your workflow:
1. Run cleanup monthly
2. Keep project list tidy (remove old projects)
3. Use `.mcp.json` per-project instead of global MCP configs

## Skill Chaining

### Skills Required Before
- None

### Input Expected
- None (operates on ~/.claude.json)

### Output Produced
- **Format**: Cleaned ~/.claude.json, console report
- **Side effects**:
  - Creates backup: ~/.claude.json.backup
- **Duration**: < 5 seconds

### Compatible Skills After
- None (standalone maintenance task)

### Called By
- Direct invocation when token limit error occurs
- Periodic maintenance

### Tools Used
- `Bash` (usage: run node script)
