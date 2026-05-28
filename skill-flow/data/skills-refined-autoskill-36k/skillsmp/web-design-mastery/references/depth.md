# Creating Depth

Detailed principles for creating depth and elevation in UI design.

---

## Emulate a Light Source

Raised and inset effects come from understanding light.

**Fundamental rule:** Light comes from above.

**Raised elements (buttons, cards):**

1. Top edge faces sky → slightly lighter color (top border or inset shadow)
2. Element blocks light below → dark box shadow with slight vertical offset

```css
/* Raised button */
box-shadow: 
  inset 0 1px 0 hsl(220, 80%, 65%),  /* lighter top edge */
  0 2px 4px rgba(0, 0, 0, 0.15);      /* shadow below */
```

**Inset elements (wells, inputs):**

1. Bottom lip faces sky → slightly lighter (bottom border or inset shadow)
2. Area above blocks light → dark inset shadow at top

```css
/* Inset input */
box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
border-bottom: 1px solid hsl(220, 20%, 90%);
```

**Tip:** Choose lighter color by hand. Semi-transparent white sucks saturation out.

---

## Use Shadows to Convey Elevation

Shadows position elements on virtual z-axis. Closer to user = more attention.

**Shadow scale by use case:**

| Level | Shadow | Use Case |
|-------|--------|----------|
| 1 | Small, tight blur | Buttons |
| 2 | Small-medium | Cards, inputs |
| 3 | Medium | Dropdowns, popovers |
| 4 | Medium-large | Sticky headers |
| 5 | Large, soft | Modals, dialogs |

**Establishing system:** Define smallest and largest, fill in linearly.

**Example scale:**

```css
--shadow-1: 0 1px 2px rgba(0,0,0,0.05);
--shadow-2: 0 2px 4px rgba(0,0,0,0.1);
--shadow-3: 0 4px 8px rgba(0,0,0,0.1);
--shadow-4: 0 8px 16px rgba(0,0,0,0.1);
--shadow-5: 0 16px 32px rgba(0,0,0,0.15);
```

**Interactive shadows:**

- Drag item: Increase shadow (pops above others)
- Button press: Decrease/remove shadow (pressed into page)

---

## Shadows Can Have Two Parts

Premium shadows often combine two shadows with different jobs.

**First shadow (direct light):**

- Larger, softer
- Considerable vertical offset
- Large blur radius

**Second shadow (ambient occlusion):**

- Tighter, darker
- Less vertical offset
- Smaller blur radius

```css
box-shadow:
  0 10px 25px rgba(0, 0, 0, 0.15),  /* direct light shadow */
  0 2px 4px rgba(0, 0, 0, 0.12);     /* ambient shadow */
```

**Elevation adjustment:** As element gets higher (further from surface), the tight ambient shadow should become more subtle or disappear entirely.

---

## Even Flat Designs Can Have Depth

Depth without shadows or gradients.

**Depth with color:**

- Lighter than background = raised
- Darker than background = inset

**Solid shadows:**

- Short, vertical offset, NO blur
- Maintains flat aesthetic while adding depth

```css
box-shadow: 0 4px 0 hsl(220, 20%, 85%);
```

---

## Overlap Elements to Create Layers

Overlapping creates visual depth without shadows.

**Techniques:**

1. **Cross backgrounds:** Card offset to overlap two different background sections
2. **Taller than parent:** Element overlaps on both top and bottom
3. **Component overlaps:** Carousel controls overlapping edge of image

**Overlapping images:** Add "invisible border" matching background color to prevent clashing.

```css
.overlapping-image {
  border: 4px solid var(--background-color);
}
```
