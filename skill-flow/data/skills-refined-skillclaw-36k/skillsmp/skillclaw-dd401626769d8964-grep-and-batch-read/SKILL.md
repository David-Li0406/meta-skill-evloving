---
name: grep-and-batch-read
description: Use this skill to efficiently find and read multiple files matching a pattern in a single operation, significantly reducing time and resource usage during codebase exploration.
---

# Skill body

**Purpose**: Search for a pattern and read all matching files in a single coordinated operation, eliminating the need for sequential round-trips.

**Performance**: Achieve 50-70% time savings and reduce token usage compared to traditional methods.

## When to Use This Skill
- Exploring a codebase for specific functionality.
- Finding all files containing a particular pattern.
- Researching implementation approaches or investigating errors across multiple files.
- Gathering context for code changes or reviewing similar functionalities.

## Anti-Pattern This Skill Replaces

### Inefficient Pattern
```
1. Grep "FormattingRule" -> returns 5 files
2. Read each file sequentially
```
**Impact**: Multiple round-trips leading to significant delays.

### Efficient Pattern
```
1. Execute grep-and-batch-read pattern="FormattingRule" max_files=5
2. Grep finds matches and reads all matching files in parallel
```
**Impact**: Single round-trip with consolidated output.

## Skill Parameters

| Parameter        | Required | Default | Description                                      |
|------------------|----------|---------|--------------------------------------------------|
| `pattern`        | Yes      | -       | Grep pattern to search for (regex supported)    |
| `path`           | No       | `.`     | Directory to search in                           |
| `glob`           | No       | -       | File type filter (e.g., "*.java", "*.md")      |
| `max_files`      | No       | 5       | Maximum number of files to read                  |
| `context_lines`  | No       | 100     | Lines to read per file (0 = all)                |
| `case_sensitive` | No       | true    | Case-sensitive search                            |

## Skill Workflow

### Step 1: Search for Pattern
Use the Grep tool to find all files containing the pattern:

```bash
# Search for pattern with optional filters
Grep: pattern="{pattern}"
  path="{path}"
  glob="{glob}"
  output_mode="files_with_matches"
  -i={!case_sensitive}
```

**Example**:
```bash
Grep: pattern="FormattingRule"
  path="/path/to/project"
  glob="*.java"
  output_mode="files_with_matches"
```

**Output**: List of file paths

### Step 2: Read Matching Files
Read the contents of the matching files:

```bash
# Read each file with line numbers
for f in $(grep -rl "{pattern}" {path} --include="{glob}" | head -{max_files}); do
  echo "=== $f ==="
  cat -n "$f" | head -{context_lines}
done
```

This skill allows for efficient exploration of codebases by reducing the number of necessary interactions and speeding up the process of gathering information from multiple files.