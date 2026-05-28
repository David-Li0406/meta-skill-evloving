# Component Classes (Layer 3)

**The Patterns**: Pre-built styling patterns using Layer 1 token names.

## Overview

Component classes are **optional** pre-built patterns in `assets/elementary/components.css`. They work with ANY Layer 2 theme.

**Key Insight**: Component classes use token NAMES, not VALUES. This means they automatically adapt when you switch themes.

## When to Use Component Classes

**Use component classes when**:
- Rapid prototyping with consistent patterns
- Building common UI elements (buttons, cards, heroes)
- Want pre-built responsive layouts
- Design system compliance required

**Use tokens directly when**:
- Custom designs not covered by component library
- Full control over styling
- Creating new patterns not in the library

## Available Components

### Buttons & CTAs

**`.wf-btn`** - Button component
```jsx
<button className="wf-btn primary">Primary Button</button>
<button className="wf-btn secondary">Secondary Button</button>
<button className="wf-btn action">Call to Action</button>
```

**Modifiers**:
- `.primary` - Surface background, text color
- `.secondary` - App background, text color
- `.action` - Primary color background, white text
- `.full` - Full width button

**Token Customization**:
```css
.wf-btn {
  padding: var(--p-btn);           /* Default padding */
  border-radius: var(--r-btn);     /* Button radius */
  font: var(--t-body);             /* Typography */
}
```

**`.wf-cta`** - Call-to-action section
```jsx
<div className="wf-cta">
  <h2 className="title">Ready to get started?</h2>
  <p className="description">Join thousands of users</p>
  <div className="actions">
    <button className="wf-btn action">Get Started</button>
  </div>
</div>
```

---

### Layout Components

**`.wf-hero`** - Hero section
```jsx
<div className="wf-hero">
  <div className="content">
    <span className="badge">New</span>
    <h1 className="title">Hero Title</h1>
    <p className="description">Hero description text</p>
    <div className="actions">
      <button className="wf-btn action">Primary CTA</button>
      <button className="wf-btn secondary">Learn More</button>
    </div>
  </div>
</div>
```

**Token Customization**:
```css
.wf-hero {
  background-color: var(--c-text);  /* Dark background */
  color: var(--c-white);
  padding: var(--p-card);
  border-radius: var(--r-card);
}
```

**`.wf-grid`** - Grid layout
```jsx
<div className="wf-grid">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

**`.wf-features`** - Feature grid section
```jsx
<div className="wf-features">
  <div className="header">
    <h2 className="title">Features</h2>
    <p className="description">Everything you need</p>
  </div>
  <div className="wf-grid">
    <div className="wf-card">
      <div className="icon">🚀</div>
      <h3 className="title">Fast</h3>
      <p className="description">Lightning quick performance</p>
    </div>
    <!-- More cards -->
  </div>
</div>
```

**`.wf-footer`** - Footer layout
```jsx
<footer className="wf-footer">
  <div className="content">
    <div className="brand">© 2026 Company</div>
    <nav className="links">
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
    </nav>
  </div>
</footer>
```

---

### Content Components

**`.wf-card`** - Card container
```jsx
<div className="wf-card">
  <h3 className="title">Card Title</h3>
  <p className="description">Card description text</p>
  <div className="actions">
    <button className="wf-btn primary">Action</button>
  </div>
</div>
```

**Token Customization**:
```css
.wf-card {
  padding: var(--p-card);          /* Card padding */
  border-radius: var(--r-card);    /* Card radius */
  background-color: var(--bg-surface);
  border: var(--b-standard);
}
```

**`.wf-list`** - List layouts
```jsx
<div className="wf-list">
  <div className="wf-list-item">
    <div className="label">Name</div>
    <div className="value">John Doe</div>
  </div>
  <div className="wf-list-item">
    <div className="label">Email</div>
    <div className="value">john@example.com</div>
  </div>
</div>
```

**`.wf-pricing`** - Pricing tables
```jsx
<div className="wf-pricing">
  <div className="wf-pricing-tier">
    <h3 className="title">Starter</h3>
    <div className="price">$9/mo</div>
    <ul className="features">
      <li>Feature 1</li>
      <li>Feature 2</li>
    </ul>
    <button className="wf-btn primary">Select Plan</button>
  </div>
</div>
```

**`.wf-dashboard`** - Dashboard layouts
```jsx
<div className="wf-dashboard">
  <aside className="sidebar">
    <!-- Navigation -->
  </aside>
  <main className="content">
    <!-- Dashboard content -->
  </main>
</div>
```

---

### UI Patterns

**`.wf-empty-state`** - Empty states
```jsx
<div className="wf-empty-state">
  <div className="icon">📭</div>
  <h3 className="title">No items yet</h3>
  <p className="description">Get started by creating your first item</p>
  <button className="wf-btn action">Create Item</button>
</div>
```

**`.wf-skeleton`** - Loading skeletons
```jsx
<div className="wf-skeleton">
  <div className="wf-skeleton-line"></div>
  <div className="wf-skeleton-line short"></div>
</div>
```

**`.wf-wizard`** - Step wizards
```jsx
<div className="wf-wizard">
  <div className="steps">
    <div className="step active">Step 1</div>
    <div className="step">Step 2</div>
    <div className="step">Step 3</div>
  </div>
  <div className="content">
    <!-- Current step content -->
  </div>
