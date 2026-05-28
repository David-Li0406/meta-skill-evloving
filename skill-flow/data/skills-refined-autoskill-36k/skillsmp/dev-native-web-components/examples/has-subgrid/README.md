# :has() + Subgrid Spec Table

Spec list showing `:has()` for contextual styling and `subgrid` for aligned rows.

## Features Used

- **`:has()`** - Parent reacts to child badges
- **`subgrid`** - Rows reuse the parent grid columns
- **Declarative Shadow DOM** - Component markup without JS

## Key Patterns

### Row Highlighting with :has()

```css
.row:has(.status--warn) {
  border-color: var(--warn);
}
```

### Subgrid Alignment

```css
@supports (grid-template-columns: subgrid) {
  .row {
    grid-column: 1 / -1;
    grid-template-columns: subgrid;
  }
}
```

## Browser Support

- `:has()` baseline 2023
- `subgrid` baseline 2023 (Firefox, Safari, Chrome 117+)
