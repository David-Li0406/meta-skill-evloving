---
name: industrial-amber-design
description: Guidelines and components for the Gosling2 "Industrial Amber" workstation aesthetic.
---

# Industrial Amber Design System

This skill provides component references and implementation guides for the "Industrial Amber" workstation look.

**NOTE**: Strict design rules (No Hardcoded QSS, Use GlowFactory) are enforced by `rules/architecture.md`.

## 1. Core Palette (Logic Fallbacks Only)

| Element | Color | Usage |
| :--- | :--- | :--- |
| **Amber** | `#FFC66D` | Primary accent, text, active signals, glowing controls. |
| **Muted Amber** | `#FF8C00` | Secondary highlights, warnings, tactical data. |
| **Magenta** | `#FF00FF` | Critical buttons, destructive actions, surgical focus. |
| **Cyan** | `#00E5FF` | Unprocessed data, cloud/virtual sources, metadata previews. |
| **Red** | `#FF4444` | Errors, raw WAV files, invalid states. |
| **Void** | `#000000` | Main background, chassis, depth. |

## 2. Component Factory usage

ALWAYS use the `GlowFactory` (found in `src.presentation.widgets.glow`) when creating interactive elements.

### GlowButton
Standard action button with halo effect.
```python
from ..widgets.glow import GlowButton
btn = GlowButton("COMMAND")
btn.setObjectName("PrimaryAction")
btn.setGlowColor("#FFC66D") # Default Amber
```

### GlowLineEdit
Search boxes and input fields.
```python
from ..widgets.glow import GlowLineEdit
search = GlowLineEdit()
search.setPlaceholderText("SCANNING...")
```

### GlowLED Status Indicators
Use these for mode signals (e.g., Prep Mode, Edit Mode).
```python
from ..widgets.glow import GlowLED
led = GlowLED(color="#FFC66D", size=10)
led.setActive(True) # Causes the "heartbeat" glow pulse
```

## 6. Layout and Spacing Guidelines

*   **The "Heavy" Separator:** Blocks of UI should be separated by 7px black bars. These should be `QFrame` widgets with the object name `SeparatorLine` or `HeavySeparator`.
*   **Splitters:** Use `QSplitter` for all main panels. Never hard-code panel widths unless they are "system buttons" or "islands".
*   **Borders:** Handled via `theme.qss`.

## 7. Typography Rules

*   **Primary:** Use **Bahnschrift Condensed** (fallback: "Segoe UI", sans-serif).
*   **Case:** Titles and button labels should be **ALL CAPS** (e.g., "RESTORE ON DRAG", "SAVE CHANGES").
*   **Branding:** Use the stacked label pattern for the application title to create the double-glow effect.

## 8. Industrial Details

*   **Glow Margins:** Interactive components should usually have a `4px` to `8px` glow margin to prevent the halo from being clipped by parents.
*   **Tooltips:** Use the `ReviewTooltip` or `GlowTooltip` for a dark-themed popover.
