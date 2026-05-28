# Mobile Spacing & Layout

Spacing principles optimized for touch interfaces and mobile screens.

---

## Touch Target Requirements

**Minimum sizes:**

| Platform | Minimum | Comfortable |
|----------|---------|-------------|
| iOS | 44×44 pt | 48×48 pt |
| Android | 48×48 dp | 56×56 dp |

**Common mistakes:**

- Icon buttons without padding (24px icon = 24px target ❌)
- Links in body text (hard to tap accurately)
- Close buttons in corners (fingers slip off edges)

**Solution:** Add invisible padding to reach minimum target size.

---

## Spacing Scale

Mobile spacing should be tighter than web but still comfortable.

| Token | Size | Use Case |
|-------|------|----------|
| 4 | Micro | Icon-to-text, tight inline |
| 8 | Small | Within components (button padding) |
| 12 | Medium | Between related elements |
| 16 | Base | Standard screen padding |
| 24 | Large | Between sections |
| 32 | XL | Major content separation |
| 48+ | 2XL | Hero areas, tablets |

**Screen edge padding:** 16dp minimum, 24dp preferred.

---

## Avoid Ambiguous Spacing

Even more critical on mobile—users need clear grouping.

**Rule:** More space between groups than within groups.

**List items:**

- Vertical padding within item: 12-16
- Divider + space between items: appears as break

**Forms:**

- Label to input: 4-8
- Between field groups: 24-32

---

## Don't Fill the Screen

Just because you have 375pt width doesn't mean you use it all.

- Text shouldn't touch screen edges
- Cards need margin from edges
- Bottom buttons need breathing room

**Content width limits:**

- Paragraphs: 280-320pt (not full width)
- Forms: Leave margin for visual comfort

---

## Mobile Grid Considerations

Grids are less useful on mobile due to narrow screens.

**Single column:** Default for phones
**Two columns:** Only on tablets or for thumbnails/cards
**Responsive:** Switch layouts at breakpoints, don't squeeze to fit

**Fixed elements:**

- Bottom navigation: fixed height
- App bar: fixed height
- Content area: flexible

---

## Safe Areas

Account for device notches and home indicators.

- iOS: Respect `safeAreaInsets`
- Android: System bar insets
- Don't place interactive elements in unsafe areas
