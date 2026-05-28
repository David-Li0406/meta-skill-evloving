# Token System

## Token Inventory

Each player (Red and Blue) has 3 tokens:

| Token       | Phase    | Purpose                       |
| ----------- | -------- | ----------------------------- |
| **Attack**  | Phase 1  | Navigate toward firewall      |
| **Exploit** | Midpoint | Mark breach point permanently |
| **Ghost**   | Phase 2  | Retreat from breach point     |

**Total:** 6 tokens (3 red, 3 blue)

## Token Designs

### Attack Token Design

- Filled target (concentric circles with crosshair)
- Three solid concentric circles
- Cross pattern overlay

### Exploit Token Design

- Hollow rings with faint crosshair
- Two concentric circles (outline only)
- Faint cross pattern

### Ghost Token Design

- Gradient opacity circles (fading outward)
- Four concentric circles
- Graduated opacity: 30%, 50%, 70%, 100%

## Token Colors

| Player | Hex Code  |
| ------ | --------- |
| Red    | `#FF2244` |
| Blue   | `#44BBFF` |

## Positioning Rules

1. **Edge Nodes Only:** Tokens always reside on edge nodes, never inside tiles
2. **Color Requirement:** Edge node must include a path segment of:
   - Player's color, OR
   - Purple (shared)
3. **Non-Blocking:** Both players' tokens may occupy the same edge node simultaneously

## Token Lifecycle

### Attack Token Lifecycle

- **Starts:** On starting tile's edge node matching player color
- **During Phase 1:** Moves along valid paths toward firewall
- **Ends:** Replaced by Exploit when reaching board edge

### Exploit Token Lifecycle

- **Placed:** Automatically when Attack reaches firewall
- **Location:** Same node where Attack reached firewall
- **Duration:** Remains for rest of game (never moves)

### Ghost Token Lifecycle

- **Placed:** At Exploit node on first Move action after Exploit
- **Moves:** Away from Exploit, following valid paths
- **Duration:** Active for rest of game

## Token Transitions

```text
Attack Token → [reaches firewall] → Replaced by Exploit Token
                                    ↓
                          [first Move action]
                                    ↓
                          Ghost Token deployed from Exploit location
```
