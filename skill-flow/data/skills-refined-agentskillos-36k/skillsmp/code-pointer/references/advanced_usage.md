# Advanced VSCode CLI Usage

Window control, multiple files, and advanced features.

## Opening Multiple Files

```bash
# Open multiple files at different positions
code -g file1.js:10 -g file2.js:20 -g file3.py:100

# Mix different files and positions
code -g src/main.ts:1:1 -g src/types.ts:50:0 -g README.md:1
```

Each `-g` flag opens a separate file at its specified position.

## Window Control

### New Window (-n)
```bash
# Force opening in brand new VSCode window
code -n -g file.js:10

# Useful when you don't want to disturb current work
code -n -g important.js:42
```

### Reuse Window (-r)
```bash
# Opens in existing VSCode window as new tab
code -r -g file.js:10

# Default behavior without -n flag
code -g file.js:10  # Opens in existing window by default
```

### Wait for Close (-w)
```bash
# Shell waits until user closes the file
code -w -g file.js:10

# Useful for git commit messages, etc.
git config core.editor "code -w"
```

## Diff View

```bash
# Open side-by-side diff comparison
code -d original.js modified.js

# Compare two versions of a file
code -d old-version.py new-version.py
```

## Merge Editor

```bash
# Open three-way merge editor
code -m modified1.js modified2.js common.js result.js

# Useful for resolving merge conflicts
```

## Add to Workspace

```bash
# Adds folder to current workspace
code -a /path/to/folder

# Add multiple folders
code -a /path/one -a /path/two
```

## Profile and Data Directory

### Open with Profile
```bash
# Uses specific VSCode profile settings
code --profile my-profile -g src/index.ts:42

# Useful for different development environments
code --profile python-dev -g main.py:10
```

### Custom Data Directory
```bash
# Uses isolated VSCode instance with separate settings
code --user-data-dir /tmp/vscode-instance -g file.js:10

# Useful for testing or isolated environments
```

## Combining Options

```bash
# New window with multiple files
code -n -g file1.js:10 -g file2.js:20

# Reuse window and wait
code -r -w -g file.js:10

# Profile with specific file position
code --profile work -g project/src/app.js:42:10
```

## URL Scheme Alternative

**Syntax:**
```
vscode://file/{absolute_path}:line:column
```

**Usage:**
```bash
# Can be used in shell as URI
xdg-open "vscode://file//home/user/project/main.js:5:10"

# Useful for integration with web apps or other tools
```

**Requirements:**
- Full absolute paths required
- File must be on local filesystem
- VSCode must be registered as URI handler (automatic on install)
