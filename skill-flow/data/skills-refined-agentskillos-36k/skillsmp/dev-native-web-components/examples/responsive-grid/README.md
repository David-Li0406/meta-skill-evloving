# Responsive Grid Example

Fluid grid layout using container queries and subgrid.

## Features Used

- **Container Queries** (`@container grid`)
- **Subgrid** (`grid-template-rows: subgrid`)
- **Fluid Columns** (`repeat(auto-fill, minmax())`)
- **clamp()** for fluid spacing
- **Container Query Units** (`cqi`)

## Key Patterns

### Fluid Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 15rem), 1fr));
}
```

### Container-Based Breakpoints

```css
.grid-container {
  container-type: inline-size;
}

@container grid (width >= 60rem) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Subgrid for Alignment

```css
.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;
}
```

## Browser Support

- Chrome 117+ (subgrid)
- Firefox 71+ (subgrid)
- Safari 16.0+ (subgrid)
