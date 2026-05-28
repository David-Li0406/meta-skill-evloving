---
name: revit-dynamo-start
description: Starts Revit 2024 maximized, opens a bundled template, and auto-starts Dynamo via dynamic journal generation.
metadata:
  short-description: Complete Revit + Dynamo automated startup
---

# Autodesk Revit Dynamo Starter

## Overview
This skill provides a fully automated entry into the Revit 2024 environment with Dynamo ready to use. It addresses common automation hurdles like modal dialogs and absolute path requirements in Revit journals.

## Key Features
- **Dynamic Path Resolution**: Automatically detects the local path of the skill to ensure the template file is found.
- **Maximized Startup**: Uses the `-WindowStyle Maximized` flag for immediate full-screen workspace.
- **Bypass Dialogs**: Specifically handles the Revit 2024 "Project vs Template" selection dialog (ID 1001).
- **Tab Selection**: Explicitly activates the "Manage" tab before calling Dynamo to mimic standard user interaction.

## Files Structure
- `scripts/start.ps1`: The main controller script (PowerShell).
- `assets/journal_template.txt`: The base journal logic with placeholders.
- `assets/2024templaterevitskill.rte`: The default template file opened on startup.
- `assets/Dynamo.addin`: Secondary add-in manifest to assist in loading the Dynamo environment.

## Usage
Execute the starter via PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File "scripts\start.ps1"
```

## Maintenance
To update the template file, replace `assets/2024templaterevitskill.rte`. To change the Dynamo start sequence, edit `assets/journal_template.txt`.
