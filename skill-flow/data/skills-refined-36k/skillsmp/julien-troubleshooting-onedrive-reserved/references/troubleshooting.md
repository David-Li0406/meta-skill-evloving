# Troubleshooting Guide

## Git Bash Not Found

**Symptom:** `bash: command not found` or similar error

**Solution:**
```bash
# Install Git for Windows (includes Git Bash)
# Download: https://git-scm.com/download/win
```

## Search Taking Too Long

**Symptom:** Full directory scan exceeds 2 minutes

**Solutions:**
1. Use targeted search in recent directories first
2. Limit search depth:
   ```bash
   find "path" -maxdepth 3 -type f \( -iname "nul" \) 2>/dev/null
   ```
3. Use bundled script with targeted mode:
   ```bash
   bash scripts/find_reserved_names.sh "/path/to/search" targeted
   ```

## Permission Denied

**Symptom:** `rm: cannot remove 'file': Permission denied`

**Solution:**
```bash
# Stop OneDrive first
powershell.exe -Command "Stop-Process -Name OneDrive -Force"

# Wait a moment
sleep 2

# Retry deletion
rm -f "/path/to/file"
```

## OneDrive Sync Error Persists

**Symptom:** OneDrive still shows sync errors after deletion

**Solutions:**
1. Wait 5-10 minutes for OneDrive to complete synchronization
2. Verify no remaining reserved files exist
3. Restart OneDrive manually again:
   ```bash
   powershell.exe -Command "Stop-Process -Name OneDrive -Force"
   powershell.exe -Command "Start-Process 'C:\Program Files\Microsoft OneDrive\OneDrive.exe'"
   ```
4. Check OneDrive system tray icon for sync status
5. Restart computer if issue persists

## File Still Appears After Deletion

**Symptom:** File shows in directory listing after `rm -f`

**Possible causes:**
1. OneDrive is still holding file lock
2. Insufficient permissions
3. File is actually a directory, not a file

**Solution:**
```bash
# Verify it's truly gone
ls -la "/path/to/directory/" | grep -i nul

# If still present, close all applications and retry
powershell.exe -Command "Stop-Process -Name OneDrive -Force"
rm -f "/path/to/file"
```

## Common Path Issues

**Symptom:** `No such file or directory` errors

**Common mistakes:**
- Using backslashes `\` instead of forward slashes `/`
- Missing quotes around paths with spaces
- Using `C:\` instead of `/c/`

**Correct format:**
```bash
# ✅ Correct
rm -f "/c/Users/username/OneDrive/Coding/My Project/nul"

# ❌ Incorrect
rm -f C:\Users\username\OneDrive\Coding\My Project\nul
rm -f /c/Users/username/OneDrive/Coding/My Project/nul  # Missing quotes!
```
