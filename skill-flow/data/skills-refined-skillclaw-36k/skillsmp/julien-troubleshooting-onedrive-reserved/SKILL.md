---
name: julien-troubleshooting-onedrive-reserved
description: This skill should be used when the user reports OneDrive sync errors caused by Windows reserved filenames (NUL, CON, PRN, AUX, COM1-9, LPT1-9). It efficiently locates and removes these undeletable files using Git Bash.
tags: [windows, onedrive, troubleshooting, files]
version: 3.0.0
---

# Delete Windows Reserved Names

## Workflow

### Step 1: Search for Reserved Files

Use `fd` for ultra-fast search (5-10x faster than find):

```bash
# Search reserved names (nul, null, con, prn, aux)
fd -t f -i "^(nul|null|con|prn|aux)$" "/c/Users/$USER/OneDrive/Coding/_Projets de code"

# Search short names (0-1 character)
fd -t f "^.$" "/c/Users/$USER/OneDrive/Coding/_Projets de code"
```

**Alternative:** Use bundled script `scripts/find_reserved_names.sh` for automated search.

### Step 2: Display Results

Report findings to user:
- Total count
- Full paths
- Comparison with OneDrive's reported count

### Step 3: Delete Files

Execute deletion with `fd` + `xargs` + `rm -f`:
```bash
# Delete reserved names
fd -t f -i "^(nul|null|con|prn|aux)$" "/c/Users/$USER/OneDrive/Coding/_Projets de code" -0 | xargs -0 -I{} rm -f '{}'

# Delete short names (0-1 char)
fd -t f "^.$" "/c/Users/$USER/OneDrive/Coding/_Projets de code" -0 | xargs -0 -I{} rm -f '{}'
```

Or delete individual files:
```bash
rm -f "/c/Users/$USER/path/to/file"
```

### Step 4: Restart OneDrive

Execute OneDrive restart command:
```bash
powershell.exe -Command "Stop-Process -Name OneDrive -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; Start-Process 'C:\Program Files\Microsoft OneDrive\OneDrive.exe'"
```

### Step 5: Confirm Completion

Report to user:
- Number of files deleted
- OneDrive restart status
- Expected wait time (2-5 minutes)

## Key Requirements

- Git Bash installed (https://git-scm.com/download/win)
- Use forward slashes `/` in all paths
- Quote paths containing spaces
- Use `$USER` variable for dynamic username

## Bundled Resources

- `scripts/find_reserved_names.sh` - Automated search script with targeted/full modes
- `references/technical-notes.md` - Technical explanation of why Git Bash works
- `references/troubleshooting.md` - Common issues and solutions
- `../../README.md` - Complete user documentation
- `../../delete-nul-gitbash.sh` - Interactive deletion script (alternative)
