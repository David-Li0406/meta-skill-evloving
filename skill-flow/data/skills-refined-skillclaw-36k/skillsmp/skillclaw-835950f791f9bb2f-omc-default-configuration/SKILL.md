---
name: omc-default-configuration
description: Use this skill to configure OMC either locally for a specific project or globally for all projects.
---

# OMC Default Configuration

## Task: Configure OMC Default Mode (Local or Global)

**CRITICAL**: This skill ALWAYS downloads fresh CLAUDE.md from GitHub to your specified configuration. DO NOT use the Write tool - use bash curl exclusively.

### Step 1: Determine Configuration Scope

Decide whether you want to configure OMC for a **local project** or **globally**. 

- For **local project**: Use `.claude/CLAUDE.md`
- For **global configuration**: Use `~/.claude/CLAUDE.md`

### Step 2: Create Directory (if Local)

If configuring locally, ensure the local project has a `.claude` directory:

```bash
# Create .claude directory in current project
mkdir -p .claude && echo "✅ .claude directory created" || echo "❌ Failed to create .claude directory"
```

### Step 3: Download Fresh CLAUDE.md (MANDATORY)

Execute the appropriate bash command to download fresh CLAUDE.md:

- For **local project**:

```bash
# Download fresh CLAUDE.md to project-local .claude/
curl -fsSL "https://raw.githubusercontent.com/Yeachan-Heo/oh-my-claudecode/main/docs/CLAUDE.md" -o .claude/CLAUDE.md && \
echo "✅ CLAUDE.md downloaded successfully to .claude/CLAUDE.md" || \
echo "❌ Failed to download CLAUDE.md"
```

- For **global configuration**:

```bash
# Remove existing CLAUDE.md and download fresh from GitHub
rm -f ~/.claude/CLAUDE.md && \
curl -fsSL "https://raw.githubusercontent.com/Yeachan-Heo/oh-my-claudecode/main/docs/CLAUDE.md" -o ~/.claude/CLAUDE.md && \
echo "✅ CLAUDE.md downloaded successfully to ~/.claude/CLAUDE.md" || \
echo "❌ Failed to download CLAUDE.md"
```

**FALLBACK** if curl fails:
Tell user to manually download from:
https://raw.githubusercontent.com/Yeachan-Heo/oh-my-claudecode/main/docs/CLAUDE.md

### Step 4: Clean Up Legacy Hooks (if Global)

If configuring globally, check if old manual hooks exist and remove them to prevent duplicates:

```bash
# Remove legacy bash hook scripts (now handled by plugin system)
rm -f ~/.claude/hooks/keyword-detector.sh
rm -f ~/.claude/hooks/stop-continuation.sh
rm -f ~/.claude/hooks/persistent-mode.sh
rm -f ~/.claude/hooks/session-start.sh
```

Check `~/.claude/settings.json` for manual hook entries. If the "hooks" key exists with UserPromptSubmit, Stop, or SessionStart entries pointing to bash scripts, inform the user:

> **Note**: Found legacy hooks in settings.json. These should be removed since the plugin now provides hooks automatically. Remove the "hooks" section from ~/.claude/settings.json to prevent duplicate hook execution.

### Step 5: Verify Plugin Installation

The oh-my-claudecode plugin provides all hooks automatically via the plugin system. Verify the plugin is enabled:

```bash
grep -q "oh-my-claudecode" ~/.claude/settings.json && echo "Plugin enabled" || echo "Plugin NOT enabled"
```

If the plugin is not enabled, instruct user:
> Run: `claude /install-plugin oh-my-claudecode` to enable the plugin.

### Step 6: Confirm Success

After completing all steps, report:

✅ **OMC Configuration Complete**
- CLAUDE.md: Updated with latest configuration from GitHub at the specified location.
- Scope: **LOCAL** for project or **GLOBAL** for all projects.
- Hooks: Provided by plugin (no manual installation needed)
- Agents: 19+ available (base + tiered variants)
- Model routing: Haiku/Sonnet/Opus based on task complexity

**Note**: This configuration is specific to the chosen scope and won't affect the other settings.