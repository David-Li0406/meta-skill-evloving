# Accessible Navigation Reference

## Skip Links

Allow keyboard users to skip repetitive content:

```html
<body>
  <!-- First focusable element -->
  <a href="#main" class="skip-link">Skip to main content</a>
  <a href="#nav" class="skip-link">Skip to navigation</a>

  <header>
    <nav id="nav" aria-label="Main navigation">
      <!-- Navigation links -->
    </nav>
  </header>

  <main id="main">
    <!-- Main content -->
  </main>
</body>
```

CSS for skip links:

```css
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  position: static;
  left: auto;
}
```

## Navigation Landmarks

Use `<nav>` with aria-label when multiple navs exist:

```html
<!-- Main navigation -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Secondary navigation -->
<nav aria-label="Account navigation">
  <ul>
    <li><a href="/profile">Profile</a></li>
    <li><a href="/settings">Settings</a></li>
    <li><a href="/logout">Log out</a></li>
  </ul>
</nav>

<!-- Footer navigation -->
<nav aria-label="Footer navigation">
  <ul>
    <li><a href="/privacy">Privacy Policy</a></li>
    <li><a href="/terms">Terms of Service</a></li>
  </ul>
</nav>
```

## Current Page Indicator

```html
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/products" aria-current="page">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

## Breadcrumbs

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/electronics">Electronics</a></li>
    <li><span aria-current="page">Laptops</span></li>
  </ol>
</nav>
```

## Pagination

```html
<nav aria-label="Pagination">
  <ul>
    <li><a href="/page/1" aria-label="Go to page 1">1</a></li>
    <li><a href="/page/2" aria-label="Go to page 2" aria-current="page">2</a></li>
    <li><a href="/page/3" aria-label="Go to page 3">3</a></li>
    <li><a href="/page/3" aria-label="Go to next page">Next</a></li>
  </ul>
</nav>
```

## Table of Contents

```html
<nav aria-label="Table of contents">
  <h2>On this page</h2>
  <ul>
    <li><a href="#introduction">Introduction</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li>
      <a href="#features">Features</a>
      <ul>
        <li><a href="#feature-1">Feature 1</a></li>
        <li><a href="#feature-2">Feature 2</a></li>
      </ul>
    </li>
    <li><a href="#conclusion">Conclusion</a></li>
  </ul>
</nav>
```

## Menu Disclosure

**Modern approach: Use `popover` with `command`/`commandfor`** for automatic accessibility:

```html
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li>
      <button commandfor="products-menu" command="toggle-popover">
        Products
      </button>
      <ul popover id="products-menu">
        <li><a href="/products/software">Software</a></li>
        <li><a href="/products/hardware">Hardware</a></li>
      </ul>
    </li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

The browser automatically handles:
- `aria-expanded` state on the button
- `aria-details` relationship
- Focus management
- Escape key dismissal
- Click-outside dismissal

**Legacy pattern** (requires JavaScript for state management):

```html
<button aria-expanded="false" aria-controls="products-menu">
  Products
</button>
<ul id="products-menu" hidden="">
  <!-- Menu items -->
</ul>
```

## Link Accessibility

### Descriptive Link Text

```html
<!-- Bad -->
<a href="/report.pdf">Click here</a>
<a href="/docs">Read more</a>
<a href="/pricing">Learn more</a>

<!-- Good -->
<a href="/report.pdf">Download the 2024 annual report (PDF)</a>
<a href="/docs">Read the complete documentation</a>
<a href="/pricing">View pricing plans</a>
```

### Links That Open New Windows

```html
<a href="https://external.com" target="_blank" rel="noopener">
  External Site (opens in new tab)
</a>
```

### Links to Non-HTML Resources

```html
<a href="/report.pdf">Annual Report (PDF, 2.5 MB)</a>
<a href="/data.xlsx">Download Spreadsheet (Excel)</a>
<a href="/video.mp4">Watch Video (MP4, 15 min)</a>
```

## Keyboard Navigation

Ensure all interactive elements are:
- Focusable (in tab order)
- Have visible focus indicator
- Activated with Enter or Space
- Can be dismissed with Escape (for menus/dialogs)
