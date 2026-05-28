---
name: host
description: Quickly clone latest from GitHub and host the Flask app. No watching for updates - just fast one-time hosting. Use when user says "host", "run", "start server", or wants to quickly test the latest version.
---

# Host

Clone latest from GitHub and start the Flask server immediately.

## Workflow

### 0. Rename Session

Run `/rename Hosting` to name the session for easy identification and resumption.

### 1. Clone Latest (Minimal Clone)

```powershell
# Shallow clone for speed (only latest commit)
$TIMESTAMP = Get-Date -Format "yyyy-MM-dd-HHmm"
$WORKSPACE = "..\workspaces\$TIMESTAMP-host"
git clone --depth 1 https://github.com/YujieHua/AM_Overheating_Predictor.git $WORKSPACE
Set-Location $WORKSPACE
```

### 2. Find Port and Start Server

```powershell
# Find available port (6000-9000 range)
do {
    $PORT = Get-Random -Minimum 6000 -Maximum 9000
} while (Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue)

# Update terminal title
$Host.UI.RawUI.WindowTitle = "Hosting (port $PORT)"

# Start server
Write-Host "Starting server on http://localhost:$PORT/"
python app.py --port=$PORT
```

### 3. Report Ready

Present the URL using the standard template (do NOT open browser automatically):

```
╔══════════════════════════════════════════════════════════════════╗
║  SERVER RUNNING                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  URL: http://localhost:$PORT/                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  SOURCE: Fresh clone from GitHub (latest commit)                 ║
╚══════════════════════════════════════════════════════════════════╝
```

Play the ready sound:
```powershell
(New-Object System.Media.SoundPlayer "C:\Windows\Media\chimes.wav").PlaySync()
```

## Key Points

- Uses `--depth 1` for fastest possible clone
- Random port avoids conflicts with other sessions
- No GitHub monitoring - single clone and host
- Does NOT open browser - just provides the link
- Clean: just clone, start, present URL
