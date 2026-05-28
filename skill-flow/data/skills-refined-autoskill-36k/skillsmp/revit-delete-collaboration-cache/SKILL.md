---
name: revit-delete-collaboration-cache
description: Delete local Autodesk Revit cache/collaboration copies under %LOCALAPPDATA%\Autodesk\Revit (Autodesk Docs / Autodesk Construction Cloud) to reset local issues and reduce disk use. Use when asked to delete local Revit cache files, remove Revit version subfolders, or clean collaboration cache for specific versions. Always ask for explicit confirmation before running deletions.
metadata:
  short-description: Delete local Revit cache and collaboration files
---

# Revit Delete Collaboration Cache

## Overview

Delete local Revit cache/copy data stored in `C:\Users\darick\AppData\Local\Autodesk\Revit` (default `%LOCALAPPDATA%\Autodesk\Revit`), including version subfolders. Use the included PowerShell script to preview and then delete.

## Workflow

1. Confirm scope with the user (all versions vs a specific folder). Restate the exact path to be affected.
2. Preview with the script (no deletion) and report what would be removed.
3. Ask for explicit confirmation before deletion.
4. Execute deletion with `-ConfirmDeletion`.
5. Verify and report remaining items or errors.

## Safety rules

- Always ask before executing delete; do not run deletion without explicit user confirmation.
- Only delete inside `%LOCALAPPDATA%\Autodesk\Revit`.
- Do not delete the root folder unless the user explicitly asks and `-DeleteRoot` is set.

## Script

`scripts/clear_revit_local_cache.ps1`

Parameters:
- `RootPath`: Root Revit cache directory. Defaults to `%LOCALAPPDATA%\Autodesk\Revit`.
- `TargetPath`: Optional subfolder (relative to RootPath or absolute) to delete. If omitted, deletes contents of RootPath only.
- `ConfirmDeletion`: Required to actually delete. Without it, the script only previews.
- `DeleteRoot`: If set, deletes the root folder itself (only when explicitly requested).

Examples:

Preview all contents (no deletion):

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\darick\.config\opencode\skills\revit-delete-collaboration-cache\scripts\clear_revit_local_cache.ps1"
```

Delete all contents after confirmation:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\darick\.config\opencode\skills\revit-delete-collaboration-cache\scripts\clear_revit_local_cache.ps1" -ConfirmDeletion
```

Delete a specific version folder after confirmation:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\darick\.config\opencode\skills\revit-delete-collaboration-cache\scripts\clear_revit_local_cache.ps1" -TargetPath "Autodesk Revit 2024" -ConfirmDeletion
```
