---
name: slack-notify
description: Auto-send Slack notifications when TodoWrite tasks complete. Includes task summary, file changes, execution time, and repository context. Supports config file (no env vars needed) and manual `/devnogari:slack-notify` trigger.
---

# Slack Notify Skill

## Purpose
Automatically send Slack notifications when TodoWrite tasks are completed, providing real-time updates on work progress with repository context.

## Activation Triggers
- **Auto-trigger (Default: ON)**: Automatically activates when ALL TodoWrite tasks are marked as `completed`
  - Receives hook context via **stdin as JSON** (not environment variables)
  - Context includes `transcript_path` pointing to conversation history in JSONL format
  - Hook parses transcript to extract completed TodoWrite tasks
- **Manual invocation**: `/devnogari:slack-notify` command
- **Alternative triggers**: Git hooks, build scripts, time-based, error-based, etc. (see `docs/triggers.md`)
- **Configurable**: Can be disabled via `SLACK_NOTIFY_AUTO_TRIGGER=false` or config file

## Prerequisites

### Required
- **Slack Webhook URL**: Must be configured via **config file** (recommended) OR environment variable
- **Node.js**: Version 16.0.0 or higher
- **Plugin Installation**: Installed at `~/.claude/plugins/slack-notify/`

### Configuration

**IMPORTANT**: Webhook URL can be provided via config file OR environment variable. The script will check both locations automatically.

**📁 Config File Locations** (✅ Recommended - checked in priority order):
1. `./.claude-slack-notify.json` - Project-level (highest priority)
2. `~/.config/claude-slack-notify/config.json` - Global (✅ recommended)
3. `~/.claude-slack-notify.json` - Home directory
4. `~/.config/claude-code/slack-notify.json` - Legacy location

If a valid config file exists with `webhookUrl` set, the script will use it automatically. **No environment variable needed.**

**⚙️ Environment Variables** (Optional override):
- `SLACK_WEBHOOK_URL` - Webhook URL (only required if no config file exists)
- `SLACK_NOTIFY_PROFILE` - Config profile to use (default: "default")
- `SLACK_NOTIFY_ENABLED` - Enable/disable (default: true)
- `SLACK_NOTIFY_AUTO_TRIGGER` - Auto-trigger on TodoWrite (default: true)
- `SLACK_NOTIFY_DEBUG` - Debug logging (default: false)

**Configuration Priority**: CLI args > Environment variables > Config file > Defaults

## Behavior
When activated, this skill:
1. **Receives Hook Context**: Reads stdin JSON containing `session_id`, `transcript_path`, and hook metadata
2. **Loads Configuration**: Checks config file locations first, then falls back to environment variables
3. **Parses Transcript**: Extracts TodoWrite tool calls from conversation history (JSONL format)
4. **Collects Task Summary**: Gathers completed task information by filtering `status == "completed"`
5. **Tracks File Changes**: Identifies modified/created files during session via `git status`
6. **Records Execution Time**: Captures start and end timestamps
7. **Aggregates Errors/Warnings**: Summarizes any issues encountered (future enhancement)
8. **Sends Slack Message**: Posts formatted notification to configured channel

**Important**: Do NOT block execution if `SLACK_WEBHOOK_URL` environment variable is not set. The script will automatically load webhook URL from config file at `~/.config/claude-slack-notify/config.json` if it exists.

## Message Format
```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "✅ Claude Code Task Completed"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Task Summary:*\n[Task description]"
        },
        {
          "type": "mrkdwn",
          "text": "*Execution Time:*\n[Duration]"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*📁 Files Changed:*\n• file1.js\n• file2.ts"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*⚠️ Errors/Warnings:*\n[Error summary or 'None']"
      }
    }
  ]
}
```

## Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
# Run interactive setup script
npm run setup-config

# Follow prompts:
# 1. Choose config location (recommended: ~/.config/claude-slack-notify/config.json)
# 2. Enter Slack Webhook URL
# 3. Configure options (min tasks, auto-trigger)
# 4. Send test notification
```

### Option 2: Manual Setup
```bash
# 1. Create config directory
mkdir -p ~/.config/claude-slack-notify

