# Theme Implementations (Layer 2)

**The Values**: Different VALUE assignments to the same token NAMES.

## Key Concept

Token NAMES stay constant. Token VALUES change. This allows switching visual fidelity by changing a single CSS import.

## Available Themes

### Polished Theme

**File**: `../assets/elementary/tokens/polished.css`

**Characteristics**:
- Semantic colors with light/dark mode support
- Uses `light-dark()` CSS function for automatic theming
- Professional typography (system font stack)
- Refined shadows and smooth transitions
- Production-ready polish

**Example Token Values**:
```css
:root {
  /* Colors adapt to light/dark mode */
  --c-primary: light-dark(#0066cc, #4d9fff);
  --c-secondary: light-dark(#64748b, #94a3b8);
  --bg-surface: light-dark(#ffffff, #1a1a1a);
  --bg-overlay: light-dark(#f8fafc, #0f172a);
  
  /* Structure (same across modes) */
  --s-4: 16px;
  --r-btn: 8px;
  --r-card: 12px;
  
  /* Effects (adapt to mode) */
  --x-card: light-dark(
    0 1px 3px rgba(0,0,0,0.1),
    0 1px 3px rgba(0,0,0,0.5)
  );
}
```

**Use When**:
- Feature specs showing "this is what we're building"
- Polished prototypes for stakeholder demos
- Design system documentation
- Light/dark mode support required
- Production-ready interfaces

**Light/Dark Mode**:
```javascript
// User control
document.documentElement.style.colorScheme = 'dark'; // or 'light'

// System preference (automatic)
// Already set in high-fidelity.css:
// :root { color-scheme: light dark; }
```

**Browser Support**:
- `light-dark()` function: Chrome 123+, Safari 17.5+, Firefox 120+
- Fallback: Use media queries for older browsers

---

### Sketch Theme (Low-Fidelity)

**File**: `../assets/elementary/tokens/sketch.css`

**Characteristics**:
- Monospace typography ("sketch aesthetic")
- Grayscale palette only
- Minimal shadows
- No light/dark mode (intentional)
- Focus on structure over aesthetics

**Example Token Values**:
```css
:root {
  /* Grayscale only */
  --c-primary: #000000;
  --c-secondary: #666666;
  --bg-surface: #ffffff;
  --bg-overlay: #f5f5f5;
  
  /* Structure (same as high-fidelity) */
  --s-4: 16px;
  --r-btn: 0px;  /* Square corners for wireframe feel */
  --r-card: 0px;
  
  /* Minimal effects */
  --x-card: none;
}
```

**Use When**:
- Exploring layout options without visual distraction
- Reviewing structure before committing to aesthetics
- User testing focused on functionality, not appearance
- Documenting "how it works" not "how it looks"
- Early-stage prototyping

---

## Import Patterns

**Path Convention**: The examples below use source-relative paths in relation to the source file that imports them. Adjust the path based on your file's location relative to the `assets/elementary/` directory.

### Basic Import (After Installation)
```css
/* High-fidelity */
@import './assets/elementary/tokens/polished.css';

/* OR Low-fidelity */
@import './assets/elementary/tokens/sketch.css';
```

Note: Install Elementary assets first using `elementary.mjs install .` from the skill directory.

### With Component Library
```css
/* Theme + optional component classes */
@import './assets/elementary/tokens/polished.css';
@import './assets/elementary/components.css';  /* optional */
```

## Theme Switching

**At Build Time** (change import):
```css
/* Before: High-fidelity */
@import './assets/elementary/tokens/polished.css';

/* After: Low-fidelity */
@import './assets/elementary/tokens/sketch.css';
```

**At Runtime** (light/dark mode only, polished theme):
```javascript
// Toggle between light and dark
const currentScheme = document.documentElement.style.colorScheme;
document.documentElement.style.colorScheme = 
  currentScheme === 'dark' ? 'light' : 'dark';
```

## Creating Custom Themes

To create a custom theme:

1. **Copy a base theme** (after installing Elementary):
   ```bash
   cp ./assets/elementary/tokens/polished.css ./assets/elementary/tokens/my-brand.css
   ```

2. **Modify semantic token values** (keep names the same):
   ```css
   :root {
     /* Your brand colors */
     --c-primary: #ff6b35;
     --c-secondary: #004e89;
     
     /* Keep structure tokens the same (or customize) */
     --s-4: 16px;
     --r-btn: 12px;
   }
   ```

3. **Import your theme**:
   ```css
   @import './assets/elementary/tokens/my-brand.css';
   @import './assets/elementary/components.css';
   ```

**Rule**: Never change token NAMES. Only change VALUES.

## Theme Comparison

| Aspect | High-Fidelity | Sketch |
|--------|---------------|-----------|
| **Colors** | Full palette + light/dark | Grayscale only |
| **Typography** | System font stack | Monospace |
| **Shadows** | Refined, mode-aware | None or minimal |
| **Corners** | Rounded (`8px-12px`) | Square (`0px`) |
| **Mode Support** | Light/dark automatic | No (single mode) |
| **Use Case** | Production prototypes | Structural mockups |

## Token Value Consistency

**What stays the same**:
- Space scale values (`--s-4: 16px`)
- Border widths (`--b-1: 1px`)
- Z-index layering (`--z-modal: 1000`)

**What changes**:
- Color values (semantic meanings stay, hex/rgb values change)
- Radius values (rounded vs square)
- Shadow values (refined vs minimal)
- Typography (system fonts vs monospace)

## See Also

- `token-system.md` - Complete token naming taxonomy
- `components.md` - How component classes work with themes
- `../assets/elementary/tokens/polished.css` - Source code for polished theme
- `../assets/elementary/tokens/sketch.css` - Source code for sketch theme
