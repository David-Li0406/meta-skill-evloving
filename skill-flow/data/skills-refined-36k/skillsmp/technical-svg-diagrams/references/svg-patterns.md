# SVG Pattern Templates

Complete, copy-ready SVG patterns for technical diagrams.

## Base Template

```xml
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e5e5e5" stroke-width="0.5"/>
    </pattern>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#ccc"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="800" height="400" fill="#fafafa"/>
  <rect width="800" height="400" fill="url(#grid)"/>

  <!-- Title -->
  <text x="40" y="40" font-family="monospace" font-size="14" fill="#333" font-weight="bold">TITLE_HERE</text>
  <text x="140" y="40" font-family="monospace" font-size="12" fill="#888">[ TAG_HERE ]</text>

  <!-- Content goes here -->

  <!-- Bottom note -->
  <text x="400" y="360" font-family="monospace" font-size="10" fill="#999" text-anchor="middle">summary note here</text>
</svg>
```

## Arrow Markers

**Gray arrow (default):**
```xml
<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
  <path d="M0,0 L0,6 L9,3 z" fill="#ccc"/>
</marker>
```

**Green arrow (success/positive):**
```xml
<marker id="arrowGreen" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
  <path d="M0,0 L0,6 L9,3 z" fill="#27ae60"/>
</marker>
```

**Red arrow (error/warning):**
```xml
<marker id="arrowRed" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
  <path d="M0,0 L0,6 L9,3 z" fill="#e74c3c"/>
</marker>
```

## Node Patterns

**Client/Entity node (circle with inner dot):**
```xml
<!-- Neutral state -->
<circle cx="100" cy="175" r="35" fill="none" stroke="#ccc" stroke-width="2"/>
<circle cx="100" cy="175" r="18" fill="#999"/>

<!-- Success state (green inner) -->
<circle cx="100" cy="175" r="35" fill="none" stroke="#ccc" stroke-width="2"/>
<circle cx="100" cy="175" r="18" fill="#27ae60"/>
```

**Node with label:**
```xml
<circle cx="100" cy="175" r="35" fill="none" stroke="#ccc" stroke-width="2"/>
<circle cx="100" cy="175" r="18" fill="#27ae60"/>
<rect x="60" y="225" width="80" height="24" fill="none" stroke="#ccc" stroke-width="1"/>
<text x="100" y="241" font-family="monospace" font-size="11" fill="#666" text-anchor="middle">NODE_NAME</text>
```

## Container Patterns

**Standard container:**
```xml
<rect x="250" y="130" width="130" height="90" fill="none" stroke="#ccc" stroke-width="2"/>
<text x="315" y="115" font-family="monospace" font-size="10" fill="#666" text-anchor="middle">CONTAINER_NAME</text>
```

**Sandbox/isolated container (dashed border):**
```xml
<rect x="470" y="130" width="120" height="90" fill="none" stroke="#f39c12" stroke-width="2" stroke-dasharray="5,3"/>
<text x="530" y="115" font-family="monospace" font-size="10" fill="#f39c12" text-anchor="middle">SANDBOX</text>
```

**Tool/component box (inside container):**
```xml
<rect x="270" y="155" width="90" height="40" fill="#fff" stroke="#27ae60" stroke-width="2"/>
<text x="315" y="180" font-family="monospace" font-size="10" fill="#27ae60" text-anchor="middle">tool_name</text>
```

**Multiple tools stacked:**
```xml
<rect x="300" y="120" width="160" height="45" fill="#fff" stroke="#3498db" stroke-width="1.5"/>
<text x="380" y="148" font-family="monospace" font-size="10" fill="#3498db" text-anchor="middle">tool_one</text>

<rect x="300" y="177" width="160" height="45" fill="#fff" stroke="#3498db" stroke-width="1.5"/>
<text x="380" y="205" font-family="monospace" font-size="10" fill="#3498db" text-anchor="middle">tool_two</text>

<rect x="300" y="234" width="160" height="45" fill="#fff" stroke="#3498db" stroke-width="1.5"/>
<text x="380" y="262" font-family="monospace" font-size="10" fill="#3498db" text-anchor="middle">tool_three</text>
```

## Arrow/Connection Patterns

**Horizontal arrow:**
```xml
<path d="M 140 175 L 240 175" stroke="#27ae60" stroke-width="2" fill="none" marker-end="url(#arrowGreen)"/>
<text x="190" y="195" font-family="monospace" font-size="9" fill="#27ae60" text-anchor="middle">label</text>
```

**Multiple outgoing arrows (fan out):**
```xml
<g stroke="#e74c3c" stroke-width="1.5" fill="none" stroke-dasharray="4,4">
  <path d="M 160 175 L 280 135"/>
  <path d="M 160 200 L 280 200"/>
  <path d="M 160 225 L 280 265"/>
</g>
```

**Return arrows (responses, lighter):**
```xml
<g stroke="#e74c3c" stroke-width="1" fill="none" opacity="0.5">
  <path d="M 280 145 L 160 185"/>
  <path d="M 280 210 L 160 210"/>
  <path d="M 280 275 L 160 235"/>
</g>
```

## Flow Diagram Elements

