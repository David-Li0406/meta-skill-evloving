# Accessibility Checklist

Guide consolidé des bonnes pratiques d'accessibilité pour le design system, conforme aux standards **WCAG 2.1 AA**.

## Vue d'ensemble WCAG

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WCAG 2.1 PRINCIPLES                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. PERCEIVABLE                                                     │
│     └── Content must be presentable in ways users can perceive      │
│                                                                      │
│  2. OPERABLE                                                        │
│     └── UI must be operable by various input methods                │
│                                                                      │
│  3. UNDERSTANDABLE                                                  │
│     └── Content and operation must be understandable                │
│                                                                      │
│  4. ROBUST                                                          │
│     └── Content must work with current and future technologies      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. Color & Contrast

### Contrast Ratios

| Élément | Ratio minimum | Standard |
|---------|---------------|----------|
| Texte normal (< 18px) | **4.5:1** | WCAG AA |
| Texte large (≥ 18px ou 14px bold) | **3:1** | WCAG AA |
| Composants UI et graphiques | **3:1** | WCAG AA |
| Texte normal (enhanced) | **7:1** | WCAG AAA |

### Tokens conformes

```css
/* ✅ Backgrounds avec texte blanc (4.5:1+) */
--color-primary: #2563eb;        /* 4.6:1 */
--color-success: #16a34a;        /* 4.5:1 - default, WCAG AA compliant */
--color-error: #dc2626;          /* 4.5:1 */

/* ⚠️ Attention - contraste insuffisant avec blanc */
--color-success-bg: #22c55e;     /* 2.8:1 - backgrounds only, use dark text */
--color-error-bg: #ef4444;       /* 3.9:1 - backgrounds only, use dark text */
--color-warning: #eab308;        /* Utiliser avec --color-gray-900 */

/* ✅ Foreground sur backgrounds clairs */
--color-foreground: #18181b;     /* 15:1+ sur blanc */
--color-foreground-muted: #71717a; /* 4.6:1 sur blanc */
```

### Checklist Couleurs

- [ ] Texte normal a un contraste ≥ 4.5:1
- [ ] Texte large a un contraste ≥ 3:1
- [ ] Les icônes informatives ont un contraste ≥ 3:1
- [ ] Les bordures de focus ont un contraste ≥ 3:1
- [ ] L'information n'est pas transmise uniquement par la couleur
- [ ] Les états (error, success) utilisent icônes + couleur + texte

### Outils de vérification

```bash
# Chrome DevTools
# - Inspect element > Styles > Contrast ratio

# Extensions
# - axe DevTools
# - WAVE Evaluation Tool

# CLI
npx pa11y https://example.com

# En ligne
# https://webaim.org/resources/contrastchecker/
# https://colorable.jxnblk.com/
```

---

## 2. Typography

### Règles fondamentales

| Règle | Valeur | Raison |
|-------|--------|--------|
| Taille minimum body | **16px** | Lisibilité mobile |
| Line-height minimum | **1.5** | Dyslexie, fatigue visuelle |
| Longueur de ligne max | **75ch** | Confort de lecture |
| Letter-spacing | ≥ 0.12em pour body | WCAG AAA |

### CSS accessible

```css
body {
  font-size: 1rem;                /* 16px minimum */
  line-height: 1.5;               /* Espacement suffisant */
  max-width: 75ch;                /* Limite de caractères */
  text-size-adjust: 100%;         /* Empêche auto-zoom iOS */
}

/* Respecter les préférences utilisateur */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Ne pas désactiver le zoom */
/* ❌ */ html { user-scalable: no; }
/* ✅ */ html { user-scalable: yes; }
```

### Checklist Typographie

- [ ] Taille de base ≥ 16px
- [ ] Line-height ≥ 1.5 pour le body text
- [ ] Pas de texte justifié (ragged right préféré)
- [ ] Pas de CAPS lock pour de longs textes
- [ ] Zoom jusqu'à 200% sans perte de fonctionnalité
- [ ] Text resize possible sans horizontal scroll

---

## 3. Keyboard Navigation

### Focus visible

```css
/* ✅ Focus ring visible */
:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--color-background),
    0 0 0 4px var(--color-primary);
}

/* ❌ Ne jamais supprimer le focus sans alternative */
:focus {
  outline: none; /* Mauvais si pas de remplacement */
}
```

### Ordre de tabulation

```html
<!-- ✅ Ordre logique naturel -->
<header>
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
</header>
<main>
  <input type="text" />
  <button>Submit</button>
</main>

<!-- ❌ Éviter tabindex positif -->
<button tabindex="3">Third</button>
<button tabindex="1">First</button>
<button tabindex="2">Second</button>
```

### Skip links

```html
<!-- Premier élément du body -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<style>
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  z-index: 9999;
  padding: 1rem;
  background: var(--color-background);
}

.skip-link:focus {
  top: 0;
}
</style>
```

### Checklist Clavier

