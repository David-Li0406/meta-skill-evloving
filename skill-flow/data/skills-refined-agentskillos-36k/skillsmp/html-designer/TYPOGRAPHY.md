# Typography System

## Schrift-Hierarchie

### Headings

```css
/* H1 - Page Title (nur 1x) */
.h1 {
  @apply text-3xl md:text-4xl lg:text-5xl;
  @apply font-bold;
  @apply text-brand-primary;
  @apply leading-tight;
  @apply mb-6;
}

/* H2 - Section Headings */
.h2 {
  @apply text-2xl md:text-3xl;
  @apply font-semibold;
  @apply text-gray-900;
  @apply leading-snug;
  @apply mt-12 mb-4;
  @apply scroll-mt-20; /* für Anchor-Links */
}

/* H3 - Subsection Headings */
.h3 {
  @apply text-xl md:text-2xl;
  @apply font-medium;
  @apply text-gray-800;
  @apply leading-snug;
  @apply mt-8 mb-3;
}

/* H4 - Minor Headings */
.h4 {
  @apply text-lg md:text-xl;
  @apply font-medium;
  @apply text-gray-700;
  @apply mt-6 mb-2;
}
```

### Body Text

```css
/* Standard Paragraph */
.paragraph {
  @apply text-base md:text-lg;
  @apply text-gray-700;
  @apply leading-relaxed;
  @apply mb-4;
}

/* Lead Paragraph (Intro) */
.lead {
  @apply text-xl md:text-2xl;
  @apply text-gray-600;
  @apply leading-relaxed;
  @apply mb-8;
}

/* Small Text */
.small {
  @apply text-sm;
  @apply text-gray-500;
}

/* Caption */
.caption {
  @apply text-sm;
  @apply text-gray-500;
  @apply italic;
}
```

---

## Font Stacks

### Sans-Serif (Headings & UI)

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont,
             'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
```

### Serif (Alternative für Body)

```css
font-family: 'Georgia', 'Times New Roman', serif;
```

### Mono (Code)

```css
font-family: 'JetBrains Mono', 'Fira Code',
             'SF Mono', Consolas, monospace;
```

---

## Tailwind Typography Plugin

### Prose Classes

```html
<!-- Standard Prose -->
<div class="prose prose-lg max-w-none">
  <!-- Markdown-rendered content -->
</div>

<!-- Customized Prose -->
<div class="prose prose-lg
            prose-headings:text-brand-primary
            prose-a:text-brand-accent
            prose-strong:text-gray-900
            max-w-none">
  <!-- Content -->
</div>
```

### Prose Modifiers

```css
/* Size */
prose-sm    /* smaller */
prose       /* default */
prose-lg    /* larger */
prose-xl    /* extra large */

/* Color Scheme */
prose-gray    /* gray tones */
prose-slate   /* slate tones */
prose-zinc    /* zinc tones */

/* Dark Mode */
dark:prose-invert
```

---

## Responsive Typography

### Mobile → Desktop Scale

```html
<!-- H1 -->
<h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">

<!-- H2 -->
<h2 class="text-xl sm:text-2xl md:text-3xl">

<!-- H3 -->
<h3 class="text-lg sm:text-xl md:text-2xl">

<!-- Body -->
<p class="text-base md:text-lg">

<!-- Small -->
<span class="text-xs sm:text-sm">
```

### Fluid Typography (Alternative)

```css
/* Using clamp() */
h1 {
  font-size: clamp(1.75rem, 4vw, 3rem);
}

h2 {
  font-size: clamp(1.5rem, 3vw, 2.25rem);
}
```

---

## Text Styling

### Emphasis

```html
<!-- Bold -->
<strong class="font-semibold text-gray-900">Important text</strong>

<!-- Italic -->
<em class="italic">Emphasized text</em>

<!-- Underline (sparsam) -->
<span class="underline decoration-brand-accent decoration-2">
  Highlighted
