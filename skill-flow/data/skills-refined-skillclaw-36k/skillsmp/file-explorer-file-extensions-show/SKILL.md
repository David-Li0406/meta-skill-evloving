---
name: file-explorer-file-extensions-show
description: Configure Windows Explorer to globally show file extensions and hidden files.
metadata:
  short-description: Show hidden files and extensions
---

# Show File Extensions and Hidden Files

## Description
This skill runs a PowerShell script to modify the Current User registry settings for Windows Explorer. It enables the visibility of:
1.  **Hidden files and folders**
2.  **File extensions** (e.g., `.txt`, `.csv`)

## Usage
Run the configuration script:

```powershell
powershell -ExecutionPolicy Bypass -File "scripts\configure-explorer.ps1"
```

## Effects
- **Registry Keys Modified**:
    - `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Hidden` -> Set to `1`
    - `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\HideFileExt` -> Set to `0`
- **Process**: Windows Explorer (`explorer.exe`) will be restarted automatically to apply the changes immediately. Your taskbar and desktop icons may briefly disappear and reappear.