- [ ] Tous les éléments interactifs focusables
- [ ] Focus visible sur tous les éléments
- [ ] Ordre de tab logique (pas de tabindex positif)
- [ ] Skip links pour navigation rapide
- [ ] Pas de piège à clavier (focus trap seulement pour modals)
- [ ] Escape ferme les overlays
- [ ] Enter/Space activent les buttons
- [ ] Arrow keys pour navigation dans menus/tabs

---

## 4. ARIA Patterns

### Buttons

```html
<!-- Button standard -->
<button type="button">Click me</button>

<!-- Button avec icône seule -->
<button type="button" aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Button loading -->
<button type="button" aria-busy="true" aria-disabled="true">
  <span class="spinner" aria-hidden="true"></span>
  Loading...
</button>

<!-- Toggle button -->
<button
  type="button"
  aria-pressed="false"
  onclick="this.setAttribute('aria-pressed', this.getAttribute('aria-pressed') === 'true' ? 'false' : 'true')"
>
  Toggle
</button>
```

### Inputs

```html
<!-- Input avec label -->
<label for="email">Email address</label>
<input
  type="email"
  id="email"
  name="email"
  aria-describedby="email-hint email-error"
  aria-invalid="false"
/>
<span id="email-hint">We'll never share your email.</span>
<span id="email-error" role="alert"></span>

<!-- Required field -->
<label for="name">
  Name <span aria-hidden="true">*</span>
</label>
<input
  type="text"
  id="name"
  required
  aria-required="true"
/>

<!-- Checkbox group -->
<fieldset>
  <legend>Notifications</legend>
  <label>
    <input type="checkbox" name="notifications" value="email" />
    Email
  </label>
  <label>
    <input type="checkbox" name="notifications" value="sms" />
    SMS
  </label>
</fieldset>
```

### Modals

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure you want to proceed?</p>

  <button type="button">Cancel</button>
  <button type="button">Confirm</button>
</div>
```

```tsx
// Focus trap implementation
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const modal = modalRef.current;
    const focusableElements = modal?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements?.[0] as HTMLElement;
    const lastElement = focusableElements?.[focusableElements.length - 1] as HTMLElement;

    // Focus first element
    firstElement?.focus();

    // Trap focus
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        onClose();
        return;
      }

      if (e.key !== 'Tab') return;

      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement?.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement?.focus();
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  return <div ref={modalRef} role="dialog" aria-modal="true">{children}</div>;
}
```

### Alerts & Notifications

```html
<!-- Inline alert (static) -->
<div role="alert">
  <strong>Error:</strong> Please fill in all required fields.
</div>

<!-- Live region for dynamic updates -->
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
>
  <!-- Content updated dynamically -->
  3 items in cart
</div>

<!-- Toast notification -->
<div
  role="alert"
  aria-live="assertive"
>
  Your changes have been saved.
</div>
```

### Navigation

```html
<!-- Main navigation -->
<nav aria-label="Main navigation">
  <ul role="list">
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Breadcrumbs -->
<nav aria-label="Breadcrumb">
  <ol role="list">
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/shoes" aria-current="page">Shoes</a></li>
  </ol>
</nav>

<!-- Tabs -->
<div role="tablist" aria-label="Account settings">
  <button
    role="tab"
    aria-selected="true"
    aria-controls="panel-1"
    id="tab-1"
  >
    Profile
  </button>
  <button
    role="tab"
    aria-selected="false"
    aria-controls="panel-2"
    id="tab-2"
    tabindex="-1"
  >
    Settings
  </button>
</div>

<div
  role="tabpanel"
  id="panel-1"
  aria-labelledby="tab-1"
>
  Profile content...
</div>
```

### Badges & Status

```html
<!-- Notification badge -->
<button>
  <span class="sr-only">Notifications,</span>
  <svg aria-hidden="true"><!-- bell icon --></svg>
  <span aria-live="polite">
    <span class="sr-only">unread count:</span>
    5
  </span>
</button>

<!-- Status indicator -->
<span class="status-dot" role="status" aria-label="Online"></span>
```

---

## 5. Images & Media

### Images informatives

```html
<!-- Image avec alt descriptif -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2" />

<!-- Image décorative -->
<img src="decoration.svg" alt="" role="presentation" />

<!-- Image complexe -->
<figure>
  <img src="diagram.png" alt="System architecture" aria-describedby="diagram-desc" />
  <figcaption id="diagram-desc">
    The system consists of three layers: frontend, API, and database...
  </figcaption>
</figure>

<!-- SVG icon -->
<svg aria-hidden="true" focusable="false">
  <use href="#icon-search" />
</svg>
```

### Vidéo

```html
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <track kind="captions" src="captions.vtt" srclang="en" label="English" />
  <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Descriptions" />
