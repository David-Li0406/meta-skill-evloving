# Create Issue Commands

Reference for creating Jira issues using `jira-cli`.

## Getting Help

```bash
jira issue create --help
jira epic create --help
```

## Create Issue

```bash
jira issue create [options]
```

### Options

| Flag                        | Description                                             |
| --------------------------- | ------------------------------------------------------- |
| `-t, --type <type>`         | Issue type (Bug, Story, Task, Sub-task, etc.)           |
| `-s, --summary <text>`      | Issue summary/title (required)                          |
| `-b, --body <text>`         | Issue description                                       |
| `-y, --priority <priority>` | Priority (Highest, High, Medium, Low, Lowest)           |
| `-a, --assignee <user>`     | Assignee username or email                              |
| `-r, --reporter <user>`     | Reporter username                                       |
| `-l, --label <label>`       | Add label (can be used multiple times)                  |
| `-C, --component <name>`    | Add component (can be used multiple times)              |
| `-P, --parent <key>`        | Parent issue/epic key (attach to epic)                  |
| `--fix-version <version>`   | Fix version                                             |
| `--custom <field=value>`    | Set custom field                                        |
| `--template <path>`         | Load description from template file (use `-` for stdin) |
| `--no-input`                | Disable interactive prompts                             |
| `--web`                     | Open created issue in browser                           |

### Examples

```bash
# Interactive creation (prompts for all fields)
jira issue create

# Create bug with all details
jira issue create \
  -tBug \
  -s"Login fails with special characters in password" \
  -b"When password contains & or < characters, login returns 500 error" \
  -yHigh \
  -lauth \
  -lurgent \
  --no-input

# Create story under an epic (using -P/--parent)
jira issue create \
  -tStory \
  -s"Implement OAuth2 login" \
  -PEPIC-42 \
  --no-input

# Create sub-task under a parent issue
jira issue create \
  -tSub-task \
  -s"Write unit tests" \
  -PPROJ-123 \
  --no-input

# Create task with component and assignee
jira issue create \
  -tTask \
  -s"Update documentation" \
  -CDocumentation \
  -a"john.doe" \
  --no-input

# Create with description from file
jira issue create \
  -tBug \
  -s"Memory leak in parser" \
  --template /path/to/description.md \
  --no-input

# Create with description from stdin
echo "Detailed description here" | jira issue create \
  -tTask \
  -s"Investigate performance issue"
```

### Custom Fields

Use `--custom` for non-standard fields:

```bash
jira issue create \
  -tBug \
  -s"Summary" \
  --custom "customfield_10001=value" \
  --no-input
```

## Create Epic

```bash
jira epic create [options]
```

Epics require an additional `-n/--name` flag for the epic name.

### Options

Same as `jira issue create` plus:

| Flag                | Description                    |
| ------------------- | ------------------------------ |
| `-n, --name <name>` | Epic name (required for epics) |

### Examples

```bash
# Interactive epic creation
jira epic create

# Non-interactive epic creation
jira epic create \
  -n"Q1 Authentication Improvements" \
  -s"Improve authentication security and UX" \
  -yHigh \
  -lauthentication \
  -lq1 \
  --no-input
```

## Add Issues to Epic

```bash
jira epic add <EPIC-KEY> <ISSUE-KEY>...
```

Add up to 50 issues to an epic at once.

```bash
# Add single issue
jira epic add EPIC-1 PROJ-123

# Add multiple issues
jira epic add EPIC-1 PROJ-123 PROJ-124 PROJ-125
```

## Template Files

Description templates support GitHub-flavored and Jira-flavored markdown.

Example template (`bug-template.md`):

```markdown
## Environment

- OS:
- Browser:
- Version:

## Steps to Reproduce

1.
2.
3.

## Expected Behavior

## Actual Behavior

## Screenshots/Logs
```

Usage:

```bash
jira issue create -tBug -s"Bug title" --template bug-template.md --no-input
```

## Best Practices

1. **Always use `--no-input`** for scripted/automated creation
2. **Validate issue type** exists in project before creating
3. **Quote summaries and descriptions** containing special characters
4. **Use templates** for consistent issue formatting
5. **Confirm with user** before executing create commands

## Output Parsing

On successful creation, `jira issue create` outputs the issue key:

```
Issue created: PROJ-123
```

Capture the key for follow-up operations:

```bash
key=$(jira issue create -tTask -s"Summary" --no-input 2>&1 | grep -oE '[A-Z]+-[0-9]+')
echo "Created: $key"
```
