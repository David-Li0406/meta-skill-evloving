# Web Components

Tailwind CSS-based components for web pages. All components are WCAG AA compliant.

---

## Buttons

### Primary Button (Sage)
```html
<button class="bg-sage-text text-white px-6 py-3 rounded-lg font-semibold hover:bg-sage-dark transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2">
  Primary Button
</button>
```

### Secondary Button (Cream)
```html
<button class="bg-cream text-text-heading px-6 py-3 rounded-lg font-semibold hover:bg-sand transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2">
  Secondary Button
</button>
```

### Outline Button
```html
<button class="bg-transparent border-2 border-sage-text text-sage-text px-6 py-3 rounded-lg font-semibold hover:bg-sage-text hover:text-white transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2">
  Outline Button
</button>
```

### Dark Button
```html
<button class="bg-charcoal text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2">
  Dark Button
</button>
```

### Small Button
```html
<button class="bg-sage-text text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-sage-dark transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2">
  Small Button
</button>
```

---

## Links

Always underlined for accessibility:

```html
<a href="#" class="text-sage-text underline underline-offset-2 decoration-sage-light hover:decoration-sage-text transition-colors">
  Link text
</a>
```

Text link with arrow:
```html
<a href="#" class="text-sage-text font-medium underline underline-offset-2 decoration-sage-light hover:decoration-sage-dark focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 rounded">
  Text Link →
</a>
```

---

## Tags & Badges

### Coloured Tags
```html
<span class="bg-sage-text text-white text-xs font-medium px-3 py-1 rounded-full">Sage Tag</span>
<span class="bg-coral-text text-white text-xs font-medium px-3 py-1 rounded-full">Coral Tag</span>
<span class="bg-sky-text text-white text-xs font-medium px-3 py-1 rounded-full">Sky Tag</span>
```

### Muted Tags
```html
<span class="bg-cream text-text-muted text-xs font-medium px-3 py-1 rounded-full">Muted Tag</span>
<span class="bg-transparent border border-border text-text-muted text-xs font-medium px-3 py-1 rounded-full">Outline Tag</span>
```

---

## Cards

### Default Card (White with border)
```html
<div class="bg-white rounded-xl border border-border p-6 hover:shadow-lg transition-shadow">
  <h3 class="text-lg font-bold text-text-heading mb-2">Card Title</h3>
  <p class="text-text-body text-sm">Card content goes here.</p>
</div>
```

### Cream Card
```html
<div class="bg-cream rounded-xl p-6">
  <h3 class="text-lg font-bold text-text-heading mb-2">Cream Card</h3>
  <p class="text-text-body text-sm">Warm background for callouts.</p>
</div>
```

### Dark Card
```html
<div class="bg-charcoal rounded-xl p-6">
  <h3 class="text-lg font-bold text-white mb-2">Dark Card</h3>
  <p class="text-gray-400 text-sm">High contrast for CTAs.</p>
</div>
```

### Accent Border Cards
```html
<!-- Sage accent -->
<div class="bg-white rounded-xl border border-border border-t-4 border-t-sage-text p-6">
  <h3 class="text-lg font-bold text-text-heading mb-2">Sage Accent</h3>
  <p class="text-text-body text-sm">Coloured top border.</p>
</div>

<!-- Coral accent -->
<div class="bg-white rounded-xl border border-border border-t-4 border-t-coral-text p-6">
  <h3 class="text-lg font-bold text-text-heading mb-2">Coral Accent</h3>
  <p class="text-text-body text-sm">For emphasis.</p>
</div>

<!-- Sky accent -->
<div class="bg-white rounded-xl border border-border border-t-4 border-t-sky-text p-6">
  <h3 class="text-lg font-bold text-text-heading mb-2">Sky Accent</h3>
  <p class="text-text-body text-sm">Cool accent variety.</p>
</div>
```

---

## Callouts

### Sage Callout (Tips, best practices)
```html
<div class="bg-sage-light border-l-4 border-sage-text p-6 rounded-r-lg" role="note">
  <p class="font-semibold text-sage-dark mb-1">Tip</p>
  <p class="text-text-body">Use for tips, best practices, and positive information.</p>
</div>
```

