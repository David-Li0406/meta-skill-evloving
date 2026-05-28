# Finishing Touches

Detailed principles for polishing and completing UI designs.

---

## Supercharge the Defaults

Add flare by enhancing existing elements, not adding new ones.

**Bulleted lists → Icons:**

- Replace bullets with checkmarks, arrows, or contextual icons
- Padlock icons for security features
- Sparkle icons for premium features

**Quotes → Visual elements:**

- Increase quote mark size
- Change quote color to accent
- Add background tint

**Links → Custom styling:**

- Change color and font weight
- Custom thick/colorful underline partially overlapping text

**Form elements:**

- Custom styled checkboxes and radio buttons
- Brand color for selected states (not browser defaults)

---

## Add Color with Accent Borders

Simple trick for visual flair without graphic design skills.

**Placement options:**

- Top of cards
- Side of active navigation items
- Side of alert messages
- Under headlines
- Top of entire page layout

```css
.card { border-top: 4px solid var(--primary); }
.nav-item.active { border-left: 3px solid var(--primary); }
.alert { border-left: 4px solid var(--warning); }
```

---

## Decorate Your Backgrounds

Break monotony without drastically changing design.

**Change background color:**

- Emphasize individual panels
- Distinguish page sections
- Subtle gradient (use hues within 30° of each other)

**Repeating patterns:**

- Subtle, low contrast against background
- Can repeat along single edge
- Resources: Hero Patterns, etc.

**Shapes and illustrations:**

- Simple geometric shapes in corners
- Chunks of repeatable pattern
- Simplified illustrations (world maps, abstract shapes)

**Rule:** Keep contrast low so nothing interferes with content.

---

## Don't Overlook Empty States

Empty state is often user's first interaction. Make it count.

**Bad empty state:** "No data"

**Good empty state:**

- Illustration or image to grab attention
- Clear call-to-action to take next step
- Hide irrelevant UI (tabs, filters that don't work yet)

**Empty states are opportunities** to be interesting and exciting.

---

## Use Fewer Borders

Too many borders make design busy and cluttered.

**Alternatives to borders:**

1. **Box shadow:** Outlines element subtly (best when element color differs from background)
2. **Different background colors:** Adjacent elements with slight color difference
3. **Extra spacing:** Simply increase separation

```css
/* Instead of border */
.card { box-shadow: 0 0 0 1px rgba(0,0,0,0.05); }

/* Or background difference */
.sidebar { background: hsl(220, 15%, 97%); }
.content { background: white; }
```

---

## Think Outside the Box

Don't be constrained by preconceived notions of how components should look.

**Dropdowns:** Don't just do white box with link list.

- Break into sections
- Use multiple columns
- Add supporting text
- Include colorful icons

**Tables:** Don't need one-data-per-column.

- Combine related columns with hierarchy
- Add images
- Use color to enrich data

**Radio buttons:** Don't just do circles with labels.

- Selectable cards
- Visual representations

---

## Working with Images

**Use good photos:** Bad photos ruin designs. Hire professionals or use quality stock.

**Text on images - The problem:** Dynamic images have light and dark areas.

**Solutions:**

1. **Overlay:** Semi-transparent black (for light text) or white (for dark text)
2. **Lower image contrast:** Adjust brightness to compensate
3. **Colorize:** Desaturate + solid fill with multiply blend
4. **Text shadow:** Large blur radius, no offset (subtle glow)

**Don't scale icons beyond intended size:** 16-24px icons look chunky at 3-4x.

- Enclose in shape with background color instead

**Don't shrink screenshots too much:** Text becomes unreadable.

- Use smaller screen size layout
- Take partial screenshots
- Draw simplified version

**User-uploaded content:**

- Control shape/size with fixed containers + background-size: cover
- Prevent background bleed with subtle inner box-shadow
