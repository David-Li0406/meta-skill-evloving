# Terminal Heritage Color Palette

## Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Surface | `C8C4B5` | 200, 196, 181 | Slide background |
| Navy | `1A2238` | 26, 34, 56 | Primary blocks, text |
| Navy Light | `2D3A52` | 45, 58, 82 | Secondary blocks |

## Accent Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Cream | `F5F3E8` | 245, 243, 232 | Human/outlined elements |
| Green | `4CAF50` | 76, 175, 80 | Success, completion |
| Orange | `FFA726` | 255, 167, 38 | Warnings, emphasis |
| Yellow | `FFD93D` | 255, 217, 61 | Highlights |
| Red | `C41E3A` | 196, 30, 58 | Errors, failures |

## Utility Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Muted | `9A968A` | 154, 150, 138 | Footers, secondary text |

## Color Constants (JavaScript)

```javascript
const COLORS = {
  surface: "C8C4B5",
  navy: "1A2238",
  navyLight: "2D3A52",
  cream: "F5F3E8",
  muted: "9A968A",
  green: "4CAF50",
  orange: "FFA726",
  yellow: "FFD93D",
  red: "C41E3A"
};
```

## Color Pairing Rules

### Text on Backgrounds

| Background | Text Color |
|------------|------------|
| Navy | Surface (C8C4B5) |
| Navy Light | Surface (C8C4B5) |
| Surface | Navy (1A2238) |
| Cream | Navy (1A2238) |
| Green | Navy (1A2238) |
| Orange | Navy (1A2238) |
| Yellow | Navy (1A2238) |
| Red | White (FFFFFF) |

### Gradient Simulation

To create the signature green-to-orange gradient:
1. Base shape with `fill: { color: "4CAF50" }`
2. Overlay shape with `fill: { color: "FFA726" }, transparency: 40`

```javascript
// Gradient accent example
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 0, y: 0, w: 4, h: 1,
  fill: { color: "4CAF50" }
});
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 2, y: 0, w: 2, h: 1,
  fill: { color: "FFA726" },
  transparency: 40
});
```

## Semantic Usage

- **AI activities**: Navy blocks
- **Human checkpoints**: Cream blocks with navy outline
- **External data/MCP**: Navy Light blocks
- **Success/completion**: Green blocks
- **Signals/awaits**: Green badges
- **Timeouts/warnings**: Orange badges
- **Failures**: Red blocks or text
- **Connectors**: Navy lines
