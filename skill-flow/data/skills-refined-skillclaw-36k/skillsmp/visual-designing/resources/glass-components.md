# Glassmorphism Components

The signature look of modern "Premium" apps.

## 1. The Glass Card
A card that blurs the background behind it.

```jsx
<div className="
  relative overflow-hidden
  rounded-2xl
  bg-white/10        /* Translucent white */
  backdrop-blur-md   /* The blur magic */
  border border-white/20 /* Subtle border */
  shadow-xl
  p-6
">
  <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent pointer-events-none" />
  <h2 className="text-white font-bold text-xl relative z-10">Glass Card</h2>
</div>
```

## 2. Neo-Brutalism Label (Alternative Style)
High contrast, sharp shadows. Use for "Geeky" or "Retro" tools.

```jsx
<div className="
  bg-yellow-400
  text-black font-bold
  border-2 border-black
  shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]
  px-4 py-2
  active:shadow-none active:translate-x-[4px] active:translate-y-[4px]
  transition-all
">
  Hard Shadow Button
</div>
```

## 3. Spotlight Hover Effect
A radial gradient that follows the mouse cursor (requires JS for mouse tracking, or pure CSS group-hover hack).

```css
/* Simple CSS version (static spotlight) */
.spotlight-card:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(800px circle at var(--mouse-x) var(--mouse-y), rgba(255,255,255,0.06), transparent 40%);
  z-index: 3;
}
```
