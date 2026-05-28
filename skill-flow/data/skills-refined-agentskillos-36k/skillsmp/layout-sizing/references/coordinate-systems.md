# Coordinate Systems

## Three Coordinate Systems

| System     | Origin             | Units           | Range                          |
| ---------- | ------------------ | --------------- | ------------------------------ |
| **Grid**   | Bottom-left of 5x5 | Integer indices | (0,0) to (4,4)                 |
| **World**  | Screen center      | Float units     | -9.6 to +9.6 X, -5.4 to +5.4 Y |
| **Screen** | Bottom-left        | Pixels          | 0 to 1920 X, 0 to 1080 Y       |

## Grid to World Conversion

```csharp
// From LayoutConfig
float x = GridLeft + (gridX * TileSize) + (TileSize / 2f);
float y = GridBottom + (gridY * TileSize) + (TileSize / 2f);
```

| Grid  | World Center |
| ----- | ------------ |
| (0,0) | (-4, -4)     |
| (2,2) | (0, 0)       |
| (4,4) | (4, 4)       |
| (0,4) | (-4, 4)      |
| (4,0) | (4, -4)      |

## Screen to World Conversion

```csharp
Vector3 screenPoint = new Vector3(screenX, screenY, Camera.main.nearClipPlane);
Vector3 worldPoint = Camera.main.ScreenToWorldPoint(screenPoint);
```

Board SDK uses bottom-left origin, same as Unity's Screen space.

## Node Positions (Tile-Relative)

Each tile has 4 edge nodes at side midpoints:

| Node   | Offset from Tile Center |
| ------ | ----------------------- |
| Top    | (0, +1.0)               |
| Right  | (+1.0, 0)               |
| Bottom | (0, -1.0)               |
| Left   | (-1.0, 0)               |
