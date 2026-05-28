# Styling Guide

Modern styling patterns for using MUI v7 sx prop, inline styles, and theme integration.

---

## Inline vs Separate Styles

### Decision Threshold

**<100 lines: Inline styles at top of component**

```typescript
import type { SxProps, Theme } from '@mui/material';

const componentStyles: Record<string, SxProps<Theme>> = {
    container: {
        p: 2,
        display: 'flex',
        flexDirection: 'column',
    },
    header: {
        mb: 2,
        borderBottom: '1px solid',
        borderColor: 'divider',
    },
};

export const MyComponent: React.FC = () => {
    return (
        <Box sx={componentStyles.container}>
            <Box sx={componentStyles.header}>
                <h2>Title</h2>
            </Box>
        </Box>
    );
};
```

**>100 lines: Separate `.styles.ts` file**

```typescript
// MyComponent.styles.ts
import type { SxProps, Theme } from '@mui/material';

export const componentStyles: Record<string, SxProps<Theme>> = {
    container: { ... },
    header: { ... },
    // ... 100+ lines of styles
};

// MyComponent.tsx
import { componentStyles } from './MyComponent.styles';
```

---

## MUI v7 Styling

### sx Prop Pattern

```typescript
import { Box, Paper, Typography } from '@mui/material';

export const MyComponent: React.FC = () => {
    return (
        <Box sx={{ p: 2, display: 'flex', gap: 2 }}>
            <Paper sx={{ p: 3, flex: 1 }}>
                <Typography variant="h5" sx={{ mb: 2 }}>
                    Title
                </Typography>
            </Paper>
        </Box>
    );
};
```

### Type-Safe Styles

```typescript
import type { SxProps, Theme } from '@mui/material';

const styles: SxProps<Theme> = {
    p: 2,
    bgcolor: 'background.paper',
    color: 'text.primary',
    borderColor: 'divider',
};
```

### Theme Access in sx

```typescript
<Box sx={(theme) => ({
    bgcolor: theme.palette.background.paper,
    borderRadius: theme.shape.borderRadius,
    [theme.breakpoints.down('sm')]: {
        p: 1,
    },
})} />
```

---

## MUI v7 Grid

### New Grid Syntax

```typescript
import { Grid } from '@mui/material';

// ✅ MUI v7 - Use size prop
<Grid container spacing={2}>
    <Grid size={{ xs: 12, md: 6 }}>
        <Paper>Left</Paper>
    </Grid>
    <Grid size={{ xs: 12, md: 6 }}>
        <Paper>Right</Paper>
    </Grid>
</Grid>

// ❌ OLD - Don't use item/xs props
<Grid container spacing={2}>
    <Grid item xs={12} md={6}>  // WRONG
```

---

## Responsive Styles

### Breakpoint Pattern

```typescript
<Box sx={{
    p: { xs: 1, sm: 2, md: 3 },
    flexDirection: { xs: 'column', md: 'row' },
    display: { xs: 'none', sm: 'block' },
}} />
```

### Breakpoint Values

| Breakpoint | Pixels |
|------------|--------|
| xs | 0px+ |
| sm | 600px+ |
| md | 900px+ |
| lg | 1200px+ |
| xl | 1536px+ |

---

## Common Style Patterns

### Flexbox Layout

```typescript
const styles = {
    flexRow: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        gap: 2,
    },
    flexColumn: {
        display: 'flex',
        flexDirection: 'column',
        gap: 1,
    },
    spaceBetween: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
};
```

### Spacing

```typescript
// Padding
p: 2           // All sides
px: 2          // Horizontal (left + right)
py: 2          // Vertical (top + bottom)
pt: 2, pr: 1   // Specific sides

// Margin
m: 2, mx: 2, my: 2, mt: 2, mr: 1

// Units: 1 = 8px (theme.spacing(1))
p: 2  // = 16px
p: 0.5  // = 4px
```

### Positioning

```typescript
const styles = {
    relative: {
        position: 'relative',
    },
    absolute: {
        position: 'absolute',
        top: 0,
        right: 0,
    },
    sticky: {
        position: 'sticky',
        top: 0,
        zIndex: 1000,
    },
};
```

---

## Anti-Patterns

### ❌ NEVER Use

```typescript
// ❌ makeStyles (deprecated)
const useStyles = makeStyles((theme) => ({ ... }));

// ❌ styled() (use sx instead)
const StyledBox = styled(Box)({ ... });

// ❌ CSS files for components
import './MyComponent.css';
```

### ✅ ALWAYS Use

```typescript
// ✅ sx prop
<Box sx={{ p: 2 }} />

// ✅ Type-safe style objects
const styles: Record<string, SxProps<Theme>> = { ... };

// ✅ Theme values
sx={{ bgcolor: 'background.paper' }}
```

---

## Summary

**Styling Checklist:**
- ✅ Use `sx` prop for MUI styling
- ✅ Type-safe with `SxProps<Theme>`
- ✅ <100 lines: inline; >100 lines: separate file
- ✅ MUI v7 Grid: `size={{ xs: 12 }}`
- ✅ Theme values for colors and spacing
- ❌ No makeStyles or styled()
- ❌ No CSS files

**See Also:**
- [component-patterns.md](component-patterns.md) - Component structure
