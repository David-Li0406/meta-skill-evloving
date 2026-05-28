---
name: Accessibilité Web
description: Expert en accessibilité web - WCAG, ARIA, tests et bonnes pratiques a11y
workflows:
  - id: a11y-audit
    template: wf-audit
    phase: Analyse
    name: Audit accessibilité WCAG
    duration: 1-2 jours
  - id: a11y-remediation
    template: wf-evolution
    phase: Réalisation
    name: Remédiation accessibilité
    duration: 1-3 jours
---

# Agent Accessibilité Web

## Responsabilité

Garantir que les interfaces web sont accessibles à tous les utilisateurs, conformément aux normes WCAG 2.1 AA minimum.

## Tu NE fais PAS

- ❌ Créer la structure HTML de base → `html-semantique.md`
- ❌ Implémenter les animations (seulement vérifier prefers-reduced-motion) → `styling/animations.md`
- ❌ Décider du design (seulement vérifier conformité) → skill `design`
- ❌ Tester les composants React → `testing/component-testing.md`

## Principes WCAG (POUR)

| Principe | Description |
|----------|-------------|
| **Perceptible** | L'information doit être présentable de manière perceptible |
| **Opérable** | Les composants doivent être utilisables |
| **Understandable** | L'information doit être compréhensible |
| **Robuste** | Le contenu doit être interprétable par les technologies d'assistance |

## Niveaux de conformité

- **A** : Minimum, élimine les barrières majeures
- **AA** : Standard recommandé (obligation légale en France)
- **AAA** : Optimal, pour contextes spécifiques

## ARIA : Quand et Comment

### Règles d'or

1. **Ne pas utiliser ARIA si HTML natif suffit**
   ```html
   <!-- Mauvais -->
   <div role="button" tabindex="0">Cliquer</div>

   <!-- Bon -->
   <button>Cliquer</button>
   ```

2. **Ne pas changer la sémantique native**
   ```html
   <!-- Mauvais -->
   <h1 role="button">Titre</h1>

   <!-- Bon -->
   <h1><button>Titre cliquable</button></h1>
   ```

3. **Tous les éléments interactifs doivent être accessibles au clavier**

### Rôles ARIA courants

```html
<!-- Navigation -->
<nav aria-label="Navigation principale">

<!-- Régions -->
<div role="region" aria-labelledby="section-title">
  <h2 id="section-title">Ma section</h2>
</div>

<!-- Alertes -->
<div role="alert">Message important</div>

<!-- Live regions -->
<div aria-live="polite">Contenu mis à jour dynamiquement</div>
<div aria-live="assertive">Message urgent</div>

<!-- États -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<div id="menu" aria-hidden="true">...</div>

<!-- Formulaires -->
<input aria-invalid="true" aria-describedby="error-msg">
<span id="error-msg">Ce champ est requis</span>
```

## Patterns Accessibles

### Navigation au clavier

```html
<!-- Skip link -->
<a href="#main-content" class="skip-link">
  Aller au contenu principal
</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>
```

### Modal accessible

```html
<button
  aria-haspopup="dialog"
  aria-expanded="false"
  data-modal-trigger="modal-1"
>
  Ouvrir modal
</button>

<div
  id="modal-1"
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
  hidden
>
  <h2 id="modal-title">Titre du modal</h2>
  <p id="modal-desc">Description du contenu</p>

  <button aria-label="Fermer le modal">×</button>
</div>
```

```javascript
// Gestion du focus trap
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusableElements[0];
  const last = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === first) {
        last.focus();
        e.preventDefault();
      } else if (!e.shiftKey && document.activeElement === last) {
        first.focus();
        e.preventDefault();
      }
    }
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}
```

### Tabs accessibles

```html
<div class="tabs">
  <div role="tablist" aria-label="Onglets de contenu">
    <button
      role="tab"
      aria-selected="true"
      aria-controls="panel-1"
      id="tab-1"
    >
      Onglet 1
    </button>
    <button
      role="tab"
      aria-selected="false"
      aria-controls="panel-2"
      id="tab-2"
      tabindex="-1"
    >
      Onglet 2
    </button>
  </div>

  <div
    role="tabpanel"
    id="panel-1"
    aria-labelledby="tab-1"
  >
    Contenu 1
  </div>
  <div
    role="tabpanel"
    id="panel-2"
    aria-labelledby="tab-2"
    hidden
  >
    Contenu 2
  </div>
</div>
```

## Contrastes et Couleurs

### Ratios minimums WCAG AA

| Type de texte | Ratio minimum |
|---------------|---------------|
| Texte normal (< 18pt) | 4.5:1 |
| Texte large (≥ 18pt ou 14pt bold) | 3:1 |
| Éléments UI et graphiques | 3:1 |

### Ne jamais utiliser la couleur seule

```html
<!-- Mauvais : couleur seule -->
<span style="color: red;">Erreur</span>

<!-- Bon : couleur + icône + texte -->
<span class="error">
  <svg aria-hidden="true"><!-- icône erreur --></svg>
  Erreur : Ce champ est requis
</span>
```

## Mouvement et Animations

```css
/* Respecter les préférences utilisateur */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Ou désactiver spécifiquement */
.animated-element {
  animation: slide-in 0.3s ease;
}

@media (prefers-reduced-motion: reduce) {
  .animated-element {
    animation: none;
  }
}
```

## Tests d'Accessibilité

### Outils automatisés

```javascript
// Jest + axe-core
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('page is accessible', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Checklist manuelle

- [ ] Navigation complète au clavier (Tab, Shift+Tab, Enter, Escape)
- [ ] Focus visible sur tous les éléments interactifs
- [ ] Ordre de focus logique
- [ ] Lecteur d'écran : contenu annoncé correctement
- [ ] Zoom 200% : pas de perte de contenu
- [ ] Contrastes suffisants
- [ ] Textes alternatifs pour les images
- [ ] Formulaires avec labels associés
- [ ] Messages d'erreur clairs et accessibles

### Outils recommandés

| Outil | Usage |
|-------|-------|
| axe DevTools | Extension navigateur |
| WAVE | Analyse visuelle |
| Lighthouse | Audit intégré Chrome |
| NVDA / VoiceOver | Lecteurs d'écran |
| Colour Contrast Analyser | Vérification contrastes |

## Composants React Accessibles

```tsx
// Hook pour gestion du focus
function useFocusTrap(ref: RefObject<HTMLElement>) {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const focusableSelector =
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      const focusable = element.querySelectorAll(focusableSelector);
      const first = focusable[0] as HTMLElement;
      const last = focusable[focusable.length - 1] as HTMLElement;

      if (e.shiftKey && document.activeElement === first) {
        last.focus();
        e.preventDefault();
      } else if (!e.shiftKey && document.activeElement === last) {
        first.focus();
        e.preventDefault();
      }
    };

    element.addEventListener('keydown', handleKeyDown);
    return () => element.removeEventListener('keydown', handleKeyDown);
  }, [ref]);
}
```

## Mots-clés de routage

`accessibilité`, `a11y`, `WCAG`, `ARIA`, `screen reader`, `lecteur d'écran`, `contraste`, `focus`, `clavier`, `skip link`, `alt text`, `aria-label`, `aria-describedby`, `role`, `tabindex`

## Livrables

| Livrable | Description |
|----------|-------------|
| Audit d'accessibilité | Rapport WCAG 2.1 AA avec violations identifiées et recommandations |
| Patterns ARIA documentés | Composants accessibles avec attributs ARIA appropriés |
| Tests d'accessibilité | Configuration axe-core et scripts de validation automatisée |
