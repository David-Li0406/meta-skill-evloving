# SVG Specifications

## ViewBox Standard

### Tiles

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
```

### Tokens

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
```

## Edge Node Positions (SVG Units)

For 200x200 tile:

| Node   | Position   | World Equivalent |
| ------ | ---------- | ---------------- |
| Top    | (100, 0)   | (0, +1.0)        |
| Right  | (200, 100) | (+1.0, 0)        |
| Bottom | (100, 200) | (0, -1.0)        |
| Left   | (0, 100)   | (-1.0, 0)        |

## Path Attributes

```svg
<path
    d="..."
    fill="none"
    stroke="#FF2244"     <!-- or #44BBFF or #BB88FF -->
    stroke-width="8"
    stroke-linecap="butt"
/>
```

## Bezier Curves

Curved paths use cubic beziers:

```svg
<path d="M 100,0 C 100,55 145,100 200,100"/>
```

- Start: edge midpoint
- Control points: create smooth quarter-circle
- End: adjacent edge midpoint

## Grid Pattern (Background)

```svg
<line x1="40" y1="0" x2="40" y2="200"
      stroke="#222630" stroke-opacity="0.5"/>
```

40-unit spacing creates 5x5 internal grid.

## Color Values

| Element      | Hex     | Usage        |
| ------------ | ------- | ------------ |
| Red paths    | #FF2244 | stroke       |
| Blue paths   | #44BBFF | stroke       |
| Purple paths | #BB88FF | stroke       |
| Tile bg      | #151820 | fill         |
| Grid lines   | #222630 | stroke @ 50% |
