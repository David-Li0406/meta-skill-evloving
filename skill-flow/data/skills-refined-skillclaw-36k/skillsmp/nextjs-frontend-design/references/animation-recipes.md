# Animation Recipes

High-impact motion design patterns for Next.js applications.

## CSS Variables Setup

```css
/* globals.css */
:root {
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-in-out-circ: cubic-bezier(0.85, 0, 0.15, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --duration-slower: 600ms;
}
```

## Page Load Animations

### Staggered Reveal (CSS Only)

```css
/* Staggered fade-up on page load */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-stagger > * {
  opacity: 0;
  animation: fadeUp 0.6s var(--ease-out-expo) forwards;
}

.animate-stagger > *:nth-child(1) { animation-delay: 0ms; }
.animate-stagger > *:nth-child(2) { animation-delay: 80ms; }
.animate-stagger > *:nth-child(3) { animation-delay: 160ms; }
.animate-stagger > *:nth-child(4) { animation-delay: 240ms; }
.animate-stagger > *:nth-child(5) { animation-delay: 320ms; }
.animate-stagger > *:nth-child(6) { animation-delay: 400ms; }
```

```tsx
// Usage
function HeroSection() {
  return (
    <section className="animate-stagger">
      <Badge>New Release</Badge>
      <h1>Welcome to the future</h1>
      <p>Description text here</p>
      <Button>Get Started</Button>
    </section>
  );
}
```

### Hero Text Reveal

```css
@keyframes slideReveal {
  from {
    clip-path: inset(0 100% 0 0);
    transform: translateX(-20px);
  }
  to {
    clip-path: inset(0 0 0 0);
    transform: translateX(0);
  }
}

.text-reveal {
  animation: slideReveal 0.8s var(--ease-out-expo) forwards;
  animation-delay: 0.2s;
  opacity: 0;
  animation-fill-mode: forwards;
}

.text-reveal.visible {
  opacity: 1;
}
```

### Scale & Fade Entry

```css
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.scale-in {
  animation: scaleIn 0.5s var(--ease-out-back) forwards;
}
```

## Hover Effects

### Magnetic Button

```tsx
'use client';
import { useRef, useState } from 'react';

interface Position {
  x: number;
  y: number;
}

function MagneticButton({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLButtonElement>(null);
  const [position, setPosition] = useState<Position>({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    const { clientX, clientY } = e;
    const { left, top, width, height } = ref.current!.getBoundingClientRect();
    
    const x = (clientX - left - width / 2) * 0.3;
    const y = (clientY - top - height / 2) * 0.3;
    
    setPosition({ x, y });
  };

  const handleMouseLeave = () => {
    setPosition({ x: 0, y: 0 });
  };

  return (
    <button
      ref={ref}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: `translate(${position.x}px, ${position.y}px)`,
        transition: 'transform 0.15s ease-out',
      }}
      className="px-6 py-3 bg-primary text-primary-foreground rounded-lg"
    >
      {children}
    </button>
  );
}
```

### Card Tilt Effect

```tsx
'use client';
import { useRef, useState } from 'react';

function TiltCard({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const [transform, setTransform] = useState('');

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!ref.current) return;
    
    const { left, top, width, height } = ref.current.getBoundingClientRect();
    const x = (e.clientX - left - width / 2) / 10;
    const y = (e.clientY - top - height / 2) / 10;
    
    setTransform(`perspective(1000px) rotateY(${x}deg) rotateX(${-y}deg)`);
  };

  const handleMouseLeave = () => {
    setTransform('perspective(1000px) rotateY(0deg) rotateX(0deg)');
  };

  return (
    <div
      ref={ref}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        transform,
        transition: 'transform 0.1s ease-out',
      }}
      className="rounded-xl bg-card p-6 shadow-lg"
    >
      {children}
    </div>
  );
}
```

### Shine Effect

```css
.shine-effect {
  position: relative;
  overflow: hidden;
}

.shine-effect::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s ease;
}

.shine-effect:hover::before {
  left: 100%;
}
```

### Border Gradient Animation

```css
@keyframes borderGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.gradient-border {
  position: relative;
  border-radius: 12px;
  padding: 1px;
  background: linear-gradient(
    90deg,
    #ff6b6b,
    #4ecdc4,
    #45b7d1,
    #ff6b6b
  );
  background-size: 300% 100%;
}

.gradient-border:hover {
  animation: borderGradient 3s linear infinite;
}

.gradient-border > * {
  background: var(--background);
  border-radius: 11px;
}
```

## Scroll Animations

### Intersection Observer Hook

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';

interface UseInViewOptions {
  threshold?: number;
  triggerOnce?: boolean;
  rootMargin?: string;
}

function useInView({
  threshold = 0.1,
  triggerOnce = true,
  rootMargin = '0px',
}: UseInViewOptions = {}) {
  const ref = useRef<HTMLElement>(null);
  const [isInView, setIsInView] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          if (triggerOnce) {
            observer.unobserve(element);
          }
        } else if (!triggerOnce) {
          setIsInView(false);
        }
      },
      { threshold, rootMargin }
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, [threshold, triggerOnce, rootMargin]);

  return { ref, isInView };
}

