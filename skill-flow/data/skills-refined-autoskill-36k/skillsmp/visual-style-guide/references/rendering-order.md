# Rendering Order

## Sorting Order Values

Higher = renders in front.

| Layer         | Sorting Order | Content                      | Component           |
| ------------- | ------------- | ---------------------------- | ------------------- |
| Background    | -10           | Solid dark color (#0D0F14)   | BackgroundRenderer  |
| Tiles         | 0             | Tile sprites                 | TileView            |
| Grid Glow     | 1             | Wide semi-transparent purple | GridOverlayRenderer |
| Grid Core     | 2             | Thin bright purple lines     | GridOverlayRenderer |
| Reserve Lines | 1             | Blue/red zone boundaries     | GridOverlayRenderer |
| Edge Nodes    | 3             | Connection point indicators  | (future)            |
| Tokens        | 10            | Token sprites                | TokenView           |
| UI            | Canvas        | Player text, scores          | Unity UI            |

## Grid Glow Effect

Two-layer approach for cyberpunk glow:

```csharp
// Glow layer (sorting order 1)
Color glowColor = new Color(0.73f, 0.53f, 1f, 0.3f);  // #BB88FF @ 30%
float glowWidth = 0.2f;

// Core layer (sorting order 2)
Color coreColor = new Color(0.73f, 0.53f, 1f, 0.9f);  // #BB88FF @ 90%
float coreWidth = 0.08f;
```

## Common Issues

**Grid not visible?**

- Check TileView sortingOrder is 0 (not higher)
- Check GridOverlayRenderer glow=1, core=2
- Grid MUST have higher order than tiles
