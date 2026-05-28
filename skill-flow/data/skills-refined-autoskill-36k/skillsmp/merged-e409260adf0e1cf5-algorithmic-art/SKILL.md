---
name: algorithmic-art
description: Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this skill when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems.
---

# Algorithmic Art Creation Guide

Create generative art using p5.js, featuring seeded randomness for reproducibility and interactive parameter exploration.

## The Process

This skill involves two main stages:

1. **Algorithmic Philosophy Creation** — Articulate a computational aesthetic philosophy that guides the generative process.
2. **Interactive p5.js Code** — Implement the philosophy in a self-contained HTML artifact that expresses the generative art through code.

## Algorithmic Philosophy Creation

To begin, create an **ALGORITHMIC PHILOSOPHY** that will be interpreted through:

- Computational processes, emergent behavior, mathematical beauty
- Seeded randomness, noise fields, organic systems
- Particles, flows, fields, forces
- Parametric variation and controlled chaos

### How to Generate an Algorithmic Philosophy

**Name the movement** (1-2 words): "Organic Turbulence" / "Quantum Harmonics" / "Emergent Stillness"

**Articulate the philosophy** (4-6 paragraphs):

- Describe how this philosophy manifests through computational processes and mathematical relationships.
- Discuss noise functions and randomness patterns.
- Explain particle behaviors and field dynamics.
- Explore temporal evolution and system states.
- Define parametric variation and emergent complexity.

**Critical Guidelines:**

- Avoid redundancy: Each algorithmic aspect should be mentioned once.
- Emphasize craftsmanship: The final algorithm should appear meticulously crafted, refined through countless iterations.
- Leave creative space: Be specific about the algorithmic direction, but concise enough to allow for interpretive implementation choices.

### Philosophy Examples

- **"Organic Turbulence"**: Chaos constrained by natural law, order emerging from disorder.
- **"Quantum Harmonics"**: Discrete entities exhibiting wave-like interference patterns.
- **"Recursive Whispers"**: Self-similarity across scales, infinite depth in finite space.
- **"Field Dynamics"**: Invisible forces made visible through their effects on matter.
- **"Stochastic Crystallization"**: Random processes crystallizing into ordered structures.

## Technical Implementation

### Seeded Randomness

Always use seeded randomness for reproducibility:

```javascript
function setup() {
  randomSeed(42);
  noiseSeed(42);
}
```

### Parameter Structure

Define parameters that control the generative art:

```javascript
let params = {
  seed: 12345, // Always include seed for reproducibility
  // Add parameters that control YOUR algorithm:
  // - Quantities (how many?)
  // - Scales (how big? how fast?)
  // - Probabilities (how likely?)
  // - Ratios (what proportions?)
  // - Angles (what direction?)
  // - Thresholds (when does behavior change?)
};
```

### Core Algorithm

The algorithm should express the philosophy. Consider the following:

- If the philosophy is about **organic emergence**, use elements that accumulate or grow over time.
- If the philosophy is about **mathematical beauty**, utilize geometric relationships and ratios.
- If the philosophy is about **controlled chaos**, implement random variation within strict boundaries.

### Canvas Setup

Standard p5.js structure:

```javascript
function setup() {
  createCanvas(1200, 1200);
  // Initialize your system
}

function draw() {
  // Your generative algorithm
}
```

## Craftsmanship Requirements

To achieve mastery, create algorithms that feel like they emerged through countless iterations by a master generative artist. Ensure every pattern emerges with purpose, maintaining:

- Balance: Complexity without visual noise.
- Color Harmony: Thoughtful palettes.
- Composition: Visual hierarchy and flow.
- Performance: Smooth execution.
- Reproducibility: Same seed produces identical output.

## Interactive Artifact Creation

Create a single, self-contained HTML artifact that works immediately in any browser. Use the following structure:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
  <style>
    /* All styling inline - clean, minimal */
  </style>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="controls">
    <!-- All parameter controls -->
  </div>
  <script>
    // ALL p5.js code inline here
  </script>
</body>
</html>
```

### Required Features

1. **Parameter Controls**: Sliders for numeric parameters, color pickers for palette colors, and real-time updates.
2. **Seed Navigation**: Display current seed number with buttons for previous, next, random, and jump to specific seed.
3. **Actions**: Include buttons for regenerating, resetting, and downloading the artwork.

## The Creative Process

1. **Interpret the user's intent** - What aesthetic is being sought?
2. **Create an algorithmic philosophy** (4-6 paragraphs) describing the computational approach.
3. **Implement it in code** - Build the algorithm that expresses this philosophy.
4. **Design appropriate parameters** - What should be tunable?
5. **Build matching UI controls** - Sliders/inputs for those parameters.

## Resources

This skill includes helpful templates and documentation:

- **templates/viewer.html**: Starting point for all HTML artifacts.
- **templates/generator_template.js**: Reference for p5.js best practices and code structure principles.

Trust creativity and let the philosophy guide the implementation to achieve the best results in generative art.