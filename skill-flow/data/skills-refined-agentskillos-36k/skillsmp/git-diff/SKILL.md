---
name: git-diff
description: Show changes between two commits or between a commit and the working tree. Returns file-by-file diff information including additions, deletions, and change hunks.
allowed-tools: Bash
metadata:
  category: git
  version: 1.0.0
---

# Git Diff Skill

This skill shows changes between two commits or between a commit and the working tree, providing detailed diff information for each changed file.

## Usage

The git-diff skill compares two points in the repository history and returns detailed information about what changed.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| from_commit | string | Yes | - | Starting commit reference (hash, branch, tag, HEAD~n) |
| to_commit | string | No | HEAD | Ending commit reference |
| path | string | No | - | Filter diff to specific file or directory |

### Commit References

You can use various formats for commit references:
- Full commit hash: `abc123def456...`
- Short hash: `abc123`
- Branch name: `main`, `feature/auth`
- Tag: `v1.0.0`
- Relative: `HEAD~1`, `HEAD~3`
- Range: Compare between any two references

### Example Usage

Show changes in the last commit:
```
Show diff from HEAD~1 to HEAD
```

Show changes between branches:
```
Show diff from main to feature/auth
```

Show changes for a specific file:
```
Show diff from HEAD~5 to HEAD for path /src/main.go
```

### Result Format

The diff result includes:
- List of changed files with:
  - File path (and old path if renamed)
  - Status (A=Added, M=Modified, D=Deleted, R=Renamed)
  - Number of additions and deletions
  - Change hunks with line numbers
- Total additions across all files
- Total deletions across all files

### Status Codes

| Code | Meaning |
|------|---------|
| A | Added - New file |
| M | Modified - Existing file changed |
| D | Deleted - File removed |
| R | Renamed - File moved/renamed |
| C | Copied - File copied |

### Best Practices

1. Use relative references (HEAD~n) for recent changes
2. Filter by path for large diffs
3. Compare against main/master to see feature changes
4. Check both additions and deletions for context
