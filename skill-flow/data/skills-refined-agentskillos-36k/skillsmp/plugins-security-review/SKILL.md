---
name: plugins-security-review
description: Use this skill when the user asks to review the security of plugins, scan plugins for vulnerabilities, or audit installed plugins. Also suggest this skill when you notice a new plugin has been added.
---

# Plugins Security Review Skill

Review installed Claude Code plugins for security issues by launching parallel subagent scans.

## When to Use

- User explicitly asks to review plugin security
- User asks to audit or scan plugins
- **Proactively suggest** when you notice a new plugin has been added (e.g., user runs a plugin install command or you see a new entry in settings.json)

## How to Review Plugins

### Step 1: Identify Installed Plugins

Read `~/.claude/settings.json` and look at the `enabledPlugins` object. Each entry has the format:
```
"plugin-name@marketplace-name": true/false
```

Only consider plugins where the value is `true` (enabled). If the file doesn't exist or `enabledPlugins` is missing, inform the user no plugins are installed.

### Step 2: Locate Plugin Folders

Plugin source code is cached at:
```
~/.claude/plugins/cache/{marketplace-name}/{plugin-name}/
```

For example, `hookify@claude-plugins-official` would be at:
```
~/.claude/plugins/cache/claude-plugins-official/hookify/
```

**Note:** Local/dev plugins may have different paths (e.g., a local directory the user is developing in). If a plugin isn't found in the cache, ask the user for its path.

### Step 3: Launch Parallel Security Scans

For each plugin to scan (or a subset if user specified), launch a subagent using the Task tool:

- Use `subagent_type: "general-purpose"`
- Run all agents in parallel (single message with multiple Task tool calls)
- Use `run_in_background: true` so scans run asynchronously

**Prompt template for each subagent:**

```
Security review the Claude Code plugin at: {plugin_path}

Prioritize scanning executable code files (.js, .ts, .sh, .py, hooks/, commands/, agents/) over docs and assets.

Look for:

1. **Command injection risks** - Shell commands built from user input, unsafe exec/spawn calls
2. **Data exfiltration** - Suspicious network calls, sending data to external servers
3. **File system abuse** - Reading/writing sensitive paths (~/.ssh, ~/.aws, credentials files)
4. **Privilege escalation** - Attempts to modify system files or gain elevated access
5. **Obfuscated code** - Base64 encoded strings, eval(), minified code hiding malicious intent
6. **Hook abuse** - Hooks that silently modify behavior or intercept sensitive data
7. **Dependency risks** - Suspicious npm/pip packages, pinned to specific vulnerable versions
8. **Sandbox bypass** - Use of `dangerouslyDisableSandbox: true` in hook scripts or commands

For each finding, report:
- Severity: Critical / High / Medium / Low
- File and line number
- Description of the risk
- Code snippet if relevant

If no issues found, state that the plugin appears safe.
```

### Step 4: Collect and Present Results

After all subagents complete, summarize:
1. Plugins scanned
2. Critical/High severity findings (if any)
3. Medium/Low findings grouped by plugin
4. Overall assessment
5. **Recommended actions** for any issues found:
   - Critical: Disable plugin immediately (`enabledPlugins` → `false`), report to marketplace maintainer
   - High: Review the specific code, consider disabling until fixed
   - Medium/Low: Note for awareness, optionally report upstream

### Step 5: Save Review Results

After completing the review, save the results so the plugin won't be flagged as "unreviewed" on next session start.

1. **Create the reviews directory** (if it doesn't exist):
   ```bash
   mkdir -p ~/.claude/plugin-reviews
   ```

2. **Compute the plugin hash** using this command:
   ```bash
   find {plugin_path} -type f -not -path '*/.git/*' -print0 | sort -z | xargs -0 cat 2>/dev/null | shasum -a 256 | cut -d' ' -f1
   ```

3. **Save the review file** at `~/.claude/plugin-reviews/{plugin-name}-{hash}.json`:
   ```json
   {
     "plugin": "{plugin-name}",
     "marketplace": "{marketplace-name}",
     "hash": "{computed-hash}",
     "reviewed_at": "{ISO-8601-timestamp}",
     "result": "passed|issues_found",
     "findings": [
       {
         "severity": "Critical|High|Medium|Low",
         "file": "path/to/file.sh",
         "line": 42,
         "description": "Description of the issue"
       }
     ]
   }
   ```

Use the Write tool to create this file. This ensures the SessionStart hook knows this plugin version has been reviewed.

## Example Usage

**User:** "Review my installed plugins for security issues"

**Action:**
1. Read ~/.claude/settings.json to find enabled plugins
2. For each enabled plugin, launch a background security scan subagent
3. Inform user that scans are running
4. When results come back, present consolidated security report

**User:** "Scan only the hookify plugin"

**Action:**
1. Launch single subagent to scan ~/.claude/plugins/cache/claude-plugins-official/hookify/
2. Present results when complete

## Proactive Suggestion

When you see a user install a new plugin (e.g., via `/plugins install` command output), say:

> "I notice you've added a new plugin. Would you like me to run a security review on it? You can use `/plugins-security-review` to scan installed plugins."
