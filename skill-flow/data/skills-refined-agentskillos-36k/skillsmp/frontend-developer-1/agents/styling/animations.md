---
name: Animations Expert
description: Expert en animations web - CSS transitions, keyframes, Framer Motion
workflows:
  - id: animations-creation
    template: wf-creation
    phase: Production
    name: Création animations
    duration: 0.5-2 jours
  - id: animations-optimization
    template: wf-evolution
    phase: Réalisation
    name: Optimisation animations
    duration: 0.5-1 jour
---

# Agent Animations

## Responsabilité

Créer des animations fluides et performantes pour améliorer l'expérience utilisateur.

## Tu NE fais PAS

- ❌ Gérer le styling général (layouts, couleurs) → `tailwind-expert.md` ou `css-in-js.md`
- ❌ Créer des animations 3D complexes (Three.js, WebGL) → Déléguer à un expert 3D si nécessaire
- ❌ Gérer les canvas/WebGL → Spécialiste canvas/WebGL
- ❌ Vérifier l'accessibilité des animations → `foundations/accessibilite.md`

## Transitions CSS

### Syntaxe de base

```css
.button {
  background-color: #0070f3;
  transform: scale(1);

  /* Transition unique */
  transition: background-color 0.3s ease;

  /* Transitions multiples */
  transition:
    background-color 0.3s ease,
    transform 0.2s ease-out;

  /* Shorthand */
  transition: all 0.3s ease;
}

.button:hover {
  background-color: #0051a2;
  transform: scale(1.05);
}
```

### Timing Functions

```css
/* Fonctions prédéfinies */
transition-timing-function: ease;        /* Défaut */
transition-timing-function: ease-in;     /* Lent au début */
transition-timing-function: ease-out;    /* Lent à la fin */
transition-timing-function: ease-in-out; /* Lent aux deux */
transition-timing-function: linear;      /* Constant */

/* Cubic-bezier personnalisé */
transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); /* Ease standard */
transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55); /* Bounce */

/* Steps */
transition-timing-function: steps(4, end); /* Animation en étapes */
```

### Propriétés performantes

```css
/* ✅ Performant (GPU accelerated) */
.performant {
  transform: translateX(100px);
  transform: translateY(50px);
  transform: scale(1.2);
  transform: rotate(45deg);
  opacity: 0.5;
}

/* ❌ Éviter (trigger layout/paint) */
.slow {
  width: 200px;    /* Layout */
  height: 100px;   /* Layout */
  top: 50px;       /* Layout */
  left: 100px;     /* Layout */
  margin: 10px;    /* Layout */
  padding: 20px;   /* Layout */
  border-width: 2px; /* Layout */
}

/* Forcer l'accélération GPU */
.gpu-accelerated {
  transform: translateZ(0);
  /* ou */
  will-change: transform, opacity;
}
```

## Animations Keyframes

### Syntaxe de base

```css
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.element {
  animation: fadeIn 0.5s ease-out forwards;
}

.card {
  animation: slideUp 0.3s ease-out;
}

.button {
  animation: pulse 2s ease-in-out infinite;
}
```

### Propriétés d'animation

```css
.animated {
  animation-name: slideUp;
  animation-duration: 0.5s;
  animation-timing-function: ease-out;
  animation-delay: 0.2s;
  animation-iteration-count: 1; /* ou infinite */
  animation-direction: normal; /* reverse, alternate */
  animation-fill-mode: forwards; /* none, backwards, both */
  animation-play-state: running; /* paused */

  /* Shorthand */
  animation: slideUp 0.5s ease-out 0.2s 1 normal forwards;
}
```

### Animations courantes

```css
/* Fade in up (entrée) */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Shake (erreur) */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Spin (loading) */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Bounce */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

/* Skeleton loading */
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

## Framer Motion

### Installation

```bash
npm install framer-motion
```

### Animations de base

```tsx
import { motion } from 'framer-motion';

// Animation simple
function FadeIn() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      Contenu
    </motion.div>
  );
}

// Animation au hover
function HoverCard() {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 300 }}
    >
      Card
    </motion.div>
  );
}

// Animation d'entrée/sortie
function Modal({ isOpen }: { isOpen: boolean }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.2 }}
        >
          Modal content
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

### Variants

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
    },
  },
};

function List({ items }: { items: string[] }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.li key={item} variants={itemVariants}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Gestures et Drag

```tsx
function DraggableCard() {
  return (
    <motion.div
      drag
      dragConstraints={{ left: -100, right: 100, top: -50, bottom: 50 }}
      dragElastic={0.2}
      whileDrag={{ scale: 1.1, cursor: 'grabbing' }}
    >
      Drag me
    </motion.div>
  );
}

// Swipe
function SwipeCard({ onSwipe }: { onSwipe: (dir: string) => void }) {
  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={(_, info) => {
        if (info.offset.x > 100) onSwipe('right');
        if (info.offset.x < -100) onSwipe('left');
      }}
    >
      Swipe me
    </motion.div>
  );
}
```

### Layout animations

```tsx
function LayoutExample() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div
      layout
      onClick={() => setIsExpanded(!isExpanded)}
      style={{
        width: isExpanded ? 300 : 100,
        height: isExpanded ? 200 : 100,
      }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
    >
      Click to expand
    </motion.div>
  );
}

// Shared layout animation
function TabContent({ selectedTab }: { selectedTab: string }) {
  return (
    <div className="tabs">
      {tabs.map((tab) => (
        <button key={tab.id} onClick={() => setSelectedTab(tab.id)}>
          {tab.label}
          {selectedTab === tab.id && (
            <motion.div
              layoutId="activeTab"
              className="underline"
              transition={{ type: 'spring', stiffness: 500, damping: 30 }}
            />
          )}
        </button>
      ))}
    </div>
  );
}
```

### Scroll animations

```tsx
import { useScroll, useTransform, motion } from 'framer-motion';

function ParallaxSection() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -100]);
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [1, 0.5, 0]);

  return (
    <motion.div style={{ y, opacity }}>
      Parallax content
    </motion.div>
  );
}

// Animate on scroll into view
function ScrollReveal({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.5 }}
    >
      {children}
    </motion.div>
  );
}
```

## Accessibilité

```css
/* Respecter les préférences utilisateur */
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
```

```tsx
// Framer Motion avec reduced motion
import { useReducedMotion } from 'framer-motion';

function AccessibleAnimation() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      animate={{ x: 100 }}
      transition={{
        duration: shouldReduceMotion ? 0 : 0.5,
      }}
    />
  );
}
```

## Mots-clés de routage

`animation`, `transition`, `keyframes`, `Framer Motion`, `motion`, `animate`, `whileHover`, `AnimatePresence`, `variants`, `parallax`, `scroll animation`

## Livrables

| Livrable | Description |
|----------|-------------|
| Bibliothèque d'animations | Keyframes CSS et patterns d'animation réutilisables |
| Configuration Framer Motion | Variants et animations pour composants interactifs |
| Guide des animations | Documentation des timing, easing et bonnes pratiques |
