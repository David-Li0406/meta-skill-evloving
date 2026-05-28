---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

---

## Mobile-First Design (OBLIGATOIRE)

**Penser mobile AVANT desktop.** Chaque interface doit être conçue pour fonctionner parfaitement sur un écran de 375px, puis enrichie pour les écrans plus grands.

### Principes fondamentaux

1. **Commencer par mobile** : Écrire le CSS de base pour mobile, ajouter les breakpoints pour enrichir
2. **Contenu d'abord** : Le contenu doit être lisible et accessible sur petit écran
3. **Touch-friendly** : Tout élément interactif doit être facilement cliquable au doigt
4. **Performance** : Mobile = souvent connexion lente, optimiser les assets

### Breakpoints Tailwind

```
Base     → Mobile (0-639px)     ← ÉCRIRE LE CSS ICI D'ABORD
sm:      → 640px+               ← Grands phones
md:      → 768px+               ← Tablettes
lg:      → 1024px+              ← Laptops
xl:      → 1280px+              ← Desktops
```

---

## Patterns Mobile-First Concrets

### Navigation

```jsx
// ✅ BON : Navigation adaptative
function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-sm">
      <div className="flex items-center justify-between p-4 md:px-8">
        <Logo />

        {/* Mobile: Hamburger */}
        <button
          className="md:hidden p-2 -mr-2"
          onClick={() => setIsOpen(!isOpen)}
        >
          <MenuIcon className="w-6 h-6" />
        </button>

        {/* Desktop: Full nav */}
        <nav className="hidden md:flex items-center gap-8">
          <NavLinks />
        </nav>
      </div>

      {/* Mobile menu drawer */}
      {isOpen && (
        <nav className="md:hidden border-t p-4 space-y-4">
          <NavLinks vertical />
        </nav>
      )}
    </header>
  );
}
```

### Grilles

```jsx
// ✅ BON : Grille mobile-first
<div className="grid grid-cols-1 gap-4
                sm:grid-cols-2 sm:gap-6
                lg:grid-cols-3 lg:gap-8">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>

// ❌ MAUVAIS : Desktop-first (casse sur mobile)
<div className="grid grid-cols-3 gap-8">
```

### Typographie

```jsx
// ✅ BON : Tailles qui scalent
<h1 className="text-2xl font-bold
               sm:text-3xl
               md:text-4xl
               lg:text-5xl">
  Titre Principal
</h1>

<p className="text-base leading-relaxed md:text-lg">
  Paragraphe avec bonne lisibilité sur tous les écrans.
</p>

// ❌ MAUVAIS : Taille fixe trop grande pour mobile
<h1 className="text-6xl">
```

### Spacing

```jsx
// ✅ BON : Padding adaptatif
<section className="px-4 py-12
                    md:px-8 md:py-16
                    lg:px-12 lg:py-24">

// ✅ BON : Container responsive
<div className="w-full max-w-7xl mx-auto px-4 md:px-8">

// ❌ MAUVAIS : Largeur fixe
<div className="w-[1200px]">
<div style={{ width: '1000px' }}>
```

### Flexbox

```jsx
// ✅ BON : Stack sur mobile, row sur desktop
<div className="flex flex-col gap-4
                md:flex-row md:gap-8 md:items-center">
  <div className="flex-1">Contenu gauche</div>
  <div className="flex-1">Contenu droite</div>
</div>

// ✅ BON : Wrap intelligemment
<div className="flex flex-wrap gap-2">
  {tags.map(tag => <Tag key={tag} label={tag} />)}
</div>
```

### Images

```jsx
// ✅ BON : Images responsive
<div className="relative aspect-video w-full overflow-hidden rounded-lg">
  <img
    src={src}
    alt={alt}
    className="absolute inset-0 w-full h-full object-cover"
  />
</div>

// ✅ BON : Image avec taille max
<img
  src={src}
  alt={alt}
  className="w-full max-w-md mx-auto rounded-lg"
/>

// ❌ MAUVAIS : Dimensions fixes
<img src={src} width="800" height="600" />
```

### Boutons et éléments interactifs

```jsx
// ✅ BON : Touch-friendly (min 44px)
<button className="px-6 py-3 min-h-[44px]
                   text-base font-medium
                   rounded-lg
                   active:scale-95
                   transition-transform">
  Action
</button>

// ✅ BON : Full-width sur mobile
<button className="w-full md:w-auto px-8 py-3">
  Valider
</button>

// ❌ MAUVAIS : Trop petit pour le touch
<button className="px-2 py-1 text-xs">
```

### Formulaires

```jsx
// ✅ BON : Inputs adaptés mobile
<input
  type="email"
  className="w-full px-4 py-3
             text-base  /* Évite le zoom iOS */
             rounded-lg border
             focus:ring-2 focus:ring-primary"
  placeholder="Email"
/>

// ✅ BON : Form layout responsive
<form className="space-y-4 md:space-y-6">
  <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
    <Input label="Prénom" />
    <Input label="Nom" />
  </div>
  <Input label="Email" type="email" />
  <Button type="submit" className="w-full md:w-auto">
    Envoyer
  </Button>
</form>
```

---

## UX Mobile Spécifique

### Ce qu'il faut faire

- **Espacement généreux** entre les éléments cliquables (éviter les missclicks)
- **Feedback tactile** : `active:scale-95`, `active:bg-opacity-80`
- **États de chargement** visibles (skeleton, spinner)
- **Scroll naturel** : Éviter les scroll horizontaux cachés
- **Bottom sheet** ou **drawer** au lieu de modals complexes sur mobile

### Ce qu'il ne faut JAMAIS faire

```jsx
// ❌ Hover-only interactions (pas de hover sur mobile)
<div className="opacity-0 hover:opacity-100">
  Contenu caché
</div>

// ✅ Alternative accessible
<div className="opacity-100 md:opacity-0 md:hover:opacity-100">

// ❌ Largeurs fixes en pixels
<div className="w-[800px]">
<div style={{ width: '1200px' }}>
<div style={{ minWidth: '900px' }}>

// ❌ Overflow horizontal forcé
<div className="overflow-x-scroll">
  <div className="w-[2000px]">

// ❌ Texte trop petit
<p className="text-xs"> {/* Difficile à lire sur mobile */}

// ❌ Éléments cliquables trop proches
<div className="flex gap-1"> {/* Pas assez d'espace */}
  <button>A</button>
  <button>B</button>
</div>
```

---

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose distinctive fonts. Avoid generic fonts like Arial and Inter. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents.
- **Motion**: Focus on high-impact moments: page load with staggered reveals, scroll-triggered animations, hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Gradient meshes, noise textures, geometric patterns, dramatic shadows, grain overlays.

NEVER use generic AI aesthetics: overused fonts (Inter, Roboto), cliched purple gradients, predictable layouts, cookie-cutter design.

---

## Checklist Finale

Avant de livrer une interface :

- [ ] **Mobile** : Testé sur viewport 375px, tout est lisible et cliquable
- [ ] **Tablet** : Layout adapté, pas de contenu écrasé
- [ ] **Desktop** : Utilise bien l'espace disponible
- [ ] **Touch** : Tous les boutons/liens font minimum 44x44px
- [ ] **Scroll** : Pas de scroll horizontal non voulu
- [ ] **Texte** : Minimum 16px pour le body, titres lisibles
- [ ] **Images** : Toutes responsive avec max-width: 100%
- [ ] **Performance** : Pas d'assets énormes sur mobile

**Une interface qui casse sur mobile est une interface ratée, peu importe sa beauté sur desktop.**
