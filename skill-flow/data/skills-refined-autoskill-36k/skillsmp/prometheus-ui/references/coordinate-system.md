# Prometheus Coordinate System Reference

## Complete Conversion Tables

### X-Axis: Grid Units to CSS (left)

| Grid X | CSS left (vw) | Grid X | CSS left (vw) |
|--------|---------------|--------|---------------|
| -945 | 0.00vw | 0 | 50.00vw |
| -900 | 2.38vw | +100 | 55.29vw |
| -850 | 5.03vw | +200 | 60.58vw |
| -800 | 7.67vw | +300 | 65.87vw |
| -750 | 10.32vw | +400 | 71.16vw |
| -700 | 12.96vw | +500 | 76.46vw |
| -600 | 18.25vw | +600 | 81.75vw |
| -500 | 23.54vw | +700 | 87.04vw |
| -400 | 28.84vw | +800 | 92.33vw |
| -300 | 34.13vw | +850 | 94.97vw |
| -200 | 39.42vw | +900 | 97.62vw |
| -100 | 44.71vw | +945 | 100.00vw |

### Y-Axis: Grid Units to CSS (bottom)

| Grid Y | CSS bottom (vh) | Grid Y | CSS bottom (vh) |
|--------|-----------------|--------|-----------------|
| +470 | 100.00vh | 0 | 50.00vh |
| +400 | 92.55vh | -100 | 39.36vh |
| +350 | 87.23vh | -200 | 28.72vh |
| +300 | 81.91vh | -300 | 18.09vh |
| +250 | 76.60vh | -340 | 13.83vh |
| +200 | 71.28vh | -350 | 12.77vh |
| +150 | 65.96vh | -400 | 7.45vh |
| +100 | 60.64vh | -430 | 4.26vh |
| +50 | 55.32vh | -460 | 1.06vh |
| | | -470 | 0.00vh |

## Size Conversion

### Width (px to vw)

| px | vw | px | vw |
|----|----|----|-----|
| 100 | 5.29vw | 600 | 31.75vw |
| 150 | 7.94vw | 700 | 37.04vw |
| 200 | 10.58vw | 800 | 42.33vw |
| 250 | 13.23vw | 900 | 47.62vw |
| 300 | 15.87vw | 908 | 48.04vw |
| 400 | 21.16vw | 1000 | 52.91vw |
| 500 | 26.46vw | 1890 | 100.00vw |

### Height (px to vh)

| px | vh | px | vh |
|----|----|----|-----|
| 44 | 4.68vh | 300 | 31.91vh |
| 50 | 5.32vh | 400 | 42.55vh |
| 76 | 8.09vh | 500 | 53.19vh |
| 100 | 10.64vh | 600 | 63.83vh |
| 150 | 15.96vh | 690 | 73.40vh |
| 200 | 21.28vh | 940 | 100.00vh |

## Common Element Positions

### Frame Elements (Reference Only - IMMUTABLE)

| Element | Grid X | Grid Y | CSS left | CSS bottom |
|---------|--------|--------|----------|------------|
| Logo (approx) | -900 | +400 | 2.38vw | 92.55vh |
| Title (centre) | 0 | +380 | 50vw | 90.43vh |
| Top Line | full | +360 | 0-100vw | 88.30vh |
| PKE Interface | 0 | -400 | 50vw | 7.45vh |
| SAVE Button | +870 | -400 | 96.03vw | 7.45vh |
| Bottom Line | full | -430 | 0-100vw | 4.26vh |

### Content Zone Boundaries

| Boundary | Grid Position | CSS Position |
|----------|---------------|--------------|
| Top-Left | X:-940, Y:+350 | left:0.26vw, bottom:87.23vh |
| Top-Right | X:+940, Y:+350 | left:99.74vw, bottom:87.23vh |
| Bottom-Left | X:-940, Y:-340 | left:0.26vw, bottom:13.83vh |
| Bottom-Right | X:+940, Y:-340 | left:99.74vw, bottom:13.83vh |

## JavaScript Conversion Functions

```javascript
// Grid X to CSS left (vw)
function gridXToVw(x) {
  return ((945 + x) / 1890) * 100;
}

// Grid Y to CSS bottom (vh)
function gridYToVh(y) {
  return ((470 + y) / 940) * 100;
}

// Width px to vw
function pxToVw(px) {
  return (px / 1890) * 100;
}

// Height px to vh
function pxToVh(px) {
  return (px / 940) * 100;
}

// Usage examples:
// gridXToVw(-875) → 3.70vw
// gridYToVh(-375) → 10.11vh
// pxToVw(908) → 48.04vw (PKE Interface width)
// pxToVh(76) → 8.09vh (PKE Interface height)
```

## Python Conversion Script

```python
def grid_to_css(x, y):
    """Convert Grid Units to CSS vw/vh"""
    left = ((945 + x) / 1890) * 100
    bottom = ((470 + y) / 940) * 100
    return f"left: {left:.2f}vw; bottom: {bottom:.2f}vh;"

def px_to_viewport(width_px, height_px):
    """Convert pixel dimensions to viewport units"""
    vw = (width_px / 1890) * 100
    vh = (height_px / 940) * 100
    return f"width: {vw:.2f}vw; height: {vh:.2f}vh;"

# Example usage:
# grid_to_css(-875, -375) → "left: 3.70vw; bottom: 10.11vh;"
# px_to_viewport(908, 76) → "width: 48.04vw; height: 8.09vh;"
```

## Verification Checklist

After positional changes:

- [ ] Grid coordinates documented
- [ ] CSS conversion calculated
- [ ] Affirmation protocol stated
- [ ] Viewport baseline confirmed (1890×940)
- [ ] Frame boundaries respected
- [ ] Content Zone limits verified
