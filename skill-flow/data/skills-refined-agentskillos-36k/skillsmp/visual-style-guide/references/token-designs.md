# Token Designs

## Token Dimensions

| Property | SVG Units   | World Units |
| -------- | ----------- | ----------- |
| Size     | 80x80       | 0.4x0.4     |
| Scale    | 20% of tile | -           |

## Import Settings

| Setting         | Value |
| --------------- | ----- |
| Texture Size    | 40    |
| Pixels Per Unit | 100   |

## Attack Token

Visual design:

- Three concentric circles (solid fill)
- Cross pattern overlay
- Color matches player (red/blue)

Represents: Active attack phase

## Exploit Token

Visual design:

- Two concentric circles (outline only)
- Faint cross pattern overlay
- Color matches player (red/blue)

Represents: Planted exploit marker (stays at firewall breach point)

## Ghost Token

Visual design:

- Four concentric circles
- Graduated opacity (30%, 50%, 70%, 100%)
- Color matches player (red/blue)

Represents: Shielded retreat phase

## Token Set (per player)

| Token        | File                   | GlyphId (example) |
| ------------ | ---------------------- | ----------------- |
| Red Attack   | token-red-attack.svg   | 0                 |
| Red Exploit  | token-red-exploit.svg  | 1                 |
| Red Ghost    | token-red-ghost.svg    | 2                 |
| Blue Attack  | token-blue-attack.svg  | 3                 |
| Blue Exploit | token-blue-exploit.svg | 4                 |
| Blue Ghost   | token-blue-ghost.svg   | 5                 |
