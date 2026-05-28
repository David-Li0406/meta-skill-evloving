---
name: daemon-build
description: Detailed instructions for building, deploying, and restarting the AutomateLinux daemon.
---

# Building the Daemon

Managing the AutomateLinux daemon build process is streamlined through shell functions and a core build script.

## The `bd` Terminal Function

The fastest way to rebuild the daemon from anywhere in the terminal is the `bd` function.

```bash
bd
```

### What `bd` does:
1.  Temporarily changes directory to the daemon source folder.
2.  Runs the build script using the `bs` (build-source) alias.
3.  Returns to your original directory.

## The Build Script (`daemon/build.sh`)

The underlying logic resides in `daemon/build.sh`. It performs high-level system maintenance alongside the compilation:

1.  **Stop Daemon**: Runs `stop_daemon.sh` to ensure no active process holds files.
2.  **Socket Setup**: Ensures `/run/automatelinux` exists with correct permissions (required for Unix Domain Socket communication).
3.  **CMake Build**:
    - Enters the `build/` directory.
    - Executes `cmake ..`.
    - Executes `make`.
4.  **Deployment**:
    - Copies the resulting `daemon` binary back to the root of the daemon directory.
    - Reloads systemd configs: `sudo systemctl daemon-reload`.
    - Restarts the service: `sudo systemctl restart daemon.service`.

## Technical Requirements
- **Permissions**: The build process frequently calls `sudo` for systemd and socket management.
- **Dependencies**: Requires `cmake`, `libevdev`, `libsystemd`, and `libmysqlclient`.
- **UDS Path**: The daemon communicates via `/run/automatelinux/automatelinux-daemon.sock`.

> [!IMPORTANT]
> Always use `bd` rather than calling `make` directly in the `build/` folder to ensure the binary is correctly deployed and the systemd service is refreshed.
