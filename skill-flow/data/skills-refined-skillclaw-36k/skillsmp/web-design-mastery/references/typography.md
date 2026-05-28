# Typography

Detailed principles for effective typography in UI design.

---

## Establish a Type Scale

Most interfaces use too many font sizes. Define a system.

**Why not modular scales (4:5 ratio, etc.):**

1. Fractional values (31.25px, 39.063px) cause subpixel issues
2. Often not enough sizes for UI work

**Recommended hand-crafted scale:**

```
12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72
```

**Usage by role:**

| Size | Role |
|------|------|
| 12px | Labels, meta, fine print |
| 14px | Body text, default |
| 16px | Emphasis, large body |
| 18px | Subheadings |
| 20-24px | Card/section titles |
| 30-36px | Page headings |
| 48-72px | Hero/display text |

**Avoid em units:** Nested elements compute unexpected sizes. Use px or rem.

---

## Use Good Fonts

**Safe bet:** Neutral sans-serif (Helvetica, system fonts).

**Filtering good fonts:**

- Ignore typefaces with less than 5 weights (10+ styles including italics)
- This cuts 85% of Google Fonts options

**Optimize for legibility:**

- Headlines: Tighter letter-spacing, shorter x-height
- Body text: Wider letter-spacing, taller x-height
- Don't use condensed fonts with short x-height for UI text

**Trust the crowd:** Popular fonts are usually good. Sort by popularity.

**Steal from people who care:** Inspect favorite sites for font choices.

---

## Keep Your Line Length in Check

Fitting text to layout often means lines that are too long.

**Optimal:** 45-75 characters per line (20-35em width).

**Going wider (75+):** Risky territory for readability.

**Mixing content widths:** If paragraphs are with images, still limit paragraph width even if overall content area is wider.

---

## Baseline, Not Center

When mixing font sizes on a single line, don't vertically center.

**Problem:** Centering creates awkward baseline offsets.

**Solution:** Align by baseline—the imaginary line letters rest on.

Your eyes already perceive the baseline. Aligning to it feels natural and clean.

---

## Line-Height Is Proportional

"1.5 line-height for readability" isn't universal.

**Line length affects line-height:**

- Narrow content: 1.5 is fine
- Wide content: May need 2.0 (easier to find next line)

**Font size affects line-height:**

- Small text: Extra line spacing helps eyes find next line
- Large headlines: Line-height of 1.0 is often perfect

**Rule:** Taller line-height for small text, shorter for large text.

---

## Not Every Link Needs a Color

In paragraph text, links should stand out and look clickable.

**But in interfaces where almost everything is a link:**

- Colored links are overbearing
- Use heavier font weight or darker color instead
- Ancillary links: Color/underline only on hover

---

## Align with Readability in Mind

**Default:** Left-aligned for English (and most languages).

**Center alignment:**

- Great for headlines, short independent blocks
- If longer than 2-3 lines, left-align or rewrite shorter

**Right-align numbers:** Decimal points align, easier to compare.

**Justified text:** Enable hyphenation to avoid awkward word gaps.

---

## Use Letter-Spacing Effectively

**Trust the typeface designer** by default, but adjust for:

**Tightening headlines:**

- Fonts optimized for body text have wider letter-spacing
- For headlines, decrease letter-spacing to mimic condensed look
- Don't try the reverse (headline fonts for body text)

**Improving all-caps legibility:**

- Default letter-spacing is for sentence case
- All-caps text lacks visual diversity
- Increase letter-spacing for better readability
