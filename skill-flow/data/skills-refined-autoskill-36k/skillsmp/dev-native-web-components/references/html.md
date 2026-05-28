# HTML Best Practices

## What is it?

A comprehensive guide to writing semantic, accessible, and performant HTML for modern web applications and native web components.

## Why follow these practices?

- **Accessibility**: Semantic HTML provides built-in accessibility
- **SEO**: Proper structure improves search engine understanding
- **Maintainability**: Semantic markup is self-documenting
- **Performance**: Native elements require no JavaScript
- **Browser Compatibility**: All features are Baseline-supported

---

## Document Structure

### Essential Document Template

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title - Site Name</title>
  <meta name="description" content="Page description for SEO">
  <link rel="canonical" href="https://example.com/page/">
  
  <!-- Preconnect to critical origins -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  
  <!-- Preload critical resources -->
  <link rel="preload" href="critical.css" as="style">
  
  <!-- Stylesheets -->
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <nav aria-label="Main navigation">...</nav>
  </header>
  
  <main>
    <article>
      <h1>Page Title</h1>
      <!-- Content -->
    </article>
  </main>
  
  <footer>...</footer>
  
  <!-- Scripts at end or with defer -->
  <script src="app.js" defer></script>
</body>
</html>
```

---

## Semantic Landmark Elements

Use semantic elements instead of generic `<div>` containers.

### Document Landmarks

| Element | Purpose | ARIA Role |
|---------|---------|-----------|
| `<header>` | Page or section header | `banner` (page-level) |
| `<nav>` | Navigation links | `navigation` |
| `<main>` | Primary content (one per page) | `main` |
| `<article>` | Self-contained content | `article` |
| `<section>` | Thematic grouping | `region` (with label) |
| `<aside>` | Tangentially related content | `complementary` |
| `<footer>` | Page or section footer | `contentinfo` (page-level) |

### Proper Structure

```html
<body>
  <header>
    <a href="/" aria-label="Home">Logo</a>
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/products">Products</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  </header>
  
  <main>
    <article>
      <h1>Article Title</h1>
      <p>Content...</p>
      
      <section aria-labelledby="features-heading">
        <h2 id="features-heading">Features</h2>
        <p>Section content...</p>
      </section>
    </article>
    
    <aside aria-label="Related articles">
      <h2>Related</h2>
      <nav aria-label="Related articles">
        <ul>...</ul>
      </nav>
    </aside>
  </main>
  
  <footer>
    <nav aria-label="Footer navigation">...</nav>
    <p>&copy; 2025 Company Name</p>
  </footer>
</body>
```

---

## Headings

### Heading Hierarchy Rules

- **One `<h1>` per page** (main page title)
- **Never skip levels** (h1 → h2 → h3, not h1 → h3)
- **Describe content** (not just "Introduction")

```html
<h1>Building Accessible Web Apps</h1>

<section>
  <h2>Why Accessibility Matters</h2>
  <p>Content...</p>
  
  <h3>Legal Requirements</h3>
  <p>Content...</p>
  
  <h3>Business Benefits</h3>
  <p>Content...</p>
</section>

<section>
  <h2>Implementation Guide</h2>
  <p>Content...</p>
</section>
```

---

## Interactive Elements

### Dialog (Modal)

Native modal with built-in focus trapping and backdrop.

```html
<button type="button" onclick="dialog.showModal()">Open Modal</button>

<dialog id="dialog">
  <form method="dialog">
    <h2>Confirm Action</h2>
    <p>Are you sure you want to proceed?</p>
    <button type="submit" value="cancel">Cancel</button>
    <button type="submit" value="confirm">Confirm</button>
  </form>
</dialog>
```

```javascript
const dialog = document.getElementById('dialog');

dialog.addEventListener('close', () => {
  console.log('Dialog closed with:', dialog.returnValue);
});
```

### Popover

Non-modal overlays without JavaScript.

```html
<!-- Manual popover (stays open until closed) -->
<button popovertarget="menu">Open Menu</button>
<div id="menu" popover>
  <nav>
    <a href="/profile">Profile</a>
    <a href="/settings">Settings</a>
    <a href="/logout">Logout</a>
  </nav>
</div>

<!-- Auto popover (closes on outside click, Escape, or another popover) -->
<button popovertarget="tooltip">Hover me</button>
<div id="tooltip" popover="auto">Tooltip content</div>
```

### Details/Summary (Disclosure)

Native accordion without JavaScript.

```html
<details>
  <summary>Click to expand</summary>
  <p>Hidden content that appears when expanded.</p>
</details>

<!-- Open by default -->
<details open>
  <summary>FAQ Question</summary>
  <p>Answer to the question.</p>
