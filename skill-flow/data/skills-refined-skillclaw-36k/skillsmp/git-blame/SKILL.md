---
name: git-blame
description: Show line-by-line authorship information for a file. Returns the commit hash, author, and date for each line.
allowed-tools: Bash
metadata:
  category: git
  version: 1.0.0
---

# Git Blame Skill

This skill shows line-by-line authorship information for a file, revealing who last modified each line and when.

## Usage

The git-blame skill analyzes a file and returns authorship information for each line, with optional line range filtering.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| path | string | Yes | - | File path to blame |
| start_line | int | No | 1 | Starting line number (1-indexed) |
| end_line | int | No | - | Ending line number (inclusive) |

### Example Usage

Blame an entire file:
```
Show blame for /src/main.go
```

Blame specific lines:
```
Show blame for lines 10-20 of /src/auth.go
```

### Result Format

The blame result includes:

For each line:
- Line number (1-indexed)
- Commit hash that last modified this line
- Author name
- Author email
- Timestamp of the modification
- Line content

Summary statistics:
- Unique authors count
- Unique commits count

### Line Information Fields

| Field | Description |
|-------|-------------|
| line_number | 1-indexed line number |
| commit_hash | Hash of commit that last changed this line |
| author | Name of the author |
| author_email | Author's email address |
| author_time | When the line was last modified |
| content | The actual line content |

### Use Cases

1. **Find code ownership**: Identify who wrote specific code
2. **Track bug origins**: Find when a problematic line was introduced
3. **Review history**: Understand how code evolved
4. **Contact experts**: Find who to ask about specific code
5. **Code review**: See recent changes in context

### Best Practices

1. Use line ranges for large files to focus on relevant sections
2. Cross-reference commit hashes with git-log for full context
3. Check unique authors to understand code ownership patterns
4. Use for debugging to find when issues were introduced
5. Combine with git-log to trace the full history of changes

### Interpreting Results

- Multiple unique commits suggests the code evolved over time
- Single commit for all lines indicates recently added code
- Single author suggests concentrated ownership
- Many authors suggests collaborative development
