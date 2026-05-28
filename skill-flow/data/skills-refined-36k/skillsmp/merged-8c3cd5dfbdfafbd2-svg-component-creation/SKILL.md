---
name: svg-component-creation
description: Use this skill to create dynamic SVG components and diagrams, allowing for state-based color control and precise layout design.
---

# SVG Component and Diagram Creation

This skill enables the transformation of inline SVG HTML into **state-based dynamic components** and the direct creation of detailed diagrams using SVG code.

## SVG Component Creation

Transform inline SVG HTML into a **state-based dynamic component**. Control colors using the `data-status` attribute and CSS selectors.

### ⚠️ Prerequisites

Before coding, ensure to read the following files with the Read tool:
1. [/RNBT_architecture/README.md](/RNBT_architecture/README.md) - Understand the architecture
2. [/.claude/guides/CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) - Coding style

### Core Principles

1. Define three sets of gradients in SVG `<defs>` (e.g., paint0-green, paint0-yellow, paint0-red).
2. Assign layer classes to SVG paths (e.g., layer-grad0, layer-fill-primary).
3. Control fill URLs using CSS `[data-status="xxx"]` selectors.
4. Change only the `dataset.status` in JS to trigger CSS color transitions.

**Advantage:** Efficient DOM manipulation without replacing innerHTML.

### Input/Output

**Input:** `Figma_Conversion/Static_Components/[project_name]/[component_name]/`

**Output:**
```
components/[ComponentName]/
├── views/component.html       # SVG + gradients + layer classes
├── styles/component.css       # [data-status] selectors
├── scripts/
│   ├── register.js            # setStatus, getStatus API
│   └── beforeDestroy.js
├── preview.html
└── README.md
```

### Layer Class Naming Conventions

| Class                | Purpose                |
|----------------------|-----------------------|
| `layer-grad0` ~ `layer-grad9` | Gradient fill         |
| `layer-fill-primary` | Primary solid color    |
| `layer-fill-secondary` | Secondary solid color  |
| `layer-stroke`      | Outline                |

### Core API

```javascript
// Change status - only modify data-status attribute
function setStatus(config, status) {
    container.dataset.status = status;  // CSS controls color
    this._currentStatus = status;
}

// Return current status
function getStatus() {
    return this._currentStatus;
}
```

### Prohibitions

- ❌ Changing colors by replacing innerHTML
- ❌ Mismatched creation/cleanup
- ❌ Using `function(response)` → must use `function({ response })`

## SVG Diagram Creation

Directly write SVG code to create detailed diagrams. This method is suitable for various layouts, including hierarchical structures, comparison diagrams, and tables.

### When to Use This Method

| Situation            | Suitable for Direct SVG Creation |
|----------------------|----------------------------------|
| **Hierarchical**     | OSI layers, organization charts   |
| **Structural**       | Architecture, system configuration |
| **Data Structures**  | Packet/frame structures, memory layouts |
| **Table Format**     | Comparison tables, specifications  |
| **Comparison Diagrams** | Side-by-side comparisons        |
| **State Diagrams**   | Circuit breakers, state machines   |
| **Detailed Layouts** | When precise positioning, size, and alignment are needed |

### Advantages

- Precise layout control
- Visual effects like gradients and shadows
- Consistent color palette application
- Full support for Korean text
- No additional tool installation required

### SVG Generation Rules

1. **Basic Structure**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
  <defs>
    <!-- Define gradients, markers -->
  </defs>
  <!-- Diagram elements -->
</svg>
```

2. **Color Palette (Required)**

#### Basic Node Colors

| Purpose | Gradient Start Color | Gradient End Color | Text Color |
|---------|----------------------|--------------------|------------|
| **Blue (Default)** | #3498DB | #2980B9 | white |
| **Green (Success)** | #2ECC71 | #27AE60 | white |
| **Red (Warning)** | #E74C3C | #C0392B | white |
| **Orange** | #E67E22 | #D35400 | white |
| **Yellow** | #F1C40F | #F39C12 | white |
| **Purple** | #9B59B6 | #8E44AD | white |
| **Teal** | #1ABC9C | #16A085 | white |

#### Background/Secondary Colors

| Purpose          | Color     | Usage               |
|------------------|-----------|---------------------|
| Title Text       | #2C3E50  | Header, title       |
| Secondary Text   | #7F8C8D  | Subtitle, labels     |
| Line/Border      | #7F8C8D  | Edges, dividers     |
| Light Background  | #ECF0F1  | Containers          |

3. **Gradient Definition Template**

```xml
<defs>
  <linearGradient id="nodeBlue" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#3498DB"/>
    <stop offset="100%" style="stop-color:#2980B9"/>
  </linearGradient>
  <!-- Additional gradients -->
</defs>
```

4. **Arrow Marker Definition**

```xml
<defs>
  <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#7F8C8D"/>
  </marker>
  <!-- Additional markers -->
</defs>
```

5. **Element Style Rules**

#### Circular Nodes (Trees, Graphs)

```xml
<circle cx="150" cy="50" r="18" fill="url(#nodeBlue)"/>
<text x="150" y="55" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">1</text>
```

#### Rectangular Boxes (Frames, Blocks)

```xml
<rect x="20" y="30" width="120" height="35" rx="5" fill="url(#nodeBlue)"/>
<text x="80" y="53" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Text</text>
```

#### Connecting Lines

```xml
<!-- Regular line -->
<line x1="50" y1="50" x2="150" y2="50" stroke="#7F8C8D" stroke-width="2"/>

