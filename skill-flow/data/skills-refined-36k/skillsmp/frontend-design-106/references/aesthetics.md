# Aesthetics Reference

## Contents
- Color System
- Typography
- Visual Identity
- Gradients
- Anti-Patterns

## Color System

XOP.ai uses a dark-first palette with semantic accent colors:

| Token | Tailwind Class | Usage |
|-------|---------------|-------|
| Background | `bg-black` | Page base |
| Surface | `bg-gray-900` | Cards, panels |
| Surface elevated | `bg-gray-800` | Inputs, dropdowns |
| Border | `border-gray-800` | Card borders |
| Border subtle | `border-gray-700` | Input borders |
| Text primary | `text-white` | Headings |
| Text secondary | `text-gray-300` | Body text |
| Text muted | `text-gray-400` | Descriptions |
| Accent green | `text-green-400` | Solutions, success |
| Accent yellow | `text-yellow-400` | Apps, emphasis |
| Accent purple | `text-purple-400` | Resources |
| Accent blue | `text-blue-400` | About, links |

### Semantic Color Usage

```tsx
// Navigation sections - each has distinct color
<span className="text-yellow-400">Our Apps</span>
<span className="text-green-400">Solutions</span>
<span className="text-purple-400">Resources</span>
<span className="text-blue-400">About Us</span>
```

### WARNING: Inconsistent Accent Colors

**The Problem:**
```tsx
// BAD - Using random colors breaks visual hierarchy
<h3 className="text-blue-400">Engineer Efficiency</h3>  // Solutions should be green
```

**Why This Breaks:** Users learn the color → section mapping. Blue means "About/Contact" in this system.

**The Fix:**
```tsx
// GOOD - Consistent with navigation
<h3 className="text-green-400">Engineer Efficiency</h3>
```

## Typography

Font: Inter (loaded via `next/font/google` in `app/layout.tsx`)

| Element | Classes |
|---------|---------|
| Hero heading | `text-4xl md:text-6xl font-bold` |
| Section heading | `text-3xl md:text-4xl font-bold` |
| Card heading | `text-xl font-semibold` |
| Body large | `text-xl text-gray-300` |
| Body | `text-gray-300` or `text-gray-400` |
| Small | `text-sm text-gray-400` |

### WARNING: System Font Fallback

**The Problem:**
```tsx
// BAD - Overriding the Inter font
<div style={{ fontFamily: 'Arial, sans-serif' }}>
```

**Why This Breaks:** Inter is the brand font. Fallbacks create visual inconsistency.

**The Fix:** Never override. Inter is already configured in `layout.tsx`.

## Visual Identity

What makes XOP.ai distinctive:

1. **High contrast dark theme** - Black backgrounds, not dark gray
2. **Gradient accents on CTAs** - Purple-to-pink primary gradient
3. **Color-coded navigation** - Each section has a semantic color
4. **Emoji icons** - Used consistently in service cards and nav
5. **Animated gradient text** - Hero headlines use `text-gradient` class

### Signature Gradient Text

```tsx
// Defined in globals.css
.text-gradient {
  background: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #4facfe);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient 3s ease infinite;
}
```

## Gradients

| Purpose | Gradient |
|---------|----------|
| Primary CTA | `from-purple-600 to-pink-600` |
| Secondary CTA | `from-green-600 to-emerald-500` |
| Feature card | `from-blue-600 to-cyan-500` |
| Warning/Highlight | `from-yellow-600 to-orange-500` |
| Gradient border | `linear-gradient(135deg, #667eea, #764ba2)` |

### Gradient Shadow Pairing

Always pair gradient buttons with matching shadows:

```tsx
// Purple gradient → purple shadow
className="bg-gradient-to-r from-purple-600 to-pink-600 hover:shadow-purple-500/50"

// Green gradient → green shadow
className="bg-gradient-to-r from-green-600 to-emerald-500 hover:shadow-green-500/50"
```

## Anti-Patterns

### WARNING: Generic AI Aesthetics

**The Problem:** Default purple/blue gradients everywhere, Inter/Roboto, generic tech look.

**Why This Breaks:** XOP.ai has established its own visual language. Deviating looks like a different product.

**The Fix:** Reference existing pages. Use the color system. Match the established gradient pairings.