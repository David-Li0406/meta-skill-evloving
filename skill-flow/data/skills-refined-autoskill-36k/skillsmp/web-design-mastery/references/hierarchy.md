# Visual Hierarchy

Detailed principles for creating effective visual hierarchy in UI design.

---

## Not All Elements Are Equal

Visual hierarchy refers to how important elements appear in relation to one another. When everything competes for attention, the interface feels noisy and chaotic.

**Text color hierarchy (3 levels):**

- **Primary**: Dark color for headlines, key content
- **Secondary**: Grey for supporting content, dates
- **Tertiary**: Light grey for metadata, copyright

**Font weight hierarchy (2 levels):**

- **Normal** (400-500): Most text
- **Heavy** (600-700): Text to emphasize

---

## Size Isn't Everything

Relying too much on font size leads to primary content that's too large and secondary content that's too small.

**Better approaches:**

- Make primary element bolder (not just larger)
- Use softer color for supporting text (not tiny font size)
- Stay away from font weights under 400 for UI work

---

## Don't Use Grey Text on Colored Backgrounds

Grey on white reduces contrast, but grey on colored backgrounds looks washed out.

**Solution:** Hand-pick a new color based on the background:

1. Choose same hue as background
2. Adjust saturation and lightness until it looks right
3. Avoid reducing opacity of white text (looks dull, shows background through)

---

## Emphasize by De-emphasizing

When the main element doesn't stand out enough, don't add more emphasis to it—de-emphasize the competing elements instead.

**Example:** Active nav item not standing out?

- Don't make it bolder/brighter
- Make inactive items softer/lighter

**For larger sections:** Remove competing background colors, let content sit directly on page background.

---

## Labels Are a Last Resort

The label: value format makes hierarchy difficult—every piece gets equal emphasis.

**Strategies:**

1. **You might not need a label:** Format often speaks for itself (email, phone, price)
2. **Combine labels and values:** "In stock: 12" → "12 left in stock"
3. **Labels are secondary:** De-emphasize with smaller size, lighter color, lighter weight
4. **When to emphasize labels:** Information-dense pages where users scan for labels (tech specs)

---

## Separate Visual Hierarchy from Document Hierarchy

Just because something is an `<h1>` doesn't mean it needs to be visually dominant.

- Section titles often act more like labels—they're supportive
- The content should be the focus, not the title
- Don't let the HTML element dictate styling

---

## Balance Weight and Contrast

Bold text feels emphasized because it covers more surface area.

**Icons problem:** Icons are "heavy" and tend to feel emphasized next to text.
**Solution:** Lower the contrast of the icon by giving it a softer color.

**Thin borders problem:** 1px borders can be too subtle.
**Solution:** Instead of darkening (looks harsh), increase width to 2px.

---

## Semantics Are Secondary

Don't design button actions purely on semantics. Every action has a place in the hierarchy pyramid.

**Button hierarchy:**

- **Primary**: Obvious, solid high-contrast background (one per section)
- **Secondary**: Clear but not prominent, outline or low-contrast background
- **Tertiary**: Discoverable but unobtrusive, styled like links

**Destructive actions:** Not always big/red/bold. On confirmation dialogs, yes. On regular pages where delete is secondary? Use tertiary styling.