<!-- Arrow line -->
<line x1="50" y1="50" x2="150" y2="50" stroke="#7F8C8D" stroke-width="2" marker-end="url(#arrowhead)"/>

<!-- Dashed line -->
<line x1="50" y1="50" x2="150" y2="50" stroke="#BDC3C7" stroke-width="2" stroke-dasharray="5,5"/>
```

#### Text

```xml
<!-- Title -->
<text x="200" y="25" text-anchor="middle" fill="#2C3E50" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Title</text>

<!-- Subtitle -->
<text x="200" y="40" text-anchor="middle" fill="#7F8C8D" font-family="Arial, sans-serif" font-size="10">Subtitle</text>

<!-- Label -->
<text x="100" y="80" fill="#7F8C8D" font-family="Arial, sans-serif" font-size="9">Label</text>
```

### Diagram Type Templates

1. **Tree Diagram**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200">
  <defs>
    <linearGradient id="nodeBlue" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3498DB"/>
      <stop offset="100%" style="stop-color:#2980B9"/>
    </linearGradient>
  </defs>

  <!-- Draw lines first -->
  <line x1="150" y1="35" x2="80" y2="85" stroke="#7F8C8D" stroke-width="2"/>
  <line x1="150" y1="35" x2="220" y2="85" stroke="#7F8C8D" stroke-width="2"/>

  <!-- Draw nodes -->
  <circle cx="150" cy="25" r="18" fill="url(#nodeBlue)"/>
  <text x="150" y="30" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">1</text>
</svg>
```

2. **Hierarchical Table (OSI Style)**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 200">
  <defs>
    <linearGradient id="layer1" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#E74C3C"/>
      <stop offset="100%" style="stop-color:#C0392B"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="250" y="20" text-anchor="middle" fill="#2C3E50" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Hierarchical Structure</text>

  <!-- Rows -->
  <rect x="20" y="35" width="40" height="25" fill="url(#layer1)" rx="3"/>
  <text x="40" y="52" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="11" font-weight="bold">1</text>
</svg>
```

3. **Sequence/Handshake Diagram**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300">
  <defs>
    <linearGradient id="clientGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3498DB"/>
      <stop offset="100%" style="stop-color:#2980B9"/>
    </linearGradient>
    <marker id="arrowR" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#E74C3C"/>
    </marker>
  </defs>

  <!-- Entities -->
  <rect x="80" y="40" width="80" height="30" fill="url(#clientGrad)" rx="5"/>
  <text x="120" y="60" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Client</text>

  <!-- Vertical line -->
  <line x1="120" y1="70" x2="120" y2="280" stroke="#3498DB" stroke-width="3"/>

  <!-- Message arrow -->
  <line x1="120" y1="100" x2="370" y2="100" stroke="#E74C3C" stroke-width="2" marker-end="url(#arrowR)"/>
  <rect x="200" y="85" width="100" height="22" fill="#E74C3C" rx="3"/>
  <text x="250" y="100" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="10" font-weight="bold">SYN</text>
</svg>
```

4. **Architecture/System Configuration Diagram**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="lbGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#E74C3C"/>
      <stop offset="100%" style="stop-color:#C0392B"/>
    </linearGradient>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#7F8C8D"/>
    </marker>
  </defs>

  <!-- Load Balancer -->
  <rect x="200" y="50" width="200" height="40" fill="url(#lbGrad)" rx="5"/>
  <text x="300" y="75" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Load Balancer</text>

  <!-- Arrow -->
  <line x1="300" y1="90" x2="300" y2="130" stroke="#7F8C8D" stroke-width="2" marker-end="url(#arrow)"/>
</svg>
```

5. **State Diagram (Circuit Breaker Style)**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 280">
  <defs>
    <linearGradient id="closedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#2ECC71"/>
      <stop offset="100%" style="stop-color:#27AE60"/>
    </linearGradient>
    <linearGradient id="openGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#E74C3C"/>
      <stop offset="100%" style="stop-color:#C0392B"/>
    </linearGradient>
  </defs>

  <!-- State Circle -->
  <circle cx="100" cy="100" r="45" fill="url(#closedGrad)"/>
  <text x="100" y="105" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="11" font-weight="bold">Closed</text>

  <!-- Transition Arrow (Curved) -->
  <path d="M 145 85 Q 225 40 305 85" fill="none" stroke="#E74C3C" stroke-width="2"/>
</svg>
```

### Writing Procedure

1. **Determine Diagram Type**: Select the appropriate template based on the content to be represented.
2. **Create SVG File**: Save as `cs/{category}/images/{diagram-name}.svg`.
3. **Reference in Markdown**: Use `![Description](./images/{diagram-name}.svg)`.
4. **Run git add**.

### Important Notes

1. **File Naming**: Use kebab-case (e.g., `osi-7-layer-structure.svg`).
2. **Location**: Save in the `cs/{category}/images/` folder.
3. **Font**: Use Arial, sans-serif (cross-platform compatibility).
4. **viewBox**: Adjust according to content size.
5. **Gradients**: Differentiate colors based on hierarchy/importance.
6. **Lines**: Draw before nodes (to appear behind).
7. **Text Size**: Title 14px, body