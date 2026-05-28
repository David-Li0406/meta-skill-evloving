---
name: frontend-creative-design
description: Use this skill when creating distinctive, bold UI designs that avoid generic AI aesthetics, focusing on typography, color palettes, layouts, and animations for various applications.
---

# Frontend Creative Design

Create distinctive, memorable interfaces that stand out from generic AI-generated aesthetics. This skill is ideal for designing new UI components, landing pages, marketing sites, or any project requiring a strong visual identity.

## Core Philosophy

Most AI-generated UIs suffer from "AI slop" - they're technically correct but visually bland. This skill helps you break that pattern by making **bold aesthetic choices** that give your interface a distinctive personality.

## When to Use

- Designing new UI components or layouts
- Selecting typography and font pairings
- Choosing color schemes and themes
- Implementing animations and micro-interactions
- Reviewing frontend designs for generic patterns
- Making design decisions for landing pages, dashboards, or web applications

## Instructions

### Step 1: Assess Design Context

Understand the project's brand identity, purpose, and target aesthetic before making design decisions.

**Key Questions**:
- What is the project's brand personality? (playful, professional, technical, etc.)
- Who is the target audience?
- What emotional response should the design evoke?
- What makes this project unique?

### Step 2: Typography Selection

Choose beautiful, unique, and interesting fonts that match the project's character.

**AVOID These Generic Fonts**:
- Inter, Roboto, Arial, System fonts

**Recommended Font Categories**:
- **Code/Technical Aesthetics**: JetBrains Mono, Fira Code
- **Editorial/Sophisticated**: Playfair Display, Crimson Pro
- **Modern/Clean**: Space Grotesk, DM Sans, Outfit

**Critical**: Vary font choices across different projects. No two designs should look like siblings.

### Step 3: Intentional Color Palettes

Create cohesive color systems using CSS variables with dominant colors and sharp accents.

**Principles**:
- Dominant colors with sharp accents > timid, evenly-distributed palettes
- Commit to a cohesive aesthetic using CSS variables
- Avoid clichéd color schemes (e.g., purple gradients on white backgrounds)

**Approach**:
- Choose 1-2 dominant colors that define the brand
- Add 1-2 sharp accent colors for calls-to-action and highlights

### Step 4: Bold Spatial Composition

Break the grid intentionally to create unique layouts.

**Avoid**: Everything centered, symmetric, grid-locked.

**Techniques**:
- Use negative space as a design element
- Overlap elements to create depth
- Break alignment rules purposefully

### Step 5: Motion as Personality

Use animations strategically for high-impact moments and delightful micro-interactions.

**Animation Priorities**:
1. High-impact moments: Orchestrated page loads with staggered reveals
2. Micro-interactions: Button hovers, transitions, state changes

**Implementation Guidelines**:
- Use CSS-only solutions for performance
- For React, use Framer Motion when available

### Step 6: Background & Atmosphere

Create depth and atmosphere through layered backgrounds and contextual effects.

**AVOID**:
- Defaulting to solid colors
- Flat, lifeless surfaces

**Recommended Approaches**:
- Layer CSS gradients for depth
- Use geometric patterns and subtle textures

### Step 7: Validate Against Anti-Patterns

Review the design against common AI-generated UI pitfalls.

**Anti-Pattern Checklist**:
- [ ] Not using Inter, Roboto, Arial, or system fonts
- [ ] Color palette has clear hierarchy (dominant + accent)
- [ ] Animations are orchestrated and purposeful
- [ ] Backgrounds have depth and atmosphere
- [ ] Typography is distinctive and matches brand personality

## Checklist

- [ ] No default fonts (Inter, Roboto, Arial)
- [ ] Custom color palette (not Tailwind defaults)
- [ ] Asymmetric or distinctive layout
- [ ] 1-2 high-impact animations only
- [ ] Background has depth (texture, gradient, or pattern)
- [ ] Coherent theme/mood throughout

## Recommended Tools

- **Fonts**: Google Fonts, Fontshare
- **Colors**: Realtime Colors, Happy Hues
- **Icons**: Lucide, Phosphor
- **Animation**: Framer Motion, React Spring

## Integration with Agents

This skill complements frontend-focused agents by providing specific, opinionated guidance for avoiding generic AI aesthetics. Use this skill when you need:
- Distinctive visual identity
- Creative typography and color choices
- Bold spatial compositions
- Production-ready animated components