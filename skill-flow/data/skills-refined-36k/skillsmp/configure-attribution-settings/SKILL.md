---
name: Configure Attribution Settings
description: This skill should be used when the user asks to "change the commit attribution", "remove the co-authored by", "stop adding the co-authored by", "change Claude's name", "configure the PR attribution", "update attribution settings", "show that Claude is helping write commits", or "reset co-authored by settings". Manages git commit and pull request attribution in Claude Code settings.
version: 0.1.0
---

# Configure Attribution Settings

## Purpose

Manage Claude Code's attribution settings for git commits and pull requests. Configure the `Co-Authored-By` git trailer and PR description attribution in `.claude/settings.local.json`. Handle customization of Claude's name, model information, and complete removal of attribution while preserving other settings.

## When to Use

Activate when users want to:
- Change Claude's name in commit attribution
- Add or remove model information from attribution
- Customize PR description attribution
- Remove attribution entirely
- Reset attribution to defaults

## Configuration Workflow

Follow this safe, confirmable workflow for all attribution changes:

### 1. Understand User Intent

Parse the user's request to determine:
- **Name changes**: "Change Claude's name to X" → Update name in attribution
- **Remove attribution**: "Remove co-authored by", "stop adding attribution" → Clear attribution
- **PR attribution**: "Change PR attribution to X" → Update PR description
- **Model information**: Mentions of model version → Ask if they want to include/exclude it
- **Partial updates**: Only commit or only PR mentioned → Preserve the other

### 2. Read Existing Configuration

Always check current settings before making changes:

```bash
# Check if .claude directory exists
if [ ! -d ".claude" ]; then
    mkdir -p .claude
fi

# Read existing settings if present
if [ -f ".claude/settings.local.json" ]; then
    cat .claude/settings.local.json
fi
```

Extract current attribution values if they exist:
```bash
# Get current commit attribution
CURRENT_COMMIT=$(jq -r '.attribution.commit // empty' .claude/settings.local.json 2>/dev/null)

# Get current PR attribution
CURRENT_PR=$(jq -r '.attribution.pr // empty' .claude/settings.local.json 2>/dev/null)
```

### 3. Create Backup

Before any modifications, create backup with `.backup` extension:

```bash
if [ -f ".claude/settings.local.json" ]; then
    cp .claude/settings.local.json .claude/settings.local.json.backup
fi
```

### 4. Validate Existing File

If settings file exists, verify it contains valid JSON:

```bash
if [ -f ".claude/settings.local.json" ]; then
    if ! jq empty .claude/settings.local.json 2>/dev/null; then
        echo "ERROR: .claude/settings.local.json contains invalid JSON"
        exit 1
    fi
fi
```

**On validation failure**: Abort and ask user to fix the malformed JSON before proceeding.

### 5. Handle Name Changes

When user requests name changes, determine model handling:

**User says:** "Change Claude's name to Big Dawg"

**Ask user:**
```
I'll update Claude's name to "Big Dawg" in the commit attribution.

Do you want to:
1. Keep the model name (e.g., "Big Dawg Sonnet 4.5")
2. Remove the model name (e.g., "Big Dawg")

What would you prefer?
```

**Parse existing format** to understand current structure:
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
                [NAME] [MODEL]      [EMAIL]
```

**Preserve email address** unless user explicitly requests changing it.

### 6. Handle Removal Requests

When user requests removing attribution, confirm scope:

**User says:** "Remove the co-authored by"

**If user specified only commit attribution:**
```
I'll remove the commit attribution. Do you also want me to remove the PR attribution?

Current PR attribution: "🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

**Wait for user response** before proceeding.

**If user says remove both or confirms:**
- Set `commit` to `""`
- Set `pr` to `""`

**If user says keep PR attribution:**
- Set `commit` to `""`
- Preserve existing `pr` value

### 7. Build New Configuration

Create the new attribution configuration based on user request:

**Preserve other settings**: Only modify the `attribution` object, preserve everything else.

**Example merge logic:**
```bash
# Read existing settings or create empty object
EXISTING=$(cat .claude/settings.local.json 2>/dev/null || echo '{}')

# Merge with new attribution (example: change name)
echo "$EXISTING" | jq '. + {
  "attribution": {
    "commit": "Co-Authored-By: Big Dawg Sonnet 4.5 <noreply@anthropic.com>",
    "pr": (.attribution.pr // "🤖 Generated with [Claude Code](https://claude.com/claude-code)")
  }
}' > .claude/settings.local.json
```

**Critical**: When updating one field (commit or pr), explicitly preserve the other using `(.attribution.commit // "default")` or `(.attribution.pr // "default")`.

### 8. Write New Configuration

Write the updated `.claude/settings.local.json`:

```bash
# If settings doesn't exist, create it
if [ ! -f ".claude/settings.local.json" ]; then
    echo '{}' > .claude/settings.local.json
fi

# Use jq to merge attribution settings
jq '. + {
  "attribution": {
    "commit": "...",
    "pr": "..."
  }
}' .claude/settings.local.json > .claude/settings.local.json.tmp
mv .claude/settings.local.json.tmp .claude/settings.local.json
```

### 9. Confirm with User

After writing new configuration, show what changed:

```
I've updated your attribution settings:

Commit attribution:
OLD: Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
NEW: Co-Authored-By: Big Dawg <noreply@anthropic.com>

PR attribution: (unchanged)
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Do the changes work as expected?
```

### 10. Cleanup Based on Response

