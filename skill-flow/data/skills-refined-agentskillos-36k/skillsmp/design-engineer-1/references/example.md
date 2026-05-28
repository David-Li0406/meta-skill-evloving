# Craft in Action

This shows how subtle layering translates to real decisions. Learn the thinking, not the code. Your values will differ — the approach won't.

## The Subtle Layering Mindset

Before looking at any example, internalize this: **you should barely notice the system working.**

When you look at Vercel's dashboard, you don't think "nice borders." You just understand the structure. When you look at Supabase, you don't think "good surface elevation." You just know what's above what. The craft is invisible — that's how you know it's working.

---

## Example: Dashboard with Sidebar

### Surface Decisions

**Why so subtle?** Each elevation jump should be only a few percentage points of lightness. You can barely see the difference in isolation. But when surfaces stack, the hierarchy emerges.

```css
/* Dark theme example */
--surface-0: hsl(220, 10%, 8%);   /* Canvas */
--surface-1: hsl(220, 10%, 10%);  /* Cards */
--surface-2: hsl(220, 10%, 12%);  /* Dropdowns */
--surface-3: hsl(220, 10%, 14%);  /* Tooltips */
```

**What NOT to do:** Don't make dramatic jumps between elevations. Don't use different hues for different levels. Keep the same hue, shift only lightness.

### Border Decisions

**Why rgba, not solid colors?** Low opacity borders blend with their background. A low-opacity white border on a dark surface is barely there — it defines the edge without demanding attention.

```css
/* Good - blends naturally */
border: 1px solid rgba(255, 255, 255, 0.06);

/* Harsh - stands out too much */
border: 1px solid #444;
```

**The test:** Look at your interface from arm's length. If borders are the first thing you notice, reduce opacity.

### Sidebar Decision

**Why same background as canvas, not different?**

Many dashboards make the sidebar a different color. This fragments the visual space — now you have "sidebar world" and "content world."

Better: Same background, subtle border separation. The sidebar is part of the app, not a separate region. Vercel does this. Supabase does this. The border is enough.

### Dropdown Decision

**Why surface-2, not surface-1?**

The dropdown floats above the card it emerged from. If both were surface-1, the dropdown would blend into the card — you'd lose the sense of layering. Surface-2 is just light enough to feel "above" without being dramatically different.

---

## Example: Form Controls

### Input Background

**Why darker, not lighter?**

Inputs are "inset" — they receive content, they don't project it. A slightly darker background signals "type here" without needing heavy borders.

```css
input {
  background: var(--surface-inset); /* Darker than card */
  border: 1px solid rgba(255, 255, 255, 0.06);
}
```

### Focus States

**Why subtle focus?**

Focus needs to be visible, but you don't need a glowing ring. A noticeable increase in border opacity is enough:

```css
input:focus {
  border-color: rgba(255, 255, 255, 0.15);
  outline: none;
}
```

Subtle-but-noticeable — the same principle as surfaces.

---

## Example: Button Hierarchy

### Primary Button

The one thing you want users to click. Uses brand color, full opacity:

```css
.btn-primary {
  background: var(--brand);
  color: white;
  border: none;
}
```

### Secondary Button

Important but not primary. Border-only or muted background:

```css
.btn-secondary {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--text-secondary);
}
```

### Ghost Button

Least prominent. Appears on hover:

```css
.btn-ghost {
  background: transparent;
  border: none;
  color: var(--text-secondary);
}

.btn-ghost:hover {
  background: rgba(255, 255, 255, 0.05);
}
```

---

## Adapt to Context

Your product might need:
- Warmer hues (slight yellow/orange tint)
- Cooler hues (blue-gray base)
- Different lightness progression
- Light mode (principles invert — higher elevation = shadow, not lightness)

**The principle is constant:** barely different, still distinguishable.

---

## The Craft Check

Apply the squint test to your work:

1. Blur your eyes or step back
2. Can you still perceive hierarchy?
3. Is anything jumping out at you?
4. Can you tell where regions begin and end?

If hierarchy is visible and nothing is harsh — the subtle layering is working.