</details>
```

### Exclusive Accordion

```html
<!-- Only one open at a time (same name attribute) -->
<details name="faq">
  <summary>Question 1</summary>
  <p>Answer 1</p>
</details>

<details name="faq">
  <summary>Question 2</summary>
  <p>Answer 2</p>
</details>
```

---

## Forms

### Accessible Form Pattern

```html
<form action="/submit" method="POST">
  <div class="form-group">
    <label for="email">Email Address</label>
    <input 
      type="email" 
      id="email" 
      name="email" 
      required
      autocomplete="email"
      aria-describedby="email-hint"
    >
    <span id="email-hint" class="hint">We'll never share your email</span>
  </div>
  
  <div class="form-group">
    <label for="password">Password</label>
    <input 
      type="password" 
      id="password" 
      name="password" 
      required
      minlength="8"
      autocomplete="new-password"
      aria-describedby="password-requirements"
    >
    <span id="password-requirements" class="hint">
      Minimum 8 characters
    </span>
  </div>
  
  <fieldset>
    <legend>Notification Preferences</legend>
    
    <div>
      <input type="checkbox" id="notify-email" name="notify" value="email">
      <label for="notify-email">Email notifications</label>
    </div>
    
    <div>
      <input type="checkbox" id="notify-sms" name="notify" value="sms">
      <label for="notify-sms">SMS notifications</label>
    </div>
  </fieldset>
  
  <button type="submit">Create Account</button>
</form>
```

### Form Validation Error Pattern

```html
<div class="form-group">
  <label for="email">Email Address</label>
  <input 
    type="email" 
    id="email" 
    aria-invalid="true"
    aria-describedby="email-error"
  >
  <span id="email-error" class="error" role="alert">
    Please enter a valid email address
  </span>
</div>
```

### Autocomplete Attributes

| Attribute | Use For |
|-----------|---------|
| `autocomplete="name"` | Full name |
| `autocomplete="email"` | Email address |
| `autocomplete="tel"` | Phone number |
| `autocomplete="address-line1"` | Street address |
| `autocomplete="postal-code"` | ZIP/postal code |
| `autocomplete="country"` | Country |
| `autocomplete="cc-number"` | Credit card number |
| `autocomplete="new-password"` | New password (signup) |
| `autocomplete="current-password"` | Existing password (login) |
| `autocomplete="one-time-code"` | OTP/verification code |

---

## Images

### Responsive Images

```html
<picture>
  <!-- Modern format for supporting browsers -->
  <source 
    srcset="image-400.avif 400w, image-800.avif 800w, image-1200.avif 1200w"
    sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
    type="image/avif"
  >
  <source 
    srcset="image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w"
    sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
    type="image/webp"
  >
  <!-- Fallback -->
  <img 
    src="image-800.jpg" 
    alt="Descriptive alt text"
    width="800" 
    height="600"
    loading="lazy"
    decoding="async"
  >
</picture>
```

### Alt Text Guidelines

| Scenario | Alt Text |
|----------|----------|
| Informative image | Describe the content/information |
| Decorative image | `alt=""` (empty, not omitted) |
| Image of text | Include the text |
| Linked image | Describe the link destination |
| Complex image | Brief alt + link to long description |

```html
<!-- Informative -->
<img src="chart.png" alt="Sales increased 25% in Q4 2024">

<!-- Decorative -->
<img src="decorative-border.png" alt="">

<!-- Linked -->
<a href="/products">
  <img src="product.jpg" alt="View our products">
</a>
```

---

## Tables

### Accessible Table Pattern

```html
<table>
  <caption>Monthly Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th>
      <td>$10,000</td>
      <td>+5%</td>
    </tr>
    <tr>
      <th scope="row">February</th>
      <td>$12,000</td>
      <td>+20%</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$22,000</td>
      <td>+12.5%</td>
    </tr>
  </tfoot>
</table>
```

---

## Focus Management

### Inert Attribute

Disable entire regions without JavaScript focus management.

```html
<!-- Disable background when modal is open -->
<div inert>
  <!-- Background content cannot be focused -->
</div>

<dialog open>
  <!-- Modal content is focusable -->
</dialog>
```

### Tabindex

| Value | Behavior |
|-------|----------|
| `tabindex="0"` | Add to natural tab order |
| `tabindex="-1"` | Focusable via JS, not tab |
| `tabindex="1+"` | **Never use** (disrupts order) |

```html
<!-- Only use tabindex="0" when necessary -->
<div role="button" tabindex="0" onclick="handleClick()">
  Custom button (prefer <button>)
</div>

<!-- tabindex="-1" for programmatic focus -->
<div id="modal" tabindex="-1">
  <!-- Focus here via JS: modal.focus() -->
