# UI Components Library

## Callout Boxes

### Info Box

```html
<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-6 rounded-r-lg">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
      </svg>
    </div>
    <div class="ml-3">
      <h4 class="text-sm font-medium text-blue-800">Hinweis</h4>
      <p class="text-sm text-blue-700 mt-1">
        Informationstext hier...
      </p>
    </div>
  </div>
</div>
```

### Warning Box

```html
<div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-6 rounded-r-lg">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
    </div>
    <div class="ml-3">
      <h4 class="text-sm font-medium text-yellow-800">Achtung</h4>
      <p class="text-sm text-yellow-700 mt-1">
        Warnungstext hier...
      </p>
    </div>
  </div>
</div>
```

### Success Box

```html
<div class="bg-green-50 border-l-4 border-green-500 p-4 my-6 rounded-r-lg">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
      </svg>
    </div>
    <div class="ml-3">
      <h4 class="text-sm font-medium text-green-800">Tipp</h4>
      <p class="text-sm text-green-700 mt-1">
        Profi-Tipp hier...
      </p>
    </div>
  </div>
</div>
```

### Error Box

```html
<div class="bg-red-50 border-l-4 border-red-500 p-4 my-6 rounded-r-lg">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
      </svg>
    </div>
    <div class="ml-3">
      <h4 class="text-sm font-medium text-red-800">Fehler vermeiden</h4>
      <p class="text-sm text-red-700 mt-1">
        Was du nicht tun solltest...
      </p>
    </div>
  </div>
</div>
```

---

## Table of Contents

### Sticky TOC (Sidebar)

```html
<aside class="hidden lg:block lg:w-64 lg:sticky lg:top-24 lg:self-start">
  <nav class="bg-gray-50 rounded-lg p-4" aria-label="Inhaltsverzeichnis">
    <h2 class="text-sm font-semibold text-gray-900 uppercase tracking-wide mb-4">
      Inhalt
    </h2>
    <ul class="space-y-2 text-sm">
      <li>
        <a href="#section-1" class="text-gray-600 hover:text-brand-primary block py-1">
          Section 1
        </a>
      </li>
      <li>
        <a href="#section-2" class="text-gray-600 hover:text-brand-primary block py-1">
          Section 2
        </a>
        <ul class="ml-3 mt-1 space-y-1">
          <li>
            <a href="#section-2-1" class="text-gray-400 hover:text-gray-600 block py-1">
              Subsection 2.1
            </a>
          </li>
        </ul>
      </li>
    </ul>
  </nav>
</aside>
```

### Inline TOC (In Content)

```html
<nav class="bg-gray-50 rounded-lg p-6 my-8" aria-label="Inhaltsverzeichnis">
  <h2 class="text-lg font-semibold text-gray-900 mb-4">
    📖 In diesem Artikel
  </h2>
  <ol class="space-y-2">
    <li class="flex items-start">
      <span class="text-brand-accent font-mono text-sm mr-2">01</span>
      <a href="#section-1" class="text-gray-700 hover:text-brand-accent">
        Section Title
      </a>
    </li>
    <li class="flex items-start">
      <span class="text-brand-accent font-mono text-sm mr-2">02</span>
      <a href="#section-2" class="text-gray-700 hover:text-brand-accent">
        Section Title
      </a>
    </li>
  </ol>
</nav>
```

---

## Cards

### Article Card

```html
<article class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
  <img src="..." alt="..." class="w-full h-48 object-cover" />
  <div class="p-6">
    <span class="text-xs font-semibold text-brand-accent uppercase">
      Kategorie
    </span>
    <h3 class="text-xl font-semibold text-gray-900 mt-2">
      <a href="#" class="hover:text-brand-primary">
        Artikel Titel
      </a>
    </h3>
    <p class="text-gray-600 mt-2 line-clamp-2">
      Kurze Beschreibung des Artikels...
    </p>
    <div class="mt-4 flex items-center text-sm text-gray-500">
      <span>15. Januar 2024</span>
      <span class="mx-2">•</span>
      <span>5 min Lesezeit</span>
    </div>
  </div>
</article>
```

### Feature Card

```html
<div class="bg-white rounded-lg p-6 shadow-md border border-gray-100">
  <div class="w-12 h-12 bg-brand-primary/10 rounded-lg flex items-center justify-center mb-4">
    <svg class="w-6 h-6 text-brand-primary"><!-- icon --></svg>
  </div>
  <h3 class="text-lg font-semibold text-gray-900">Feature Title</h3>
  <p class="text-gray-600 mt-2">
    Feature description text...
  </p>
</div>
```

### Stats Card

```html
<div class="bg-gradient-to-br from-brand-primary to-brand-primary/80 rounded-lg p-6 text-white">
  <p class="text-4xl font-bold">72%</p>
  <p class="text-white/80 mt-2">der Unternehmen nutzen Content Marketing</p>
</div>
```

---

## Buttons & CTAs

### Primary Button

```html
<a href="#" class="inline-flex items-center justify-center
                   px-6 py-3
                   bg-brand-accent text-white
                   font-semibold rounded-lg
                   hover:bg-brand-accent/90
                   focus:outline-none focus:ring-2 focus:ring-brand-accent focus:ring-offset-2
                   transition-colors">
  Call to Action
</a>
```

