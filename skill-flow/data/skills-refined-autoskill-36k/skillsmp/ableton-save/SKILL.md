---
name: ableton-save
description: This skill should be used when the user asks to "save the ableton project", "save ableton live", "save the current live set", or mentions saving Ableton Live projects to a specific path. Provides automated saving functionality for Ableton Live on macOS using AppleScript.
version: 1.0.0
---

# Ableton Live Save Automation

This skill provides automated saving functionality for Ableton Live projects on macOS using AppleScript and Python integration. When users need to save their current Ableton Live project to a specific location, this skill handles the automation by navigating to the target directory and entering the filename.

## Purpose

Enable users to save Ableton Live projects through natural language commands or explicit slash commands. The skill uses AppleScript automation to interact with Ableton Live's Save As dialog, navigating to directories and entering filenames automatically.

## When to Use

Trigger this skill when users:
- Ask to save the current Ableton Live project
- Specify a save path for their Live set
- Want to automate saving as part of a workflow
- Need to create backups with specific paths

## How to Save

### Using Natural Language

When a user asks to save an Ableton project with a path like:

> "Save the ableton project to ~/Music/Projects/song.als"
> "Save my live set to ../backups/test.als"

Execute the save command with the specified path:

1. Extract the file path from the user's request
2. Run: `/ableton-save:save-live-set <path>`
3. The script will open Ableton Live's Save As dialog
4. Navigate to the target directory automatically
5. Enter the filename automatically
6. Instruct the user to press Enter to complete

### Path Handling

- Accept both absolute and relative paths
- The `.als` extension is optional
- Ableton Live creates a project folder automatically
- The filename field is populated with the base name

### Error Handling

- If Ableton Live is not running, show: "Error: Ableton Live is not running"
- If the path is invalid, the dialog still opens but without navigation
- This functionality requires macOS with AppleScript support

## Implementation

The save functionality is implemented through:

1. **Python wrapper** (`scripts/ableton_save.py`)
   - Handles path conversion and argument formatting
   - Splits paths into directory and filename components
   - Executes the AppleScript

2. **AppleScript** (`scripts/save_ableton_project.scpt`)
   - Activates Ableton Live
   - Opens Save As dialog (Cmd+Shift+S)
   - Navigates to directory using Cmd+Shift+G
   - Enters filename using Cmd+A + text entry

## Quick Reference

| User Query | Action |
|------------|--------|
| "Save to /path/to/file.als" | Execute `/ableton-save:save-live-set /path/to/file.als` |
| "Save the project" | Ask for destination path |
| "Backup to foo.als" | Execute `/ableton-save:save-live-set foo.als` |

## Requirements

- macOS operating system
- Ableton Live installed and running
- Terminal app with Accessibility permissions
- Python 3 for script execution
