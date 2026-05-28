---
name: mockup-ui
description: Generate UI mockups for VeilBreakers before implementation (ASCII layout + optional FLUX)
---

# UI Mockup Generator for VeilBreakers

Show visual layout mockups BEFORE writing any UI code.

## When to Use
- Before implementing any new UI screen
- When designing HUD elements
- Menu layouts and panels
- Any visual component

## Process

1. **Understand the request** - What UI element needs mockup?
2. **Create ASCII layout** showing placement, sizes, elements
3. **Optionally try FLUX** if AI image would help (may not work)
4. **Get user approval** before coding

## ASCII UI Mockup Format

```
┌─────────────────────────────────────────────────────────┐
│                     SCREEN NAME                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐                    ┌──────────────┐   │
│   │  Element 1  │                    │  Element 2   │   │
│   │  (size/pos) │                    │  (size/pos)  │   │
│   └─────────────┘                    └──────────────┘   │
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │              Main Content Area                  │   │
│   │              (width x height)                   │   │
│   └─────────────────────────────────────────────────┘   │
│                                                         │
│   [ Button 1 ]    [ Button 2 ]    [ Button 3 ]          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Example: Health Bar with Corruption

```
┌──────────────────────────────────────┐
│  MONSTER NAME           Lv.45       │
├──────────────────────────────────────┤
│  HP  [████████████░░░░░░] 847/1200  │
│  COR [██████░░░░░░░░░░░░]  35%      │
│       ↑ purple, cracks when >50%    │
└──────────────────────────────────────┘
Width: 300px | Position: top-left floating
Colors: HP=red, Corruption=purple, BG=semi-transparent black
```

## VeilBreakers Style Notes

**Colors:**
- HP Bar: Red (#ff4040)
- Corruption: Purple (#a020ff)
- Backgrounds: Semi-transparent black (rgba 0,0,0,0.7)
- Accents: Glowing borders (cyan, magenta, orange)

**Effects:**
- Corruption >50%: Add crack effects
- Corruption >75%: Add tendril animations
- Low HP: Pulse effect

## After Mockup

Ask user:
1. Does this layout work?
2. Any size/position adjustments?
3. Ready to implement?

Only proceed to code after approval.
