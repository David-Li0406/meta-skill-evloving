---
name: services-guide
description: System services configuration guide including Yabai tiling window manager, skhd keyboard shortcuts, and macOS window management
---

# Services Configuration

This document provides information about the services configured in this dotfiles repository, focusing on window management with yabai and keyboard shortcuts with skhd.

## Yabai

[Yabai](https://github.com/koekeishiya/yabai) is a tiling window manager for macOS that allows you to organize your windows in a more efficient way.

### Installation and Setup

Yabai is installed and configured through Nix using both darwin-nix and home-manager:

- The system-level service is configured in `darwin/service/yabai/default.nix`
- The user-level configuration is in `home-manager/yabai/yabairc`

### Starting and Stopping Yabai

To start, stop, or restart the yabai service:

```bash
# Start yabai
yabai --start-service

# Stop yabai
yabai --stop-service

# Restart yabai
yabai --restart-service
```

When using Nix, the service is managed by launchd:

```bash
# Check status
launchctl list | grep yabai

# Manual restart
launchctl kickstart -k gui/$(id -u)/org.nixos.yabai
```

### Key Features

- Tiling window management with BSP (Binary Space Partitioning) layout
- Automatic window organization
- Workspace (Space) management with labels
- Mouse and keyboard control
- Application-specific rules

## Skhd

[Simple Hotkey Daemon (skhd)](https://github.com/koekeishiya/skhd) is a hotkey daemon for macOS that works well with yabai to provide keyboard shortcuts for window management.

### Installation and Setup

Skhd is configured through Nix:

- System-level service configuration (if applicable)
- User-level configuration in home-manager

### Keyboard Shortcuts

Below are the key shortcuts configured for window management with yabai:

#### Window Navigation

| Shortcut | Action |
|----------|--------|
| `alt + h` | Focus window to the left |
| `alt + j` | Focus window below |
| `alt + k` | Focus window above |
| `alt + l` | Focus window to the right |

#### Window Movement

| Shortcut | Action |
|----------|--------|
| `shift + alt + h` | Swap window with the one to the left |
| `shift + alt + j` | Swap window with the one below |
| `shift + alt + k` | Swap window with the one above |
| `shift + alt + l` | Swap window with the one to the right |

#### Window Resizing

| Shortcut | Action |
|----------|--------|
| `alt + r` | Toggle resize mode |
| `h` | Resize left (in resize mode) |
| `j` | Resize down (in resize mode) |
| `k` | Resize up (in resize mode) |
| `l` | Resize right (in resize mode) |
| `escape` | Exit resize mode |

#### Space Management

| Shortcut | Action |
|----------|--------|
| `ctrl + alt + 1-9` | Focus space 1-9 |
| `ctrl + alt + shift + 1-9` | Move window to space 1-9 |
| `alt + f` | Toggle window fullscreen |
| `alt + shift + f` | Toggle window native fullscreen |

#### Layout Management

| Shortcut | Action |
|----------|--------|
| `alt + e` | Toggle split orientation (vertical/horizontal) |
| `alt + shift + space` | Toggle floating mode for window |
| `alt + shift + r` | Rotate layout clockwise |

### Starting and Stopping Skhd

To start, stop, or restart the skhd service:

```bash
# Start skhd
skhd --start-service

# Stop skhd
skhd --stop-service

# Restart skhd
skhd --restart-service
```

When using Nix, the service is managed by launchd:

```bash
# Check status
launchctl list | grep skhd

# Manual restart
launchctl kickstart -k gui/$(id -u)/org.nixos.skhd
```

## Troubleshooting

### Common Issues with Yabai

- **Scripting Addition not loaded**: Ensure System Integrity Protection (SIP) is properly configured
- **Windows not tiling**: Check if the application has a rule to be managed
- **Keyboard shortcuts not working**: Verify skhd is running and check for conflicts with system shortcuts

### Logs and Debugging

To view logs for troubleshooting:

```bash
# Yabai logs
tail -f /tmp/yabai_$(whoami).log

# Skhd logs
tail -f /tmp/skhd_$(whoami).log
```

## Customization

To customize the configuration:

1. Edit `home-manager/yabai/yabairc` for yabai settings
2. Edit the skhd configuration file for keyboard shortcuts
3. Run `home-manager switch` to apply changes
4. Restart the services to apply the new configuration
