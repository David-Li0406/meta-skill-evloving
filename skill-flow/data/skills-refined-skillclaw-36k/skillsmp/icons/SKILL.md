---
name: icons
description: Use consistent Lucide icons with the <icon-wc> component. Use when adding icons to pages, buttons, or UI elements.
allowed-tools: Read, Write, Edit, Bash
---

# Icons Skill

Use the Lucide icon library with local SVG files and the `<icon-wc>` Web Component for consistent, accessible icons.

## CRITICAL: When to Use This Skill

**ALWAYS use the `<icon-wc>` component. NEVER use inline SVGs.**

| You Are Adding... | USE THIS SKILL |
|-------------------|----------------|
| Icon button (close, menu, etc.) | YES |
| Navigation icons | YES |
| Status indicators (success, error, warning) | YES |
| Toggle switches with icons (theme, settings) | YES |
| Action buttons (save, delete, edit) | YES |
| Social sharing icons | YES |
| ANY visual indicator or icon | YES |

### Bad (Do NOT do this):

```html
<!-- WRONG: Inline SVG -->
<button>
  <svg viewBox="0 0 24 24"><path d="M12 3v1m0 16v1..."/></svg>
</button>
```

### Good (Do this instead):

```html
<!-- CORRECT: icon-wc component -->
<button>
  <icon-wc name="sun" label="Light theme"></icon-wc>
</button>
```

**Why?** The `<icon-wc>` component:
- Ensures consistent sizing across the app
- Handles accessibility automatically
- Uses optimized, cached SVG loading
- Inherits color from CSS (no hardcoded colors)
- Works with any icon set (Lucide, custom, etc.)

---

## Quick Start

```html
<!-- Basic usage -->
<icon-wc name="menu"></icon-wc>
<icon-wc name="arrow-right"></icon-wc>
<icon-wc name="check"></icon-wc>

<!-- With size -->
<icon-wc name="home" size="lg"></icon-wc>

<!-- With accessible label (for functional icons) -->
<button>
  <icon-wc name="x" label="Close"></icon-wc>
</button>

<!-- Custom icon set -->
<icon-wc name="logo" set="custom"></icon-wc>
```

## Directory Structure

```
.assets/
├── js/
│   └── components/
│       └── x-icon/          # Icon Web Component
│           ├── icon-wc.js
│           └── x-icon-styles.js
└── icons/
    ├── lucide/              # Lucide icons (synced from npm)
    │   ├── index.json       # Icon manifest
    │   ├── menu.svg
    │   ├── x.svg
    │   └── ...              # ~1900 icons
    └── custom/              # Project-specific icons
        └── logo.svg
```

## Setup

Run `/scaffold-icons` to set up icons in a project, or manually:

```bash
# 1. Install lucide-static
npm install lucide-static --save-dev

# 2. Sync icons
npm run icons:sync

# 3. Copy icon-wc component
mkdir -p .assets/js/components/icon-wc
cp .claude/skills/icons/templates/icon-wc/*.js .assets/js/components/icon-wc/

# 4. Include in HTML
<script type="module" src="/.assets/js/components/icon-wc/icon-wc.js"></script>
```

## The `<icon-wc>` Component

### Attributes

| Attribute | Description | Default |
|-----------|-------------|---------|
| `name` | Icon name (filename without .svg) | Required |
| `set` | Icon set directory | `"lucide"` |
| `size` | Size preset: xs, sm, md, lg, xl, 2xl | `"md"` |
| `label` | Accessible label for functional icons | None |
| `base-path` | Override default icon path | `/.assets/icons` |

### Size Reference

| Size | Dimensions |
|------|------------|
| xs | 1em (16px at base) |
| sm | 1.25em (20px) |
| md | 1.5em (24px) |
| lg | 2em (32px) |
| xl | 2.5em (40px) |
| 2xl | 3em (48px) |

### Styling

Icons inherit `currentColor` for stroke color:

```css
/* Change icon color */
.danger icon-wc {
  color: var(--color-error);
}

/* Custom sizing */
icon-wc.hero-icon {
  width: 4rem;
  height: 4rem;
}
```

## Syncing Icons

Icons are sourced from the `lucide-static` npm package:

```bash
# Install package (one-time)
npm install lucide-static --save-dev

# Sync icons to .assets/icons/lucide/
npm run icons:sync
```

Run `icons:sync` after:
- Initial project setup
- Updating lucide-static version
- Fresh npm install

## Accessibility

### Decorative Icons (default)

Icons without a `label` are hidden from screen readers:

```html
<!-- Decorative - hidden from screen readers -->
<button>
  <icon-wc name="save"></icon-wc>
  Save Document
</button>
```

### Functional Icons

Add `label` for icon-only buttons or links:

```html
<!-- Functional - announced to screen readers -->
<button aria-label="Close dialog">
  <icon-wc name="x" label="Close"></icon-wc>
</button>
```

### Guidelines

| Context | Pattern |
|---------|---------|
| Icon + visible text | No label needed (decorative) |
| Icon-only button | Add `label` attribute |
| Status indicator | Add `label` describing status |
| Purely decorative | No label needed |

## Adding Custom Icons

1. Create SVG file in `.assets/icons/custom/`:

```xml
<!-- .assets/icons/custom/logo.svg -->
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2L2 7l10 5 10-5-10-5z"/>
</svg>
```

2. Use with `set="custom"`:

```html
<icon-wc name="logo" set="custom"></icon-wc>
```

### Custom Icon Requirements

- SVG format with `viewBox` attribute
- No fixed `width`/`height` (component handles sizing)
- Use `currentColor` for strokes/fills to inherit color
- Keep file size small (optimize with SVGO)

## Replacing the Icon Set

To use a different icon library:

1. Remove lucide-static: `npm uninstall lucide-static`
2. Install alternative: `npm install [other-library]`
3. Update `.claude/scripts/sync-icons.js` source path
4. Run `npm run icons:sync`
5. Or manually copy SVGs to `.assets/icons/[set-name]/`

The `<icon-wc>` component works with any SVG icon library.

## Finding Icons

Browse available icons:
- **Lucide**: https://lucide.dev/icons
- **Local manifest**: `.assets/icons/lucide/index.json`

```bash
# Search for icons locally
grep -l "arrow" .assets/icons/lucide/*.svg | head -10
```

## Common Icons

| Purpose | Icon Name |
|---------|-----------|
| Navigation | `menu`, `x`, `arrow-left`, `arrow-right` |
| Actions | `plus`, `minus`, `edit`, `trash`, `save` |
| Status | `check`, `x`, `alert-circle`, `info` |
| Media | `play`, `pause`, `volume-2`, `image` |
| User | `user`, `users`, `settings`, `log-out` |
| Files | `file`, `folder`, `download`, `upload` |
| Social | `share`, `heart`, `star`, `message-circle` |

## Checklist

When using icons:

- [ ] Icon name matches file in `.assets/icons/[set]/`
- [ ] Functional icons have `label` attribute
- [ ] Icon size appropriate for context
- [ ] Color inherits from parent (uses `currentColor`)
- [ ] Custom icons saved to `.assets/icons/custom/`

## Related Skills

- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **accessibility-checker** - Ensure WCAG2AA accessibility compliance
- **css-author** - Modern CSS organization with native @import, @layer casca...
- **performance** - Write performance-friendly HTML pages
