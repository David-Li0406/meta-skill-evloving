---
title: CSS Patterns Reference
description: Hover effects, transitions, gradients, pseudo-elements for GenerateBlocks
---

# CSS Patterns Reference

Common CSS patterns for GenerateBlocks V2 layouts.

## Styles vs CSS Attribute

| Feature | `styles` (JSON) | `css` (string) |
|---------|-----------------|----------------|
| Basic properties | Yes | Yes (duplicate) |
| Hover states | No | Yes |
| Focus states | No | Yes |
| Pseudo-elements | No | Yes |
| Media queries | No | Yes |
| Transitions | No | Yes |
| Animations | No | Yes |
| Gradients | No | Yes |
| Complex selectors | No | Yes |

**Rule:** Put basic properties in BOTH. Put complex features in `css` only.

---

## Hover Effects

### Basic Hover

```json
{
  "styles": {"backgroundColor": "#c0392b", "color": "#ffffff"},
  "css": ".gb-text-btn001{background-color:#c0392b;color:#ffffff;transition:all 0.3s}.gb-text-btn001:hover{background-color:#a33024}"
}
```

### Lift on Hover (Cards)

```css
.gb-text-card001{transition:all 0.3s}.gb-text-card001:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.15)}
```

### Scale on Hover (Icons)

```css
.gb-shape-icon001{transition:transform 0.3s}.gb-shape-icon001:hover{transform:scale(1.1)}
```

### Color Change on Hover

```css
.gb-text-link001{color:#0a0a0a;transition:color 0.3s}.gb-text-link001:hover{color:#c0392b}
```

### Parent Hover Affecting Child

```css
.gb-text-card001:hover .gb-element-icon001{background-color:#c0392b;color:white;transform:scale(1.05) rotate(-3deg)}
```

---

## Transition Patterns

### Standard Transition

```css
transition:all 0.3s
```

### Cubic Bezier (Smooth)

```css
transition:all 0.4s cubic-bezier(0.16, 1, 0.3, 1)
```

### Specific Properties

```css
transition:transform 0.3s, box-shadow 0.3s, background-color 0.3s
```

### Staggered Transition

```css
transition:transform 0.3s, opacity 0.3s 0.1s
```

---

## Pseudo-Elements

### Animated Underline (::after)

```css
.gb-text-card001::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:3px;background:#c0392b;transform:scaleX(0);transform-origin:left;transition:transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)}.gb-text-card001:hover::after{transform:scaleX(1)}
```

### Decorative Border (::before)

```css
.gb-element-quote001::before{content:'';position:absolute;top:0;left:0;width:4px;height:100%;background:#c0392b}
```

### Background Gradient Overlay (::before)

```css
.gb-element-hero001::before{content:'';position:absolute;top:0;right:0;width:60%;height:100%;background:radial-gradient(circle at 100% 0%, rgba(192, 57, 43, 0.2) 0%, transparent 60%);pointer-events:none}
```

### Stat Dividers (::after)

```css
.gb-element-stat001:not(:last-child)::after{content:'';position:absolute;right:0;top:50%;transform:translateY(-50%);width:1px;height:40px;background:linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.08) 50%, transparent 100%)}
```

---

## Gradient Patterns

### Linear Gradient Background

```css
background:linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)
```

### Radial Gradient Accent

```css
background:radial-gradient(circle at 100% 0%, rgba(192, 57, 43, 0.15) 0%, transparent 60%)
```

### Text Overlay Gradient

```css
background:linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.7) 100%)
```

### Border Gradient (Fake)

```css
.gb-element-card001{background:linear-gradient(white, white) padding-box, linear-gradient(135deg, #c0392b, #e74c3c) border-box;border:2px solid transparent}
```

---

## Box Shadows

### Subtle Elevation

```css
box-shadow:0 2px 4px rgba(0,0,0,0.1)
```

### Medium Elevation

```css
box-shadow:0 4px 12px rgba(0,0,0,0.15)
```

### Strong Elevation (Hover)

```css
box-shadow:0 20px 60px rgba(0,0,0,0.15)
```

### Colored Shadow

```css
box-shadow:0 4px 12px rgba(192,57,43,0.3)
```

### Inset Shadow

```css
box-shadow:inset 0 2px 4px rgba(0,0,0,0.1)
```

---

## Button Patterns

### Primary Button

```json
{
  "styles": {
    "display": "inline-flex",
    "alignItems": "center",
    "gap": "0.5rem",
    "padding": "0.875rem 1.75rem",
    "backgroundColor": "#c0392b",
    "color": "#ffffff",
    "borderRadius": "2rem",
    "fontSize": "1rem",
    "fontWeight": "600",
    "textDecoration": "none"
  },
  "css": ".gb-text-btn001{display:inline-flex;align-items:center;gap:0.5rem;padding:0.875rem 1.75rem;background-color:#c0392b;color:#ffffff;border-radius:2rem;font-size:1rem;font-weight:600;text-decoration:none;transition:all 0.3s}.gb-text-btn001:hover{background-color:#a33024;transform:translateY(-2px);box-shadow:0 4px 12px rgba(192,57,43,0.3)}"
}
```

