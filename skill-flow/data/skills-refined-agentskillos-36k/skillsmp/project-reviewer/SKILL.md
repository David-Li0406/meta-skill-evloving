---
name: project-reviewer
description: Scan entire Python project directories and review all .py files for Clean Code principles. Use when the user requests project-wide code review with /review-project command, wants to analyze multiple files, or needs to identify which files need refactoring most. Requires MCP tools list_directory and read_file.
user-invocable: true
allowed-tools:
  - list_directory
  - read_file
---

# Project Reviewer

Automated project-wide code review tool that scans Python projects and identifies files needing refactoring based on Clean Code principles.

## Quick Start

When triggered by `/review-project <directory_path>`, this skill will:
1. Recursively scan the directory for all `.py` files
2. Apply Clean Code checks to each file
3. Generate an integrated report sorted by file path

## Required MCP Tools

This skill requires the following MCP tools to be available:
- `list_directory` - For directory traversal and file discovery
- `read_file` - For reading Python file contents

If these tools are not available, the skill will fail with an error message.

## Workflow

### Step 1: Directory Scanning

Use `list_directory` tool recursively to discover all `.py` files:

1. Start with the provided directory path
2. List all entries in the directory
3. For each entry:
   - If it's a `.py` file, add to the review queue
   - If it's a subdirectory, recursively scan it
4. Skip common directories: `__pycache__`, `.git`, `.venv`, `venv`, `node_modules`, `.pytest_cache`

### Step 2: File Review

For each Python file found, use `read_file` tool and apply Clean Code checks:

**Variable Naming Check:**
- Single letter names (except i, j, k in loops)
- Unclear abbreviations (d, tmp, val, etc.)
- Non-descriptive names (data, info, obj)
- Names not revealing intent (flag, check)

**Function Length Check:**
- Target: Maximum 20 lines (excluding blank lines and docstrings)
- Flag functions exceeding this limit

**Redundant Comments Check:**
- Comments repeating what code clearly states
- Comments explaining obvious operations
- Comments that could be replaced by better naming

See [clean-code-rules.md](references/clean-code-rules.md) for detailed checking criteria.

### Step 3: Generate Integrated Report

Produce a comprehensive report with:

1. **Executive Summary**
   - Total files scanned
   - Total issues found
   - Top 3 files needing refactoring (by issue count)

2. **Detailed Results** (sorted by file path)
   - File path
   - Issue counts by category (naming, length, comments)
   - Specific issues with line numbers

3. **Recommendations**
   - Priority ranking for refactoring
   - Common patterns observed across files

## Report Format

```
=== Project Code Review Report ===

Executive Summary:
- Files Scanned: 15
- Total Issues: 47
- Top 3 Files Needing Refactoring:
  1. src/utils/helper.py (12 issues)
  2. src/main.py (9 issues)
  3. tests/test_api.py (8 issues)

=== Detailed Results ===

File: src/main.py (9 issues)
├─ Variable Naming (4):
│  ├─ Line 12: 'd' -> Use descriptive name
│  ├─ Line 25: 'tmp' -> Rename to indicate purpose
│  ├─ Line 40: 'x' -> Use meaningful name
│  └─ Line 55: 'flag' -> Use descriptive boolean name
├─ Function Length (2):
│  ├─ process_data() (lines 30-55): 26 lines
│  └─ handle_request() (lines 60-85): 26 lines
└─ Redundant Comments (3):
   ├─ Line 10: "// Set name" - Remove
   ├─ Line 35: "// Loop through items" - Remove
   └─ Line 70: "// Return result" - Remove

File: src/utils/helper.py (12 issues)
[... similar format ...]

=== Recommendations ===

Priority 1 - Critical (>10 issues):
- src/utils/helper.py: Heavy refactoring needed

Priority 2 - High (6-10 issues):
- src/main.py: Focus on variable naming and function splitting
- tests/test_api.py: Improve test function names

Priority 3 - Medium (3-5 issues):
- src/api/routes.py: Minor improvements needed

Priority 4 - Low (1-2 issues):
- src/config.py: Minimal changes required

Common Patterns:
- Frequent use of single-letter variables across 8 files
- Long functions (>20 lines) found in 5 files
- Redundant comments in 10 files
```

## Error Handling

Handle common errors gracefully:

- **Directory not found**: Display clear error message with the attempted path
- **No .py files found**: Report that the directory contains no Python files
- **File read errors**: Skip the file and note it in the report
- **MCP tools unavailable**: Fail fast with clear message about missing tools

## Performance Considerations

For large projects (>100 files):
- Process files in batches
- Provide progress updates
- Consider offering to focus on specific subdirectories

## Integration with clean-code-reviewer

This skill uses the same checking logic as clean-code-reviewer but applies it across multiple files. The rules are consistent:

- Python: 20 line function limit
- Same variable naming conventions
- Same comment redundancy criteria

For language-specific Python rules, refer to the clean-code-reviewer skill's Python guidelines.
