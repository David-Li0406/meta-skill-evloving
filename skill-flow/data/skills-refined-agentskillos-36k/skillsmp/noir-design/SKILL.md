---
name: noir-design
description: Enforces the "Noir" aesthetic standards for THE LOST+UNFOUNDS. Use when creating or modifying UI components.
---

# Noir Design Skill

This skill ensures that all UI elements adhere to the project's signature "Noir" aesthetic.

## Core Design Principles

### 1. Color Palette (Monochrome)
- **Background**: ALWAYS `#000000` (Pure Black).
- **Text**: `#ffffff` (Pure White) or `rgba(255, 255, 255, 0.87)` for secondary text.
- **Borders**: `1px solid #ffffff` or semi-transparent white `rgba(255, 255, 255, 0.1)`.

### 2. Geometry & Borders
- **No Rounded Corners**: Set `border-radius: 0 !important` on all buttons, cards, and containers.
- **Borders**: Use rigid, thin borders. Avoid heavy shadows; use thin white outlines instead.

### 3. Typography
- **Font**: Use `Inter` or system sans-serif.
- **Case**: Use **UPPERCASE** for headers (h1, h2) and important navigation items to emphasize the "Noir" look.
- **Alignment (Critical)**: All body text MUST be `text-left`. Only the Amazon disclosure may be justified.

### 4. Interactive Elements
- **Glassmorphism**: When using overlays, use `rgba(0, 0, 0, 0.95)` with a white border.
- **Hover States**: Invert colors on hover (Black text on White background).
- **Animations**: Use "mechanical" animations (blinking cursors, sliding toasts) rather than soft fades.

## Common CSS Classes
- `.noir-card`: `border: 1px solid white; background: black; border-radius: 0;`
- `.noir-button`: `background: transparent; color: white; border: 1px solid white; padding: 0.5rem 1rem;`
- `.text-left`: Always prefer this for layout.
