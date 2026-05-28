# Technical Notes: Why Git Bash Works

## The Problem

Windows reserves certain filenames as MS-DOS device names:
- `NUL` - Null device
- `CON` - Console
- `PRN` - Printer  
- `AUX` - Auxiliary
- `COM1-9` - Serial ports
- `LPT1-9` - Parallel ports

These files:
- Cannot be deleted using Windows Explorer
- Cannot be deleted using PowerShell `Remove-Item`
- Cannot be deleted using CMD `del` command
- Cannot be deleted using Python `os.remove()`
- Block OneDrive synchronization
- Are case-insensitive and apply with or without extensions

## The Solution

Git Bash uses a Cygwin/MSYS2 POSIX layer that:
- Bypasses Windows reserved name filter
- Uses Unix system calls instead of Windows API
- Treats "nul" as a regular filename
- No special UNC paths or tricks needed

The Unix `rm` command doesn't check for Windows reserved names, allowing successful deletion.

## Performance Metrics

- **Targeted search:** ~3 seconds (15-20 recent directories)
- **Full directory scan:** 1-2 minutes (entire OneDrive tree)
- **Deletion:** <1 second per file
- **OneDrive restart:** 2 seconds

## Safety Considerations

- Deletion is permanent (no recycle bin)
- Always verify file paths before deletion
- Never automatic - requires explicit execution
- OneDrive sync required after deletion