# 2. Copy example config
cp config.example.json ~/.config/claude-slack-notify/config.json

# 3. Edit with your webhook URL
vim ~/.config/claude-slack-notify/config.json
# Set "webhookUrl": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# 4. Test configuration
SLACK_NOTIFY_DEBUG=true npm run notify -- --tasks "Test notification"
```

### Option 3: Environment Variables Only
```bash
# Add to ~/.zshrc or ~/.bashrc
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Reload shell
source ~/.zshrc

# Test
npm run notify -- --tasks "Test"
```

## Implementation Process

### Step 1: Configuration Loading
The plugin loads configuration in this priority order:
1. CLI arguments (highest priority)
2. Environment variables
3. Config file (first found from priority list)
4. Default values (lowest priority)

### Step 2: Collect Session Data
```javascript
// Gathered automatically from current session:
const sessionData = {
  tasks: [], // From TodoWrite completed items
  files: [], // From git status
  startTime: null, // Session start timestamp
  endTime: Date.now(),
  errors: [], // From error logs
  repository: { // From git info
    name: "project-name",
    branch: "main",
    commit: "abc123"
  }
};
```

### Step 3: Format & Send
```javascript
// Automatic formatting with Slack Block Kit
const message = formatSlackMessage(sessionData);
await sendToSlack(message);
```

## Integration Points

### With TodoWrite
- Monitor TodoWrite tool calls via Claude Code hooks
- Detect when all tasks transition to "completed"
- Auto-trigger notification on completion

**Hook Context Structure** (received via stdin JSON):
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/xxx/xxx.jsonl",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

**Transcript Parsing**:
- Transcript is in JSONL format (one JSON object per line)
- Each line contains tool calls with `tool_name` and `tool_input`
- TodoWrite calls include `todos` array with `content` and `status` fields
- Hook extracts completed tasks: `jq '.tool_input.todos[] | select(.status == "completed") | .content'`

### With Git
- Track file changes via `git status`
- Include modified files in notification
- Optionally include commit info

### With Error Handling
- Capture tool errors and warnings
- Aggregate for summary reporting
- Include severity levels

## Usage Examples

### Manual Trigger
```
User: "Send slack notification for completed work"
Claude: [Executes slack-notify skill]
- Collects session data
- Formats message
- Sends to Slack
- Confirms delivery
```

### Auto-Trigger (Default Behavior)
```
[TodoWrite: All tasks completed]
→ Auto-detect completion (when SLACK_NOTIFY_AUTO_TRIGGER=true)
→ Execute slack-notify skill
→ Send notification
→ Continue session (non-blocking)

Example:
TodoWrite([
  { content: "Implement auth", status: "completed" },
  { content: "Add tests", status: "completed" },
  { content: "Update docs", status: "completed" }
])
→ All tasks completed! Auto-trigger Slack notification ✅
```

### Disable Auto-Trigger
```bash
# Temporarily disable for current session
export SLACK_NOTIFY_AUTO_TRIGGER=false

# Or in config file
{
  "default": {
    "autoTrigger": false
  }
}
```

## Configuration Options

### Config File (Recommended)
```json
{
  "default": {
    "webhookUrl": "https://hooks.slack.com/services/...",
    "enabled": true,
    "autoTrigger": true,
    "minTasks": 1,
    "includeErrorsOnly": false,
    "channelOverride": "",
    "messageTemplate": {
      "header": "✅ Claude Code Task Completed",
      "includeFiles": true,
      "includeErrors": true,
      "includeTimestamp": true,
      "includeRepoInfo": true,
      "maxFiles": 10,
      "maxErrors": 5
    }
  },
  "profiles": {
    "production": {
      "webhookUrl": "https://hooks.slack.com/services/PROD/...",
      "channelOverride": "#production-alerts",
      "includeErrorsOnly": true,
      "minTasks": 3
    },
    "development": {
      "webhookUrl": "https://hooks.slack.com/services/DEV/...",
      "minTasks": 1
    }
  }
}
```

**Using Profiles**:
```bash
# Set via environment variable
export SLACK_NOTIFY_PROFILE="production"

