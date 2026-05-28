# Jira CLI API Reference

Quick reference for essential jira-cli commands.

## Installation

```bash
# macOS
brew install jira

# Other platforms
# Download from https://github.com/ankitpokhrel/jira-cli/releases

# Configure
jira init

# Set auth token
export JIRA_API_TOKEN=your_token
```

## Core Commands

### `jira issue view`

```bash
jira issue view <key> [flags]

# Flags
--json              # JSON output
--comments int      # Number of comments to show
--plain            # Plain text output

# Examples
jira issue view PROJ-123 --json
jira issue view PROJ-123 --comments 10 --json
```

### `jira issue list`

```bash
jira issue list [flags]

# Key flags
--jql string       # JQL query
--json            # JSON output
--plain           # Plain text output
--no-headers      # Omit headers
--columns string  # Select columns
--limit int       # Max results

# Examples
jira issue list --jql "status = 'To Do'" --json
jira issue list --created -7d --json --limit 50
```

### `jira issue comment add`

```bash
jira issue comment add <key> [text] [flags]

# Flags
--template string  # Template file
--internal        # Internal comment

# Examples
jira issue comment add PROJ-123 "Comment text"
echo "Comment" | jira issue comment add PROJ-123
jira issue comment add PROJ-123 < questions.md
```

### `jira issue create`

```bash
jira issue create [flags]

# Key flags
-t, --type string      # Issue type (Bug, Task, Story)
-s, --summary string   # Summary
-b, --body string     # Description
--no-input           # Skip prompts

# Example
jira issue create -tBug -s"Summary" -b"Description" --no-input
```

## Output Formats

```bash
# JSON (use with jq)
jira issue view PROJ-123 --json | jq -r '.fields.summary'

# Plain (use for scripting)
jira issue list --plain --no-headers

# CSV
jira issue list --csv
```

## Environment Variables

- `JIRA_API_TOKEN` - API token (required for Cloud)
- `JIRA_AUTH_TYPE` - Auth type (`basic` or `bearer`)
- `JIRA_CONFIG_FILE` - Config file path

## Config File

Default: `~/.config/.jira/.config.yml`

```yaml
server: https://your-instance.atlassian.net
login: your-email@example.com
project:
  key: PROJ
installation: cloud  # or local
auth_type: bearer   # or basic
```

## Links

- GitHub: https://github.com/ankitpokhrel/jira-cli
- Releases: https://github.com/ankitpokhrel/jira-cli/releases