**Vertical guide line:**
```xml
<line x1="300" y1="70" x2="300" y2="650" stroke="#e0e0e0" stroke-width="1" stroke-dasharray="4,4"/>
```

**Start/end ellipse:**
```xml
<ellipse cx="300" cy="90" rx="100" ry="25" fill="#fff" stroke="#3498db" stroke-width="2"/>
<text x="300" y="95" font-family="monospace" font-size="11" fill="#3498db" text-anchor="middle">START_STATE</text>
```

**Process step (rectangle):**
```xml
<rect x="180" y="150" width="240" height="50" fill="#fff" stroke="#9b59b6" stroke-width="2"/>
<text x="300" y="180" font-family="monospace" font-size="11" fill="#9b59b6" text-anchor="middle">PROCESS_STEP</text>
```

**Decision diamond:**
```xml
<polygon points="300,320 380,365 300,410 220,365" fill="#fff" stroke="#e74c3c" stroke-width="2"/>
<text x="300" y="360" font-family="monospace" font-size="10" fill="#e74c3c" text-anchor="middle">DECISION</text>
<text x="300" y="375" font-family="monospace" font-size="8" fill="#999" text-anchor="middle">(detail)</text>
```

**Reject/fail path from decision:**
```xml
<path d="M 380 365 L 450 365" stroke="#e74c3c" stroke-width="1" stroke-dasharray="3,3"/>
<text x="470" y="370" font-family="monospace" font-size="9" fill="#e74c3c">REJECT</text>
```

**Vertical arrow with polygon head:**
```xml
<path d="M 300 115 L 300 140" stroke="#ccc" stroke-width="1.5"/>
<polygon points="295,138 300,148 305,138" fill="#ccc"/>
```

## Code Display (inside containers)

**Small code snippet:**
```xml
<text x="530" y="158" font-family="monospace" font-size="8" fill="#999" text-anchor="middle">async (api) =&gt; {</text>
<text x="530" y="172" font-family="monospace" font-size="8" fill="#666" text-anchor="middle">api.readDocument()</text>
<text x="530" y="186" font-family="monospace" font-size="8" fill="#999" text-anchor="middle">}</text>
```

## Labels and Notes

**Round trip labels:**
```xml
<text x="195" y="125" font-family="monospace" font-size="8" fill="#e74c3c">call_1</text>
<text x="195" y="145" font-family="monospace" font-size="7" fill="#e74c3c" opacity="0.6">response</text>
```

**Sub-label (smaller detail):**
```xml
<text x="380" y="158" font-family="monospace" font-size="7" fill="#999" text-anchor="middle">schema + validation + handler</text>
```

**Bottom summary note:**
```xml
<text x="400" y="360" font-family="monospace" font-size="10" fill="#999" text-anchor="middle">3 tools · multiple round trips</text>
```

## Complete Example: Architecture Diagram

```xml
<svg viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e5e5e5" stroke-width="0.5"/>
    </pattern>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#ccc"/>
    </marker>
    <marker id="arrowGreen" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#27ae60"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="800" height="350" fill="#fafafa"/>
  <rect width="800" height="350" fill="url(#grid)"/>

  <!-- Title -->
  <text x="40" y="40" font-family="monospace" font-size="14" fill="#333" font-weight="bold">SYSTEM_NAME</text>
  <text x="160" y="40" font-family="monospace" font-size="12" fill="#888">[ ARCHITECTURE ]</text>

  <!-- Client Node -->
  <circle cx="100" cy="175" r="35" fill="none" stroke="#ccc" stroke-width="2"/>
  <circle cx="100" cy="175" r="18" fill="#27ae60"/>
  <rect x="60" y="225" width="80" height="24" fill="none" stroke="#ccc" stroke-width="1"/>
  <text x="100" y="241" font-family="monospace" font-size="11" fill="#666" text-anchor="middle">CLIENT</text>

  <!-- Arrow to Service -->
  <path d="M 140 175 L 240 175" stroke="#27ae60" stroke-width="2" fill="none" marker-end="url(#arrowGreen)"/>
  <text x="190" y="195" font-family="monospace" font-size="9" fill="#27ae60" text-anchor="middle">request</text>

  <!-- Service Container -->
  <rect x="250" y="130" width="130" height="90" fill="none" stroke="#ccc" stroke-width="2"/>
  <text x="315" y="115" font-family="monospace" font-size="10" fill="#666" text-anchor="middle">SERVICE</text>

  <!-- Tool inside Service -->
  <rect x="270" y="155" width="90" height="40" fill="#fff" stroke="#27ae60" stroke-width="2"/>
  <text x="315" y="180" font-family="monospace" font-size="10" fill="#27ae60" text-anchor="middle">handler</text>

  <!-- Arrow to Database -->
  <path d="M 380 175 L 460 175" stroke="#ccc" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>

  <!-- Database -->
  <rect x="470" y="140" width="80" height="70" fill="none" stroke="#ccc" stroke-width="2"/>
  <text x="510" y="180" font-family="monospace" font-size="10" fill="#666" text-anchor="middle">DATABASE</text>

  <!-- Bottom note -->
  <text x="400" y="300" font-family="monospace" font-size="10" fill="#999" text-anchor="middle">simplified architecture · single request flow</text>
</svg>
```