# Or via CLI argument
npm run notify -- --profile production --tasks "Deploy completed"
```

### Environment Variables (Alternative)
```bash
# Required (if no config file)
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional
SLACK_NOTIFY_ENABLED="true"              # Enable/disable (default: true)
SLACK_NOTIFY_AUTO_TRIGGER="true"         # Auto-trigger on TodoWrite (default: true)
SLACK_NOTIFY_PROFILE="default"           # Profile to use (default: "default")
SLACK_NOTIFY_MIN_TASKS="1"               # Minimum tasks to trigger (default: 1)
SLACK_NOTIFY_INCLUDE_ERRORS_ONLY="false" # Only notify if errors (default: false)
SLACK_NOTIFY_CHANNEL_OVERRIDE=""         # Override webhook channel
SLACK_NOTIFY_DEBUG="false"               # Enable debug logging (default: false)
```

### Priority Order
Configuration is merged with this priority:
1. **CLI arguments** (highest priority)
2. **Environment variables**
3. **Config file** (selected profile or default)
4. **Built-in defaults** (lowest priority)

Example:
```bash
# Profile sets minTasks=3, but CLI overrides to 1
SLACK_NOTIFY_PROFILE=production npm run notify -- --tasks "task1"
# Result: Uses production webhook URL but triggers with 1 task
```

### Customization
- **Message Template**: Configure in config file `messageTemplate` section
- **Trigger Conditions**: Adjust `autoTrigger`, `minTasks`, `includeErrorsOnly`
- **Alternative Triggers**: See `docs/triggers.md` for git hooks, build scripts, etc.

## Error Handling

### Common Issues
1. **Webhook URL not set**: Skill will warn and skip notification
2. **Network failure**: Retry with exponential backoff
3. **Invalid webhook**: Log error, don't block workflow
4. **Missing session data**: Send partial notification

### Fallback Behavior
- Never block Claude Code workflow
- Log errors to console for debugging
- Graceful degradation if Slack unavailable

## Quality Standards
- **Non-Blocking**: Never interrupt Claude Code operations
- **Reliable**: Retry logic for transient failures
- **Privacy**: Only include non-sensitive information
- **Performance**: Execute asynchronously, <2s overhead

## Installation

### Global Plugin Installation (Recommended)
```bash
# Clone or download the plugin
cd ~/.claude/plugins
git clone https://github.com/devnogari/devnogari-claude-plugins.git slack-notify

# Or copy from local repository
cp -r /path/to/devnogari-claude-plugins ~/.claude/plugins/slack-notify

# Install dependencies and build
cd ~/.claude/plugins/slack-notify
npm install
npm run build

# Run setup
npm run setup-config
```

### Project-Level Installation
```bash
# In your project directory
npm install @devnogari/claude-code-slack-notify

# Setup project config
cp node_modules/@devnogari/claude-code-slack-notify/config.example.json .claude-slack-notify.json

# Edit config
vim .claude-slack-notify.json
```

### Verification
```bash
# Test notification with debug
SLACK_NOTIFY_DEBUG=true npm run notify -- --tasks "Installation test"

# Check which config is loaded
# Output should show: [DEBUG] Loaded config from: /path/to/config.json
```

## Maintenance

### Health Check
```bash
# 1. Test webhook connectivity
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test from Claude Code"}'

# 2. Verify config loading
SLACK_NOTIFY_DEBUG=true npm run notify -- --tasks "Health check"
# Expected output:
# [DEBUG] Loaded config from: ~/.config/claude-slack-notify/config.json
# [DEBUG] Using profile: default
# [INFO] ✅ Notification sent successfully

# 3. Check plugin installation
ls -la ~/.claude/plugins/slack-notify/
# Should show: dist/, scripts/, skills/, plugin.json, package.json
```

### Debugging

**Enable Debug Mode**:
```bash
# Temporary (current session)
export SLACK_NOTIFY_DEBUG=true

# Permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export SLACK_NOTIFY_DEBUG=true' >> ~/.zshrc
source ~/.zshrc
```

**Debug Output**:
```bash
$ SLACK_NOTIFY_DEBUG=true npm run notify -- --tasks "Debug test"

