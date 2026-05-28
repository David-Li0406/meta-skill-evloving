# VSCode CLI Basics

Core syntax and essential usage for opening files at specific positions.

## Primary Command: `-g` / `--goto`

**Syntax:**
```bash
code -g <file:line[:character]>
code --goto <file:line[:character]>
```

**Format:**
- `file` - Absolute or relative file path
- `line` - Line number (1-indexed, first line is 1)
- `character` - Optional column position (0-indexed, first column is 0)

## Basic Examples

### Line Only
```bash
# Open file at line 10
code -g myfile.js:10

# Open file at line 42
code -g src/app.js:42
```

### Line and Column
```bash
# Open at line 10, column 5
code -g myfile.js:10:5

# Open at line 42, column 15
code -g src/index.ts:42:15
```

### Shorthand (No Flag)
```bash
# The -g flag is optional
code myfile.js:10
code src/app.js:42:10
```

## Line and Column Numbering

**Lines are 1-indexed:**
- Line 1 is the first line
- Line 10 is the tenth line

**Columns are 0-indexed:**
- Column 0 is the first character
- Column 10 is the eleventh character

**Example:**
```bash
# Line 5, column 0 (first character of line 5)
code -g file.js:5:0

# Line 5, column 10 (eleventh character of line 5)
code -g file.js:5:10
```

## Path Handling

### Relative Paths
```bash
# Resolves from current working directory
code -g src/app.js:42
code -g ../other-project/file.js:10
```

### Absolute Paths
```bash
# Always reliable, no dependency on current directory
code -g /home/user/project/src/app.js:42
code -g /Users/mae/Documents/code/main.py:100
```

### Paths with Spaces
```bash
# Must be quoted (single or double quotes)
code -g "my project/src/app.js:42"
code -g 'path with spaces/file.js:10'

# Unquoted will fail
code -g my project/src/app.js:42  # ❌ Error
```

## Non-existent Files

VSCode will create an empty file if the path doesn't exist:

```bash
# If newfile.js doesn't exist, VSCode creates it
code -g newfile.js:10

# Cursor will be at line 10 when user starts editing
```

## Full `code --help` Reference

```
Usage: code [options] [paths...]

Options
  -g --goto <file:line[:character]> Open a file at the path on the specified
                                    line and character position.
  -n --new-window                   Force to open a new window.
  -r --reuse-window                 Force to open in already opened window.
  -w --wait                         Wait for files to be closed before returning.
  -d --diff <file> <file>           Compare two files.
  -m --merge <path1> <path2> <base> <result>
                                    Perform a three-way merge.
  --profile <profileName>           Opens with the given profile.
  --user-data-dir <dir>             Specifies user data directory.
  -h --help                         Print usage.
```
