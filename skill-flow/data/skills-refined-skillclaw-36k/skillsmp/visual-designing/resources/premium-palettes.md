# Premium Color Palettes & Gradients

Stop using default Tailwind colors. Use these curated tokens for a "Production-Ready" look.

## 1. The "Cosmic" Dark Mode (Deep & Vibrant)
Best for: SaaS Dashboards, Developer Tools, AI Interfaces.

```css
:root {
  --bg-deep: #030014;
  --bg-card: #0F0E24;
  --accent-primary: #7C3AED; /* Violet */
  --accent-secondary: #EC4899; /* Pink */
  --text-primary: #F8FAFC;
  --text-secondary: #94A3B8;
}
```

**Tailwind Config Extension:**
```javascript
colors: {
  cosmic: {
    900: '#030014', // Main Background
    800: '#0F0E24', // Card Background
    700: '#1E1B4B', // Hover State
  }
}
```

## 2. The "Neo-Natural" Light Mode (Clean & Soft)
Best for: Consumer Apps, Blogs, Landing Pages.

Colors are derived from nature but boosted for screens.
- **Organic Green**: `#10B981` (Emerald) -> tweaked to `#059669`
- **Soft Clay**: `#F5F5F4` (Stone-100) background
- **Text**: Never use `#000000`. Use `#1C1917` (Stone-900).

## 3. High-Impact Gradients

### "Northern Lights"
`bg-gradient-to-r from-teal-400 via-blue-500 to-purple-600`

### "Sunset Vibes"
`bg-gradient-to-br from-orange-400 via-pink-500 to-rose-600`

### "Cyberpunk Glass"
Background: `#000`
Overlay: `bg-white/5` + `backdrop-blur-xl` + Border `border-white/10`
Text: `bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400`