[DEBUG] Loaded config from: /Users/you/.config/claude-slack-notify/config.json
[DEBUG] Using profile: default
[DEBUG] Session data collected: {
  tasks: [ 'Debug test' ],
  files: [ 'M src/main.ts', 'A tests/new.test.ts' ],
  startTime: 1761623307000,
  endTime: 1761623307521,
  errors: [],
  repository: { name: 'my-project', branch: 'main', commit: 'abc123' }
}
[DEBUG] Sending to Slack: {blocks: [...]}
[INFO] ✅ Notification sent successfully
```

**Common Debug Scenarios**:

1. **Config not found**:
```bash
[DEBUG] No config file found, using environment variables and defaults
# Solution: Check config file location and permissions
```

2. **Webhook URL not set**:
```bash
[ERROR] SLACK_WEBHOOK_URL not set
# Solution: Set in config file or environment variable
```

3. **Network failure**:
```bash
[ERROR] Failed to send notification: ECONNREFUSED
# Solution: Check internet connection and webhook URL validity
```

4. **Wrong profile**:
```bash
[DEBUG] Using profile: production
# If unexpected, check: echo $SLACK_NOTIFY_PROFILE
```

## Alternative Triggers

Beyond TodoWrite auto-trigger, you can trigger notifications from various events. See `docs/triggers.md` for detailed examples.

### Quick Examples

**Git Commit Hook**:
```bash
# .git/hooks/post-commit
#!/bin/bash
COMMIT_MSG=$(git log -1 --pretty=%B)
node ~/.claude/plugins/slack-notify/dist/slack-notify.js \
  --tasks "Committed: $COMMIT_MSG" \
  --startTime $(date +%s000)
```

**Build Script**:
```json
// package.json
{
  "scripts": {
    "build": "tsc && node ~/.claude/plugins/slack-notify/dist/slack-notify.js --tasks 'Build completed'"
  }
}
```

**Terminal Alias**:
```bash
# ~/.zshrc
alias sn="node ~/.claude/plugins/slack-notify/dist/slack-notify.js --tasks"

# Usage: sn "Task completed"
```

**CI/CD Pipeline**:
```yaml
# .github/workflows/deploy.yml
- name: Notify deployment
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
  run: |
    node ~/.claude/plugins/slack-notify/dist/slack-notify.js \
      --tasks "Deployed to production" \
      --startTime $(date +%s000)
```

See `docs/triggers.md` for 8+ trigger options including:
- Git hooks (commit, push, PR)
- Time-based (cron, intervals)
- File changes (fswatch)
- Error detection
- Conditional triggers (branch, time)

## Future Enhancements
- [x] ✅ Config file support with profiles
- [x] ✅ Interactive setup script
- [x] ✅ Debug mode and logging
- [x] ✅ Git integration and repository info
- [x] ✅ Configurable message templates
- [ ] Support multiple Slack channels simultaneously
- [ ] Rich formatting with syntax-highlighted code snippets
- [ ] Integration with Jira, Linear, GitHub Issues
- [ ] Scheduled summary reports (daily/weekly digests)
- [ ] Team collaboration features (mentions, thread replies)
- [ ] Message templates library
- [ ] Webhook response handling and analytics

## License
MIT License - Free to use and modify

## Support

### Documentation
- **README**: `./README.md` - Quick start and overview
- **Configuration Guide**: `./docs/configuration.md` - Detailed config options
- **Trigger Options**: `./docs/triggers.md` - Alternative trigger methods (8+ options)
- **API Reference**: `./docs/api.md` - Programmatic usage
- **Troubleshooting**: `./docs/troubleshooting.md` - Common issues and solutions

### Getting Help
- **GitHub Issues**: https://github.com/devnogari/devnogari-claude-plugins/issues
- **Discussions**: https://github.com/devnogari/devnogari-claude-plugins/discussions
- **Quick Debug**: Run `SLACK_NOTIFY_DEBUG=true npm run notify -- --tasks "test"`

### Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests if applicable
4. Submit a pull request

### Repository
- **GitHub**: https://github.com/devnogari/devnogari-claude-plugins
- **NPM**: `@devnogari/claude-code-slack-notify`
- **License**: MIT
