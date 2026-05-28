# Skill Creator Guidelines

**Version 1.0.0**  
Anthropic / User  
January 2026

> **Note:**  
> This document is mainly for agents and LLMs to follow when creating,  
> maintaining, or refactoring AI agent skills. Humans may also find  
> it useful, but guidance here is optimized for automation and  
> consistency by AI-assisted workflows.

---

## Abstract

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic 'AI slop' aesthetics.

---

## Table of Contents

1. [Design Thinking](#1-design-thinking) — **CRITICAL**
   - 1.1 [Establish Creative Direction](#11-establish-creative-direction)
2. [Visual Aesthetics](#2-visual-aesthetics) — **HIGH**
   - 2.1 [Atmospheric Details](#21-atmospheric-details)
   - 2.2 [Color & Theme](#22-color--theme)
   - 2.3 [Motion & Interactivity](#23-motion--interactivity)
   - 2.4 [Typography Choices](#24-typography-choices)
3. [Composition & Layout](#3-composition-&-layout) — **HIGH**
   - 3.1 [Spatial Composition](#31-spatial-composition)
4. [Implementation](#4-implementation) — **MEDIUM**
   - 4.1 [Implementation Quality](#41-implementation-quality)

---

## 1. Design Thinking

**Impact: CRITICAL**

Conceptual direction, purpose, and tone.

### 1.1 Establish Creative Direction

**Impact: MEDIUM**

Before coding, understand the context and commit to a BOLD aesthetic direction. Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

- **Purpose**: What problem does this interface solve? Who uses it?

- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.

- **Constraints**: Technical requirements (framework, performance, accessibility).

- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**Incorrect:**

**Generic/Vague**

Make a modern, clean landing page for a SaaS product.

**Correct:**

**Specific/Bold**

Design a brutalist, industrial landing page. Use raw layout lines, monospace typography (JetBrains Mono), and high-contrast black and electric blue (#00F0FF). The interface should feel like a technical blueprint or terminal, with grid-breaking heavy borders and rigid spacing.

---

## 2. Visual Aesthetics

**Impact: HIGH**

Typography, color, motion, and visual details.

### 2.1 Atmospheric Details

**Impact: MEDIUM**

Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

**Incorrect:**

**Flat Surfaces**

Using plain solid colors for backgrounds and cards. The interface feels paper-thin and digital-default.

**Correct:**

**Texture & Depth**

Layer visual elements to create a sense of material or space.

- **Noise/Grain**: Overlay a subtle static noise texture to soften digital sharpness.

- **Lighting**: Use radial gradients to simulate a light source (vignette), drawing focus to the center.

- **Blur**: Use backdrop-blur on overlay elements to create a "frosted glass" depth.

- **Borders**: Instead of a 1px solid border, try a semi-transparent white border that looks like a highlight catching the edge of glass.

### 2.2 Color & Theme

**Impact: MEDIUM**

Commit to a cohesive aesthetic. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Vary between light and dark themes. NEVER use generic AI-generated aesthetics like cliched color schemes (particularly purple gradients on white backgrounds).

**Incorrect:**

**The "AI Default"**

Using a white background (`#ffffff`) with a generic primary blue/purple (`#6366f1`) and dark grey text. This signals "unbranded prototype" immediately.

**Correct:**

**Cohesive Atmosphere**

Define a palette where the background and text interact to create a mood, not just contrast. Use slightly tinted blacks or whites.

_Example Concept: "Midnight Rust"_

- **Background**: Warm, deep charcoal (not pure black).

- **Text**: Off-white/Bone (softer than pure white).

- **Primary Accent**: International Safety Orange (high energy, restricted usage).

- **Secondary Accent**: Warm Grey (supporting structure).

- **Result**: Feels industrial, warm, and sophisticated.

### 2.3 Motion & Interactivity

**Impact: MEDIUM**

Use animations for effects and micro-interactions. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.

**Incorrect:**

**Static or jarring**

Elements appear instantly upon load, or everything animates chaotically at the same time. Hover states are limited to simple color changes.

**Correct:**

**Choreographed & Fluid**

Orchestrate entrances so the user is guided through the content.

_Example Choreography:_

1.  **Stage**: Layout loads invisibly.

2.  **Act 1 (0ms)**: Main headline rises from below with a heavy ease-out.

3.  **Act 2 (+100ms)**: Navigation fades in from top.

4.  **Act 3 (+200ms)**: Content cards cascade in one by one (staggered delay).

5.  **Interaction**: Cards don't just change color on hover—they lift (scale up), cast a deeper shadow, and perhaps reveal secondary information.

### 2.4 Typography Choices

**Impact: MEDIUM**

Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.

**Incorrect:**

**Generic Default**

Relying on system fonts or ubiquitous, neutral sans-serifs (like Inter or Roboto) without intent. This creates a "generic template" feel.

**Correct:**

**Intentional Pairing**

Select a display font with strong personality (e.g., an expressive serif, a brutalist mono, or a high-contrast geometric sans) for headings. Pair it with a highly legible but distinct body font.

_Example Pairing:_

- **Headings**: _Syne_ (Art-house, wide distinct curves)

- **Body**: _Space Grotesk_ (Technical, monospace-inspired sans)

- **Effect**: Creates a "Gallery/Tech" atmosphere rather than a "Std Admin Dashboard" look.

---

## 3. Composition & Layout

**Impact: HIGH**

Spatial arrangement, grids, and layout patterns.

### 3.1 Spatial Composition

**Impact: MEDIUM**

Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density. Avoid predictable layouts.

**Incorrect:**

**Standard Container**

Centering everything in a standard 1200px container with consistent padding. Header centered, Subtext centered, 3-column grid below. It looks like a template.

**Correct:**

**Dynamic Tension**

Break the grid to create visual interest.

- **Asymmetry**: Place a massive headline on the left, but balance it with a small, dense block of technical text on the far bottom-right.

- **Overlap**: Allow images to drift behind text, or text to overlap borders.

- **Whitespace**: Leave 40% of the screen empty to give the remaining elements monumental weight.

- **Scale**: Contrast tiny meta-data (10px) with enormous display text (120px).

---

## 4. Implementation

**Impact: MEDIUM**

Technical implementation, code quality, and framework usage.

### 4.1 Implementation Quality

**Impact: MEDIUM**

Implement real working code that is production-grade, functional, and meticulously refined. Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code; minimalist designs need restraint/precision. Avoid cookie-cutter design that lacks context-specific character.

**Incorrect:**

**MVP/Prototype Quality**

Code that technically "works" but lacks polish—jumpy transitions, default browser focus rings, unstyled loading states, or poor responsiveness on mobile.

**Correct:**

**Production Craftsmanship**

The implementation creates a seamless, app-like feel regardless of the technology stack.

- **Interaction State**: Every interactive element has defined hover, focus, active, and disabled states.

- **Accessibility**: Focus indicators are styled to match the theme but remain high-contrast. Semantic HTML is used for structure.

- **Resilience**: Layouts adapt fluidly to any screen size, not just rigid breakpoints. Text doesn't overflow containers when content changes.

---