### Coral Callout (Warnings)
```html
<div class="bg-coral-light border-l-4 border-coral-text p-6 rounded-r-lg" role="note">
  <p class="font-semibold text-coral-dark mb-1">Warning</p>
  <p class="text-text-body">Use for warnings and important notes.</p>
</div>
```

### Sky Callout (Notes, context)
```html
<div class="bg-sky-light border-l-4 border-sky-text p-6 rounded-r-lg" role="note">
  <p class="font-semibold text-sky-dark mb-1">Note</p>
  <p class="text-text-body">Use for additional context and asides.</p>
</div>
```

---

## Quote Block

```html
<figure class="relative bg-gradient-to-br from-sage-text to-sage-dark rounded-xl p-10 md:p-16 overflow-hidden">
  <!-- Decorative quote mark (optional) -->
  <div class="absolute top-[-30px] left-5 text-[250px] font-serif text-white/10 leading-none" aria-hidden="true">"</div>

  <blockquote class="text-2xl md:text-3xl font-semibold text-white leading-relaxed max-w-2xl relative z-10">
    Quote text here.
  </blockquote>
  <figcaption class="text-sm text-white/85 mt-6 relative z-10">— Attribution</figcaption>
</figure>
```

---

## Stats Section

```html
<div class="bg-charcoal rounded-xl p-8">
  <div class="grid grid-cols-3 gap-8 text-center">
    <div>
      <div class="text-5xl font-bold text-sage mb-2">20+</div>
      <div class="text-sm text-gray-400 uppercase tracking-wider">Years Experience</div>
    </div>
    <div>
      <div class="text-5xl font-bold text-coral mb-2">£1M+</div>
      <div class="text-sm text-gray-400 uppercase tracking-wider">Revenue Built</div>
    </div>
    <div>
      <div class="text-5xl font-bold text-sky mb-2">20</div>
      <div class="text-sm text-gray-400 uppercase tracking-wider">Person Team</div>
    </div>
  </div>
</div>
```

---

## Checklist

```html
<ul class="space-y-4" role="list">
  <li class="flex items-start gap-3">
    <span class="w-6 h-6 bg-sage-text rounded-md flex items-center justify-center text-white text-sm flex-shrink-0 mt-0.5" aria-hidden="true">✓</span>
    <span class="text-lg text-text-heading">First item with sage checkmark</span>
  </li>
  <li class="flex items-start gap-3">
    <span class="w-6 h-6 bg-coral-text rounded-md flex items-center justify-center text-white text-sm flex-shrink-0 mt-0.5" aria-hidden="true">✓</span>
    <span class="text-lg text-text-heading">Second item uses coral for variety</span>
  </li>
  <li class="flex items-start gap-3">
    <span class="w-6 h-6 bg-sky-text rounded-md flex items-center justify-center text-white text-sm flex-shrink-0 mt-0.5" aria-hidden="true">✓</span>
    <span class="text-lg text-text-heading">Third item completes the colour sequence</span>
  </li>
</ul>
```

---

## Process Flow

```html
<div class="bg-cream rounded-xl p-8">
  <h3 class="text-xl font-bold text-text-heading text-center mb-8">The Slow Development Path</h3>

  <div class="flex items-center justify-center gap-4 flex-wrap" role="list" aria-label="Process steps">
    <div class="bg-sage-text text-white px-8 py-5 rounded-lg text-center min-w-[140px]" role="listitem">
      <div class="text-lg font-semibold">Deliberate</div>
      <div class="text-sm opacity-90">Decisions</div>
    </div>

    <span class="text-sand text-3xl" aria-hidden="true">→</span>

    <div class="bg-coral-text text-white px-8 py-5 rounded-lg text-center min-w-[140px]" role="listitem">
      <div class="text-lg font-semibold">Sustainable</div>
      <div class="text-sm opacity-90">Pace</div>
    </div>

    <span class="text-sand text-3xl" aria-hidden="true">→</span>

    <div class="bg-sky-text text-white px-8 py-5 rounded-lg text-center min-w-[140px]" role="listitem">
      <div class="text-lg font-semibold">Compounding</div>
      <div class="text-sm opacity-90">Quality</div>
    </div>
  </div>

  <p class="font-annotation text-xl text-text-annotation text-center mt-8">
    The counterintuitive path to shipping faster
  </p>
</div>
```

