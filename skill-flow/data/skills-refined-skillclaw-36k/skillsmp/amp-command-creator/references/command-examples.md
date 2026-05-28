# Command Examples

Complete working examples of custom Amp commands.

## Example 1: PR Review (Markdown)

A static prompt template for code review. Place in `.agents/commands/pr-review.md`:

```markdown
# PR Review

## SYSTEM

You are a seasoned staff engineer acting as a code reviewer.  
Your objectives are to  
• improve correctness, security, performance and readability,  
• keep the author's intent and style,  
• be concise and constructive.

## ASSISTANT RULES

1. Read the diff **twice** before commenting.
2. Categorise each comment with one of these tags (uppercase, in square brackets):  
   [BUG], [SECURITY], [PERF], [STYLE], [DOCS], [TEST], [NIT].
3. For every finding provide:  
   • **File + line range** in `path:line‑start‑line‑end` form,  
   • A short title,  
   • A 1‑to‑3 sentence explanation,  
   • An optional **suggested patch** inside a <details> block with ```diff fencing.
4. Praise good patterns; at least one **"kudos"** comment if applicable.
5. Never mention GPT or that you are an AI.
6. Output only Markdown; no additional prose before or after.

## OUTPUT FORMAT

```markdown
### Review Summary

| Category   | Count |
| ---------- | ----- |
| [BUG]      | ⟨n⟩   |
| [SECURITY] | ⟨n⟩   |
| [PERF]     | ⟨n⟩   |
| [STYLE]    | ⟨n⟩   |
| [DOCS]     | ⟨n⟩   |
| [TEST]     | ⟨n⟩   |
| [NIT]      | ⟨n⟩   |

### Inline Comments

1. **[TAG] path/to/file.ext:42‑47 – Short title**  
   Explanation sentence(s).
   <details>
   <summary>Suggested patch</summary>

   ```diff
   ⟨patch⟩
   ```

   </details>

2. **[TAG] …**
   …

### Kudos

• path/to/other_file.ts:110 – Great use of descriptive variable names!
```
```

## Example 2: Work On Issue (Bash Executable)

A dynamic command that fetches Linear issue details. Place in `.agents/commands/work-on-issue`:

```bash
#!/bin/bash
# Fetch a Linear issue and generate an investigation prompt
# Usage: work-on-issue <issue-abbreviation>
# Examples:
#   work-on-issue AB-123
#   work-on-issue https://linear.app/abc/issue/AB-123/issue-title

set -euo pipefail

