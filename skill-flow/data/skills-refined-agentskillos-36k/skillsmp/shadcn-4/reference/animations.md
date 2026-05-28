# Animations Reference

Guide to adding animations and micro-interactions with shadcn/ui components.

## Tailwind CSS Animate

### Installation

```bash
npm install tailwindcss-animate
```

```typescript
// tailwind.config.ts
plugins: [require("tailwindcss-animate")]
```

### Built-in Animations

```tsx
// Fade in
<div className="animate-in fade-in">Content</div>

// Fade out
<div className="animate-out fade-out">Content</div>

// Slide in from bottom
<div className="animate-in slide-in-from-bottom">Content</div>

// Slide in from top
<div className="animate-in slide-in-from-top">Content</div>

// Slide in from left
<div className="animate-in slide-in-from-left">Content</div>

// Slide in from right
<div className="animate-in slide-in-from-right">Content</div>

// Zoom in
<div className="animate-in zoom-in">Content</div>

// Spin
<div className="animate-spin">Loading...</div>

// Pulse
<div className="animate-pulse">Loading...</div>

// Bounce
<div className="animate-bounce">Attention!</div>
```

### Animation Modifiers

```tsx
// Duration
<div className="animate-in duration-300">300ms</div>
<div className="animate-in duration-500">500ms</div>
<div className="animate-in duration-700">700ms</div>

// Delay
<div className="animate-in delay-150">150ms delay</div>
<div className="animate-in delay-300">300ms delay</div>

// Combined
<div className="animate-in fade-in slide-in-from-bottom duration-500 delay-150">
  Fade + Slide with timing
</div>
```

## CSS Transitions

### Hover Effects

```tsx
// Scale on hover
<Button className="transition-transform hover:scale-105">
  Hover me
</Button>

// Background transition
<Card className="transition-colors hover:bg-accent">
  Hover card
</Card>

// Shadow on hover
<Card className="transition-shadow hover:shadow-lg">
  Hover for shadow
</Card>

// Multiple properties
<div className="transition-all duration-200 hover:scale-105 hover:shadow-lg">
  Combined effects
</div>
```

### Focus Effects

```tsx
// Ring animation
<Input className="transition-shadow focus:ring-2 focus:ring-primary" />

// Border color
<Input className="transition-colors focus:border-primary" />
```

## Framer Motion

### Installation

```bash
npm install framer-motion
```

### Basic Animations

```tsx
import { motion } from "framer-motion";

// Fade in on mount
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
>
  Fades in
</motion.div>

// Slide up on mount
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Slides up
</motion.div>

// Exit animation
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  exit={{ opacity: 0 }}
>
  With exit
</motion.div>
```

### AnimatePresence

```tsx
import { AnimatePresence, motion } from "framer-motion";

function Notifications({ items }) {
  return (
    <AnimatePresence>
      {items.map((item) => (
        <motion.div
          key={item.id}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.2 }}
        >
          {item.message}
        </motion.div>
      ))}
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
  visible: { opacity: 1, y: 0 },
};

function List({ items }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Gestures

```tsx
// Hover
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  Interactive button
</motion.button>

// Drag
<motion.div
  drag
  dragConstraints={{ left: 0, right: 300, top: 0, bottom: 300 }}
>
  Drag me
</motion.div>
```

## Loading States

### Skeleton

```tsx
import { Skeleton } from "@/components/ui/skeleton";

function CardSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="h-[200px] w-full rounded-xl" />
      <div className="space-y-2">
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-4 w-1/2" />
      </div>
    </div>
  );
}
```

### Spinner

```tsx
import { Loader2 } from "lucide-react";

<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Loading...
</Button>
```

### Progress

```tsx
import { Progress } from "@/components/ui/progress";

function UploadProgress({ value }) {
  return (
    <Progress
      value={value}
      className="transition-all duration-300"
    />
  );
}
```

## Micro-interactions

### Button Click

```tsx
<motion.button
  whileTap={{ scale: 0.95 }}
  className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
>
  Click me
</motion.button>
```

### Toggle Switch

```tsx
const spring = {
  type: "spring",
  stiffness: 700,
  damping: 30,
};

function Toggle({ isOn, toggle }) {
  return (
    <button
      onClick={toggle}
      className={cn(
        "w-14 h-8 rounded-full p-1 transition-colors",
        isOn ? "bg-primary" : "bg-muted"
      )}
    >
      <motion.div
        className="w-6 h-6 bg-white rounded-full"
        layout
        transition={spring}
      />
    </button>
  );
}
```

### Card Hover

```tsx
<motion.div
  whileHover={{ y: -5 }}
  transition={{ type: "spring", stiffness: 300 }}
  className="p-4 bg-card rounded-lg shadow-sm"
>
  <h3>Card Title</h3>
  <p>Card content</p>
</motion.div>
```

## Reduced Motion

### CSS Media Query

```css
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

### React Hook

```tsx
import { useReducedMotion } from "framer-motion";

function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      animate={shouldReduceMotion ? {} : { scale: 1.1 }}
    >
      Respects motion preferences
    </motion.div>
  );
}
```

### Custom Hook

```tsx
function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    );
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (event) => setPrefersReducedMotion(event.matches);
    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, []);

  return prefersReducedMotion;
}
```

## Page Transitions

### Layout Animation

```tsx
// app/template.tsx
"use client";

import { motion } from "framer-motion";

export default function Template({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

### Shared Layout

```tsx
import { LayoutGroup, motion } from "framer-motion";

function Tabs({ activeTab, setActiveTab, tabs }) {
  return (
    <LayoutGroup>
      <div className="flex gap-2">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className="relative px-4 py-2"
          >
            {tab}
            {activeTab === tab && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"
              />
            )}
          </button>
        ))}
      </div>
    </LayoutGroup>
  );
}
```
