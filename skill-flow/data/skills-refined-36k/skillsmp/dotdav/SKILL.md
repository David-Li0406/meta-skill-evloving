---
name: dotdav
description: A dotfile management tool using rclone and webdav.
---

# Dotdav

A simple dotfile synchronization tool that uses `rclone` to sync files to a WebDAV server (or any other rclone remote). It supports multiple device profiles and systemd-based auto-sync.

## Prerequisites

- Python 3
- `rclone` installed and configured
- `uv` (optional, for dependency management)

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   uv sync
   # OR
   pip install pyyaml watchdog
   ```
3. Initialize the repository:
   ```bash
   python dotdav.py init --remote myremote --path dotfiles
   ```

## Usage

### Managing Files

- **Add a file**:
  ```bash
  python dotdav.py add ~/.bashrc
  ```
  This copies the file to the repo and adds it to `mappings.yaml` for the *current profile*.

- **Deploy files**:
  ```bash
  python dotdav.py deploy
  ```
  Creates symlinks in your home directory pointing to the repository files.

### Profiles

Dotdav allows different versions of files for different devices.

1. **Switch profile**:
   ```bash
   python dotdav.py profile laptop
   ```
2. **Add specific version**:
   After switching, `add` operations will save to a profile-specific filename (e.g., `bashrc_laptop`) and update `mappings.yaml`.
3. **Deploy**:
   `deploy` will choose the file matching the current profile, falling back to 'default'.

### Syncing

- **Manual Sync**:
  ```bash
  python dotdav.py sync push
  python dotdav.py sync pull
  ```

- **Auto Sync**:
  Start the daemon directly:
  ```bash
  python dotdav.py autosync
  ```

- **Systemd Service**:
  Install and enable the user service for background syncing:
  ```bash
  python dotdav.py service install
  ```
  Check status:
  ```bash
  systemctl --user status dotdav.service
  ```

## Fish Completion

Source the completion script:
```fish
source completions.fish
```