</div>
```

### Skip Links

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  
  <header>...</header>
  <nav>...</nav>
  
  <main id="main-content" tabindex="-1">
    <h1>Page Title</h1>
    <!-- Content -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
}

.skip-link:focus {
  left: 0;
  top: 0;
  z-index: 9999;
  padding: 1rem;
  background: #000;
  color: #fff;
}
```

---

## Web Components

### Declarative Shadow DOM

```html
<my-component>
  <template shadowrootmode="open">
    <style>
      :host {
        display: block;
        padding: var(--space-md);
      }
    </style>
    <slot></slot>
  </template>
  <p>Light DOM content goes here</p>
</my-component>
```

### Template and Slot

```html
<template id="card-template">
  <style>
    .card {
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      padding: var(--space-md);
    }
  </style>
  <div class="card">
    <h2><slot name="title">Default Title</slot></h2>
    <div class="content">
      <slot>Default content</slot>
    </div>
  </div>
</template>

<!-- Usage -->
<my-card>
  <span slot="title">Card Title</span>
  <p>Card content here</p>
</my-card>
```

---

## Performance Attributes

### Resource Hints

```html
<head>
  <!-- Preconnect: Establish connection early -->
  <link rel="preconnect" href="https://api.example.com">
  <link rel="dns-prefetch" href="https://analytics.example.com">
  
  <!-- Preload: Load critical resources early -->
  <link rel="preload" href="hero.jpg" as="image" fetchpriority="high">
  <link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
  
  <!-- Prefetch: Load resources for next page -->
  <link rel="prefetch" href="/next-page.html">
</head>
```

### Image Loading

```html
<!-- Above fold: Eager load, high priority -->
<img 
  src="hero.jpg" 
  alt="Hero image"
  width="1920" 
  height="1080"
  loading="eager"
  fetchpriority="high"
  decoding="async"
>

<!-- Below fold: Lazy load -->
<img 
  src="gallery.jpg" 
  alt="Gallery image"
  width="800" 
  height="600"
  loading="lazy"
  decoding="async"
>
```

### Script Loading

```html
<!-- Defer: Download parallel, execute after HTML parse -->
<script src="app.js" defer></script>

<!-- Async: Download parallel, execute immediately when ready -->
<script src="analytics.js" async></script>

<!-- Module: Automatically deferred -->
<script type="module" src="module.js"></script>
```

---

## Internationalization

### Language Attributes

```html
<!-- Document language -->
<html lang="en" dir="ltr">

<!-- Language change within content -->
<p>The French phrase <span lang="fr">c'est la vie</span> means "that's life."</p>

<!-- RTL language -->
<html lang="ar" dir="rtl">
```

### Translate Attribute

```html
<!-- Prevent translation -->
<code translate="no">npm install</code>
<span translate="no">iPhone</span>
```

---

## HTML Checklist

### Document Structure

- [ ] Valid `<!DOCTYPE html>` declaration
- [ ] `<html lang="xx">` attribute set
- [ ] `<meta charset="UTF-8">` first in head
- [ ] Viewport meta tag configured
- [ ] Unique `<title>` per page
- [ ] Single `<h1>` per page

### Semantics

- [ ] Landmark elements used (`<header>`, `<main>`, `<footer>`, `<nav>`)
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] Lists use `<ul>`, `<ol>`, `<dl>` appropriately
- [ ] Tables use `<thead>`, `<tbody>`, `scope` attributes

### Accessibility

- [ ] All images have appropriate `alt` text
- [ ] Form inputs have associated `<label>` elements
- [ ] Focus order is logical
- [ ] Skip link provided
- [ ] Color is not the only means of conveying information

### Performance

- [ ] Images have `width` and `height` to prevent CLS
- [ ] Below-fold images use `loading="lazy"`
- [ ] Critical resources use `rel="preload"`
- [ ] Scripts use `defer` or `async`
- [ ] LCP image uses `fetchpriority="high"`

### Native Elements Over JavaScript

- [ ] `<dialog>` instead of modal libraries
- [ ] `<details>` instead of accordion libraries
- [ ] `popover` instead of dropdown libraries
- [ ] `<datalist>` for autocomplete suggestions

---

## Baseline Status Reference

| Feature | Baseline Status |
|---------|-----------------|
| `<dialog>` element | Baseline 2022 |
| `<details>` element | Baseline 2020 |
| Popover API | Baseline 2024 |
| Declarative Shadow DOM | Baseline 2024 |
| `inert` attribute | Baseline 2023 |
| `loading="lazy"` | Baseline 2020 |
| `fetchpriority` | Baseline 2023 |
| `<search>` element | Baseline 2023 |
