# East UI

> UI component definitions for the East language

[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE.md)
[![Node Version](https://img.shields.io/badge/node-%3E%3D22.0.0-brightgreen.svg)](https://nodejs.org)

**East UI** provides typed UI component definitions for the [East language](https://github.com/elaraai/East). Components return data structures describing UI layouts rather than rendering directly, enabling portability across different rendering environments.

## Features

- **📦 Layout Components** - Box, Stack, Grid, Splitter, Separator
- **📝 Typography** - Text, Code, Heading, Link, Highlight, Mark, List, CodeBlock
- **🔘 Buttons** - Button, IconButton with variants and states
- **📋 Forms** - Field, Input, Select, Checkbox, Switch, Slider, Textarea, TagsInput, FileUpload
- **📊 Collections** - Table, Gantt, DataList, TreeView
- **📈 Charts** - Area, Bar, Line, Pie, Radar, Scatter, Sparkline, BarList, BarSegment
- **💬 Feedback** - Alert, Progress
- **🏷️ Display** - Badge, Tag, Avatar, Stat, Icon
- **📂 Disclosure** - Accordion, Tabs, Carousel
- **🪟 Overlays** - Dialog, Drawer, Popover, Tooltip, Menu, HoverCard, ToggleTip, ActionBar
- **🎨 Styling** - Type-safe style variants (FontWeight, TextAlign, ColorScheme, Size, etc.)
- **🔄 State Management** - Platform functions for state read/write

## Installation

```bash
npm install @elaraai/east-ui @elaraai/east
```

## Quick Start

```typescript
import { East, ArrayType } from "@elaraai/east";
import { Stack, Text, Button, UIComponentType } from "@elaraai/east-ui";

// Define a UI component
const MyComponent = East.function(
    [],
    UIComponentType,
    $ => {
        return Stack.Root([
            Text.Root("Hello, World!", { fontSize: "xl", fontWeight: "bold" }),
            Button.Root("Click Me", { variant: "solid", colorPalette: "blue" }),
        ], { gap: "4", direction: "column" });
    }
);

// Convert to IR for serialization or rendering
const ir = MyComponent.toIR();
```

## Component Categories

| Category | Components | Description |
|----------|------------|-------------|
| **Layout** | `Box`, `Stack`, `Grid`, `Splitter`, `Separator` | Container and layout components |
| **Typography** | `Text`, `Code`, `Heading`, `Link`, `Highlight`, `Mark`, `List`, `CodeBlock` | Text and typography components |
| **Buttons** | `Button`, `IconButton` | Interactive button components |
| **Forms** | `Input`, `Select`, `Checkbox`, `Switch`, `Slider`, `Textarea`, `TagsInput`, `FileUpload`, `Field` | Form input components |
| **Collections** | `Table`, `Gantt`, `DataList`, `TreeView` | Data display components |
| **Charts** | `Chart.Area`, `Chart.Bar`, `Chart.Line`, `Chart.Pie`, `Chart.Radar`, `Chart.Scatter`, `Chart.BarList`, `Chart.BarSegment`, `Sparkline` | Data visualization |
| **Display** | `Badge`, `Tag`, `Avatar`, `Stat`, `Icon` | Visual display components |
| **Feedback** | `Alert`, `Progress` | User feedback components |
| **Disclosure** | `Accordion`, `Tabs`, `Carousel` | Content organization |
| **Overlays** | `Dialog`, `Drawer`, `Popover`, `Tooltip`, `Menu`, `HoverCard`, `ToggleTip`, `ActionBar` | Overlay components |
| **Container** | `Card` | Content container |

## Documentation

- **[USAGE.md](USAGE.md)** - Comprehensive guide with examples for all components
- **[East Documentation](https://github.com/elaraai/East)** - Core East language documentation

## Design Philosophy

East UI components are **declarative data structures**, not rendered elements:

1. **Portability** - UI definitions can be serialized and rendered in any environment
2. **Type Safety** - Full compile-time checking of component structure and styling
3. **Composability** - Components are East functions that return typed values
4. **Separation of Concerns** - UI logic (East UI) is separate from rendering (@elaraai/east-ui-components)

## Development

```bash
npm run build     # Compile TypeScript
npm run test      # Run test suite (requires build)
npm run lint      # Check code quality
```

## License

Dual-licensed:
- **Open Source**: [AGPL-3.0](LICENSE.md) - Free for open source use
- **Commercial**: Available for proprietary use - contact support@elara.ai

## Links

- **Live Showcase**: [https://elaraai.github.io/east-ui/](https://elaraai.github.io/east-ui/)
- **Website**: [https://elaraai.com/](https://elaraai.com/)
- **East Repository**: [https://github.com/elaraai/East](https://github.com/elaraai/East)
- **Issues**: [https://github.com/elaraai/east-ui/issues](https://github.com/elaraai/east-ui/issues)
- **Email**: support@elara.ai

---

*Developed by [Elara AI Pty Ltd](https://elaraai.com/) - Powering the computational layer of AI-driven business optimization.*
