# SVG Annotation Zones

**Responsibility:** Quick zone reference for annotation placement.

---

## ⚠️ REQUIRED: Read the HTML File First

**Before using this reference, you MUST read:**

```
READ: ../card-patterns/complex-patterns/annotation-snippet.html
```

This markdown file contains ONLY the zone diagram and placement rules. The actual HTML patterns you will copy are in `annotation-snippet.html`.

---

## Zone Diagram

```
┌─────────────────────────────────────────────────────┐
│                    ZONE A (Top)                      │
│                    y: 0-15                           │
├─────┬───────────────────────────────────────┬───────┤
│     │                                       │       │
│  B  │          PLOT AREA                    │   C   │
│     │          (data only)                  │       │
│ x:  │          40-260, 20-170               │  x:   │
│ 0-38│                                       │262-280│
│     │                                       │       │
├─────┴───────────────────────────────────────┴───────┤
│                    ZONE D (Bottom)                   │
│                    y: 175-200                        │
└─────────────────────────────────────────────────────┘
```

| Zone | Use For |
|------|---------|
| A | Title, legend |
| B | Y-intercept labels, vertical arrows |
| C | Line labels (equations), endpoint annotations |
| D | X-axis labels, horizontal annotations |
| Plot | Data lines and points ONLY |

---

## Zone Assignment

| Annotation Type | Zone | X Position | Notes |
|-----------------|------|------------|-------|
| Y-intercept label | B | x="5" | Left-align, use line color |
| Y-intercept arrow | B | x="25" | Points to y-axis |
| Line equation | C | x="265" | Right side of graph |
| Slope (rise) | B | x="5" to x="38" | Label left of arrow |
| Slope (run) | D | y="180" to y="195" | Label below arrow |
| Point label (upper) | Plot | y - 12 | Above point, centered |
| Point label (lower) | Plot | y + 15 | Below point, centered |

---

## Stacking Rules

When multiple annotations compete for the same zone:
- First annotation: natural y-position
- Second annotation: offset by 15px
- Third annotation: offset by 30px

---

## Checklist

- [ ] Y-intercept labels in Zone B (x < 38)
- [ ] Line labels in Zone C (x > 262)
- [ ] No text overlaps axes (x=40 or y=170)
- [ ] Stacked annotations have 15px minimum spacing

**For styling rules and HTML patterns, see `annotation-snippet.html`.**
