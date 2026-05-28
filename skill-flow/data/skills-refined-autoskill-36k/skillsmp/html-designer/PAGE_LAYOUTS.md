# Page Layouts

## Article Layout (Standard)

### Single Column

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Article Title | Brand</title>
  <meta name="description" content="Meta description...">

  <!-- Open Graph -->
  <meta property="og:title" content="Article Title">
  <meta property="og:description" content="Description...">
  <meta property="og:image" content="/images/og-image.jpg">
  <meta property="og:type" content="article">

  <!-- Schema -->
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "...",
      ...
    }
  </script>
</head>
<body class="bg-white text-gray-900">

  <!-- Skip to Content (Accessibility) -->
  <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-brand-primary text-white px-4 py-2 rounded">
    Zum Inhalt springen
  </a>

  <!-- Header (global) -->
  <header class="border-b">
    <!-- Navigation here -->
  </header>

  <!-- Main Content -->
  <main id="main-content">
    <article class="max-w-3xl mx-auto px-4 py-12">

      <!-- Article Header -->
      <header class="mb-8">
        <div class="flex items-center text-sm text-gray-500 mb-4">
          <a href="/kategorie" class="text-brand-accent hover:underline">Kategorie</a>
          <span class="mx-2">•</span>
          <time datetime="2024-01-15">15. Januar 2024</time>
          <span class="mx-2">•</span>
          <span>12 min Lesezeit</span>
        </div>

        <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold text-brand-primary leading-tight">
          Article Title Here
        </h1>

        <p class="text-xl text-gray-600 mt-4 leading-relaxed">
          Lead paragraph / Intro text that summarizes the article...
        </p>
      </header>

      <!-- Featured Image -->
      <figure class="mb-8 -mx-4 md:mx-0">
        <img
          src="/images/featured.jpg"
          alt="Featured image description"
          class="w-full md:rounded-lg"
          width="800"
          height="450"
        />
      </figure>

      <!-- Table of Contents -->
      <nav class="bg-gray-50 rounded-lg p-6 mb-8" aria-label="Inhaltsverzeichnis">
        <h2 class="text-lg font-semibold mb-4">Inhaltsverzeichnis</h2>
        <ul class="space-y-2">
          <!-- TOC items -->
        </ul>
      </nav>

      <!-- Article Content -->
      <div class="prose prose-lg max-w-none">
        <!-- Rendered Markdown content -->
      </div>

      <!-- Author Box -->
      <aside class="border-t pt-8 mt-12">
        <!-- Author info -->
      </aside>

    </article>

    <!-- Related Articles -->
    <section class="bg-gray-50 py-12">
      <div class="max-w-6xl mx-auto px-4">
        <h2 class="text-2xl font-bold mb-8">Ähnliche Artikel</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Article cards -->
        </div>
      </div>
    </section>
  </main>

  <!-- Footer (global) -->
  <footer class="bg-gray-900 text-white">
    <!-- Footer content -->
  </footer>

</body>
</html>
```

---

## Article with Sidebar TOC

```html
<main id="main-content" class="max-w-7xl mx-auto px-4 py-12">
  <div class="lg:grid lg:grid-cols-12 lg:gap-8">

    <!-- Sidebar TOC (Desktop) -->
    <aside class="hidden lg:block lg:col-span-3">
      <nav class="sticky top-24" aria-label="Inhaltsverzeichnis">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">
          Inhalt
        </h2>
        <ul class="space-y-2 text-sm border-l border-gray-200">
          <li>
            <a href="#section-1"
               class="block pl-4 py-1 border-l-2 border-transparent
                      text-gray-600 hover:text-brand-primary hover:border-brand-primary
                      transition-colors">
              Section 1
            </a>
          </li>
          <!-- More items -->
        </ul>
      </nav>
    </aside>

    <!-- Main Content -->
    <article class="lg:col-span-9">
      <!-- Article content -->
    </article>

  </div>
