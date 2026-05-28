---
name: Poker Table UI
description: Build pixel-perfect poker table interfaces following the Golden Template standard
---

# Poker Table UI Skill

## 🏆 GOLDEN STANDARD — MANDATORY FOR ALL POKER TABLES

**EVERY poker table in Smarter.Poker MUST look IDENTICAL to this reference. NO EXCEPTIONS.**

![Golden Table Reference](file:///Users/smarter.poker/Documents/hub-vanguard/.agent/skills/poker-table-ui/golden-table-reference.png)

---

## 🎯 Core Requirements

### 1. Table Shape: STADIUM/RACETRACK (NOT Ellipse)
```css
borderRadius: 9999  /* Creates pill/stadium shape with rounded ends and straight sides */
```

### 2. Layer Structure (Outside → Inside)
```
┌─ OUTER DARK FRAME (gradient: #1a1a1a → #0a0a0a)
│  └─ OUTER GOLD RAIL (gradient: #d4a000 → #8b6914)
│     └─ BLACK GAP (#0a0a0a)
│        └─ INNER GOLD RAIL (thinner, same gradient)
│           └─ DARK EDGE (#080808)
│              └─ THIN GOLD INNER LINE (subtle glow)
│                 └─ FELT with WHITE EDGE GLOW
```

### 3. Felt Surface — WHITE EDGE GLOW
**CRITICAL**: The felt has a distinctive WHITE/LIGHT GLOW around the inner edge that fades to dark center.
```css
background: `radial-gradient(
  ellipse at 50% 50%,
  #0a0a0a 0%,           /* Dark center */
  #0a0a0a 40%,          /* Dark mid */
  #2a2a2a 70%,          /* Lighter edge */
  #4a4a4a 85%,          /* Glow edge */
  #303030 100%          /* Outer edge */
)`,
boxShadow: 'inset 0 0 60px 20px rgba(255,255,255,0.08)'  /* White glow */
```

### 4. Background: SOLID BLACK
```css
background: '#080810'  /* Pure black, no gradients on page background */
```

### 5. Gold Rail Colors
- **Bright**: #d4a000, #f0c040
- **Dark**: #8b6914, #6b4f0a
- **Use gradients** for 3D depth effect

---

## 📐 CSS Implementation

### Stadium Shape
```jsx
borderRadius: 9999,  // NOT '50%' which creates ellipse
```

### Gold Rail Gradient
```jsx
background: 'linear-gradient(180deg, #d4a000 0%, #8b6914 50%, #6b4f0a 100%)',
boxShadow: 'inset 0 2px 3px rgba(255,220,100,0.4)',
```

### Felt with White Edge Glow
```jsx
background: `radial-gradient(
  ellipse at 50% 50%,
  #080808 0%,
  #0c0c0c 30%,
  #151515 60%,
  #252525 80%,
  #1a1a1a 100%
)`,
boxShadow: 'inset 0 0 80px 30px rgba(255,255,255,0.06)',
```

---

## 🎴 Card Standards

### Optimal Card Image Size
- **Dimensions**: 150 × 210 pixels (2x for retina)
- **Format**: WebP preferred, PNG acceptable
- **Aspect Ratio**: 5:7 (standard playing card)

### Display Size on Table
- **Hero cards**: 50-55px wide
- **Community cards**: 48-52px wide
- **Opponent cards (if shown)**: 40-45px wide

### Card Rendering
```jsx
objectFit: 'contain',  // NEVER 'cover' (causes cropping)
imageRendering: 'high-quality',
```

---

## 👤 Player Positions (9-max)

Avatars positioned OUTSIDE the table perimeter:
- **Hero**: Bottom center
- **Villain 1**: Bottom left
- **Villain 2**: Left lower
- **Villain 3**: Left upper  
- **Villain 4**: Top left
- **Villain 5**: Top right
- **Villain 6**: Right upper
- **Villain 7**: Right lower
- **Villain 8**: Bottom right

### Avatar Size
- **Hero**: 70-80px
- **Villains**: 55-65px

### Player Badge
Single gold box with:
- Name (9-10px, bold)
- BB count (11-12px, bold)
- Gradient background matching gold rails

---

## 🚫 DO NOT

- Use `borderRadius: '50%'` (creates ellipse, not stadium)
- Use `objectFit: 'cover'` on cards (crops image)
- Use colored backgrounds (must be solid black)
- Deviate from the gold rail colors
- Skip the white edge glow on felt
