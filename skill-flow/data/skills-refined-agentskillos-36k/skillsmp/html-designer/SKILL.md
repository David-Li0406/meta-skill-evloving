---
name: html-designer
description: Converts Markdown articles to beautifully styled HTML using Tailwind CSS. Creates responsive, accessible landing pages with proper semantic structure. Includes TOC generation, callouts, and interactive elements. Use after content is finalized and ready for publishing.
---

# HTML Designer

Wandelt Markdown-Artikel in gestylte HTML-Seiten mit Tailwind CSS um.

## Quick Start

```
Input: Markdown Content + Brand Guidelines
Output: Responsive HTML + Tailwind Classes + Schema Markup
```

## Workflow

1. **Markdown parsen** → Struktur analysieren
2. **Semantic HTML** → Korrekte Tags (article, section, aside)
3. **Tailwind Styling** → Brand-konforme Styles
4. **Responsive Design** → Mobile-First
5. **Accessibility** → ARIA, Alt-Texte, Kontraste
6. **Schema Markup** → Strukturierte Daten einbetten

## Output Format

```json
{
  "html": {
    "full_page": "<article>...</article>",
    "sections": [
      {
        "id": "was-ist-content-marketing",
        "html": "<section>...</section>"
      }
    ],
    "toc": "<nav class='toc'>...</nav>",
    "schema": "<script type='application/ld+json'>...</script>"
  },
  "assets": {
    "css_classes_used": ["prose", "container", "..."],
    "images_referenced": ["hero.jpg", "diagram.png"],
    "icons_used": ["info", "warning", "check"]
  },
  "meta": {
    "word_count": 2500,
    "reading_time": "12 min",
    "headings_count": {"h2": 8, "h3": 15}
  }
}
```

## Brand Styling

### Farben

```css
/* Brand Colors */
--primary: #003366;      /* Dark Blue */
--accent: #ff6600;       /* Orange */
--background: #ffffff;
--text: #333333;
--text-muted: #666666;
--border: #e5e5e5;

/* Tailwind Config */
colors: {
  brand: {
    primary: '#003366',
    accent: '#ff6600'
  }
}
```

### Typography

```css
/* Headings */
H1: text-3xl md:text-4xl font-bold text-brand-primary
H2: text-2xl md:text-3xl font-semibold text-gray-900 mt-12 mb-4
H3: text-xl md:text-2xl font-medium text-gray-800 mt-8 mb-3

/* Body */
p: text-base md:text-lg text-gray-700 leading-relaxed mb-4

/* Links */
a: text-brand-accent hover:underline
```

Details: [TYPOGRAPHY.md](TYPOGRAPHY.md)

## Component Library

### Text Elemente

```html
<!-- Paragraph -->
<p class="text-gray-700 leading-relaxed mb-4">
  Content here...
</p>

<!-- Lead Paragraph (Intro) -->
<p class="text-xl text-gray-600 leading-relaxed mb-8">
  Intro text...
</p>

<!-- Blockquote -->
<blockquote class="border-l-4 border-brand-accent pl-4 italic text-gray-600 my-6">
  "Quote text..."
</blockquote>
```

### Listen

```html
<!-- Unordered List -->
<ul class="list-disc list-inside space-y-2 text-gray-700 mb-6">
  <li>Item one</li>
  <li>Item two</li>
</ul>

<!-- Ordered List -->
<ol class="list-decimal list-inside space-y-2 text-gray-700 mb-6">
  <li>Step one</li>
  <li>Step two</li>
</ol>

<!-- Checklist -->
<ul class="space-y-2 mb-6">
  <li class="flex items-start">
    <svg class="w-5 h-5 text-green-500 mr-2 mt-1">✓</svg>
    <span>Completed item</span>
  </li>
</ul>
```

Details: [COMPONENTS.md](COMPONENTS.md)

### Callouts

```html
<!-- Info Box -->
<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-6">
  <div class="flex">
    <div class="flex-shrink-0">ℹ️</div>
    <div class="ml-3">
      <p class="text-blue-700">Info text here...</p>
    </div>
  </div>
</div>

<!-- Warning Box -->
<div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-6">
  <div class="flex">
    <div class="flex-shrink-0">⚠️</div>
    <div class="ml-3">
      <p class="text-yellow-700">Warning text here...</p>
    </div>
  </div>
</div>

<!-- Tip Box -->
<div class="bg-green-50 border-l-4 border-green-500 p-4 my-6">
  <div class="flex">
    <div class="flex-shrink-0">💡</div>
    <div class="ml-3">
      <p class="text-green-700">Pro tip here...</p>
    </div>
  </div>
</div>
```

