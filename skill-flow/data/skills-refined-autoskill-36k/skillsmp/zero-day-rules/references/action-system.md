# Action System

## Turn Structure

Each turn consists of either:

- **Two (2) Single Actions** - any combination, any order
- **One (1) Double Action** - consumes entire turn

## Single Actions

| Action      | Description                                 | Restrictions                                   |
| ----------- | ------------------------------------------- | ---------------------------------------------- |
| **Draw**    | Take top tile from deck                     | None                                           |
| **Discard** | Remove one tile from reserve permanently    | Only after deck is empty                       |
| **Steal**   | Take one tile from opponent's reserve       | Max 2 per turn; opponent can only steal 1 back |
| **Place**   | Place tile adjacent to token's current edge | Must connect to token's position               |
| **Move**    | Move token along valid paths                | Color continuity rules apply                   |

### Draw

- Take one tile from top of draw pile
- Place in your reserve pool (face up)

### Discard

- Only available after deck is exhausted
- Remove one tile from your reserve
- Tile is out of game permanently
- If last tile discarded and pool empty, player cannot complete more actions

### Steal

- Take one tile from opponent's reserve pool
- If stealing 2 tiles in one turn, opponent can only steal 1 back on their turn

### Place (Single Action)

- Place tile from reserve onto board
- New tile must connect to edge where your token currently resides
- Token remains on edge node after placement

### Move

- Move token along valid paths of your color or purple
- Must maintain single color throughout one Move action
- Can travel unlimited distance along continuous same-color path

## Double Action: Place

- Place tile on ANY empty space adjacent to the tile where your token resides
- Not limited to the edge where token is positioned
- Consumes entire turn (no other actions allowed)
- Must still follow color matching rules

## Movement Rules

1. **Color Restriction:** Only traverse your color OR purple paths
2. **Single Color Per Action:** Must stay on one color within a Move:
   - Started on your color → continue on your color only
   - Started on purple → continue on purple only
3. **Color Junction:** At a node where both your color and purple continue:
   - Continue on current color, OR
   - End Move action at that node
   - Use another Move action to switch to other color
4. **Path Length:** Unlimited distance along continuous same-color path
5. **Non-Blocking:** Opponent tokens don't block movement
