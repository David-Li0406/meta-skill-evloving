# BetterDisplay Reference

Local cache of BetterDisplay documentation for Claude Code workflow.

Source: https://github.com/waydabber/BetterDisplay

## Overview

BetterDisplay is a macOS utility for display management: brightness, resolution, HiDPI scaling, XDR brightness, DDC control, and more.

- **Website**: https://betterdisplay.pro
- **CLI Tool**: https://github.com/waydabber/betterdisplaycli
- **Discord**: Community support channel
- **License**: $21.99 USD (perpetual, 1 year updates, 14-day trial)

## Installation

```bash
brew install --cask betterdisplay
```

The CLI is bundled with the app - no separate install needed.

## System Requirements

| Version | macOS Support |
|---------|---------------|
| v4.x (current) | Tahoe 26, Sequoia, Sonoma, Ventura 13.2+ |
| v3.5.6 | Sequoia, Sonoma, Ventura |
| v2.3.9 | Sonoma, Monterey 12.4+ |

Supports Apple Silicon and Intel Macs.

---

## CLI Reference

### Binary Location

```bash
# Alias for convenience (add to fish config if desired)
alias betterdisplay='/Applications/BetterDisplay.app/Contents/MacOS/BetterDisplay'
```

### Command Syntax

```bash
# CLI
betterdisplaycli operation [-parameter[=value]]

# URL Scheme
open "BetterDisplay://operation?parameter=value&parameter=value"

# HTTP (default port 55777, configurable in Settings)
curl "http://localhost:55777/command/?parameter=value"
```

### Operations

| Operation | Description |
|-----------|-------------|
| `perform` | Execute commands without value return |
| `set` | Assign values to features |
| `get` | Retrieve current values (optional min/max) |
| `toggle` | Switch boolean states |
| `feed` | Update custom controls externally |
| `create` | Create virtual screens (`type=VirtualScreen`) |
| `discard` | Remove devices (irreversible) |
| `help` | Show usage |

### Device Selection Parameters

Identify displays using any of:

| Parameter | Example |
|-----------|---------|
| `tagID` | Assigned tag in app |
| `UUID` | Display UUID |
| `displayID` | System display ID |
| `name` | Exact display name |
| `nameLike` | Partial name match |
| `productName` | Product name |
| `vendor` | Vendor name |
| `model` | Model number |
| `serial` | Serial number |
| `displayWithMouse` | Display with cursor |
| `displayWithFocus` | Display with focused window |

### Control Parameters

**Brightness & Volume:**
- `brightness` - Combined brightness (0.0-1.0 or 0%-100%)
- `hardwareBrightness` - DDC hardware brightness
- `softwareBrightness` - Software overlay brightness
- `volume` - Audio volume
- `contrast` - Display contrast
- `hardwareContrast` - DDC hardware contrast

**Color & Image:**
- `temperature` - Color temperature
- `gamma` - Gamma correction
- `colorProfile` - Color profile name

**Display Settings:**
- `resolution` - Display resolution
- `refreshRate` - Refresh rate
- `rotation` - Screen rotation (Pro)
- `HDR` - HDR mode toggle

**Protection (Pro):**
- `protectAll` - Protect all settings
- `protectResolution` - Lock resolution
- `protectRefreshRate` - Lock refresh rate
- `protectHDR` - Lock HDR state

**DDC Direct Access:**
- `ddc` - Raw DDC command
- `vcp` - VCP code (e.g., `luminance`, `contrast`)
- `value` - Value to set

### Examples

```bash
# Set brightness to 80% on all displays
betterdisplaycli set --brightness=80%

# Set brightness on specific display
betterdisplaycli set --nameLike=LG --brightness=0.7

# Get current brightness
betterdisplaycli get --brightness

# Toggle HDR
betterdisplaycli toggle --HDR

# Direct DDC brightness (alternative to m1ddc)
betterdisplaycli set --nameLike=gp27 --ddc --vcp=luminance --value=50

# HTTP API
curl "http://localhost:55777/set?brightness=0.8"
curl "http://localhost:55777/set?namelike=gp27&ddc&vcp=luminance&value=50"

# URL scheme
open "BetterDisplay://set?name=MyDisplay&brightness=0.8"
```

---

## Feature Comparison

### Free Features

- GUI brightness/volume control
- Native brightness keys support
- Basic keyboard shortcuts
- Software dimming (color table/overlay)
- TV control (LG webOS, Samsung Tizen, Philips Android, Yamaha AVR)
- DDC support (brightness, volume, input, power)
- Virtual screen creation
- Resolution slider and refresh rate menus
- Color profile selector
- CLI and HTTP integration
- macOS Shortcuts support

### Pro Features ($21.99)

- XDR brightness upscaling to 1600 nits (Apple Silicon)
- Flexible HiDPI scaling
- Custom scaled resolutions
- Display disconnect/reconnect
- Picture in Picture
- Video filter window
- Full-screen streaming
- Color temperature control
- Mirror configuration protection
- Advanced brightness syncing
- Layout protection with anchors

---

## HiDPI Scaling Setup

### Method 1: Flexible Scaling (Recommended)

1. Open BetterDisplay menu bar icon
2. Settings → Displays → Select display
3. Enable "Edit the default system configuration of this display model"
4. Enable "Enable flexible scaling"
5. Click Apply (requires admin password)
6. Reboot
7. Use resolution sliders to adjust scaling

**Requirements:**
- macOS Monterey 12.4+
- Works with USB-C, DisplayPort, HDMI, built-in displays
- Entry M1/M2: max 6144px horizontal
- M1/M2 Pro/Max/Ultra: max 7680px horizontal

### Method 2: Virtual Screen Mirroring

Use only if flexible scaling fails:

1. Settings → Displays → Overview
2. "Create New Virtual Screen..."
3. "Match aspect ratio of and associate to a display"
4. Configure mirroring

**Drawbacks:** Sleep issues, color flickering, cursor problems.

---

## Safe Mode & Reset

### Safe Mode

Hold SHIFT while launching to prevent virtual screen connections.

### Simple Reset

Settings → Application → Advanced settings & privacy → Reset App Settings

Preserves license, removes custom settings.

### Display System Reset

Settings has built-in display system reset (v3.5.3+). Requires restart.

### Complete Reset (Terminal)

```bash
defaults delete pro.betterdisplay.BetterDisplay
# Then restart and optionally reinstall
```

---

## Integration Methods

### macOS Shortcuts

BetterDisplay supports App Intents for Shortcuts automation.

### DistributedNotificationCenter

Send JSON requests to `com.betterdisplay.BetterDisplay.request`:
```json
{
  "uuid": "request-id",
  "commands": ["set"],
  "parameters": {"brightness": 0.8}
}
```

Receive responses at `com.betterdisplay.BetterDisplay.response`.

### OSD Integration

Third-party apps (MediaMate, DynamicLakePro 3.0+) can receive display change notifications for custom OSDs.

---

## References

- [Wiki Home](https://github.com/waydabber/BetterDisplay/wiki)
- [CLI Tool](https://github.com/waydabber/betterdisplaycli)
- [Discussions](https://github.com/waydabber/BetterDisplay/discussions)
