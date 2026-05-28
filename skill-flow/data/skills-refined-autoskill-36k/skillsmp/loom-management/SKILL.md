---
name: loom-management
description: Instructions for managing the Loom screen recording integration.
---

# Loom Management

This skill provides instructions for managing the Loom screen recording integration within the AutomateLinux suite.

## Commands

### Restart Loom (`d restartLoom`)

Restarts the Loom server and client processes and attempts to automatically select the screen sharing window.

**Behavior:**
1. Stops any running Loom instances (`stop_loom.sh`).
2. Starts Loom server and client in background (`restart_loom.sh`).
3. Launches `utilities/autoSelectLoomScreen.py` to handle the "Share Screen" popup.

**Automation Logic:**
- The Python script scans for a window titled "Share Screen" or with class "xdg-desktop-portal".
- **Safety**: It ONLY sends keystrokes if the window is explicitly found and identified. It does NOT send keys blindly.
- **Key Sequence**: Sends `TAB TAB ENTER TAB TAB ENTER` (configurable via arguments) with a 1ms delay between keys to quickly select and confirm the screen.

### Stop Loom (`d stopLoom`)

Stops all Loom-related processes (server and client).

### Check Active Status (`d isLoomActive`)

Checks the systemd status of `loom-server`, `loom-client-dev`, and `loom-client-prod`.

## Configuration

- **Key Sequence**: The default key sequence is defined in `utilities/autoSelectLoomScreen.py`.
- **Delays**: The inter-key delay is set to 0.001s for rapid execution.

## Troubleshooting

- If the "Share Screen" window is not detected, check if `xdg-desktop-portal-gnome` is running.
- Use `d listWindows` to verify if the daemon can see the window.
