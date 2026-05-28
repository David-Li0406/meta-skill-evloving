---
name: Responsive Design
description: Expert en design responsive - mobile-first, breakpoints, media queries et viewport
workflows:
  - id: responsive-creation
    template: wf-creation
    phase: Production
    name: Implémentation responsive
    duration: 1-2 jours
  - id: responsive-audit
    template: wf-audit
    phase: Analyse
    name: Audit responsive design
    duration: 0.5 jour
---

# Agent Responsive Design

## Responsabilité

Concevoir et implémenter des interfaces qui s'adaptent à toutes les tailles d'écran, en suivant l'approche mobile-first.

## Tu NE fais PAS

- ❌ Créer les layouts CSS de base (Grid, Flexbox) → `css-moderne.md`
- ❌ Optimiser les performances images (formats, lazy loading) → `performance/`
- ❌ Gérer les frameworks CSS (Tailwind, etc.) → `styling/`
- ❌ Tester l'accessibilité → `accessibilite.md`

## Approche Mobile-First

### Principe

Concevoir d'abord pour les petits écrans, puis enrichir pour les plus grands.

```css
/* Mobile-first : styles de base pour mobile */
.card {
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

/* Puis enrichir pour tablette */
@media (min-width: 768px) {
  .card {
    flex-direction: row;
    padding: 2rem;
  }
}

/* Et desktop */
@media (min-width: 1024px) {
  .card {
    padding: 3rem;
  }
}
```

### Avantages

1. **Performance** : CSS minimal chargé sur mobile
2. **Priorité au contenu** : Focus sur l'essentiel
3. **Progressive enhancement** : Enrichissement graduel
4. **Maintenance** : Code plus simple et logique

## Breakpoints Recommandés

### Système de breakpoints

```css
:root {
  /* Breakpoints basés sur le contenu, pas les devices */
  --breakpoint-sm: 640px;   /* Petits écrans */
  --breakpoint-md: 768px;   /* Tablettes */
  --breakpoint-lg: 1024px;  /* Desktop */
  --breakpoint-xl: 1280px;  /* Large desktop */
  --breakpoint-2xl: 1536px; /* Extra large */
}

/* Usage avec CSS custom media (future spec) */
/* @custom-media --md (min-width: 768px); */
```

### Media queries communes

```css
/* Mobile first - min-width */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }

/* Combinaisons */
@media (min-width: 768px) and (max-width: 1023px) {
  /* Tablette uniquement */
}

/* Orientation */
@media (orientation: landscape) { }
@media (orientation: portrait) { }

/* Préférences utilisateur */
@media (prefers-color-scheme: dark) { }
@media (prefers-reduced-motion: reduce) { }
@media (hover: hover) { /* Device avec hover */ }
@media (hover: none) { /* Touch device */ }
```

## Layouts Responsives

### Container responsive

```css
.container {
  width: 100%;
  margin-inline: auto;
  padding-inline: 1rem;
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
    padding-inline: 2rem;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

@media (min-width: 1280px) {
  .container {
    max-width: 1200px;
  }
}
```

### Grid responsive

```css
/* Auto-responsive avec CSS Grid */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: 1rem;
}

/* Grid avec breakpoints explicites */
.grid-responsive {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .grid-responsive {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid-responsive {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Sidebar responsive

```css
.layout {
  display: grid;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .layout {
    grid-template-columns: 250px 1fr;
  }
}

/* Ou avec container queries */
.layout-container {
  container-type: inline-size;
}

@container (min-width: 700px) {
  .layout {
    grid-template-columns: 250px 1fr;
  }
}
```

## Typographie Responsive

### Fluid typography avec clamp()

```css
:root {
  /* Base font size qui s'adapte */
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);

  /* Échelle typographique */
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.3vw, 0.9rem);
  --font-size-lg: clamp(1.125rem, 1rem + 0.6vw, 1.25rem);
  --font-size-xl: clamp(1.25rem, 1rem + 1vw, 1.5rem);
  --font-size-2xl: clamp(1.5rem, 1.2rem + 1.5vw, 2rem);
  --font-size-3xl: clamp(2rem, 1.5rem + 2vw, 3rem);
  --font-size-4xl: clamp(2.5rem, 2rem + 3vw, 4rem);
}

