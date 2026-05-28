# DuskMoonUI Development Guide

> Material Design 3-inspired CSS-only component library for Tailwind CSS v4

## Related Projects

This package (`@duskmoon-dev/core`) provides the CSS foundation for [duskmoon-elements](https://github.com/duskmoon-dev/duskmoon-elements), a Web Components library.

Each component in this package exports its CSS styles which are consumed by the custom elements in duskmoon-elements:

```
@duskmoon-dev/core (CSS styles)
        ↓
duskmoon-elements (Web Components)
```

### Component CSS Exports

Individual component styles can be imported for use in custom elements:

```javascript
// Import specific component CSS
import '@duskmoon-dev/core/components/button';
import '@duskmoon-dev/core/components/card';
import '@duskmoon-dev/core/components/input';
```

This modular approach allows duskmoon-elements to bundle only the CSS needed for each web component.

---

## Component Overview

DuskMoonUI includes **47 components** and **layout utilities** organized by category.

### Included Components

| Category | Components |
|----------|------------|
| **Actions** | Button, File Upload |
| **Data Display** | Avatar, Badge, Card, Chip, Collapse, List, Table, Timeline, Skeleton |
| **Data Entry** | Autocomplete, Cascader, Checkbox, Datepicker, Form Group, Input, Multi-Select, OTP Input, PIN Input, Radio, Rating, Segment Control, Select, Slider, Switch, Textarea, Time Input, Tree Select |
| **Feedback** | Alert, Dialog, Modal, Progress, Snackbar, Toast, Tooltip |
| **Layout** | App Bar, Divider, Form, Grid Utilities, Markdown Body |
| **Navigation** | Bottom Navigation, Drawer, Navigation (Navbar/Tabs/Menu), Pagination, Stepper |
| **Surfaces** | Accordion, Bottom Sheet, Popover |

### Layout Utilities

Grid utilities for responsive layouts:

```html
<!-- Auto-fill: Creates as many columns as fit, empty space remains -->
<div class="grid grid-cols-auto-fill-48 gap-4">...</div>

<!-- Auto-fit: Creates columns that stretch to fill space -->
<div class="grid grid-cols-auto-fit-64 gap-4">...</div>
```

Available sizes: `48` (12rem), `64` (16rem), `80` (20rem), `96` (24rem)

### Accessibility Utilities

```html
<!-- Screen reader only (visually hidden) -->
<span class="sr-only">Hidden label</span>

<!-- Undo sr-only for focus states -->
<a class="sr-only focus:not-sr-only">Skip to content</a>
```

### Component Files

```
packages/core/src/components/
├── accordion.css       # Expandable content panels
├── alert.css           # Important messages (success, error, warning, info)
├── appbar.css          # Top/bottom action bars
├── autocomplete.css    # Search with suggestions
├── avatar.css          # User profile pictures with status
├── badge.css           # Small status indicators
├── bottom-navigation.css # Mobile bottom nav bar
├── bottomsheet.css     # Mobile bottom panels
├── button.css          # Clickable buttons (filled, outlined, text, tonal)
├── card.css            # Content container with elevation
├── cascader.css        # Hierarchical cascading selection
├── checkbox.css        # Multi-selection checkboxes
├── chip.css            # Compact elements for tags/filters
├── collapse.css        # Expandable/collapsible content
├── datepicker.css      # Calendar date selection
├── dialog.css          # Modal dialogs
├── divider.css         # Visual separators
├── drawer.css          # Side navigation panel
├── file-upload.css     # Drag-and-drop file uploader
├── form.css            # Form layout utilities
├── form-group.css      # Form field grouping with labels
├── input.css           # Text input fields
├── list.css            # Vertical list of items
├── markdown-body.css   # Markdown content styling
├── modal.css           # Full-featured modal overlays
├── multi-select.css    # Multiple selection dropdown
├── navigation.css      # Navbar, tabs, menu components
├── otp-input.css       # One-time password input fields
├── pin-input.css       # PIN entry input fields
├── popover.css         # Contextual overlays
├── progress.css        # Linear and circular indicators
├── radio.css           # Single selection radio buttons
├── rating.css          # Star/heart rating input
├── segment-control.css # Segmented button group
├── select.css          # Dropdown selection menus
├── skeleton.css        # Loading placeholders
├── slider.css          # Range value selector
├── snackbar.css        # Toast notifications
├── stepper.css         # Multi-step process guide
├── switch.css          # Toggle on/off control
├── table.css           # Data tables
├── textarea.css        # Multi-line text input
├── time-input.css      # Time selection input
├── timeline.css        # Chronological event display
├── toast.css           # Toast notification system
├── tooltip.css         # Contextual information on hover
└── tree-select.css     # Hierarchical tree selection
```

---

## Potential Future Components

The following Material Design 3 components could be added:

| Component | Description | Priority |
|-----------|-------------|----------|
| **FAB** | Floating Action Button | Medium |
| **Search Bar** | Dedicated search input | Low |
| **Navigation Rail** | Compact side navigation | Low |
| **Speed Dial** | Expandable FAB with actions | Low |

---

## Installation

### Package Manager

```bash
# Bun (recommended)
bun add @duskmoon-dev/core tailwindcss@^4.0.0

# npm
npm install @duskmoon-dev/core tailwindcss@^4.0.0

# pnpm
pnpm add @duskmoon-dev/core tailwindcss@^4.0.0
```

### CSS Import

```css
/* Import Tailwind and DuskMoonUI */
@import "tailwindcss";
@import "@duskmoon-dev/core";
```

### Theme Setup

```html
<!-- Apply theme via data attribute -->
<html data-theme="sunshine">
  <!-- Light theme -->
</html>

<html data-theme="moonlight">
  <!-- Dark theme -->
</html>
```

---

## Usage

### Basic Components

```html
<!-- Buttons -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary btn-outline">Outlined</button>
<button class="btn btn-tertiary btn-ghost">Ghost</button>
<button class="btn btn-primary btn-loading">Loading...</button>

<!-- Cards -->
<div class="card">
  <div class="card-body">
    <h2 class="card-title">Card Title</h2>
    <p>Card content</p>
  </div>
</div>

<!-- Inputs -->
<input type="text" class="input" placeholder="Default input" />
<input type="text" class="input input-primary" placeholder="Primary" />
<input type="text" class="input input-error" placeholder="Error state" />

<!-- Badges -->
<span class="badge badge-primary">New</span>
<span class="badge badge-error badge-dot"></span>

<!-- Alerts -->
<div class="alert alert-success">Success message</div>
<div class="alert alert-error">Error message</div>
```

### Navigation

```html
<!-- Navbar -->
<nav class="navbar navbar-surface-container-high">
  <div class="navbar-start">
    <a class="navbar-brand">Logo</a>
  </div>
  <div class="navbar-center">
    <a class="navbar-item navbar-item-active">Home</a>
    <a class="navbar-item">About</a>
  </div>
</nav>

<!-- Tabs -->
<div class="tabs">
  <button class="tab tab-active">Tab 1</button>
  <button class="tab">Tab 2</button>
  <button class="tab">Tab 3</button>
</div>

<!-- Bottom Navigation (mobile) -->
<nav class="bottom-nav">
  <button class="bottom-nav-item bottom-nav-item-active">
    <span class="bottom-nav-icon">🏠</span>
    <span class="bottom-nav-label">Home</span>
  </button>
</nav>
```

### Feedback Components

```html
<!-- Dialog -->
<div class="dialog-backdrop dialog-backdrop-show">
  <div class="dialog dialog-md">
    <div class="dialog-header">
      <h2 class="dialog-title">Confirm</h2>
    </div>
    <div class="dialog-body">Are you sure?</div>
    <div class="dialog-actions">
      <button class="btn btn-text">Cancel</button>
      <button class="btn btn-filled">Confirm</button>
    </div>
  </div>
</div>

<!-- Toast -->
<div class="toast toast-success toast-show">
  <span class="toast-message">Saved successfully</span>
</div>

<!-- Progress -->
<div class="progress progress-primary">
  <div class="progress-bar" style="width: 60%"></div>
</div>

<!-- Skeleton -->
<div class="skeleton skeleton-text"></div>
<div class="skeleton skeleton-circle"></div>
```

### Data Display

```html
<!-- Table -->
<table class="table table-hover table-striped">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John Doe</td>
      <td>john@example.com</td>
    </tr>
  </tbody>
</table>

<!-- List -->
<ul class="list">
  <li class="list-item list-item-interactive">
    <div class="list-item-leading">📄</div>
    <div class="list-item-content">
      <span class="list-item-text">Item Title</span>
      <span class="list-item-secondary">Description</span>
    </div>
  </li>
</ul>

<!-- Avatar -->
<div class="avatar avatar-lg avatar-status avatar-status-online">
  <img src="user.jpg" class="avatar-image" />
</div>

<!-- Chip -->
<div class="chip chip-primary">Tag</div>
<div class="chip chip-removable">
  Remove
  <button class="chip-remove">×</button>
</div>
```

---

## Color System

### Using Color Utilities

```html
<!-- Background colors -->
<div class="bg-primary">Primary</div>
<div class="bg-secondary">Secondary</div>
<div class="bg-tertiary">Tertiary</div>
<div class="bg-surface-container">Surface</div>

<!-- Text colors -->
<p class="text-primary">Primary text</p>
<p class="text-on-surface">On surface text</p>
<p class="text-on-surface-variant">Muted text</p>

<!-- Semantic colors -->
<div class="bg-success text-success-content">Success</div>
<div class="bg-error text-error-content">Error</div>
<div class="bg-warning text-warning-content">Warning</div>
<div class="bg-info text-info-content">Info</div>
```

### CSS Variables

```css
/* Access color tokens directly */
.custom-element {
  background-color: var(--color-primary);
  color: var(--color-primary-content);
  border-color: var(--color-outline);
}

/* Dynamic states with color-mix */
.custom-element:hover {
  background-color: color-mix(in oklch, var(--color-primary), black 10%);
}
```

---

## Development Commands

```bash
# Build core package
bun run build:core

# Watch mode
bun run dev:core

# Type checking
bun run typecheck

# Unit tests
cd packages/core && bun test tests/unit

# Visual regression tests
cd packages/core && bun run test:visual

# Integration tests
cd packages/core && bun run test:integration

# Accessibility tests
cd packages/core && bun run test:a11y

# All tests
cd packages/core && bun run test:all
```

---

## Project Structure

```
duskmoonui/
├── packages/
│   └── core/                   # @duskmoon-dev/core
│       ├── src/
│       │   ├── base/           # Root styles, color tokens
│       │   │   ├── colors.css  # 65+ color token definitions
│       │   │   └── utilities.css # Grid and accessibility utilities
│       │   ├── themes/         # Theme definitions
│       │   │   ├── sunshine.css # Light theme
│       │   │   └── moonlight.css# Dark theme
│       │   ├── components/     # 47 component CSS files
│       │   ├── generators/     # CSS variable generation
│       │   └── types/          # TypeScript definitions
│       ├── scripts/
│       │   └── build-css.ts    # CSS build script
│       ├── tests/
│       │   ├── unit/           # Bun unit tests
│       │   ├── visual/         # Playwright visual tests
│       │   ├── integration/    # Integration tests
│       │   └── accessibility/  # axe-core a11y tests
│       └── dist/               # Built output
├── examples/
│   ├── demo/                   # Interactive demo app
│   ├── astro-starter/          # Astro example
│   └── nextjs-starter/         # Next.js example
└── docs/                       # Documentation
```

---

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- iOS Safari 14+
- Android Chrome 90+

---

## License

MIT License - see LICENSE file for details
