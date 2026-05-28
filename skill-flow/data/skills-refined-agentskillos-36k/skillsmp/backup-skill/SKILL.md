---
name: backup-skill
description: Automatically backups an opencode skill directory to a 'backups' subfolder as a versioned zip file.
metadata:
  short-description: Versioned skill backups
---

# Backup Skill

## Description
This skill creates a versioned ZIP backup of an existing skill directory. It automatically skips the `backups` folder itself during the process.

## Usage
Run the PowerShell script and provide the name of the skill to backup:

```powershell
powershell -ExecutionPolicy Bypass -File "scripts\backup-skill.ps1" -SkillName "revit-dynamo-journal"
```

## Logic
1.  **Check Path**: Verifies the skill exists in the global skills directory.
2.  **Backup Folder**: Creates a `backups` folder inside the skill directory if it doesn't exist.
3.  **Versioning**: Scans for existing `-v{number}.zip` files, finds the highest number, and increments it by 1.
4.  **Archive**: Copies all files (excluding the `backups` folder) to a temporary location and creates a zip file.
