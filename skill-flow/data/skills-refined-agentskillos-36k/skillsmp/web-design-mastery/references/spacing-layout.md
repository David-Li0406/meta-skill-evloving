# Layout and Spacing

Detailed principles for effective layout and spacing in UI design.

---

## Start with Too Much White Space

The easiest way to clean up a design is to give every element more room to breathe.

**Problem with adding space:** You only give minimum breathing room necessary.
**Better approach:** Start with way too much space, then remove until happy.

What seems like "a little too much" when focused on an individual element ends up being "just enough" in the complete UI context.

**Exception - Dense UIs:** Dashboards with lots of information may need compact design. Make this a deliberate decision, not the default.

---

## Establish a Spacing and Sizing System

Don't nitpick between 120px and 125px. Use a constrained set of values.

**Why linear scale won't work:**

- At small end: 12px vs 16px is 33% difference (noticeable)
- At large end: 500px vs 520px is 4% difference (imperceptible)
- Values should never be closer than ~25% apart

**Recommended scale (16px base):**

```
4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512
```

**Using the system:**

1. Take a guess at what looks best
2. Try values on either side for comparison
3. Two of three will be obviously wrong
4. Pick the remaining option

---

## You Don't Have to Fill the Whole Screen

Just because you have 1400px doesn't mean you need to use it.

- If you only need 600px, use 600px
- Spreading things out makes interfaces harder to interpret
- Don't make everything full-width just because navigation is full-width

**Shrink the canvas:** If struggling on large canvas, design mobile layout first (~400px).

**Thinking in columns:** If something works best narrow but feels unbalanced, split into columns instead of making wider (e.g., form with supporting text in separate column).

---

## Grids Are Overrated

12-column grids can do more harm than good.

**Problem 1 - Not all elements should be fluid:**

- Sidebars at 25% get too wide on large screens, too narrow on small screens
- Better: Fixed width sidebar, content area flexes

**Problem 2 - Don't shrink until you need to:**

- Login card at 6 columns (50%) on large, 8 columns on medium
- Actually wider on medium than large at certain breakpoints!
- Better: Use max-width, only shrink when necessary

**Rule:** Don't be a slave to the grid. Give components the space they need.

---

## Relative Sizing Doesn't Scale

Relationships between elements should change at different screen sizes.

**Example - Headlines:**

- Desktop: Body 18px, headline 45px (2.5x ratio)
- Mobile: Body 14px, headline should NOT be 35px (too big)
- Mobile: Better at 20-24px (1.5x ratio)

**Example - Buttons:**

- Proportional padding looks same at all sizes (just zoomed)
- Better: More generous padding at larger sizes, tighter at smaller
- Large button should *feel* like a large button

**Rule:** Large elements shrink faster than small elements.

---

## Avoid Ambiguous Spacing

When groups aren't explicitly separated (no border/background), spacing creates grouping.

**Problem:** Equal margin below label and below input—which belongs to which?

**Solution:** More space between groups than within groups.

**Applies to:**

- Form labels and inputs
- Section headings in articles
- Bulleted list items
- Horizontal component layouts

**Rule:** Whenever relying on spacing to connect elements, ensure more space around the group than within it.