</main>
```

---

## Landing Page Layout

```html
<main>
  <!-- Hero Section -->
  <section class="bg-gradient-to-br from-brand-primary to-brand-primary/80 text-white py-20">
    <div class="max-w-4xl mx-auto px-4 text-center">
      <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
        Headline Here
      </h1>
      <p class="text-xl md:text-2xl text-white/90 mb-8 max-w-2xl mx-auto">
        Subheadline text...
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="#" class="px-8 py-4 bg-white text-brand-primary font-bold rounded-lg hover:bg-gray-100">
          Primary CTA
        </a>
        <a href="#" class="px-8 py-4 border-2 border-white text-white font-bold rounded-lg hover:bg-white/10">
          Secondary CTA
        </a>
      </div>
    </div>
  </section>

  <!-- Features Grid -->
  <section class="py-16">
    <div class="max-w-6xl mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-12">Features</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Feature cards -->
      </div>
    </div>
  </section>

  <!-- Content Section -->
  <section class="py-16 bg-gray-50">
    <div class="max-w-4xl mx-auto px-4">
      <!-- Content -->
    </div>
  </section>

  <!-- Testimonials -->
  <section class="py-16">
    <div class="max-w-6xl mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-12">Das sagen unsere Kunden</h2>
      <!-- Testimonial cards -->
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-20 bg-brand-primary text-white">
    <div class="max-w-4xl mx-auto px-4 text-center">
      <h2 class="text-3xl md:text-4xl font-bold mb-6">Ready to start?</h2>
      <p class="text-xl text-white/90 mb-8">Description text...</p>
      <a href="#" class="px-8 py-4 bg-white text-brand-primary font-bold rounded-lg hover:bg-gray-100 inline-block">
        Get Started
      </a>
    </div>
  </section>
</main>
```

---

## Pillar Page Layout

```html
<main>
  <!-- Hero -->
  <section class="bg-brand-primary text-white py-16">
    <div class="max-w-4xl mx-auto px-4">
      <span class="text-brand-accent font-semibold uppercase tracking-wide">
        Ultimate Guide
      </span>
      <h1 class="text-4xl md:text-5xl font-bold mt-2 mb-6">
        Content Marketing: Der ultimative Guide 2024
      </h1>
      <p class="text-xl text-white/90 max-w-2xl">
        Alles was du über Content Marketing wissen musst...
      </p>

      <!-- Quick Stats -->
      <div class="flex flex-wrap gap-8 mt-8">
        <div>
          <span class="text-3xl font-bold">5.000+</span>
          <span class="text-white/80 block text-sm">Wörter</span>
        </div>
        <div>
          <span class="text-3xl font-bold">25</span>
          <span class="text-white/80 block text-sm">Minuten Lesezeit</span>
        </div>
        <div>
          <span class="text-3xl font-bold">12</span>
          <span class="text-white/80 block text-sm">Kapitel</span>
        </div>
      </div>
    </div>
  </section>

  <!-- TOC (Full Width) -->
  <section class="bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <a href="#chapter-1" class="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <span class="text-brand-accent font-mono text-sm">01</span>
          <h3 class="font-semibold mt-1">Was ist Content Marketing?</h3>
        </a>
        <!-- More chapters -->
      </div>
    </div>
  </section>

  <!-- Content -->
  <article class="max-w-3xl mx-auto px-4 py-12">

    <!-- Chapter -->
    <section id="chapter-1" class="scroll-mt-20">
      <div class="flex items-center mb-4">
        <span class="text-5xl font-bold text-brand-primary/20 mr-4">01</span>
        <h2 class="text-3xl font-bold">Was ist Content Marketing?</h2>
      </div>

      <div class="prose prose-lg max-w-none">
        <!-- Chapter content -->
      </div>

      <!-- Chapter CTA -->
      <div class="bg-gray-50 rounded-lg p-6 mt-8">
        <h3 class="font-semibold">Weiterlesen:</h3>
        <a href="/cluster-article" class="text-brand-accent hover:underline">
          → Detaillierter Guide zu [Thema]
        </a>
      </div>
    </section>

    <hr class="my-12 border-gray-200">

    <!-- Next Chapter -->
    <section id="chapter-2" class="scroll-mt-20">
      <!-- ... -->
    </section>

  </article>

  <!-- Download CTA -->
  <section class="bg-brand-primary text-white py-16">
    <div class="max-w-4xl mx-auto px-4 text-center">
      <h2 class="text-3xl font-bold mb-4">Guide als PDF herunterladen</h2>
      <p class="text-white/90 mb-8">Inklusive Checklisten und Templates</p>
      <a href="#" class="px-8 py-4 bg-white text-brand-primary font-bold rounded-lg inline-block">
        Kostenlos downloaden
      </a>
    </div>
  </section>

  <!-- Cluster Links -->
  <section class="py-16">
    <div class="max-w-6xl mx-auto px-4">
      <h2 class="text-2xl font-bold mb-8">Weiterführende Artikel</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Cluster article cards -->
      </div>
    </div>
  </section>
</main>
```

---

## Responsive Grid Patterns

### 2-Column

```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

### 3-Column

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

### 4-Column

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
  <div>Column 4</div>
</div>
```

### Asymmetric (2:1)

```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
  <div class="lg:col-span-2">Main content (2/3)</div>
  <aside>Sidebar (1/3)</aside>
</div>
```

### Asymmetric (1:2)

```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
  <aside>Sidebar (1/3)</aside>
  <div class="lg:col-span-2">Main content (2/3)</div>
</div>
```
