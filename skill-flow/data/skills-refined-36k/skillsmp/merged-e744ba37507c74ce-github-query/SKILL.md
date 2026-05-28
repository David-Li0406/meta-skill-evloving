---
name: github-query
description: Use this skill to efficiently query GitHub discussions, issues, and pull requests with optional jq filtering support.
---

# GitHub Query Skill

This skill provides efficient querying of GitHub discussions, issues, and pull requests with built-in jq filtering support.

## Important: jq Parameter is Optional

The `--jq` parameter is **optional**. When called without `--jq`, this skill returns **schema and data size information** instead of the full data. This prevents overwhelming responses with large datasets and helps you understand the data structure before querying.

Use `--jq '.'` to get all data, or use a more specific filter for targeted results.

## Usage

Use this skill to query discussions, issues, or pull requests from the current repository or any specified repository.

### Basic Query (Returns Schema Only)

To list discussions, issues, or pull requests from the current repository:

```bash
./query-discussions.sh
# Returns schema and data size, not full data
```

### Get All Data

To get all data (discussions, issues, or pull requests):

```bash
./query-discussions.sh --jq '.'
```

### With Repository

To query a specific repository:

```bash
./query-discussions.sh --repo owner/repo
```

### With jq Filtering

Use the `--jq` argument to filter and transform the output for discussions, issues, or pull requests:

#### Discussions

```bash
# Get discussion numbers and titles
./query-discussions.sh --jq '.[] | {number, title}'

# Get discussions by a specific author
./query-discussions.sh --jq '.[] | select(.author.login == "username")'
```

#### Issues

```bash
# Get only open issues
./query-issues.sh --jq '.[] | select(.state == "OPEN")'

# Get issue numbers and titles
./query-issues.sh --jq '.[] | {number, title}'
```

#### Pull Requests

```bash
# Get only open PRs
./query-prs.sh --jq '.[] | select(.state == "open")'

# Get PR numbers and titles
./query-prs.sh --jq '.[] | {number, title}'
```

### Common Options

- `--limit`: Maximum number of items to fetch (discussions, issues, or PRs). Default: 30
- `--repo`: Repository in owner/repo format. Default: current repo
- `--jq`: (Optional) jq expression for filtering/transforming output. If omitted, returns schema info

### Example Queries

**Find discussions with many comments:**
```bash
./query-discussions.sh --jq '.[] | select(.comments.totalCount > 5) | {number, title, comments: .comments.totalCount}'
```

**Get issues assigned to someone:**
```bash
./query-issues.sh --jq '.[] | select(.assignees | length > 0) | {number, title, assignees: [.assignees[].login]}'
```

**Find large PRs (many changed files):**
```bash
./query-prs.sh --jq '.[] | select(.changedFiles > 10) | {number, title, changedFiles}'
```

## Output Format

The script outputs JSON by default, making it easy to pipe through jq for additional processing.

## Requirements

- GitHub CLI (`gh`) authenticated
- `jq` for filtering (installed by default on most systems)