### Table of Contents

```html
<nav class="bg-gray-50 rounded-lg p-6 mb-8" aria-label="Inhaltsverzeichnis">
  <h2 class="text-lg font-semibold mb-4">Inhaltsverzeichnis</h2>
  <ul class="space-y-2">
    <li>
      <a href="#section-1" class="text-brand-accent hover:underline">
        Section 1
      </a>
      <ul class="ml-4 mt-2 space-y-1">
        <li>
          <a href="#subsection-1-1" class="text-gray-600 hover:text-brand-accent">
            Subsection 1.1
          </a>
        </li>
      </ul>
    </li>
  </ul>
</nav>
```

### Images

```html
<!-- Standard Image -->
<figure class="my-8">
  <img
    src="/images/example.jpg"
    alt="Beschreibender Alt-Text"
    class="w-full rounded-lg shadow-md"
    loading="lazy"
  />
  <figcaption class="text-sm text-gray-500 mt-2 text-center">
    Bildbeschreibung
  </figcaption>
</figure>

<!-- Full Width Image -->
<div class="relative -mx-4 md:-mx-8 my-8">
  <img
    src="/images/hero.jpg"
    alt="..."
    class="w-full"
  />
</div>
```

### Tables

```html
<div class="overflow-x-auto my-8">
  <table class="min-w-full divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
          Header
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      <tr>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
          Cell
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

## Page Structure

### Article Layout

```html
<article class="max-w-4xl mx-auto px-4 py-8">
  <!-- Header -->
  <header class="mb-8">
    <h1 class="text-4xl font-bold text-brand-primary mb-4">
      Title
    </h1>
    <div class="flex items-center text-gray-500 text-sm">
      <time datetime="2024-01-15">15. Januar 2024</time>
      <span class="mx-2">•</span>
      <span>12 min Lesezeit</span>
    </div>
  </header>

  <!-- Featured Image -->
  <figure class="mb-8">
    <img src="..." alt="..." class="w-full rounded-lg" />
  </figure>

  <!-- TOC (optional) -->
  <nav class="toc">...</nav>

  <!-- Content -->
  <div class="prose prose-lg max-w-none">
    <!-- Sections here -->
  </div>

  <!-- Author Box -->
  <aside class="border-t pt-8 mt-12">
    <div class="flex items-center">
      <img src="..." alt="Author" class="w-16 h-16 rounded-full" />
      <div class="ml-4">
        <p class="font-semibold">Author Name</p>
        <p class="text-gray-500 text-sm">Author bio...</p>
      </div>
    </div>
  </aside>

  <!-- Related Articles -->
  <section class="mt-12">
    <h2>Ähnliche Artikel</h2>
    <!-- Article cards -->
  </section>
</article>
```

Details: [PAGE_LAYOUTS.md](PAGE_LAYOUTS.md)

## Responsive Design

### Breakpoints

```
sm:  640px   (Mobile landscape)
md:  768px   (Tablet)
lg:  1024px  (Desktop)
xl:  1280px  (Large desktop)
2xl: 1536px  (Extra large)
```

### Mobile-First Pattern

```html
<!-- Typography -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">

<!-- Spacing -->
<div class="px-4 md:px-8 lg:px-12">

<!-- Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

## Accessibility

### Requirements

```
✅ Semantic HTML (article, section, nav, aside)
✅ Heading hierarchy (h1 → h2 → h3)
✅ Alt-Texte für alle Bilder
✅ Aria-Labels für Navigation
✅ Skip-to-Content Link
✅ Fokus-Styles für Keyboard-Navigation
✅ Kontrastverhältnis ≥ 4.5:1
✅ Responsive Text (nicht zu klein)
```

### ARIA Beispiele

```html
<nav aria-label="Inhaltsverzeichnis">
<section aria-labelledby="section-heading">
<img alt="Beschreibung des Bildes" role="img">
```

## Schema Markup

### Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20",
  "image": "https://example.com/image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Company Name",
    "logo": {...}
  }
}
```

### FAQ Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Frage?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Antwort..."
      }
    }
  ]
}
```

## Checkliste

- [ ] Semantic HTML verwendet?
- [ ] Tailwind Classes konsistent?
- [ ] Responsive auf allen Breakpoints?
- [ ] Alt-Texte für alle Bilder?
- [ ] TOC generiert (wenn >3 H2)?
- [ ] Schema Markup eingebettet?
- [ ] Accessibility geprüft?
- [ ] Dark Mode Support (optional)?
