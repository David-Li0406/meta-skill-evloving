---
name: key-simulation
description: Instructions for simulating keyboard input using the AutomateLinux daemon.
---

# Key Simulation

The AutomateLinux daemon provides powerful capabilities to simulate keyboard input events and type strings directly.

## Type a String

To type a text string as if it were entered on the keyboard:

```bash
d simulateInput --string "Hello World"
```

## Simulate Raw Input Events

To simulate specific input events (like pressing a specific key code):

```bash
d simulateInput --type <EV_TYPE> --code <KEY_CODE> --value <VALUE>
```

- **EV_TYPE**: Usually `1` for `EV_KEY`.
- **KEY_CODE**: The Linux input event code (e.g., `28` for Enter, `30` for A).
- **VALUE**: `1` for press, `0` for release, `2` for repeat.

### Example: Pressing 'A'

```bash
# Press 'A' (code 30)
d simulateInput --type 1 --code 30 --value 1
# Release 'A'
d simulateInput --type 1 --code 30 --value 0
```

## Underlying Utilities

The daemon uses `InputMapper` internally to emit these events to `/dev/uinput` via the virtual device it creates. This bypasses physical hardware constraints and allows for automation even when physical devices are ignored or grabbed.