### Secondary Button

```html
<a href="#" class="inline-flex items-center justify-center
                   px-6 py-3
                   border-2 border-brand-primary text-brand-primary
                   font-semibold rounded-lg
                   hover:bg-brand-primary hover:text-white
                   focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2
                   transition-colors">
  Secondary Action
</a>
```

### CTA Box

```html
<div class="bg-gradient-to-r from-brand-primary to-brand-primary/80 rounded-lg p-8 my-12 text-center">
  <h3 class="text-2xl font-bold text-white mb-4">
    Bereit loszulegen?
  </h3>
  <p class="text-white/90 mb-6 max-w-xl mx-auto">
    Beschreibungstext für den CTA...
  </p>
  <a href="#" class="inline-flex items-center justify-center
                     px-8 py-4
                     bg-white text-brand-primary
                     font-bold rounded-lg
                     hover:bg-gray-100
                     transition-colors">
    Jetzt starten
  </a>
</div>
```

---

## Tables

### Standard Table

```html
<div class="overflow-x-auto my-8">
  <table class="min-w-full divide-y divide-gray-200">
    <thead>
      <tr class="bg-gray-50">
        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Header 1
        </th>
        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Header 2
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
          Cell 1
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
          Cell 2
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

### Comparison Table

```html
<div class="overflow-x-auto my-8">
  <table class="min-w-full">
    <thead>
      <tr>
        <th class="py-4 px-6"></th>
        <th class="py-4 px-6 bg-gray-50 text-center font-semibold">Option A</th>
        <th class="py-4 px-6 bg-brand-primary/10 text-center font-semibold border-2 border-brand-primary">
          Option B ⭐
        </th>
      </tr>
    </thead>
    <tbody class="divide-y">
      <tr>
        <td class="py-4 px-6 font-medium">Feature</td>
        <td class="py-4 px-6 text-center bg-gray-50">✓</td>
        <td class="py-4 px-6 text-center bg-brand-primary/5 border-x-2 border-brand-primary">✓</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## Images & Media

### Standard Image

```html
<figure class="my-8">
  <img
    src="/images/example.jpg"
    alt="Beschreibender Alt-Text"
    class="w-full rounded-lg shadow-md"
    loading="lazy"
    width="800"
    height="450"
  />
  <figcaption class="text-sm text-gray-500 mt-3 text-center">
    Bildbeschreibung und Quelle
  </figcaption>
</figure>
```

### Side-by-Side Images

```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-8">
  <figure>
    <img src="..." alt="..." class="w-full rounded-lg" />
    <figcaption class="text-sm text-gray-500 mt-2">Bild 1</figcaption>
  </figure>
  <figure>
    <img src="..." alt="..." class="w-full rounded-lg" />
    <figcaption class="text-sm text-gray-500 mt-2">Bild 2</figcaption>
  </figure>
</div>
```

### Video Embed

```html
<div class="relative my-8 aspect-video">
  <iframe
    src="https://www.youtube.com/embed/VIDEO_ID"
    class="absolute inset-0 w-full h-full rounded-lg"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen
    loading="lazy"
  ></iframe>
</div>
```

---

## Accordions / FAQ

```html
<div class="divide-y divide-gray-200 my-8">
  <details class="group py-4">
    <summary class="flex justify-between items-center cursor-pointer list-none">
      <span class="text-lg font-medium text-gray-900">
        Frage hier?
      </span>
      <svg class="w-5 h-5 text-gray-500 group-open:rotate-180 transition-transform">
        <path d="M5 7l5 5 5-5"/>
      </svg>
    </summary>
    <div class="mt-4 text-gray-600">
      <p>Antwort hier...</p>
    </div>
  </details>

  <details class="group py-4">
    <summary class="flex justify-between items-center cursor-pointer list-none">
      <span class="text-lg font-medium text-gray-900">
        Weitere Frage?
      </span>
      <svg class="w-5 h-5 text-gray-500 group-open:rotate-180 transition-transform">
        <path d="M5 7l5 5 5-5"/>
      </svg>
    </summary>
    <div class="mt-4 text-gray-600">
      <p>Antwort hier...</p>
    </div>
  </details>
</div>
```

---

## Author Box

```html
<aside class="bg-gray-50 rounded-lg p-6 my-12">
  <div class="flex items-start space-x-4">
    <img
      src="/images/author.jpg"
      alt="Author Name"
      class="w-16 h-16 rounded-full object-cover"
    />
    <div>
      <p class="font-semibold text-gray-900">Author Name</p>
      <p class="text-sm text-gray-500">Position / Titel</p>
      <p class="text-gray-600 mt-2 text-sm">
        Kurze Bio des Autors. Expertise und Hintergrund...
      </p>
      <div class="flex space-x-3 mt-3">
        <a href="#" class="text-gray-400 hover:text-gray-600">
          <svg class="w-5 h-5"><!-- LinkedIn --></svg>
        </a>
        <a href="#" class="text-gray-400 hover:text-gray-600">
          <svg class="w-5 h-5"><!-- Twitter --></svg>
        </a>
      </div>
    </div>
  </div>
</aside>
```