if [ $# -eq 0 ]; then
	echo "Usage: work-on-issue <issue-abbreviation>"
	echo "Examples:"
	echo "  work-on-issue AB-123"
	echo "  work-on-issue https://linear.app/abc/issue/AB-123/issue-title"
	exit 2
fi

ISSUE_ARG="$1"

# Find root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Load .env file from root directory
if [ -f "$ROOT_DIR/.env" ]; then
	set -a
	source "$ROOT_DIR/.env"
	set +a
fi

# Extract issue abbreviation if URL is provided
if [[ "$ISSUE_ARG" == *"linear.app"* ]]; then
	ISSUE_ABBREV=$(echo "$ISSUE_ARG" | grep -oE '[A-Z]+-[0-9]+')
else
	ISSUE_ABBREV="$ISSUE_ARG"
fi

# Validate issue format
if [[ ! "$ISSUE_ABBREV" =~ ^[A-Z]+-[0-9]+$ ]]; then
	echo "Error: Invalid issue format. Expected format: TEAM-123"
	exit 1
fi

# Check if LINEAR_API_KEY is set
if [ -z "${LINEAR_API_KEY:-}" ]; then
	echo "Error: LINEAR_API_KEY environment variable not set"
	echo "Please set your Linear API key: export LINEAR_API_KEY=your_token_here"
	exit 1
fi

# GraphQL query
read -r -d '' QUERY <<'EOF'
query($number: Float!) {
  issues(filter: { number: { eq: $number } }) {
    nodes {
      id
      identifier
      title
      description
      priority
      state { name type }
      assignee { name email }
      creator { name email }
      team { name key }
      labels { nodes { name color } }
      project { name }
      estimate
      url
      createdAt
      updatedAt
      comments {
        nodes {
          body
          user { name }
          createdAt
        }
      }
    }
  }
}
EOF

# Extract issue number
ISSUE_NUMBER=$(echo "$ISSUE_ABBREV" | grep -oE '[0-9]+$')

# Execute query
JSON_PAYLOAD=$(jq -n --arg query "$QUERY" --argjson number "$ISSUE_NUMBER" \
	'{query: $query, variables: {number: $number}}')

RESPONSE=$(curl -s -X POST https://api.linear.app/graphql \
	-H "Authorization: $LINEAR_API_KEY" \
	-H "Content-Type: application/json" \
	-d "$JSON_PAYLOAD")

# Check for errors
if echo "$RESPONSE" | jq -e '.errors' >/dev/null 2>&1; then
	echo "Error: Linear API returned an error:"
	echo "$RESPONSE" | jq -r '.errors[].message'
	exit 1
fi

# Extract issue data
ISSUE_DATA=$(echo "$RESPONSE" | jq -r '.data.issues.nodes[0]')
if [ "$ISSUE_DATA" == "null" ]; then
	echo "Error: Issue $ISSUE_ABBREV not found"
	exit 1
fi

# Extract fields
TITLE=$(echo "$ISSUE_DATA" | jq -r '.title')
DESCRIPTION=$(echo "$ISSUE_DATA" | jq -r '.description // ""')
IDENTIFIER=$(echo "$ISSUE_DATA" | jq -r '.identifier')
PRIORITY=$(echo "$ISSUE_DATA" | jq -r '.priority // "None"')
STATE=$(echo "$ISSUE_DATA" | jq -r '.state.name')
ASSIGNEE=$(echo "$ISSUE_DATA" | jq -r '.assignee.name // "Unassigned"')
CREATOR=$(echo "$ISSUE_DATA" | jq -r '.creator.name')
TEAM=$(echo "$ISSUE_DATA" | jq -r '.team.name')
URL=$(echo "$ISSUE_DATA" | jq -r '.url')
ESTIMATE=$(echo "$ISSUE_DATA" | jq -r '.estimate // "Not estimated"')

# Output formatted content
cat <<EOF
Deep-dive on this Linear issue, explore the codebase, and propose a comprehensive plan.

# $TITLE ($IDENTIFIER)
**Team:** $TEAM  
**State:** $STATE  
**Priority:** $PRIORITY  
**Assignee:** $ASSIGNEE  
**Creator:** $CREATOR  
**Estimate:** $ESTIMATE  
**URL:** $URL  

## Description
$DESCRIPTION

EOF

# Add labels if present
LABELS=$(echo "$ISSUE_DATA" | jq -r '.labels.nodes[] | .name' | tr '\n' ', ' | sed 's/, $//')
if [ -n "$LABELS" ]; then
	echo "**Labels:** $LABELS"
	echo
fi

# Add project if present
PROJECT=$(echo "$ISSUE_DATA" | jq -r '.project.name // empty')
if [ -n "$PROJECT" ]; then
	echo "**Project:** $PROJECT"
	echo
fi

# Add comments if present
COMMENTS=$(echo "$ISSUE_DATA" | jq -r '.comments.nodes[] | "**@\(.user.name)** (\(.createdAt | split("T")[0])):\n\(.body)\n"')
if [ -n "$COMMENTS" ]; then
	echo "## Comments"
	echo
	echo "$COMMENTS"
fi

cat <<'EOF'

## Your Tasks

1. **Onboard yourself** to this issue:
   - Use ultrathink
   - Explore the codebase
   - Ask questions if needed

2. **Create a comprehensive plan** covering:
   - Required code changes
   - Potential impacts on other parts of the system
   - Necessary tests to be written or updated
   - Documentation updates
   - Performance considerations
   - Security implications
   - Backwards compatibility (if applicable)

3. **ASK FOR EXPLICIT APPROVAL** before starting implementation.

Goal: Be fully prepared to start working on the task.
EOF
```

## Example 3: Daily Standup (Python Executable)

A command that generates a standup summary from git history. Place in `~/.config/amp/commands/daily-standup`:

```python
#!/usr/bin/env python3
"""
Generate a daily standup summary from recent git activity.
Usage: daily-standup [days]
"""

import subprocess
import sys
from datetime import datetime, timedelta


def get_git_log(days: int = 1) -> str:
    """Get git log for the specified number of days."""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        result = subprocess.run(
            [
                "git", "log",
                f"--since={since}",
                "--author=$(git config user.email)",
                "--pretty=format:%h %s",
                "--no-merges"
            ],
            capture_output=True,
            text=True,
            check=True,
            shell=False
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def get_branch_name() -> str:
    """Get current branch name."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def main() -> int:
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    commits = get_git_log(days)
    branch = get_branch_name()
    
    print(f"""# Daily Standup Summary

**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Current Branch:** {branch}

## Recent Commits (last {days} day{"s" if days > 1 else ""})

{commits if commits else "(No commits found)"}

## Standup Template

Based on the above activity, help me write a standup update covering:

1. **What I did yesterday/recently:**
   - Summarize the commits above into meaningful work items
   
2. **What I'm working on today:**
   - Based on the current branch and recent work, suggest focus areas
   
3. **Any blockers:**
   - Ask if there are any blockers I should mention

Keep it concise and suitable for a team standup meeting.
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Key Patterns

### Environment Variable Handling

Always load from .env and validate required variables:

```bash
# Bash
if [ -f "$ROOT_DIR/.env" ]; then
    set -a
    source "$ROOT_DIR/.env"
    set +a
fi

if [ -z "${API_KEY:-}" ]; then
    echo "Error: API_KEY not set"
    exit 1
fi
```

```python
# Python
def load_env(root: Path) -> None:
    env_file = root / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())
```

### Argument Handling

```bash
# Bash
if [ $# -eq 0 ]; then
    echo "Usage: command-name <required-arg>"
    exit 2
fi
ARG="$1"
```

```python
# Python
parser = argparse.ArgumentParser(description="Command description")
parser.add_argument("required_arg", help="Description")
parser.add_argument("--optional", "-o", default="value", help="Optional arg")
args = parser.parse_args()
```

### Error Handling

```bash
# Bash - use set -euo pipefail at the top
set -euo pipefail

# Check specific conditions
if [ ! -f "$FILE" ]; then
    echo "Error: File not found: $FILE"
    exit 1
fi
```

```python
# Python
try:
    result = api_call()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    return 1
```

### API Integration Pattern

```bash
# Bash - GraphQL example
JSON_PAYLOAD=$(jq -n --arg query "$QUERY" --argjson vars "$VARIABLES" \
    '{query: $query, variables: $vars}')

RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$JSON_PAYLOAD")

# Check for errors
if echo "$RESPONSE" | jq -e '.errors' >/dev/null 2>&1; then
    echo "API Error:" >&2
    echo "$RESPONSE" | jq -r '.errors[].message' >&2
    exit 1
fi
```

## Command Ideas

- **code-review** — Review staged changes with specific guidelines
- **explain-file** — Generate documentation for the current file
- **refactor** — Suggest refactoring improvements
- **test-generator** — Generate tests for a function or module
- **changelog-entry** — Create a changelog entry from recent commits
- **release-notes** — Compile release notes from merged PRs
- **dependency-check** — Analyze and report on outdated dependencies
