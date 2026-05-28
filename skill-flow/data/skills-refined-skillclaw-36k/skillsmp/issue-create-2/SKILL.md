---
name: issue-create
description: Create GitHub issues with AI labeling and content type detection. TRIGGERS - create issue, file bug, feature request, report issue, gh issue create, new issue.
allowed-tools: Read, Bash, Grep, Glob
---

# Issue Create Skill

Create well-formatted GitHub issues with intelligent automation including AI-powered label suggestions, content type detection, template formatting, and related issue linking.

## When to Use

- Creating bug reports, feature requests, questions, or documentation issues
- Need AI-powered label suggestions from repository's existing taxonomy
- Want automatic duplicate detection and related issue linking
- Need consistent issue formatting across different repositories

## Invocation

**Slash command**: `/gh-tools:issue-create`

**Natural language triggers**:

- "Create an issue about..."
- "File a bug for..."
- "Submit a feature request..."
- "Report this problem to..."
- "Post an issue on GitHub..."

## Features

### 1. Repository Detection

- Auto-detects repository from current git directory
- Supports explicit `--repo owner/repo` flag
- Checks permissions before attempting to create

### 2. Content Type Detection

- AI-powered detection (gpt-4.1 via gh-models)
- Fallback to keyword matching
- Types: Bug, Feature, Question, Documentation

### 3. Title Extraction

- Extracts clear title from content
- Adds type prefix (Bug:, Feature:, etc.)
- Limits to 72 characters

### 4. Template Formatting

- Auto-selects template based on content type
- Bug: Steps to reproduce, Expected/Actual behavior
- Feature: Use case, Proposed solution
- Question: Context, What was tried
- Documentation: Location, Suggested change

### 5. Label Suggestion

- Fetches repository's existing labels
- AI suggests 2-4 relevant labels
- Only suggests labels that exist (taxonomy-aware)
- 24-hour cache for performance

### 6. Related Issues

- Searches for similar issues
- Links related issues in body
- Warns about potential duplicates

### 7. Preview & Confirm

- Full preview before creation
- Dry-run mode available
- Edit option for modifications

## Usage Examples

### Basic Usage

```bash
# From within a git repository
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --body "Login page crashes when using special characters in password"
```

### With Explicit Repository

```bash
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --repo owner/repo \
  --body "Feature: Add dark mode support for better accessibility"
```

### Dry Run (Preview Only)

```bash
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --repo owner/repo \
  --body "Bug: API returns 500 error" \
  --dry-run
```

### With Custom Title and Labels

```bash
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --repo owner/repo \
  --title "Bug: Login fails with OAuth" \
  --body "Detailed description..." \
  --labels "bug,authentication"
```

### Disable AI Features

```bash
bun ~/eon/cc-skills/plugins/gh-tools/scripts/issue-create.ts \
  --body "Question: How to configure..." \
  --no-ai
```

## CLI Options

| Option      | Short | Description                     |
| ----------- | ----- | ------------------------------- |
| `--repo`    | `-r`  | Repository in owner/repo format |
| `--body`    | `-b`  | Issue body content (required)   |
| `--title`   | `-t`  | Issue title (optional)          |
| `--labels`  | `-l`  | Comma-separated labels          |
| `--dry-run` |       | Preview without creating        |
| `--no-ai`   |       | Disable AI features             |
| `--verbose` | `-v`  | Enable verbose output           |
| `--help`    | `-h`  | Show help                       |

## Dependencies

- `gh` CLI (required) - GitHub CLI tool
- `gh-models` extension (optional) - Enables AI features

### Installing gh-models

```bash
gh extension install github/gh-models
```

## Permission Handling

| Level       | Behavior                                |
| ----------- | --------------------------------------- |
| WRITE/ADMIN | Full functionality                      |
| TRIAGE      | Can apply labels                        |
| READ        | Shows formatted content for manual copy |
| NONE        | Suggests fork workflow                  |

## Logging

Logs to: `~/.claude/logs/gh-issue-create.jsonl`

Events logged:

- `preflight` - Initial checks
- `type_detected` - Content type detection
- `labels_suggested` - Label suggestions
- `related_found` - Related issues search
- `issue_created` - Successful creation
- `dry_run` - Dry run completion

## Hook Compliance

This skill uses `--body-file` pattern for issue creation, complying with the `gh-issue-body-file-guard.mjs` hook that blocks inline `--body` to prevent silent failures.

## Related Documentation

- [Content Types Reference](./references/content-types.md)
- [Label Strategy Reference](./references/label-strategy.md)
- [AI Prompts Reference](./references/ai-prompts.md)

## Troubleshooting

### "No repository context"

Run from a git directory or use `--repo owner/repo` flag.

### Labels not suggested

- Check if gh-models is installed: `gh extension list`
- Verify repository has labels: `gh label list --repo owner/repo`
- Check label cache: `ls ~/.cache/gh-issue-skill/labels/`

### AI features not working

Install gh-models extension:

```bash
gh extension install github/gh-models
```
