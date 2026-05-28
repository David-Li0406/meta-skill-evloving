# Board SDK Simulator Setup

## Accessing the Simulator

Unity Menu: **Board > Input > Simulator**

## Creating Simulation Icons

Each game piece needs a `BoardContactSimulationIcon` ScriptableObject.

### Create Icon Asset

1. Right-click in Project: **Create > Board > Simulation > Icon**
2. Configure properties:

| Property                         | Description                            |
| -------------------------------- | -------------------------------------- |
| Display Name                     | Name in simulator palette              |
| Contact Type                     | `Finger` or `Glyph`                    |
| Glyph ID                         | Piece index (must match TokenDatabase) |
| Sprite                           | Visual for the icon                    |
| Size                             | Render size relative to 1920x1080      |
| Alpha Hit Test Minimum Threshold | Click detection sensitivity            |

### Example Icons for Zero-Day Attack

```text
RedAttackIcon.asset
├── Display Name: "Red Attack"
├── Contact Type: Glyph
├── Glyph ID: 0
└── Sprite: red-attack-token.png

BlueAttackIcon.asset
├── Display Name: "Blue Attack"
├── Contact Type: Glyph
├── Glyph ID: 3
└── Sprite: blue-attack-token.png

FingerIcon.asset
├── Display Name: "Finger"
├── Contact Type: Finger
└── Sprite: finger-icon.png
```

## Simulator Settings

Edit > Project Settings > Board > Simulation Settings

### Input Controls (Defaults)

| Action          | Control                  |
| --------------- | ------------------------ |
| Touch           | Left mouse button (hold) |
| Place           | Left click               |
| Lift            | Left click on contact    |
| Cancel          | Escape                   |
| Snap Rotate CW  | + key                    |
| Snap Rotate CCW | - key                    |
| Rotate          | Scroll wheel             |
| Fast Rotate     | Shift + scroll           |

### Rotation Settings

| Setting                  | Default | Description             |
| ------------------------ | ------- | ----------------------- |
| Snap Degrees             | 45      | Snap rotation increment |
| Rotation Speed           | 1.0     | Normal rotation speed   |
| Fast Rotation Multiplier | 3.0     | Speed with Shift held   |

## Simulator Palette

The simulator palette shows available icons. To add icons:

1. Open simulator window
2. Drag `BoardContactSimulationIcon` assets into palette
3. Or configure in Simulation Settings

## Usage

1. Open simulator window
2. Select icon from palette
3. Click in Game view to place
4. Drag to move
5. Scroll to rotate (Glyph only)
6. Hold mouse to simulate touch
7. Click placed contact to lift

## Limitations

- Maximum 1000 simultaneous contacts
- Only works in Editor (not builds)
- Generates identical `BoardContact` events as real hardware