---

## Navigation

```html
<nav class="flex items-center justify-between" aria-label="Main navigation">
  <!-- Brand mark -->
  <a href="#" class="flex items-center gap-2 group">
    <div class="w-2 h-2 bg-sage rounded-full" aria-hidden="true"></div>
    <span class="text-sm font-medium text-text-muted group-hover:text-sage-text transition-colors">THE CALM CTO</span>
  </a>

  <!-- Links -->
  <div class="flex items-center gap-8">
    <a href="#" class="text-sage-text font-medium border-b-2 border-sage pb-1" aria-current="page">Home</a>
    <a href="#" class="text-text-body font-medium hover:text-sage-text border-b-2 border-transparent hover:border-sage-light pb-1 transition-colors">Blog</a>
    <a href="#" class="text-text-body font-medium hover:text-sage-text border-b-2 border-transparent hover:border-sage-light pb-1 transition-colors">About</a>
    <a href="#" class="bg-sage-text text-white px-4 py-2 rounded-md font-medium hover:bg-sage-dark transition-colors no-underline">
      Contact →
    </a>
  </div>
</nav>
```

---

## Footer

```html
<footer class="bg-cream py-12" role="contentinfo">
  <div class="max-w-6xl mx-auto px-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 bg-sage rounded-full" aria-hidden="true"></div>
        <span class="text-sm font-medium text-text-muted">THE CALM CTO</span>
      </div>

      <nav class="flex items-center gap-6 text-sm" aria-label="Footer navigation">
        <a href="#" class="text-text-muted hover:text-sage-text transition-colors underline-offset-2 hover:underline">Home</a>
        <a href="#" class="text-text-muted hover:text-sage-text transition-colors underline-offset-2 hover:underline">Blog</a>
        <a href="#" class="text-text-muted hover:text-sage-text transition-colors underline-offset-2 hover:underline">Contact</a>
      </nav>
    </div>

    <p class="text-sm text-text-muted mt-8">
      © NicAlpi.com. All rights reserved.
    </p>
  </div>
</footer>
```

---

## CTA Section

```html
<div class="bg-charcoal text-white rounded-xl p-10 text-center">
  <h3 class="text-2xl font-bold mb-2">Launching January 2026</h3>
  <p class="text-gray-400 mb-6">Fractional CTO services for Rails teams and AI integration.</p>
  <p class="text-xl text-coral mb-8">Not "10x faster." "Still here in three years."</p>
  <a href="#" class="inline-block bg-sage-text text-white px-8 py-4 rounded-lg font-semibold hover:bg-sage-dark transition-colors no-underline focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-charcoal">
    Get in touch →
  </a>
</div>
```

---

## Section Title

```html
<h2 class="text-xs font-semibold uppercase tracking-widest text-text-muted pb-2 mb-6 border-b-[3px] border-sage-text inline-block">
  Section Title
</h2>
```

---

## Annotation Text

```html
<p class="font-annotation text-2xl text-text-annotation">
  Hand-drawn annotations add a human touch
</p>
```

---

## Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title — The Calm CTO</title>

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Caveat:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  <!-- Tailwind -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>/* Tailwind config here */</script>

  <style>
    /* Skip link */
    .skip-link {
      position: absolute;
      top: -100%;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9999;
      transition: top 0.15s ease;
    }
    .skip-link:focus { top: 1rem; }

    /* Focus states */
    *:focus-visible {
      outline: 3px solid #2563EB;
      outline-offset: 2px;
    }

    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body class="bg-off-white font-body text-text-body">
  <!-- Skip link -->
  <a href="#main-content" class="skip-link bg-charcoal text-white px-6 py-3 rounded-lg font-semibold">
    Skip to main content
  </a>

  <header class="bg-charcoal text-white py-16" role="banner">
    <!-- Header content -->
  </header>

  <main id="main-content" class="max-w-6xl mx-auto px-8 py-16">
    <!-- Page content -->
  </main>

  <footer class="bg-cream py-12" role="contentinfo">
    <!-- Footer content -->
  </footer>
</body>
</html>
```
