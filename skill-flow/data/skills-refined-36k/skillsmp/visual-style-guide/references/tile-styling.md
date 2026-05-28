# Tile Styling

## Tile Dimensions

| Property | SVG Units | World Units |
| -------- | --------- | ----------- |
| Size     | 200x200   | 2.0x2.0     |

## Import Settings

| Setting         | Value |
| --------------- | ----- |
| Texture Size    | 200   |
| Pixels Per Unit | 100   |

## Background

- Color: `#151820`
- Grid pattern: 40-unit spacing
- Grid line color: `#222630` at 50% opacity

## Path Specifications

| Property      | Value       |
| ------------- | ----------- |
| Path width    | 8 SVG units |
| Line cap      | butt        |
| Border/stroke | None        |

## Path SVG Format

```svg
<path d="M [start] C [control1], [control2], [end]"
      fill="none"
      stroke="[color]"
      stroke-width="8"
      stroke-linecap="butt"/>
```

## Edge Nodes

Paths connect at edge midpoints:

- Top: (100, 0) in SVG units
- Right: (200, 100)
- Bottom: (100, 200)
- Left: (0, 100)

## Path Types

1. **Straight**: Direct line between opposite edges
2. **Curved**: Quarter-circle between adjacent edges
3. **Mixed**: Tiles can have multiple path segments

## Center Tile (game-tile-13)

- Fixed position at grid (2,2)
- Cannot rotate
- Has paths to all four edges
- Blue Attack starts on Left node
- Red Attack starts on Right node