h1 { font-size: var(--font-size-4xl); }
h2 { font-size: var(--font-size-3xl); }
h3 { font-size: var(--font-size-2xl); }
body { font-size: var(--font-size-base); }
```

## Images Responsives

### Élément picture

```html
<picture>
  <!-- Format moderne pour navigateurs compatibles -->
  <source
    srcset="image.avif"
    type="image/avif"
  >
  <source
    srcset="image.webp"
    type="image/webp"
  >
  <!-- Art direction : images différentes par taille -->
  <source
    media="(min-width: 1024px)"
    srcset="image-large.jpg"
  >
  <source
    media="(min-width: 768px)"
    srcset="image-medium.jpg"
  >
  <!-- Fallback -->
  <img
    src="image-small.jpg"
    alt="Description de l'image"
    loading="lazy"
    decoding="async"
  >
</picture>
```

### srcset pour résolutions

```html
<img
  src="image-400.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="
    (min-width: 1024px) 33vw,
    (min-width: 768px) 50vw,
    100vw
  "
  alt="Description"
>
```

### CSS pour images fluides

```css
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Aspect ratio préservé */
.image-container {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

## Navigation Responsive

### Hamburger menu pattern

```html
<header class="header">
  <a href="/" class="logo">Logo</a>

  <button
    class="menu-toggle"
    aria-expanded="false"
    aria-controls="main-nav"
    aria-label="Menu principal"
  >
    <span class="hamburger"></span>
  </button>

  <nav id="main-nav" class="nav" aria-label="Navigation principale">
    <ul class="nav-list">
      <li><a href="/">Accueil</a></li>
      <li><a href="/about">À propos</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</header>
```

```css
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

/* Mobile : menu caché */
.nav {
  position: fixed;
  inset: 0;
  background: white;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.nav.is-open {
  transform: translateX(0);
}

.menu-toggle {
  display: flex;
}

/* Desktop : menu visible */
@media (min-width: 768px) {
  .nav {
    position: static;
    transform: none;
    background: transparent;
  }

  .nav-list {
    display: flex;
    gap: 2rem;
  }

  .menu-toggle {
    display: none;
  }
}
```

## Touch Targets

```css
/* Taille minimum pour touch (44x44px selon WCAG) */
.button,
.link,
.interactive {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}

/* Espacement entre éléments touchables */
.nav-list {
  gap: 8px;
}

/* Désactiver hover sur touch */
@media (hover: none) {
  .button:hover {
    /* Pas d'effet hover sur touch */
    background: inherit;
  }
}

/* Activer hover uniquement si disponible */
@media (hover: hover) {
  .button:hover {
    background: var(--color-primary-dark);
  }
}
```

## Checklist Responsive

- [ ] Mobile-first CSS
- [ ] Breakpoints basés sur le contenu
- [ ] Typographie fluide (clamp)
- [ ] Images responsives (srcset, picture)
- [ ] Touch targets ≥ 44px
- [ ] Navigation adaptative
- [ ] Test sur vrais devices
- [ ] Container queries si approprié
- [ ] Respect prefers-reduced-motion

## Mots-clés de routage

`responsive`, `mobile-first`, `breakpoints`, `media queries`, `viewport`, `clamp`, `fluid`, `picture`, `srcset`, `hamburger`, `touch`, `tablet`, `desktop`, `adaptive`

## Livrables

| Livrable | Description |
|----------|-------------|
| Système de breakpoints | Configuration des points de rupture et media queries standardisés |
| Composants responsive | Patterns CSS mobile-first pour navigation, grilles et containers |
| Guide images responsive | Documentation srcset, picture et stratégie d'optimisation images |