// Usage
function AnimatedSection() {
  const { ref, isInView } = useInView({ threshold: 0.2 });

  return (
    <section
      ref={ref as React.RefObject<HTMLElement>}
      className={cn(
        'transition-all duration-700',
        isInView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      )}
    >
      Content that animates on scroll
    </section>
  );
}
```

### Parallax Section

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';

function ParallaxSection({ children, speed = 0.5 }: { children: React.ReactNode; speed?: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      if (!ref.current) return;
      const rect = ref.current.getBoundingClientRect();
      const scrollProgress = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      setOffset(scrollProgress * 100 * speed);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, [speed]);

  return (
    <div ref={ref} className="overflow-hidden">
      <div style={{ transform: `translateY(${offset}px)` }}>
        {children}
      </div>
    </div>
  );
}
```

## Loading States

### Skeleton Pulse

```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  background: linear-gradient(
    90deg,
    hsl(var(--muted)) 0%,
    hsl(var(--muted) / 0.7) 50%,
    hsl(var(--muted)) 100%
  );
  background-size: 200% 100%;
}
```

### Shimmer Effect

```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.shimmer {
  background: linear-gradient(
    90deg,
    hsl(var(--muted)) 25%,
    hsl(var(--muted) / 0.5) 50%,
    hsl(var(--muted)) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

### Spinner

```tsx
function Spinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizes = {
    sm: 'h-4 w-4 border-2',
    md: 'h-6 w-6 border-2',
    lg: 'h-8 w-8 border-3',
  };

  return (
    <div
      className={cn(
        'animate-spin rounded-full border-primary border-t-transparent',
        sizes[size]
      )}
    />
  );
}
```

## Motion Library Patterns

> **Note**: The `framer-motion` package has been renamed to `motion`. Use `motion/react` for imports.

### Page Transitions

```tsx
// components/page-transition.tsx
'use client';
import { motion, AnimatePresence } from 'motion/react';
import { usePathname } from 'next/navigation';

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  enter: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

export function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial="initial"
        animate="enter"
        exit="exit"
        variants={pageVariants}
        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### Staggered List

```tsx
'use client';
import { motion } from 'motion/react';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
  },
};

function StaggeredList<T>({ items, renderItem }: { items: T[]; renderItem: (item: T) => React.ReactNode }) {
  return (
    <motion.ul variants={containerVariants} initial="hidden" animate="visible">
      {items.map((item, index) => (
        <motion.li key={index} variants={itemVariants}>
          {renderItem(item)}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Expandable Card

```tsx
'use client';
import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';

function ExpandableCard({ title, preview, content }: {
  title: string;
  preview: string;
  content: React.ReactNode;
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div
      layout
      onClick={() => setIsExpanded(!isExpanded)}
      className="cursor-pointer rounded-xl bg-card p-6 shadow-lg"
    >
      <motion.h3 layout="position" className="text-xl font-semibold">
        {title}
      </motion.h3>
      
      <AnimatePresence mode="wait">
        {isExpanded ? (
          <motion.div
            key="content"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {content}
          </motion.div>
        ) : (
          <motion.p
            key="preview"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-muted-foreground"
          >
            {preview}
          </motion.p>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
```

## Tailwind Animation Utilities

Add to `tailwind.config.ts`:

```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'fade-up': 'fadeUp 0.5s ease-out forwards',
        'scale-in': 'scaleIn 0.3s ease-out forwards',
        'slide-in-right': 'slideInRight 0.3s ease-out forwards',
        'slide-in-left': 'slideInLeft 0.3s ease-out forwards',
        'bounce-in': 'bounceIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards',
      },
      keyframes: {
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        fadeUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          from: { opacity: '0', transform: 'scale(0.9)' },
          to: { opacity: '1', transform: 'scale(1)' },
        },
        slideInRight: {
          from: { opacity: '0', transform: 'translateX(20px)' },
          to: { opacity: '1', transform: 'translateX(0)' },
        },
        slideInLeft: {
          from: { opacity: '0', transform: 'translateX(-20px)' },
          to: { opacity: '1', transform: 'translateX(0)' },
        },
        bounceIn: {
          '0%': { opacity: '0', transform: 'scale(0.3)' },
          '50%': { transform: 'scale(1.05)' },
          '70%': { transform: 'scale(0.9)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
    },
  },
};

export default config;
```

## Performance Tips

1. **Prefer CSS over JavaScript** for simple animations
2. **Use `will-change`** sparingly for complex animations
3. **Avoid animating layout properties** (width, height, top, left) — use `transform` and `opacity`
4. **Use `transform: translateZ(0)`** to promote elements to their own layer
5. **Debounce scroll listeners** or use `{ passive: true }`
6. **Use `prefers-reduced-motion`** media query for accessibility

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
