# Revit Dynamo Launcher - Deep Technical Documentation

## Architecture Overview
The `autodesk-revit-dynamo-launcher` skill is designed to solve the "last mile" problem of Revit automation: starting the application into a specific state (open file + open tool) without user intervention. It relies on the Revit **Journaling** system, a VBScript-like automation engine.

---

## File Deep Dive

### 1. `scripts/launch.ps1`
**Role:** Orchestrator & Pre-processor.
- **Environment Detection:** Locates `$PSScriptRoot` to find relative assets regardless of where the skill is stored.
- **Path Resolution:** Revit Journals require *absolute* file paths for opening documents. This script converts the relative `assets/2024templaterevitskill.rte` path into a full system path.
- **Dynamic Journal Generation:** Reads `journal_template.txt`, replaces the `{{TEMPLATE_PATH}}` placeholder with the resolved path, and writes a temporary `journal_run.txt`.
- **Process Management:** Launches `Revit.exe` using `Start-Process` with the following critical arguments:
  - `journal_run.txt`: Commands Revit to follow the script immediately upon startup.
  - `/nosplash`: Speeds up launch by disabling the splash screen.
  - `-WindowStyle Maximized`: Ensures the UI is ready for work immediately.

### 2. `assets/journal_template.txt`
**Role:** The "Brain" of the automation.
- **Initialization:** Sets up the `CrsJournalScript` object.
- **Template Handling:** 
  - `ID_REVIT_FILE_OPEN`: Triggers the file open command.
  - `TaskDialog_Template_File`: Sends code `1001` to the dialog that appears when opening a `.rte` file, forcing Revit to "Create a New Project" rather than editing the template.
- **UI Interaction:** 
  - `TabActivated:Manage`: Switches the ribbon to the Manage tab. This is a safety step to ensure the Dynamo button is visible/active.
  - `ID_VISUAL_PROGRAMMING_DYNAMO`: The final command that triggers the Dynamo UI.

### 3. `assets/2024templaterevitskill.rte`
**Role:** The Workspace.
- A standard Revit template file used as the landing environment. Opening a file is required because the "Launch Dynamo" command is disabled in the Revit Home/Zero State.

### 4. `assets/Dynamo.addin`
**Role:** Dependency Management.
- A standard manifest file. While Revit typically loads Dynamo from the ProgramData location, having this asset available ensures the skill remains portable and helps debug environment-specific loading issues.

---

## Execution Flow
1. **Trigger:** User runs `launch.ps1`.
2. **Build:** `journal_run.txt` is created with absolute paths.
3. **Execution:** Revit starts -> reads `journal_run.txt`.
4. **Revit Logic:** Opens Template -> Handles Dialog -> Changes Tab -> Starts Dynamo.
5. **Completion:** User is presented with a maximized Revit window and the Dynamo editor open.

## Troubleshooting
- **interactive Mode Pop-up:** Usually caused by a secondary dialog (like an Add-in security warning or a missing link). Check the `Journals/journal.XXXX.txt` in `%LOCALAPPDATA%` to see the last recorded command.
- **Access Denied:** If ThreatLocker or Windows permissions block the `.ps1`, the logic can be run directly via a single PowerShell command string in the terminal.
