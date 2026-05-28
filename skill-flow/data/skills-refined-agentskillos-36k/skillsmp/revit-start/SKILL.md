---
name: revit-start
description: Start Autodesk Revit 2021/2023/2024/2026 with /nosplash and set the process priority to Realtime. Use when asked to start Revit, select a specific version, or ensure Revit runs at Realtime priority.
metadata:
  short-description: Start Autodesk Revit with optimized settings
---

# Autodesk Revit Starter

## Quick start

- Run `scripts/start-revit.cmd 2024` (valid versions: 2021, 2023, 2024, 2026).
- Script always adds `/nosplash` and does not accept other switches.
- If Revit is running, close it first (script will refuse to proceed).
- Run from an elevated shell if Realtime priority is blocked.

## Behavior

- Verify Revit is not running before modifying settings.
- Clear `[Recent File List]` in `%APPDATA%\Autodesk\Revit\Autodesk Revit <version>\Revit.ini` (delete entries until the next section header).
- Resolve the default install path under `C:\Program Files\Autodesk\Revit <version>\Revit.exe`.
- If the default path is missing, search `C:\Program Files\Autodesk` for a matching `Revit.exe`.
- For 2024, start with the template `assets\2024templaterevitskill.rte` and then `/nosplash`.
- For other versions, start with `/nosplash` only.
- Set process priority to Realtime.

## Troubleshooting

- If Revit is running, close it and re-run.
- If `Revit.ini` is missing, the script skips recent-list cleanup and proceeds to start.
- If the 2024 template file is missing, the script exits with an error.
- If Revit is not found, surface an error with the expected default path.
- If setting priority fails, re-run from an elevated shell.

## Resources

- `scripts/start-revit.cmd`: Start a specific Revit version with `/nosplash` and set process priority to Realtime.
- `scripts/start-revit-2021.cmd`: Start Revit 2021 with `/nosplash` and Realtime priority.
- `scripts/start-revit-2023.cmd`: Start Revit 2023 with `/nosplash` and Realtime priority.
- `scripts/start-revit-2024.cmd`: Start Revit 2024 with `/nosplash` and Realtime priority.
- `scripts/start-revit-2026.cmd`: Start Revit 2026 with `/nosplash` and Realtime priority.
- `assets/2024templaterevitskill.rte`: Template used for Revit 2024 start.
