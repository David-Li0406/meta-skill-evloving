# Troubleshooting VSCode CLI

Common issues, error messages, and solutions.

## Command Not Found

**Error:** `bash: code: command not found`

**Cause:** VSCode CLI not installed in PATH

**Solution:**
1. Open VSCode
2. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
3. Run: "Shell Command: Install 'code' command in PATH"
4. Restart terminal

**Verify installation:**
```bash
which code
# Should output: /usr/local/bin/code (or similar)
```

## Wrong Line/Column Position

**Problem:** Cursor not at expected position

**Causes:**
- Line numbers are 1-indexed (line 1 is first line, not 0)
- Column numbers are 0-indexed (column 0 is first character)
- Verify your line/column counting

**Examples:**
```bash
# First line, first character
code -g file.js:1:0  # ✓ Correct
code -g file.js:0:0  # ❌ Goes to line 1 anyway

# Fifth line, eleventh character
code -g file.js:5:10  # ✓ Correct
code -g file.js:5:11  # ❌ Off by one
```

## File Opens But Position Ignored

**Problem:** File opens but cursor is at wrong location

**Possible Causes:**

1. **Syntax Error:**
```bash
code -g file.js 42      # ❌ Missing colon
code -g file.js:42      # ✓ Correct
```

2. **File Doesn't Exist:**
```bash
# Check file exists first
[[ -f "file.js" ]] && code -g file.js:42
```

3. **Line/Column Out of Bounds:**
```bash
# If file has 50 lines and you specify line 100,
# cursor moves to last line instead
code -g file.js:100  # Goes to line 50 (last line)
```

## Path Not Found

**Problem:** `Error: Unable to resolve nonexistent file`

**Causes:**

1. **Relative Path from Wrong Directory:**
```bash
# Current dir: /home/user/
code -g project/src/app.js:42  # ✓ Works if project/src/app.js exists

# Current dir: /home/user/other/
code -g project/src/app.js:42  # ❌ Fails - wrong directory
```

2. **Spaces Not Quoted:**
```bash
code -g my project/file.js:10  # ❌ Fails
code -g "my project/file.js:10"  # ✓ Works
```

**Solution:** Use absolute paths
```bash
ABS_PATH="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
code -g "$ABS_PATH:42"
```

## Multiple Windows Opening

**Problem:** Too many VSCode windows opening unexpectedly

**Cause:** Using `-n` flag repeatedly

**Solutions:**
```bash
# Use -r to reuse existing window
code -r -g file.js:10

# Or omit -n flag (reuses window by default)
code -g file.js:10
```

## Column Position Beyond Line Length

**Problem:** Specified column exceeds actual line length

**Behavior:** Cursor moves to end of line instead

**Example:**
```bash
# Line 10 has 30 characters
code -g file.js:10:50  # Goes to column 30 (end of line)
```

**Not an Error:** This is expected behavior, VSCode handles it gracefully

## File Opens in Wrong VSCode Instance

**Problem:** File opens in unexpected VSCode window

**Solutions:**

1. **Force New Window:**
```bash
code -n -g file.js:10
```

2. **Specify Profile:**
```bash
code --profile my-profile -g file.js:10
```

3. **Use Specific Data Directory:**
```bash
code --user-data-dir ~/.vscode-work -g file.js:10
```

## Asynchronous Opening Issues

**Problem:** Script continues before file is open

**Behavior:** `code` command returns immediately, file may not be fully opened

**Solutions:**

1. **Use `-w` flag to wait:**
```bash
code -w -g file.js:10
# Script waits until user closes file
```

2. **Add delay if needed:**
```bash
code -g file.js:10
sleep 1  # Give VSCode time to open
```

## Permission Denied

**Problem:** `Error: EACCES: permission denied`

**Causes:**
- File doesn't have read permissions
- Directory doesn't have execute permissions

**Solutions:**
```bash
# Check file permissions
ls -l file.js

# Fix if needed
chmod 644 file.js  # Read/write for owner, read for others
chmod 755 directory/  # Execute permission for directory
```

## VSCode Opens But Shows Error

**Problem:** VSCode opens but displays error about file

**Common Errors:**

1. **"Unable to open file"** - File path is incorrect
2. **"File is a directory"** - Path points to directory, not file
3. **"Binary file"** - File is not a text file

**Validation Before Opening:**
```bash
if [[ -f "$FILE_PATH" ]]; then
    code -g "$FILE_PATH:$LINE"
else
    echo "Error: Not a file: $FILE_PATH"
fi
```
