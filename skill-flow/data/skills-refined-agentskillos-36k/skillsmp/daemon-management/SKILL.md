---
name: daemon-management
description: Instructions for building and restarting the AutomateLinux daemon.
---

# Daemon Management

This skill covers how to manage the lifecycle of the AutomateLinux daemon, specifically focusing on building and restarting it using custom terminal functions.

## Core Functions

### `bd` (Build Daemon)
The primary function used to build and restart the daemon. It performs the following:
1.  Remembers the current directory.
2.  Navigates to the daemon source directory (`$AUTOMATE_LINUX_DAEMON_DIR`).
3.  Calls the `bs` function.
4.  Returns to the original directory.

### `bs` (Build and Source)
An alias for `b -source`. It triggers the `b` function with the `-source` flag.

### `b` (Build Wrapper)
A wrapper for the project's build scripts. When called with `-source`, it sources the `build.sh` script instead of executing it in a subshell, allowing environments variables and function definitions within the script to persist if needed.

## Daemon Build Process (`daemon/build.sh`)

When `bd` is executed, the `daemon/build.sh` script performs these steps:
1.  **Stop Service**: Executes `daemon/stop_daemon.sh` to safely shut down any running instances.
2.  **Environment Check**: Ensures the UDS (Unix Domain Socket) directory `/run/automatelinux` exists and has the correct ownership.
3.  **Build**:
    - Creates/enters the `build` directory.
    - Runs `cmake ..`.
    - Runs `make`.
4.  **Deployment**:
    - Copies the newly built `daemon` binary to the daemon root.
    - Reloads systemd (`systemctl daemon-reload`).
    - Restarts the `daemon.service`.

## Usage

Simply run `bd` from any terminal session where the AutomateLinux terminal functions are loaded:

```bash
bd
```

> [!NOTE]
> The `bd` function is defined in `terminal/functions/misc.sh` and depends on the `AUTOMATE_LINUX_DAEMON_DIR` environment variable.
