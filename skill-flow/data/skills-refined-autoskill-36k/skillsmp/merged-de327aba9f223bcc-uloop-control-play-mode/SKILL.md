---
name: uloop-control-play-mode
description: Use this skill to control Unity Editor play mode for testing, debugging, or automated workflows.
---

# uloop control-play-mode

Control Unity Editor play mode (play/stop/pause).

## Usage

```bash
uloop control-play-mode [options]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--action` | string | `Play` | Action to perform: `Play`, `Stop`, `Pause` |

## Examples

```bash
# Start play mode
uloop control-play-mode --action Play

# Stop play mode
uloop control-play-mode --action Stop

# Pause play mode
uloop control-play-mode --action Pause
```

## Output

Returns JSON with the current play mode state:
- `IsPlaying`: Whether Unity is currently in play mode
- `IsPaused`: Whether play mode is paused
- `Message`: Description of the action performed

## Notes

- Play action starts the game in the Unity Editor (also resumes from pause).
- Stop action exits play mode and returns to edit mode.
- Pause action pauses the game while remaining in play mode.
- Useful for automated testing workflows.