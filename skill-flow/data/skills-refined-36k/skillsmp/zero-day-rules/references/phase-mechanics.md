# Phase Mechanics

## Game Flow Overview

```text
Setup → Phase 1 (Attack) → Midpoint (Exploit) → Phase 2 (Ghost) → Game End
```

Each player progresses through phases independently.

## Setup Phase

1. Determine first player and choose colors
2. Seat positions: Red at right, Blue at left (landscape orientation)
3. Attack tokens placed on starting nodes of center tile
4. Each player draws 5 tiles from shuffled deck
5. **First player:**
   - Places 1 tile adjacent to center tile (at a purple node)
   - Keeps 3 tiles in reserve pool (face down initially)
   - Shuffles 1 tile back into deck
6. **Second player:** Same as first player
7. Both players flip their 3 reserve tiles face-up

## Phase 1: Attack

**Goal:** Move Attack token to reach a firewall node (board edge)

**Actions:**

- Place tiles to extend paths
- Move Attack token along valid paths

**Phase ends when:** Attack token reaches any edge node on the board boundary (firewall breach)

## Midpoint: Exploit

**Trigger:** Attack token reaches firewall

**Actions (automatic, not consuming turn actions):**

1. Replace Attack token with Exploit token at the same node
2. Exploit token remains at this location for rest of game

If remaining actions in turn, player continues with those actions.

## Phase 2: Ghost

**Goal:** Move Ghost token as far as possible from the Exploit token

**First Move action after Exploit placement:**

1. Place Ghost token at the Exploit token's node
2. Move Ghost token away from Exploit in the same Move action

**Ongoing:**

- Place tiles to extend paths
- Move Ghost token along valid paths

## Phase Transitions

| From     | To       | Trigger                                       |
| -------- | -------- | --------------------------------------------- |
| Setup    | Phase 1  | Both players complete initial placement       |
| Phase 1  | Midpoint | Attack token reaches board edge               |
| Midpoint | Phase 2  | Exploit placed (automatic)                    |
| Phase 2  | Game End | Deck empty + player has no tiles + final turn |

## Independent Progression

Players may be in different phases simultaneously:

- Player A in Phase 2 while Player B still in Phase 1
- Both players continue taking alternating turns regardless of phase
