# Scoring and Endgame

## Game End Trigger

Three sequential conditions must occur:

1. **Deck is empty** - No tiles remain in draw pile
2. **One player ends turn with no tiles** - Reserve pool exhausted
3. **Other player takes final turn** - One more turn after trigger

## Scoring Procedure

### Step 1: Identify Path

Each player identifies the path between their Exploit and Ghost tokens.

### Step 2: Count Segments

Count segments of the player's **OWN color only** (not purple) along that path.

### Segment Types

| Type                                  | Count     |
| ------------------------------------- | --------- |
| Quarter-circle curve (player's color) | 1 segment |
| Straight line (player's color)        | 1 segment |

### Special Case: Starting Tile

If path crosses the starting tile using two quarter-curves of player's color, count both as separate segments.

### Step 3: Determine Winner

**Player with most segments of their own color wins.**

## Tiebreaker

If segment counts are equal:

- Count **purple segments** along each player's path
- Player with more purple segments wins

## Path Selection

When counting segments:

- Players select the valid path with the most segments of their color
- Each path segment can only be counted once
- Each path segment can only be traversed once in the selected path

## Example Scoring

```text
Red Player:
- Exploit at top-right edge
- Ghost at bottom-left
- Path includes: 8 red curves + 4 red straights = 12 segments

Blue Player:
- Exploit at left edge
- Ghost at right side
- Path includes: 10 blue curves + 3 blue straights = 13 segments

Winner: Blue (13 > 12)
```

## Edge Cases

### No Valid Path

If no valid path exists between Exploit and Ghost:

- Score is 0 for that player

### Player Cannot Complete Phase 1

If game ends before a player reaches the firewall:

- That player cannot score (no Exploit placed)

### Discard to Empty

If a player discards their final tile and has empty reserve:

- That player may not complete any more actions or turns
- Triggers game end sequence
