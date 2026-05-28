# LayoutConfig Constants

All layout values are in `Assets/Scripts/Config/LayoutConfig.cs`.

## Screen Dimensions

| Constant          | Value | Purpose                     |
| ----------------- | ----- | --------------------------- |
| `ScreenWidth`     | 19.2f | Total width in world units  |
| `ScreenHeight`    | 10.8f | Total height in world units |
| `CameraOrthoSize` | 5.4f  | Half of height              |

## Grid Dimensions

| Constant     | Value | Purpose                |
| ------------ | ----- | ---------------------- |
| `GridSize`   | 5     | Grid is 5x5 tiles      |
| `TileSize`   | 2.0f  | Each tile is 2x2 units |
| `GridLeft`   | -5.0f | Left edge of grid      |
| `GridRight`  | 5.0f  | Right edge of grid     |
| `GridBottom` | -5.0f | Bottom edge of grid    |
| `GridTop`    | 5.0f  | Top edge of grid       |

## Zone Dimensions

| Zone         | Left | Right | Width |
| ------------ | ---- | ----- | ----- |
| Blue UI      | -9.6 | -7.5  | 2.1   |
| Blue Reserve | -7.5 | -5.5  | 2.0   |
| Left Buffer  | -5.5 | -5.0  | 0.5   |
| Grid         | -5.0 | +5.0  | 10.0  |
| Right Buffer | +5.0 | +5.5  | 0.5   |
| Red Reserve  | +5.5 | +7.5  | 2.0   |
| Red UI       | +7.5 | +9.6  | 2.1   |

## Vertical Layout

| Zone          | Bottom | Top  | Height |
| ------------- | ------ | ---- | ------ |
| Bottom Margin | -5.4   | -5.0 | 0.4    |
| Grid          | -5.0   | +5.0 | 10.0   |
| Top Margin    | +5.0   | +5.4 | 0.4    |
