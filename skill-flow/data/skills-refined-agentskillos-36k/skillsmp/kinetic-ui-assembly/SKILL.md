---
name: Kinetic UI Assembly
description: Animation strategy for "Self-Assembling" UI with spring physics, tight staggering, and brutalist raw aesthetic
---

# Kinetic UI Assembly Strategy

## Core Philosophy

1. **Structure Before Content** — Container appears before content
2. **Conservation of Momentum** — Elements settle, don't stop instantly
3. **Tight Staggering** — 20-50ms delays create flow, not sequence
4. **Raw Brutalism** — Minimal borders, system-default feel, full-width

---

## Animation Tokens

### Spring Physics (Framer Motion / lit-motion)

```typescript
// Container (Heavy, grounded)
{ stiffness: 300, damping: 30, mass: 1 }

// Content (Light, snappy lock-in)  
{ stiffness: 400, damping: 25, mass: 0.5 }
```

### CSS Fallback (Overshoot Bezier)
```css
transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
```

---

## Sequencing Phases

### Phase A: Skeleton (0-150ms)
- Scale `0.95 → 1.0` OR height unfold
- Opacity jumps 0→1 in 50ms
- Borders/background appear first

### Phase B: Anchors (50-200ms)
- Heroes, icons, images snap in
- Move **opposing** container expansion
- Optional: `blur(4px) → blur(0px)` motion blur

### Phase C: Details (100-300ms)
- Text, metadata slide in
- 30ms stagger per line
- Short slide: `10px → 0px` (lock, not fly)

---

## CSS Implementation

```css
/* Kinetic Container */
.kinetic-container {
    animation: assemble-container 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes assemble-container {
    0% { transform: scale(0.95); opacity: 0; }
    15% { opacity: 1; }
    100% { transform: scale(1); }
}

/* Kinetic Content */
.kinetic-content {
    animation: assemble-content 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    animation-fill-mode: both;
}

@keyframes assemble-content {
    0% { 
        transform: translateY(10px); 
        opacity: 0; 
        filter: blur(4px); 
    }
    100% { 
        transform: translateY(0); 
        opacity: 1; 
        filter: blur(0); 
    }
}

/* Stagger utility */
.kinetic-stagger-1 { animation-delay: 30ms; }
.kinetic-stagger-2 { animation-delay: 60ms; }
.kinetic-stagger-3 { animation-delay: 90ms; }
```

---

## Brutalist Styling Rules

```css
/* Raw, system-default feel */
:host {
    /* Full width, no artificial constraints */
    width: 100%;
    max-width: none;
    
    /* Minimal decoration */
    border-radius: 0;
    box-shadow: none;
    
    /* System fonts as fallback */
    font-family: var(--font-nf, system-ui, sans-serif);
    
    /* High contrast, no gradients */
    background: #fff;
    color: #000;
    
    /* Single pixel borders only when needed */
    border: none;
}

/* Remove excess padding */
.container {
    padding: 0;
    margin: 0;
}
```

---

## Anti-Patterns

❌ `staggerChildren: 0.2+` — Too slow, PowerPoint-like  
❌ Scale from `0%` — Balloon inflating effect  
❌ "Floaty" movement — Must accelerate fast, stop hard  
❌ Excessive borders/shadows — Keep raw  
❌ Constrained widths — Take full space  

---

## Validation Check

> Does this look like it was **drawn by a machine in fast-forward**?
> Does it feel **raw and unpolished**?
> Does it **take maximum screen space**?

If yes to all, the code is correct.