**If user confirms changes work:**
```bash
rm -f .claude/settings.local.json.backup
```

**If user says changes don't work or wants to revert:**
```bash
if [ -f ".claude/settings.local.json.backup" ]; then
    mv .claude/settings.local.json.backup .claude/settings.local.json
fi
rm -f .claude/settings.local.json.backup
```

**Always ensure backup file is removed** regardless of outcome.

## Attribution Format Reference

### Commit Attribution

Git commit attribution uses git trailers format:

**Standard format:**
```
Co-Authored-By: Name <email@example.com>
```

**With model:**
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Custom name:**
```
Co-Authored-By: Big Dawg <noreply@anthropic.com>
```

**With custom message:**
```
Generated with AI

Co-Authored-By: AI Assistant <ai@example.com>
```

**Empty (no attribution):**
```
""
```

**Notes:**
- Can include multiple lines
- First lines can be custom text
- Trailer lines follow git-interpret-trailers format
- Empty string hides commit attribution entirely

### PR Attribution

Pull request attribution is plain text in PR descriptions:

**Standard format:**
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Custom message:**
```
🤖 Generated with ✨ Style ✨ and [Big Dawg](https://claude.com/claude-code)
```

**Simple text:**
```
Created with Claude Code
```

**Empty (no attribution):**
```
""
```

**Notes:**
- Supports markdown formatting
- Can include emojis, links, etc.
- Empty string hides PR attribution entirely

## Parsing User Requests

### Common Request Patterns

**Name changes:**
- "Change Claude's name to Big Dawg" → Update name, ask about model
- "Remove the model from Co-Authored-By" → Keep name, remove model portion
- "Change Claude's name to match the commit attribution" → Extract name from commit, use in PR

**Attribution removal:**
- "Remove co-authored by" → Confirm if both commit and PR should be removed
- "Stop adding the co-authored by" → Same as above
- "Remove commit attribution" → Clear commit, confirm about PR
- "Remove PR attribution" → Clear PR, preserve commit

**Customization:**
- "Change the PR attribution to say it's generated with style" → Update PR text
- "Update Claude's name to Big Dawg in the Co-Authored-By" → Name change with model question
- "Show that Claude is helping write these commits" → Ensure attribution is visible

**Partial updates:**
- If user only mentions commit → Preserve PR attribution
- If user only mentions PR → Preserve commit attribution
- Always confirm scope when removing attribution

### Validation Logic

Before writing configuration, validate:

1. **Email format**: If custom email provided, verify it's valid format
2. **Trailer format**: Commit attribution with trailers must follow git format
3. **JSON validity**: Ensure resulting JSON is valid
4. **Preservation check**: Verify other settings aren't accidentally removed

**On validation failure**: Inform user of issue and suggest corrections.

## Preserving Existing Settings

Critical principle: **Only modify attribution object, preserve everything else.**

### Settings.local.json Preservation

When updating `.claude/settings.local.json`:
- Only modify the `attribution` object
- Preserve all other keys (`statusLine`, `model`, `hooks`, etc.)
- When updating only `commit`, preserve existing `pr`
- When updating only `pr`, preserve existing `commit`
- Use jq to merge rather than overwrite

**Example merging logic (update commit only):**
```bash
jq --arg newCommit "Co-Authored-By: Big Dawg <noreply@anthropic.com>" \
   '. + {
     "attribution": {
       "commit": $newCommit,
       "pr": (.attribution.pr // "🤖 Generated with [Claude Code](https://claude.com/claude-code)")
     }
   }' .claude/settings.local.json
```

### Attribution Field Preservation

When user updates one field:
- Updating commit → Preserve PR (use existing value or default)
- Updating PR → Preserve commit (use existing value or default)
- Both specified → Update both

**Default values if field doesn't exist:**
- Commit: `"Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"`
- PR: `"🤖 Generated with [Claude Code](https://claude.com/claude-code)"`

## Examples

See `examples/` directory for complete working examples:
- **`examples/name-change.json`** - Changing Claude's name
- **`examples/remove-model.json`** - Removing model from attribution
- **`examples/custom-pr.json`** - Custom PR attribution
- **`examples/remove-all.json`** - Removing all attribution
- **`examples/partial-update.json`** - Updating only one field

## Additional Resources

### Reference Files

For detailed information:
- **`references/attribution-formats.md`** - Complete attribution format guide

## Error Handling

### Directory Creation
If `.claude/` doesn't exist, create it automatically:
```bash
mkdir -p .claude
```

### File Creation
If settings file doesn't exist, create with empty object:
```bash
echo '{}' > .claude/settings.local.json
```

### Malformed JSON
If existing file contains invalid JSON:
1. Detect using `jq empty`
2. Abort the operation
3. Ask user to fix JSON manually before proceeding
4. Do NOT attempt automatic fixes

### Backup Recovery
If user wants to revert:
1. Restore from backup
2. Remove backup file
3. Confirm restoration complete

### User Confirmation
When removing attribution:
1. Always confirm scope (commit only, PR only, or both)
2. Show current values being removed
3. Wait for explicit confirmation before proceeding

## Notes

- Attribution settings take effect on next commit or PR creation
- Empty strings (`""`) completely hide attribution
- Git trailers appear at end of commit message
- PR attribution appears in PR description
- Use jq for all JSON operations to ensure validity
- Always preserve settings the user didn't explicitly request to change
- When in doubt about model inclusion, ask the user
- Backup workflow provides safety without cluttering workspace
