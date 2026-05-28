---
name: uloop-capture-window
description: Use this skill when you need to take a screenshot of any Unity Editor window and save it as a PNG image for debugging or documentation purposes.
---

# Skill body

Capture any Unity EditorWindow by name and save as PNG.

## Usage

```bash
uloop capture-window [--window-name <name>] [--resolution-scale <scale>] [--match-mode <mode>]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--window-name` | string | `Game` | Window name to capture (e.g., "Game", "Scene", "Console", "Inspector", "Project", "Hierarchy", or any EditorWindow title) |
| `--resolution-scale` | number | `1.0` | Resolution scale (0.1 to 1.0) |
| `--match-mode` | enum | `exact` | Window name matching mode: `exact`, `prefix`, or `contains`. All modes are case-insensitive. |

## Match Modes

| Mode | Description | Example |
|------|-------------|---------|
| `exact` | Window name must match exactly (case-insensitive) | "Project" matches "Project" only |
| `prefix` | Window name must start with the input | "Project" matches "Project" and "Project Settings" |
| `contains` | Window name must contain the input anywhere | "set" matches "Project Settings" |

## Window Name

The window name is the text displayed in the window's title bar (tab). Common window names include:

- **Game**: Game View window
- **Scene**: Scene View window
- **Console**: Console window
- **Inspector**: Inspector window
- **Project**: Project browser window
- **Hierarchy**: Hierarchy window
- **Animation**: Animation window
- **Animator**: Animator window
- **Profiler**: Profiler window
- **Audio Mixer**: Audio Mixer window

You can also specify custom EditorWindow titles (e.g., "EditorWindow Capture Test").

## Examples

```bash
# Capture Game View at full resolution
uloop capture-window

# Capture Game View at half resolution
uloop capture-window --window-name Game --resolution-scale 0.5

# Capture Scene View
uloop capture-window --window-name Scene

# Capture Console window
uloop capture-window --window-name Console

# Capture Inspector window
uloop capture-window --window-name Inspector

# Capture Project browser (exact match - won't match "Project Settings")
uloop capture-window --window-name Project

# Capture all windows starting with "Project" (prefix match)
uloop capture-window --window-name Project --match-mode prefix
```