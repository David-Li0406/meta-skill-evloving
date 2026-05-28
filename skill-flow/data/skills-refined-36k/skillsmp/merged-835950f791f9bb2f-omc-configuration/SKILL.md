---
name: omc-configuration
description: Use this skill to configure OMC either locally for a specific project or globally for all projects.
---

# OMC Configuration

## Task: Configure OMC Default Mode

This skill allows you to configure OMC in two scopes: project-specific or global. It is critical to always download the latest CLAUDE.md from GitHub using bash curl exclusively.

### Project-Scoped Configuration

1. **Create Local .claude Directory**  
   Ensure the local project has a .claude directory:
   ```bash
   mkdir -p .claude && echo "✅ .claude directory created" || echo "❌ Failed to create .claude directory"
   ```

2. **Download Fresh CLAUDE.md (MANDATORY)**  
   Execute this command to download fresh CLAUDE.md to the local project config:
   ```bash
   curl -fsSL "https://raw.githubusercontent.com/Yeachan-Heo/oh-my-claudecode/main/docs/CLAUDE.md" -o .claude/CLAUDE.md && \
   echo "✅ CLAUDE.md downloaded successfully to .claude/CLAUDE.md" || \
   echo "❌ Failed to download CLAUDE.md"
   ```
   **Note**: If curl fails, manually download from:  
   https://raw.githubusercontent.com/Yeachan-Heo/oh-my-claudecode/main/docs/CLAUDE.md

3. **Verify Plugin Installation**  
   Check if the oh-my-claudecode plugin is enabled:
   ```bash
   grep -q "oh-my-claudecode" ~/.claude/settings.json && echo "Plugin enabled" || echo "Plugin NOT enabled"
   ```
   If not enabled, instruct the user to run:  
   `claude /install-plugin oh-my-claudecode`

4. **Confirm Success**  
   After completing all steps, report:
   ✅ **OMC Project Configuration Complete**  
   - CLAUDE.md: Updated with latest configuration from GitHub at ./.claude/CLAUDE.md  
   - Scope: **PROJECT** - applies only to this project  

### Global Configuration

1. **Download Fresh CLAUDE.md (MANDATORY)**  
   Execute this command to erase and download fresh CLAUDE.md to global config:
   ```bash
   rm -f ~/.claude/CLAUDE.md && \
   curl -fsSL "https://raw.githubusercontent.com/Yeachan-Heo/oh-my-claudecode/main/docs/CLAUDE.md" -o ~/.claude/CLAUDE.md && \
   echo "✅ CLAUDE.md downloaded successfully to ~/.claude/CLAUDE.md" || \
   echo "❌ Failed to download CLAUDE.md"
   ```
   **Note**: If curl fails, manually download from:  
   https://raw.githubusercontent.com/Yeachan-Heo/oh-my-claudecode/main/docs/CLAUDE.md

2. **Clean Up Legacy Hooks (if present)**  
   Remove any old manual hooks to prevent duplicates:
   ```bash
   rm -f ~/.claude/hooks/keyword-detector.sh
   rm -f ~/.claude/hooks/stop-continuation.sh
   rm -f ~/.claude/hooks/persistent-mode.sh
   rm -f ~/.claude/hooks/session-start.sh
   ```
   Check `~/.claude/settings.json` for manual hook entries and inform the user to remove them.

3. **Verify Plugin Installation**  
   Check if the oh-my-claudecode plugin is enabled:
   ```bash
   grep -q "oh-my-claudecode" ~/.claude/settings.json && echo "Plugin enabled" || echo "Plugin NOT enabled"
   ```
   If not enabled, instruct the user to run:  
   `claude /install-plugin oh-my-claudecode`

4. **Confirm Success**  
   After completing all steps, report:
   ✅ **OMC Global Configuration Complete**  
   - CLAUDE.md: Updated with latest configuration from GitHub at ~/.claude/CLAUDE.md  
   - Scope: **GLOBAL** - applies to all Claude Code sessions  

## Keeping Up to Date

After installing oh-my-claudecode updates (via npm or plugin update), run `/omc-default` for project or `/omc-default-global` for global configuration again to ensure you have the latest features and agent configurations.