### Secondary Button

```css
.gb-text-btn002{display:inline-flex;align-items:center;gap:0.5rem;padding:0.875rem 1.75rem;background-color:transparent;color:#0a0a0a;border:2px solid #e5e5e5;border-radius:2rem;font-size:1rem;font-weight:600;text-decoration:none;transition:all 0.3s}.gb-text-btn002:hover{border-color:#c0392b;color:#c0392b;background-color:rgba(192,57,43,0.04)}
```

### Ghost Button (Dark BG)

```css
.gb-text-btn003{display:inline-flex;padding:0.75rem 1.5rem;background:rgba(255,255,255,0.1);color:#ffffff;border-radius:0.5rem;font-weight:600;text-decoration:none;transition:all 0.3s}.gb-text-btn003:hover{background:rgba(255,255,255,0.2)}
```

---

## Card Patterns

### Basic Card with Hover

```css
.gb-text-card001{display:flex;flex-direction:column;background-color:white;border-radius:1rem;padding:2rem;border:1px solid transparent;text-decoration:none;transition:all 0.3s}.gb-text-card001:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.15);border-color:#e5e5e5}
```

### Card with Animated Underline

```css
.gb-text-card001{position:relative;display:flex;flex-direction:column;background-color:white;border-radius:1rem;padding:2rem;text-decoration:none;transition:all 0.3s}.gb-text-card001::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:3px;background:#c0392b;transform:scaleX(0);transform-origin:left;transition:transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)}.gb-text-card001:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.15)}.gb-text-card001:hover::after{transform:scaleX(1)}
```

### Featured Dark Card

```css
.gb-element-feat001{grid-column:span 2;grid-row:span 2;background:linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);min-height:26rem;position:relative;display:flex;flex-direction:column;gap:1rem;border-radius:1rem;padding:2rem}.gb-element-feat001::before{content:'';position:absolute;top:0;right:0;width:60%;height:100%;background:radial-gradient(circle at 100% 0%, rgba(192, 57, 43, 0.2) 0%, transparent 60%);pointer-events:none}.gb-element-feat001>*{position:relative;z-index:1}
```

---

## Icon Container Patterns

### Basic Icon Box

```css
.gb-element-icon001{width:3.5rem;height:3.5rem;display:flex;align-items:center;justify-content:center;background-color:#f5f5f3;border-radius:1rem;color:#c0392b;font-size:1.5rem}
```

### Icon with Parent Hover

```css
.gb-element-icon001{width:3.5rem;height:3.5rem;display:flex;align-items:center;justify-content:center;background-color:#f5f5f3;border-radius:1rem;color:#c0392b;transition:all 0.3s}.gb-text-card001:hover .gb-element-icon001{background-color:#c0392b;color:white;transform:scale(1.05) rotate(-3deg)}
```

### Social Icon Button

```css
.gb-text-social001{width:2.5rem;height:2.5rem;display:flex;align-items:center;justify-content:center;background-color:rgba(255,255,255,0.1);border-radius:50%;color:#ffffff;font-size:1.25rem;text-decoration:none;transition:all 0.3s}.gb-text-social001:hover{background-color:rgba(255,255,255,0.2);transform:translateY(-2px)}
```

---

## Badge Patterns

### Absolute Position Badge

```css
.gb-text-badge001{position:absolute;top:1rem;right:1rem;padding:0.25rem 0.625rem;font-size:0.75rem;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;background-color:#c0392b;color:white;border-radius:2rem}
```

### Inline Badge

```css
.gb-text-badge002{display:inline-flex;align-items:center;gap:0.375rem;padding:0.375rem 0.75rem;background:#16a34a;border-radius:2rem;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.03em;color:white}
```

### Status Indicator

```css
.gb-text-status001{display:inline-flex;align-items:center;gap:0.5rem;padding:0.5rem 1rem;background-color:#f5f5f3;border-radius:2rem;font-size:0.875rem;font-weight:600}.gb-text-status001::before{content:'';width:8px;height:8px;background-color:#22c55e;border-radius:50%}
```

---

## Animation Patterns

### Fade In

```css
.gb-element-anim001{animation:fadeIn 0.6s ease-out both}@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
```

### Staggered Fade In

```css
.gb-element-anim002{animation:fadeIn 0.6s ease-out 0.15s both}
.gb-element-anim003{animation:fadeIn 0.6s ease-out 0.3s both}
```

### Pulse

```css
.gb-shape-pulse001{animation:pulse 2s infinite}@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
```

---

## Focus States (Accessibility)

### Button Focus

```css
.gb-text-btn001:focus{outline:2px solid #c0392b;outline-offset:2px}
```

### Combined Hover/Focus

```css
.gb-text-btn001:is(:hover,:focus){background-color:#a33024;transform:translateY(-2px)}
```

### Focus Visible (Keyboard Only)

```css
.gb-text-link001:focus-visible{outline:2px solid #c0392b;outline-offset:2px}
```
