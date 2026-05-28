# Micro-Interactions & Animation Patterns

Motion distinguishes a "web page" from a "web app".

## 1. The "Breathe" Effect (Subtle Idle Animation)
Use this for logos, hero images, or important cards to make them feel "alive".

```css
@keyframes breathe {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.animate-breathe {
  animation: breathe 3s ease-in-out infinite;
}
```

## 2. Button Press (Tactile Feedback)
Buttons must feel clickable.

```javascript
// Tailwind + Framer Motion
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  className="bg-accent px-6 py-2 rounded-full shadow-lg"
>
  Click Me
</motion.button>
```

## 3. Staggered List Entrance
Don't show a list of items all at once.

```javascript
// Framer Motion Variant
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};
```

## 4. Skeleton Loading (Shimmer)
Never verify a "Loading..." text. Use a shimmer effect.

```javascript
// Tailwind Custom Utility
<div class="animate-pulse bg-slate-700/50 h-4 w-3/4 rounded"></div>
```
