# Theming & Design System

SciChart Engine uses a powerful CSS-in-JS design system that allows for global themes and granular overrides.

## Predefined Themes
- `midnight`: High-contrast blue-on-black (Standard for Lab software).
- `electrochemistry`: Professional teal and gray tones.
- `dark`: Minimalist dark mode.
- `light`: Clean, high-readability light mode.

## Creating a Custom Theme
Use `createTheme` to define a brand-new aesthetic.

```typescript
import { createTheme } from 'scichart-engine';

const myCustomTheme = createTheme({
  name: 'cyberpunk',
  backgroundColor: '#0d0221',
  grid: {
    color: 'rgba(255, 0, 255, 0.1)',
    width: 0.5
  },
  axis: {
    color: '#00ffcc',
    labelColor: '#00ffcc',
    labelFont: '12px "Orbitron", sans-serif'
  }
});

chart.setTheme(myCustomTheme);
```

## Overriding Specific Elements
You can toggle or tweak specific visual elements without changing the entire theme.

```typescript
chart.setTheme({
  grid: { majorVisible: true, minorVisible: false },
  background: 'transparent' // Useful for overlaying on UI backgrounds
});
```

## CSS Variables Support
The engine can read from your application's CSS variables, allowing the chart to automatically follow your system-wide dark/light mode.

```typescript
const cssTheme = createTheme({
  backgroundColor: 'var(--bg-primary)',
  axis: {
    color: 'var(--text-secondary)',
    labelColor: 'var(--text-primary)'
  }
});
```

## Layout Configuration

Beyond visual styling, SciChart provides a dedicated `layout` system for controlling component positioning and behavior. See [Layout & Positioning Guide](./layout-positioning.md) for full details.

### Key Layout Options

```typescript
const chart = createChart({
  theme: 'midnight',
  layout: {
    // Legend behavior
    legend: {
      highlightOnHover: false,   // Don't change color (default)
      bringToFrontOnHover: true, // Bring to front (default)
      position: 'top-right',
    },
    
    // Crosshair value display
    crosshair: {
      valueDisplayMode: 'corner', // 'disabled' | 'corner' | 'floating'
      cornerPosition: 'top-left',
    },
    
    // Margins around the chart
    margins: { top: 30, right: 40, bottom: 60, left: 80 },
    
    // Axis spacing
    xAxisLayout: { titleGap: 12, labelGap: 6 },
    yAxisLayout: { titleGap: 10, labelGap: 4 },
  },
});
```

### Layout vs Theme

| Concern | Use Theme | Use Layout |
|---------|-----------|------------|
| Colors | ✅ | ❌ |
| Fonts | ✅ | ❌ |
| Grid styling | ✅ | ❌ |
| Component positions | ❌ | ✅ |
| Hover behavior | ❌ | ✅ |
| Margins/Padding | ❌ | ✅ |
| Axis spacing | ❌ | ✅ |

