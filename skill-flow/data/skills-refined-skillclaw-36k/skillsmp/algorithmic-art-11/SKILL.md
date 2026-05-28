---
name: algorithmic-art
description: 'Tạo algorithmic art sử dụng p5.js với seeded randomness và interactive parameter exploration. Sử dụng khi user yêu cầu generative art, algorithmic art, flow fields, particle systems, creative coding. Tạo original algorithmic art.'
---

# Algorithmic Art Skill

Tạo algorithmic philosophies - computational aesthetic movements expressed through code. Output: .md files (philosophy), .html files (interactive viewer), .js files (algorithms).

## Khi Nào Sử Dụng

- Generative art
- Algorithmic art
- Flow fields
- Particle systems
- Creative coding với p5.js
- Interactive art pieces
- Seeded randomness art

## Workflow

```
1. Algorithmic Philosophy Creation (.md file)
2. Express by creating p5.js generative art (.html + .js files)
```

---

## Step 1: Algorithmic Philosophy Creation

### The Critical Understanding

Philosophy được interpreted through:
- Computational processes, emergent behavior, mathematical beauty
- Seeded randomness, noise fields, organic systems
- Particles, flows, fields, forces
- Parametric variation và controlled chaos

### How to Generate Algorithmic Philosophy

**1. Name the movement** (1-2 words):
- "Crystalline Emergence"
- "Digital Erosion"
- "Parametric Dreams"

**2. Articulate the philosophy** (4-6 paragraphs):

Express computational essence:
- What mathematical relationships govern the system?
- How does randomness interact with structure?
- What emergent behaviors arise?
- How does time affect the visualization?

### Essential Principles

| Principle | Description |
|-----------|-------------|
| **Algorithmic Philosophy** | Computational worldview expressed through code |
| **Process Over Product** | Beauty emerges from algorithm's execution |
| **Parametric Expression** | Ideas through mathematical relationships |
| **Artistic Freedom** | Room for interpretive implementation |
| **Pure Generative Art** | LIVING ALGORITHMS, not static images |
| **Expert Craftsmanship** | Meticulously crafted, refined through iterations |

---

## Step 2: P5.js Implementation

### Technical Requirements

**Seeded Randomness (Art Blocks Pattern)**:
```javascript
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);
```

**Parameter Structure**:
```javascript
let params = {
  seed: 12345,
  colorPalette: ['#d97757', '#6a9bcc', '#788c5d'],
  // Add parameters based on YOUR algorithm:
  // - Quantities (how many?)
  // - Scales (how big? how fast?)
  // - Probabilities (how likely?)
  // - Ratios (what proportions?)
  // - Angles (what direction?)
};
```

### Craftsmanship Requirements

**CRITICAL**: Gallery-quality computational art

- **Balance**: Complexity without visual noise
- **Color Harmony**: Thoughtful palettes, not random RGB
- **Composition**: Visual hierarchy even in randomness
- **Performance**: Smooth, optimized execution
- **Reproducibility**: Same seed = identical output

### Algorithm Guidance

| Philosophy | Consider Using |
|------------|----------------|
| **Organic emergence** | Elements accumulate/grow, natural rules, feedback loops |
| **Mathematical beauty** | Geometric relationships, trigonometric functions, ratios |
| **Controlled chaos** | Random variation within boundaries, order from disorder |

---

## Step 3: Interactive Artifact

### Required Features

**1. Seed Navigation** (FIXED):
- Seed display
- Previous/Next buttons
- Random button
- Jump to seed input

**2. Parameter Controls** (VARIABLE):
- Sliders cho numeric parameters
- Color pickers cho palette
- Real-time updates
- Reset button

**3. Actions** (FIXED):
- Regenerate button
- Reset button
- Download PNG button

### HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="controls">
    <!-- Seed controls -->
    <!-- Parameter controls -->
    <!-- Action buttons -->
  </div>
  <script>
    // ALL p5.js code inline
  </script>
</body>
</html>
```

**CRITICAL**: Single artifact. No external files (except p5.js CDN).

---

## Code Patterns

### Seeded Random
```javascript
function initializeSeed(seed) {
  randomSeed(seed);
  noiseSeed(seed);
}
```

### Color Utilities
```javascript
function colorFromPalette(index) {
  return params.colorPalette[index % params.colorPalette.length];
}
```

### Parameter Updates
```javascript
function updateParameter(paramName, value) {
  params[paramName] = value;
  regenerate();
}
```

---

## Output Format

1. **Algorithmic Philosophy** - Markdown explaining generative aesthetic
2. **Single HTML Artifact** - Self-contained interactive generative art

---

## Quick Reference

| Element | Type | Description |
|---------|------|-------------|
| Seed controls | Fixed | Always include |
| Parameters | Variable | Based on algorithm |
| Actions | Fixed | Regenerate, Reset, Download |
| Algorithm | Variable | Express philosophy |

**Remember**: The algorithm flows from the philosophy, not from a menu of options.
