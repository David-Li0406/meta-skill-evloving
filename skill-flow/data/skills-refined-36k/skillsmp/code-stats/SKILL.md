---
name: code-stats
description: Analyze code statistics including line counts, language distribution, and directory complexity. Use when the user asks to count lines of code, analyze code size, show language distribution, or compare code statistics. This skill provides fast line counting with zero dependencies, grouping by language or directory, and Markdown table output.
---

# Code Statistics

Analyze codebases to understand line counts, language distribution, and directory structure.

## Purpose

Generate comprehensive code statistics for repositories:

- **Line counts**: Code, blank, and comment lines
- **Language distribution**: Group statistics by programming language
- **Directory analysis**: Understand code organization and complexity
- **Filtered counting**: Focus on specific file types

## Quick Start

### Basic Usage

Count all code in the current directory:

```bash
python scripts/count.py --path .
```

Output:

```markdown
## Summary

- **Total Files**: 156
- **Code Lines**: 8,234
- **Blank Lines**: 412
- **Comment Lines**: 1,023
- **Total Lines**: 9,669
- **Comment Ratio**: 12.4%

| Language | Files | Code | Blank | Comment | Total |
|----------|-------|------|-------|---------|-------|
| Rust     | 156   | 8234 | 412   | 1023    | 9669  |
```

### Count Specific Languages

```bash
# Count only Rust files
python scripts/count.py --path . --extensions rs

# Count Rust and Python files
python scripts/count.py --path . --extensions rs,py

# Count web frontend files
python scripts/count.py --path . --extensions js,ts,html,css
```

### Group by Directory

```bash
# Analyze directory structure
python scripts/count.py --path . --group-by directory

# Show deeper directory nesting
python scripts/count.py --path . --group-by directory --depth 3
```

Output:

```markdown
| Directory   | Files | Code | Comment | Languages         |
|-------------|-------|------|---------|-------------------|
| src/        | 89    | 5621 | 789     | Rust              |
| examples/   | 34    | 1234 | 234     | Rust, Python      |
| tests/      | 33    | 1379 | 0       | Rust              |
```

## Command Reference

```bash
python scripts/count.py [OPTIONS]

Options:
  --path PATH           Root directory to scan (default: .)
  --extensions EXTS     Comma-separated file extensions (e.g., "rs,py,js")
  --group-by MODE       Group by: language|directory (default: language)
  --depth N             Directory depth for grouping (default: 2)
```

## Examples

### Analyze Rust Project

```bash
cd /path/to/rust-project
python ~/.claude/skills/code-stats/scripts/count.py --path . --extensions rs
```

### Compare Backend vs Frontend

```bash
# Backend code
python scripts/count.py --path backend --extensions rs,go,java

# Frontend code
python scripts/count.py --path frontend --extensions js,ts,css,html
```

### Chapter-by-Chapter Analysis (for rust-roadmap)

```bash
# Analyze specific chapter
python scripts/count.py --path 01-basics --group-by language

# Compare all chapters
for dir in */; do
  echo "## $dir"
  python scripts/count.py --path "$dir" --extensions rs
done
```

### Find Largest Directories

```bash
python scripts/count.py --path . --group-by directory --depth 1
```

## Language Detection

The skill automatically detects languages from file extensions:

| Extension | Language |
|-----------|----------|
| `.rs`     | Rust     |
| `.py`     | Python   |
| `.js`     | JavaScript |
| `.ts`     | TypeScript |
| `.c`      | C        |
| `.cpp`    | C++      |
| `.java`   | Java     |
| `.go`     | Go       |
| `.html`   | HTML     |
| `.css`    | CSS      |
| `.json`   | JSON     |
| `.yaml`   | YAML     |
| `.toml`   | TOML     |
| `.md`     | Markdown |

See `references/customization.md` to add new languages.

## How It Works

### Line Counting

For each file, the script:

1. Detects the programming language from the file extension
2. Reads the file line by line
3. Classifies each line as:
   - **Blank**: Empty or whitespace only
   - **Comment**: Matches language-specific comment patterns
   - **Code**: Everything else

### Comment Detection

Language-aware comment detection:

- **Line comments**: `//`, `#`, etc.
- **Block comments**: `/* */`, `""" """`, `<!-- -->`, etc.
- **Multi-line blocks**: Tracked across lines

### Automatic Filtering

The script automatically skips:

- Binary directories: `.git`, `target`, `node_modules`, `__pycache__`
- Binary files: `.png`, `.jpg`, `.pdf`, `.exe`, etc.
- Files that can't be decoded as UTF-8

## Output Format

### Summary Section

```markdown
## Summary

- **Total Files**: 156
- **Code Lines**: 8,234
- **Blank Lines**: 412
- **Comment Lines**: 1,023
- **Total Lines**: 9,669
- **Comment Ratio**: 12.4%
```

### Language Table

Shows statistics grouped by language, sorted by total lines.

### Directory Table

Shows statistics grouped by directory, including:
- File count
- Code and comment lines
- Languages present in that directory

## Common Use Cases

### Understand Codebase Size

```bash
# Quick overview
python scripts/count.py --path .

# Detailed breakdown
python scripts/count.py --path . --group-by directory --depth 3
```

### Measure Comment Coverage

Check the comment ratio in the summary to assess code documentation.

### Focus on Specific File Types

```bash
# Just source code (exclude configs, docs)
python scripts/count.py --path . --extensions rs,py,js,go

# Just documentation
python scripts/count.py --path . --extensions md,rst,tex
```

### Analyze Project Structure

```bash
# See which directories have the most code
python scripts/count.py --path . --group-by directory --depth 1
```

## Troubleshooting

### "No files found to analyze"

- Check that the path is correct
- Ensure you have read permissions
- Try removing the `--extensions` filter to see all files

### "Permission denied" warnings

The script will skip files it can't read and continue with other files. Warnings are printed to stderr.

### Incorrect language detection

See `references/customization.md` to add custom language mappings.

### Comment counting seems wrong

Comment detection is language-specific. Check that:
- The file extension is correct
- The language is supported (see full list in `scripts/utils/language.py`)
- For custom languages, add comment patterns (see `references/customization.md`)

## Customization

To add new languages or customize comment patterns, see [customization.md](references/customization.md).

## Performance

- **Fast**: Uses standard library only, no external dependencies
- **Efficient**: Single-pass line counting
- **Scalable**: Tested on codebases with 10,000+ files

Typical performance:
- Small project (< 100 files): < 1 second
- Medium project (< 1,000 files): 1-3 seconds
- Large project (< 10,000 files): 5-15 seconds

## Limitations

Current MVP limitations:

- **No .gitignore support**: All files are scanned (except binary directories)
- **10 core languages**: Rust, Python, JS/TS, C/C++, Java, Go, HTML, CSS, JSON, YAML
- **Markdown output only**: No JSON/CSV export (yet!)
- **Single repository**: No branch comparison

See "Future Enhancements" below.

## Future Enhancements

Planned features for post-MVP:

- `.gitignore` support for respecting project conventions
- Polars integration for statistical analysis
- Git branch comparison
- JSON/CSV export formats
- 40+ language support
- Custom filtering rules

## Technical Details

### Zero Dependencies

The core `count.py` script uses only Python standard library:

- `pathlib`: Path handling
- `os`: Directory walking
- `argparse`: CLI parsing

No external packages required!

### File Detection Algorithm

1. Walk directory tree with `os.walk()`
2. Skip known binary directories
3. Check file extension against binary types
4. Read first 1KB to check for null bytes
5. Try UTF-8 decode to verify text file
6. Process file if all checks pass

### Comment Detection Algorithm

```python
for line in file:
    if in_block_comment:
        if line contains block_end:
            in_block_comment = False
        comment_lines += 1
        continue

    if line is blank:
        blank_lines += 1
        continue

    if line starts with line_comment:
        comment_lines += 1
        continue

    if line starts with block_start:
        in_block_comment = True
        comment_lines += 1
        continue

    code_lines += 1
```

## Examples from rust-roadmap

### Analyze Current Chapter

```bash
# In 14-smart-pointers/
python .claude/skills/code-stats/scripts/count.py --path . --extensions rs
```

### Compare All Chapters

```bash
# From rust-roadmap root
for dir in */; do
  if [ -f "$dir/Cargo.toml" ]; then
    echo "## $dir"
    python .claude/skills/code-stats/scripts/count.py --path "$dir" --extensions rs
    echo ""
  fi
done
```

### Track Progress Over Time

```bash
# Save baseline
python .claude/skills/code-stats/scripts/count.py --path . > baseline.md

# After changes
python .claude/skills/code-stats/scripts/count.py --path . > current.md

# Compare manually or use diff
diff baseline.md current.md
```
