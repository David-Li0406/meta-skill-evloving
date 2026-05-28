# Player Zones

## Player Orientation

Players sit facing each other:

- **Blue player**: Left side (x < 0)
- **Red player**: Right side (x > 0)

## Zone Layout

```text
|  Blue UI  | Blue Res | Buffer |   5×5 Grid   | Buffer | Red Res |  Red UI  |
|    2.1    |   2.0    |  0.5   |     10.0     |  0.5   |   2.0   |   2.1    |
```

## Zone Coordinates

### Blue Player (Left)

| Zone    | X Range      | Center | Width |
| ------- | ------------ | ------ | ----- |
| UI      | -9.6 to -7.5 | -8.55  | 2.1   |
| Reserve | -7.5 to -5.5 | -6.5   | 2.0   |

### Red Player (Right)

| Zone    | X Range      | Center | Width |
| ------- | ------------ | ------ | ----- |
| Reserve | +5.5 to +7.5 | +6.5   | 2.0   |
| UI      | +7.5 to +9.6 | +8.55  | 2.1   |

## UI Text Rotation

- **Blue UI**: Normal rotation (readable from left)
- **Red UI**: Rotated 180 degrees (readable from right)

## Reserve Pool Purpose

- Holds drawn tiles before placement
- Visible to both players
- Can hold up to 3 tiles per player
- Tiles can be stolen from opponent's reserve