</video>
```

### Checklist Media

- [ ] Toutes les images informatives ont un alt pertinent
- [ ] Images décoratives ont alt="" ou role="presentation"
- [ ] Vidéos ont des sous-titres
- [ ] Audio a une transcription
- [ ] Pas de contenu clignotant (> 3 fois/seconde)

---

## 6. Forms

### Structure accessible

```html
<form aria-labelledby="form-title">
  <h2 id="form-title">Contact Form</h2>

  <!-- Groupe de champs -->
  <fieldset>
    <legend>Personal Information</legend>

    <div class="form-field">
      <label for="name">Full Name <span aria-hidden="true">*</span></label>
      <input
        type="text"
        id="name"
        name="name"
        required
        aria-required="true"
        autocomplete="name"
      />
    </div>

    <div class="form-field">
      <label for="email">Email</label>
      <input
        type="email"
        id="email"
        name="email"
        autocomplete="email"
        aria-describedby="email-hint"
      />
      <span id="email-hint" class="hint">Optional</span>
    </div>
  </fieldset>

  <button type="submit">Send Message</button>
</form>
```

### Validation accessible

```tsx
function FormField({ label, error, ...props }) {
  const id = useId();
  const errorId = `${id}-error`;
  const hintId = `${id}-hint`;

  return (
    <div className="form-field">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
        {...props}
      />
      {error && (
        <span id={errorId} role="alert" className="error">
          {error}
        </span>
      )}
    </div>
  );
}
```

### Checklist Formulaires

- [ ] Chaque input a un label associé
- [ ] Champs requis marqués visuellement ET avec aria-required
- [ ] Erreurs annoncées avec role="alert"
- [ ] Erreurs liées aux inputs avec aria-describedby
- [ ] aria-invalid="true" sur les champs en erreur
- [ ] Autocomplete approprié (name, email, tel, etc.)
- [ ] Fieldset/legend pour grouper les champs liés
- [ ] Messages d'erreur clairs et constructifs

---

## 7. Motion & Animation

### Respecter les préférences

```css
/* Réduire les animations */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Alternative: animations subtiles */
@media (prefers-reduced-motion: reduce) {
  .modal {
    animation: none;
    opacity: 1;
  }
}
```

### React hook

```tsx
function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
}

// Usage
function AnimatedComponent() {
  const prefersReducedMotion = usePrefersReducedMotion();

  return (
    <motion.div
      animate={{ opacity: 1 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.3 }}
    />
  );
}
```

### Checklist Animation

- [ ] Animations respectent prefers-reduced-motion
- [ ] Pas de contenu qui clignote > 3 fois/seconde
- [ ] Animations essentielles ont une alternative statique
- [ ] Durées courtes (< 500ms pour la plupart)
- [ ] Possibilité de mettre en pause les animations longues

---

## 8. Testing

### Tests automatisés

```tsx
// jest-axe pour les tests d'accessibilité
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Button Accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('has no violations when disabled', async () => {
    const { container } = render(<Button disabled>Disabled</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### Outils de test

| Outil | Type | Usage |
|-------|------|-------|
| **axe DevTools** | Extension | Audit manuel |
| **jest-axe** | Unit test | Tests automatisés |
| **pa11y** | CLI | CI/CD integration |
| **Lighthouse** | Audit | Performance + a11y |
| **NVDA/VoiceOver** | Screen reader | Test manuel |
| **WAVE** | Extension | Visualisation erreurs |

### Script CI

```yaml
# .github/workflows/a11y.yml
name: Accessibility Tests

on: [push, pull_request]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Run accessibility tests
        run: npm run test:a11y

      - name: Run pa11y
        run: |
          npm run build
          npm run start &
          npx wait-on http://localhost:3000
          npx pa11y-ci
```

---

## Checklist Globale

### Perceivable
- [ ] Contraste texte ≥ 4.5:1 (AA)
- [ ] Contraste UI ≥ 3:1
- [ ] Information pas uniquement par couleur
- [ ] Texte redimensionnable à 200%
- [ ] Images ont des alternatives textuelles
- [ ] Vidéos ont des sous-titres

### Operable
- [ ] Navigation clavier complète
- [ ] Focus visible sur tous les éléments
- [ ] Pas de piège à clavier
- [ ] Skip links disponibles
- [ ] Délais suffisants (ou ajustables)
- [ ] Pas de contenu clignotant

### Understandable
- [ ] Langue de page déclarée
- [ ] Navigation cohérente
- [ ] Labels de formulaires clairs
- [ ] Messages d'erreur explicites
- [ ] Aide contextuelle disponible

### Robust
- [ ] HTML valide
- [ ] ARIA utilisé correctement
- [ ] Compatible avec les lecteurs d'écran
- [ ] Fonctionne sans JavaScript (graceful degradation)

---

## Ressources

### Documentation
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

### Outils
- [axe-core](https://github.com/dequelabs/axe-core)
- [pa11y](https://pa11y.org/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

### Screen Readers
- [NVDA](https://www.nvaccess.org/) (Windows, gratuit)
- [VoiceOver](https://www.apple.com/accessibility/vision/) (macOS/iOS)
- [JAWS](https://www.freedomscientific.com/products/software/jaws/) (Windows)
