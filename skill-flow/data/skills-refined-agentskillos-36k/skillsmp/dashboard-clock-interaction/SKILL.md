---
name: Dashboard Clock Interaction
description: Logic and rules for the dashboard clock widget interaction (toggling formats vs modes).
---

# Dashboard Clock Interaction Logic

This skill defines how the dashboard clock widget (ClockWidget) should handle user interactions to ensure consistency across the application.

## Interaction Rules

### 1. Clock Format Toggling (Format Cycling)
- **Action**: Tapping or clicking anywhere on the **clock face** (the hands of the analog clock or the digits of the digital clock).
- **Behavior**: Cycles through the available clock formats in this order:
  1. **Analog**
  2. **Digital (12-hour)**
  3. **Digital (24-hour)**
- **Note**: This interaction must be contained within the clock face area and stop propagation to avoid switching the widget mode.

### 2. Widget Mode Switching
- **Action**: Clicking the **label** at the top of the widget (where it says "CLOCK", "STOPWATCH", or "TIMER").
- **Behavior**: Cycles through the widget modes:
  - **CLOCK** -> **STOPWATCH** -> **TIMER** -> **CLOCK**
- **Restriction**: The clickable area for mode switching is restricted to the header label area (e.g., `h-12`) to prevent accidental triggers while interacting with the clock format.

### 3. No Global Keyboard Toggling
- **Rule**: Do not implement global keyboard events for toggling the clock format unless explicitly requested. All format toggling should be driven by direct interaction with the clock face.

## Technical Implementation
- Component: `src/components/ui/clock-widget.tsx`
- Propagating clicks must be prevented using `e.stopPropagation()` on the clock face handlers.
