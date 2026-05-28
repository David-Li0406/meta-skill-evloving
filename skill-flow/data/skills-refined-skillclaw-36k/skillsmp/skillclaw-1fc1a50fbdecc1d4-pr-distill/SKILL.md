---
name: pr-distill
description: Use this skill when reviewing large PRs to surface changes requiring human attention.
---

# PR Distill Skill

<ROLE>PR Review Analyst. Your reputation depends on accurately identifying which changes need human review and which are safe to skip.</ROLE>

Analyzes pull requests to categorize changes by review necessity, reducing cognitive load on large PRs.

## Invariant Principles

1. **Heuristics First, AI Second**: Always run heuristic pattern matching before invoking AI analysis. Heuristics are fast and deterministic.
2. **Confidence Requires Evidence**: Never mark a change as "safe to skip" without a pattern match or AI explanation justifying the confidence level.
3. **Surface Uncertainty**: When confidence is low, categorize as "uncertain" rather than guessing. Humans should decide ambiguous cases.
4. **Preserve Context**: The report must include enough diff context for reviewers to understand changes without switching to the PR itself.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `pr_fetch` | Fetch PR metadata and diff from GitHub |
| `pr_diff` | Parse unified diff into FileDiff objects |
| `pr_files` | Extract file list from pr_fetch result |
| `pr_match_patterns` | Match heuristic patterns against file diffs |
| `pr_bless_pattern` | Bless a pattern for elevated precedence |
| `pr_list_patterns` | List all available patterns (builtin and blessed) |

## Execution Flow

This skill uses a **two-phase execution model** where the agent orchestrates MCP tool calls:

<analysis>
When invoked with `/pr-distill <pr>`:
1. Parse PR identifier (number or URL)
2. Run Phase 1: Fetch, parse, heuristic match
3. If unmatched files remain, use AI to analyze remaining changes
4. Run Phase 2: Generate report categorizing all changes
5. Present report to user
</analysis>

### Phase 1: Fetch, Parse, Match

```python
# Step 1: Fetch PR data
pr_data = pr_fetch("<pr-identifier>")

# Step 2: Parse the diff
diff_result = pr_diff(pr_data["diff"])

# Step 3: Match patterns against files
match_result = pr_match_patterns(
    files=diff_result["files"],
    project_root="/path/to/project"
)
```

This produces:
- `match_result["matched"]`: Files with pattern matches (categorized)
- `match_result["unmatched"]`: Files requiring AI analysis

### Phase 2: AI Analysis (if needed)

For unmatched files, analyze each to determine:
- **review_required**: Significant logic, API, or behavior changes
- **safe_to_skip**: Formatting, comments, trivial refactoring