</span>

<!-- Strikethrough -->
<del class="line-through text-gray-400">Removed</del>

<!-- Highlight -->
<mark class="bg-yellow-200 px-1 rounded">Highlighted text</mark>
```

### Links

```html
<!-- Standard Link -->
<a href="#" class="text-brand-accent hover:underline
                   focus:outline-none focus:ring-2 focus:ring-brand-accent">
  Link text
</a>

<!-- External Link -->
<a href="#" class="text-brand-accent hover:underline inline-flex items-center">
  External site
  <svg class="w-4 h-4 ml-1"><!-- external icon --></svg>
</a>
```

### Lists

```html
<!-- Unordered -->
<ul class="list-disc list-inside space-y-2 text-gray-700 ml-4">
  <li>Item text</li>
</ul>

<!-- Ordered -->
<ol class="list-decimal list-inside space-y-2 text-gray-700 ml-4">
  <li>Step text</li>
</ol>

<!-- Nested -->
<ul class="list-disc list-inside space-y-2 ml-4">
  <li>
    Parent item
    <ul class="list-circle list-inside space-y-1 ml-4 mt-2">
      <li>Child item</li>
    </ul>
  </li>
</ul>
```

---

## Code Typography

### Inline Code

```html
<code class="bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded text-sm font-mono">
  inline code
</code>
```

### Code Blocks

```html
<pre class="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
  <code class="text-sm font-mono leading-relaxed">
    // Code here
  </code>
</pre>
```

### With Syntax Highlighting

```html
<div class="relative">
  <!-- Language Label -->
  <span class="absolute top-2 right-2 text-xs text-gray-400">
    JavaScript
  </span>
  <pre class="bg-gray-900 text-gray-100 p-4 pt-8 rounded-lg overflow-x-auto">
    <code class="language-javascript">
      const example = "code";
    </code>
  </pre>
</div>
```

---

## Blockquotes

### Standard

```html
<blockquote class="border-l-4 border-brand-accent
                   pl-4 py-2 my-6
                   italic text-gray-600">
  <p>Quote text goes here...</p>
</blockquote>
```

### With Attribution

```html
<figure class="my-8">
  <blockquote class="border-l-4 border-brand-accent
                     pl-4 py-2
                     italic text-gray-600 text-lg">
    <p>"Quote text goes here..."</p>
  </blockquote>
  <figcaption class="mt-2 text-sm text-gray-500 pl-4">
    — <cite>Author Name</cite>, Position
  </figcaption>
</figure>
```

### Pull Quote (Featured)

```html
<aside class="my-12 mx-auto max-w-2xl text-center">
  <blockquote class="text-2xl md:text-3xl font-serif
                     text-brand-primary italic">
    <p>"Featured quote that stands out..."</p>
  </blockquote>
</aside>
```

---

## Numbers & Data

### Statistics

```html
<div class="text-center">
  <span class="text-4xl md:text-5xl font-bold text-brand-primary">
    72%
  </span>
  <p class="text-gray-600 mt-2">der Unternehmen nutzen...</p>
</div>
```

### Table Numbers

```html
<td class="text-right font-mono text-sm tabular-nums">
  1,234,567
</td>
```

---

## Spacing Guidelines

### Vertical Rhythm

```
Element         | Top      | Bottom
----------------|----------|--------
H1              | 0        | 1.5rem
H2              | 3rem     | 1rem
H3              | 2rem     | 0.75rem
H4              | 1.5rem   | 0.5rem
Paragraph       | 0        | 1rem
List            | 0        | 1.5rem
Blockquote      | 1.5rem   | 1.5rem
Image/Figure    | 2rem     | 2rem
```

### Tailwind Equivalents

```
0.5rem = mb-2
0.75rem = mb-3
1rem = mb-4
1.5rem = mb-6
2rem = mb-8
3rem = mb-12
```
