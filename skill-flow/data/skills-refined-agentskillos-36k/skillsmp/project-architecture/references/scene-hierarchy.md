# Scene Hierarchy

## GameplayScene Structure

```text
GameplayScene
├── MainCamera
│   └── [CameraController]
├── GlobalLight2D
├── GameManager
│   └── [GameManager]
├── TileManager
│   └── [TileManager]
├── TokenManager
│   └── [TokenManager]
├── InputManager
│   └── [InputManager]
├── BackgroundRenderer
│   └── [BackgroundRenderer]
├── GridOverlayRenderer
│   └── [GridOverlayRenderer]
├── Tiles
│   └── (spawned TileView instances at runtime)
└── Tokens
    └── (spawned TokenView instances at runtime)
```

## Parent-Child Relationships

- **Tiles** container: Parent for all spawned TileView GameObjects
- **Tokens** container: Parent for all spawned TokenView GameObjects
- Manager singletons are root-level GameObjects
- Runtime spawned objects go under appropriate containers

## Rendering Order (Sorting Order)

| Layer      | Order | Content                  |
| ---------- | ----- | ------------------------ |
| Background | -10   | Solid dark color         |
| Tiles      | 0     | TileView sprites         |
| Grid Glow  | 1-2   | GridOverlayRenderer glow |
| Grid Lines | 2     | GridOverlayRenderer core |
| Tokens     | 10    | TokenView sprites        |
