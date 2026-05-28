---
name: open-issue
description: Create a GitHub issue. Use when the user wants to create an issue, open an issue, or report a bug/feature request.
allowed-tools: [Bash]
---

# Open Issue Skill

Creates a GitHub issue with proper formatting.

**IMPORTANT: When using this skill, announce to the user**: "Using open-issue skill to create a GitHub issue."

## Workflow

### 1. Gather Information

Before creating the issue, ensure you have:
- **Title**: A clear, concise summary
- **Body**: Detailed description of the issue
- **Labels** (optional): Appropriate labels for categorization

### 2. Determine Labels

Common labels:
| Label | Use Case |
|-------|----------|
| `enhancement` | New feature requests |
| `bug` | Bug reports |
| `refactoring` | Code refactoring tasks |
| `documentation` | Documentation updates |

### 3. Create Issue

Use `gh issue create` with heredoc syntax for the body:

```bash
gh issue create \
  --title "Issue title here" \
  --body "$(cat <<'EOF'
## Summary

Description of the issue.

## Details

Additional context, code examples, etc.

```ruby
# Code example if needed
```

## Action

What needs to be done.
EOF
)" \
  --label "label-name"
```

### 4. Body Format Guidelines

- Use `## Summary` for the main description
- Use `## Details` or `## Current Implementation` for context
- Use `## Action` or `## Proposed Implementation` for solutions
- Include code blocks with proper syntax highlighting
- Keep the body well-structured and readable

## Example

```bash
gh issue create \
  --title "Add caching for API responses" \
  --body "$(cat <<'EOF'
## Summary

API responses are fetched on every request, causing unnecessary latency.

## Proposed Implementation

- Add Redis-based caching layer
- Cache responses for 5 minutes by default
- Allow cache TTL configuration

## Benefits

- Reduced API calls
- Improved response times
EOF
)" \
  --label "enhancement"
```

## Key Rules

- **Always use heredoc syntax** (`$(cat <<'EOF' ... EOF)`) for body content
- **Use single quotes around EOF** to prevent variable expansion
- **Structure the body** with markdown headers
- **Include relevant labels** when appropriate
- **Never include AI attribution** in any output
