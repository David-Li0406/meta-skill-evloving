# Tile System

## Tile Inventory

| Type            | Quantity | Notes                                         |
| --------------- | -------- | --------------------------------------------- |
| Starting tile   | 1        | Fixed at center position [2,2], cannot rotate |
| Placeable tiles | 24       | Drawn and placed during gameplay              |
| **Total**       | 25       |                                               |

## Tile Properties

- **Size:** 200 x 200 SVG units (2.0 x 2.0 world units)
- **Edge Nodes:** 4 per tile (midpoint of each side)
  - Top, Right, Bottom, Left

## Path Segment Shapes

### Quarter-Circle Curves

- Connect two adjacent edge nodes (90 degrees apart)
- Examples: Left→Top, Top→Right, Right→Bottom, Bottom→Left

### Straight Lines

- Connect two opposite edge nodes (180 degrees apart)
- Examples: Left→Right, Top→Bottom

## Path Colors

| Color  | Hex       | Traversable By   |
| ------ | --------- | ---------------- |
| Red    | `#FF2244` | Red player only  |
| Blue   | `#44BBFF` | Blue player only |
| Purple | `#BB88FF` | Either player    |

## Path Layering

When paths visually cross within a tile:

- They do NOT connect at the center
- One path shows a visual "gap" (passes underneath)
- Paths remain logically separate

## Starting Tile (game-tile-13)

Special multi-path tile at center:

- Two blue curves: Left→Top, Right→Top
- Two red curves: Left→Bottom, Right→Bottom
- One purple straight: Left→Right

Starting positions:

- Blue Attack token: Left edge node
- Red Attack token: Right edge node

## Placement Rules

1. **Adjacency:** Must place next to already-placed tile
2. **Color Matching:** At connecting edges:
   - Red ↔ Red: Valid
   - Blue ↔ Blue: Valid
   - Purple ↔ Any: Valid
   - Red ↔ Blue (exclusively): **Invalid**
3. **Permanence:** Once placed, cannot move, remove, or rotate

## Tile Rotation

- Tiles can be rotated before placement (any 90-degree increment)
- EdgeNode values (Top, Right, Bottom, Left) are tile-local
- Center tile (game-tile-13) cannot rotate