</div>
```

**`.wf-settings`** - Settings panels
```jsx
<div className="wf-settings">
  <div className="wf-settings-section">
    <h3 className="title">Account</h3>
    <div className="wf-settings-item">
      <div className="label">Email</div>
      <input type="email" />
    </div>
  </div>
</div>
```

---

## Semantic Child Elements

Component classes use semantic child elements styled via custom properties:

**`.title`** - Heading/title text
```css
.title {
  font: var(--t-title, var(--t-body));
  margin-block-end: var(--m-title, var(--s-4));
  color: var(--c-title, inherit);
}
```

**`.description`** - Descriptive text
```css
.description {
  font: var(--t-desc, var(--t-body));
  color: var(--c-desc, var(--c-text-secondary));
  opacity: var(--o-desc, 1);
}
```

**`.label`** - Label text
```css
.label {
  font: var(--t-label, var(--t-body));
  color: var(--c-label, var(--c-text-secondary));
}
```

**`.icon`** - Icon/emoji
```css
.icon {
  font: var(--t-icon, var(--t-body));
  margin-block-end: var(--m-icon, var(--s-4));
}
```

**`.badge`** - Small badge/tag
```css
.badge {
  padding: var(--p-badge, var(--s-1) var(--s-3));
  background-color: var(--bg-badge, var(--c-primary));
  color: var(--c-badge, var(--c-white));
  border-radius: var(--r-badge, var(--r-6));
}
```

**`.actions`** - Action button container
```css
.actions {
  display: flex;
  gap: var(--g-actions, var(--s-3));
  justify-content: var(--actions-justify, flex-start);
  margin-block: var(--m-actions, var(--s-5));
}
```

---

## Component-Level Token Patterns

Components use `--<property>-of-<element>` naming:

**Common patterns**:
```css
--t-title: var(--t-heading);     /* Typography for .title */
--c-title: var(--c-text);        /* Color for .title */
--m-title: var(--s-4);           /* Margin for .title */
--p-card: var(--s-6);            /* Padding for .wf-card */
--r-badge: var(--r-6);           /* Radius for .badge */
--g-actions: var(--s-4);         /* Gap for .actions */
```

---

## Three Styling Approaches

### Approach 1: Component Classes Only (Fastest)
```jsx
<div className="wf-card">
  <h3 className="title">Title</h3>
  <p className="description">Description</p>
</div>
```

### Approach 2: Tokens Only (Full Control)
```jsx
<div style={{
  padding: 'var(--s-6)',
  borderRadius: 'var(--r-card)',
  backgroundColor: 'var(--bg-surface)',
  border: 'var(--b-standard)'
}}>
  <h3 style={{ color: 'var(--c-text)' }}>Title</h3>
  <p style={{ color: 'var(--c-text-secondary)' }}>Description</p>
</div>
```

### Approach 3: Hybrid (Component + Token Overrides)
```jsx
<div className="wf-card" style={{
  backgroundColor: 'var(--bg-accent)'  /* Override */
}}>
  <h3 className="title">Title</h3>
  <p className="description">Description</p>
</div>
```

**Rule**: Pick ONE approach per component. Don't mix within a single element.

---

## Discovering Available Classes

**Read the source**:
```bash
# View all component classes
cat assets/elementary/components.css
```

**Use discover tool** (if available):
```javascript
// In agent context
list_design_classes({
  css_file: "assets/elementary/components.css",
  include_tokens: false
})
```

---

## Anti-Patterns

### ❌ Don't Invent Classes
```jsx
{/* WRONG - .wf-dashboard-card doesn't exist */}
<div className="wf-dashboard-card">
```

**Fix**: Use existing `.wf-card` inside `.wf-dashboard`:
```jsx
<div className="wf-dashboard">
  <div className="wf-card">
```

### ❌ Don't Mix Tailwind with Component Classes
```jsx
{/* WRONG - Mixing utility classes with Elementary */}
<div className="wf-card p-4 flex gap-2">
```

**Fix**: Choose ONE approach:
```jsx
{/* RIGHT - Component classes only */}
<div className="wf-card">
```

### ❌ Don't Mix className and style on Same Element
```jsx
{/* WRONG */}
<div className="wf-btn primary" style={{ padding: '16px' }}>
```

**Fix**: Use component-level tokens:
```jsx
{/* RIGHT */}
<div className="wf-btn primary" style={{ 
  '--p-btn': 'var(--s-4)' 
}}>
```

---

## Working with Themes

Component classes automatically adapt to themes:

```css
/* High-fidelity theme */
@import './assets/elementary/tokens/polished.css';
@import './assets/elementary/components.css';

/* Switch to wireframe - components adapt automatically */
@import './assets/elementary/tokens/sketch.css';
@import './assets/elementary/components.css';
```

**Why this works**: Component classes use token NAMES (`var(--c-primary)`), which have different VALUES in each theme.

---

## See Also

- `token-system.md` - Complete token naming taxonomy
- `themes.md` - How themes assign values to tokens
- `recipes/` - Complete usage examples for common patterns
- `assets/elementary/components.css` - Source code for all component classes
