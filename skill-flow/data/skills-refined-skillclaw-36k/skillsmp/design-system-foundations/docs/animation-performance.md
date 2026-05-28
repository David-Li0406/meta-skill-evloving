# Animation Performance

Guide des bonnes pratiques pour les animations performantes dans le design system.

## Principe Fondamental : GPU-Accelerated Properties

```
PROPRIÉTÉS PERFORMANTES (GPU)           PROPRIÉTÉS À ÉVITER (CPU)
├── transform                           ├── width / height
├── opacity                             ├── margin / padding
├── filter                              ├── top / left / right / bottom
└── clip-path                           ├── border-width
                                        ├── font-size
                                        └── box-shadow (animé)
```

## Pourquoi transform et opacity ?

| Propriété | Layout | Paint | Composite | Performance |
|-----------|--------|-------|-----------|-------------|
| `transform` | ❌ | ❌ | ✅ | **Excellente** |
| `opacity` | ❌ | ❌ | ✅ | **Excellente** |
| `filter` | ❌ | ✅ | ✅ | Bonne |
| `width/height` | ✅ | ✅ | ✅ | **Mauvaise** |
| `margin` | ✅ | ✅ | ✅ | **Mauvaise** |
| `box-shadow` | ❌ | ✅ | ✅ | Moyenne |

## Patterns Recommandés

### Slide-in / Slide-out

```css
/* ❌ MAUVAIS - Trigger layout */
.slide-in {
  animation: slideIn 0.3s ease;
}
@keyframes slideIn {
  from { left: -100%; }
  to { left: 0; }
}

/* ✅ BON - GPU accelerated */
.slide-in {
  animation: slideIn 0.3s ease;
}
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}
```

### Scale (Grow/Shrink)

```css
/* ❌ MAUVAIS - Trigger layout + paint */
.grow {
  animation: grow 0.2s ease;
}
@keyframes grow {
  from { width: 0; height: 0; }
  to { width: 100px; height: 100px; }
}

/* ✅ BON - GPU accelerated */
.grow {
  animation: grow 0.2s ease;
}
@keyframes grow {
  from { transform: scale(0); }
  to { transform: scale(1); }
}
```

### Fade In/Out

```css
/* ✅ Opacity est performant */
.fade-in {
  animation: fadeIn 0.2s ease;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

### Combinaison Transform + Opacity

```css
/* ✅ Pattern idéal pour les entrées/sorties */
.modal-enter {
  animation: modalEnter 0.3s ease;
}

@keyframes modalEnter {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
```

## CSS Tokens pour Animations

```css
:root {
  /* ══════════════════════════════════════════════════════════════════
     ANIMATION TIMING
     ══════════════════════════════════════════════════════════════════ */

  /* Durées */
  --duration-instant: 50ms;     /* Feedback immédiat */
  --duration-fast: 150ms;       /* Hover, focus */
  --duration-normal: 250ms;     /* Transitions standard */
  --duration-slow: 350ms;       /* Modals, drawers */
  --duration-slower: 500ms;     /* Animations complexes */

  /* Easing curves */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --ease-smooth: cubic-bezier(0.25, 0.1, 0.25, 1);

  /* ══════════════════════════════════════════════════════════════════
     ANIMATION PRESETS
     ══════════════════════════════════════════════════════════════════ */

  --transition-colors: color var(--duration-fast) var(--ease-out),
                       background-color var(--duration-fast) var(--ease-out),
                       border-color var(--duration-fast) var(--ease-out);

  --transition-transform: transform var(--duration-normal) var(--ease-out);

  --transition-opacity: opacity var(--duration-normal) var(--ease-out);

  --transition-all-fast: all var(--duration-fast) var(--ease-out);
}
```

## Forcer l'Accélération GPU

```css
/* will-change prévient le navigateur */
.will-animate {
  will-change: transform, opacity;
}

/* Retirer après animation pour libérer mémoire GPU */
.animation-done {
  will-change: auto;
}

/* Alternative: forcer nouveau layer */
.gpu-layer {
  transform: translateZ(0); /* Ou translate3d(0,0,0) */
  backface-visibility: hidden;
}
```

### Attention avec will-change

```css
/* ❌ Ne pas utiliser sur tout */
* {
  will-change: transform; /* Gaspille mémoire GPU */
}

/* ✅ Utiliser uniquement quand nécessaire */
.modal {
  will-change: auto;
}
.modal.is-opening {
  will-change: transform, opacity;
}
```

## Respecter prefers-reduced-motion

```css
/* Toujours fournir une alternative */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Alternative : animations subtiles */
@media (prefers-reduced-motion: reduce) {
  .modal-enter {
    animation: none;
    opacity: 1; /* Apparition immédiate */
  }
}
```

## Animations React Performantes

### Avec CSS Modules

```tsx
import styles from './Modal.module.css';

function Modal({ isOpen, children }: ModalProps) {
  return (
    <div
      className={cn(
        styles.modal,
        isOpen ? styles.entering : styles.exiting
      )}
    >
      {children}
    </div>
  );
}
```

### Avec Framer Motion (GPU par défaut)

```tsx
import { motion, AnimatePresence } from 'framer-motion';

function Modal({ isOpen, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: -10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: -10 }}
          transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
        >
          {children}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

## Debug Performance

### Chrome DevTools

1. **Performance Tab** → Record → Analyser les frames
2. **Rendering** → Paint flashing (zones repeintes en vert)
3. **Layers** → Voir les layers GPU

### Metrics à surveiller

| Metric | Cible | Critique |
|--------|-------|----------|
| Frame rate | 60 fps | < 30 fps |
| Paint time | < 16ms | > 50ms |
| Layout shifts | 0 | > 0.1 CLS |

## Checklist Animation Performance

- [ ] Utiliser uniquement `transform` et `opacity` pour les animations
- [ ] Éviter d'animer `width`, `height`, `margin`, `padding`
- [ ] Définir `will-change` uniquement pendant l'animation
- [ ] Respecter `prefers-reduced-motion`
- [ ] Durées courtes (150-350ms pour la plupart)
- [ ] Easing approprié (ease-out pour entrées, ease-in pour sorties)
- [ ] Tester à 60fps sur devices bas de gamme
- [ ] Profiler avec Chrome DevTools Performance tab
