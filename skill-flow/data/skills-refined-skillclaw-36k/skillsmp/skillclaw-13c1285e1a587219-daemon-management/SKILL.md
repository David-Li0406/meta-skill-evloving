---
name: daemon-management
description: Use this skill when you need to build, deploy, and restart the AutomateLinux daemon efficiently from the terminal.
---

# Skill body

## Overview

This skill provides instructions for managing the lifecycle of the AutomateLinux daemon, focusing on building, deploying, and restarting it using terminal functions.

## Core Functions

### `bd` (Build Daemon)
The primary function to build and restart the daemon. It performs the following steps:
1. Remembers the current directory.
2. Navigates to the daemon source directory (`$AUTOMATE_LINUX_DAEMON_DIR`).
3. Calls the `bs` function.
4. Returns to the original directory.

### `bs` (Build and Source)
An alias for `b -source`, which triggers the `b` function with the `-source` flag.

### `b` (Build Wrapper)
A wrapper for the project's build scripts. When called with `-source`, it sources the `build.sh` script instead of executing it in a subshell, allowing environment variables and function definitions within the script to persist.

## Daemon Build Process (`daemon/build.sh`)

When `bd` is executed, the `daemon/build.sh` script performs the following steps:

1. **Stop Service**: Executes `daemon/stop_daemon.sh` to safely shut down any running instances.
2. **Environment Check**: Ensures the UDS (Unix Domain Socket) directory `/run/automatelinux` exists and has the correct ownership.
3. **Build**:
    - Creates/enters the `build` directory.
    - Runs `cmake ..`.
    - Runs `make`.
4. **Deployment**:
    - Copies the newly built `daemon` binary to the daemon root.
    - Reloads systemd configurations with `sudo systemctl daemon-reload`.
    - Restarts the daemon service with `sudo systemctl restart daemon.service`.

## Usage

To build and restart the AutomateLinux daemon, simply run the following command in your terminal:

```bash
bd
```

> [!NOTE]
> The `bd` function is defined in `terminal/functions/misc.sh` and depends on the `AUTOMATE_LINUX_DAEMON_DIR` environment variable.

## Technical Requirements
- **Permissions**: The build process frequently requires `sudo` for systemd and socket management.
- **Dependencies**: Ensure you have `cmake`, `libevdev`, `libsystemd`, and `libmysqlclient` installed.
- **UDS Path**: The daemon communicates via `/run/automatelinux/automatelinux-daemon.sock`.

> [!IMPORTANT]
> Always use `bd` rather than calling `make` directly in the `build/` folder to ensure the binary is correctly deployed and the systemd service is refreshed.