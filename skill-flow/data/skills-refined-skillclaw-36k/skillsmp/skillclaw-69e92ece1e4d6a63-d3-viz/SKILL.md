---
name: d3-viz
description: Use this skill when creating interactive data visualisations with d3.js, especially for custom charts, graphs, network diagrams, or geographic visualisations that require detailed control over visual elements and interactions.
---

# D3.js Visualisation

## Overview

This skill provides guidance for creating sophisticated, interactive data visualisations using d3.js (Data-Driven Documents). D3.js excels at binding data to DOM elements and applying data-driven transformations to create custom, publication-quality visualisations with precise control over every visual element. The techniques work across any JavaScript environment, including vanilla JavaScript, React, Vue, Svelte, and other frameworks.

## When to use d3.js

**Use d3.js for:**
- Custom visualisations requiring unique visual encodings or layouts
- Interactive explorations with complex pan, zoom, or brush behaviours
- Network/graph visualisations (force-directed layouts, tree diagrams, hierarchies, chord diagrams)
- Geographic visualisations with custom projections
- Visualisations requiring smooth, choreographed transitions
- Publication-quality graphics with fine-grained styling control
- Novel chart types not available in standard libraries

**Consider alternatives for:**
- 3D visualisations - use Three.js instead

## Core workflow

### 1. Set up d3.js

Import d3 at the top of your script:

```javascript
import * as d3 from 'd3';
```

Or use the CDN version (7.x):

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
```

All modules (scales, axes, shapes, transitions, etc.) are accessible through the `d3` namespace.

### 2. Choose the integration pattern

**Pattern A: Direct DOM manipulation (recommended for most cases)**
Use d3 to select DOM elements and manipulate them imperatively. This works in any JavaScript environment:

```javascript
function drawChart(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart'); // Select by ID, class, or DOM element

  // Clear previous content
  svg.selectAll("*").remove();

  // Set up dimensions
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };

  // Create scales, axes, and draw visualisation
  // ... d3 code here ...
}
```