---
name: mui
description: Use this skill when working with Material-UI v7 components, styling with the sx prop, customizing themes, or implementing responsive design.
---

# MUI v7 Patterns

## Purpose

Material-UI v7 (released March 2025) patterns for component usage, styling with the sx prop, theme integration, and responsive design.

**Note**: MUI v7 breaking changes from v6:
- Deep imports no longer work - use package exports field.
- `onBackdropClick` removed from Modal - use `onClose` instead.
- All components now use standardized `slots` and `slotProps` pattern.
- CSS layers support via `enableCssLayer` config (works with Tailwind v4).

## When to Use This Skill

- Styling components with MUI sx prop.
- Using MUI components (Box, Grid, Paper, Typography, etc.).
- Theme customization and usage.
- Responsive design with MUI breakpoints.
- MUI-specific utilities and hooks.

## Quick Start

### Basic MUI Component

```typescript
import { Box, Typography, Button, Paper } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';

const styles: Record<string, SxProps<Theme>> = {
  container: {
    p: 2,
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
  },
  header: {
    mb: 3,
    fontSize: '1.5rem',
    fontWeight: 600,
  },
};

function MyComponent() {
  return (
    <Paper sx={styles.container}>
      <Typography sx={styles.header}>
        Title
      </Typography>
      <Button variant="contained">
        Action
      </Button>
    </Paper>
  );
}
```

### Styling Patterns

#### Inline Styles (< 100 lines)

For components with simple styling, define styles at the top:

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
    color: 'primary.main',
  },
  button: {
    mt: 'auto',
    alignSelf: 'flex-end',
  },
};

function Component() {
  return (
    <Box sx={componentStyles.container}>
      <Typography sx={componentStyles.header}>Header</Typography>
      <Button sx={componentStyles.button}>Action</Button>
    </Box>
  );
}
```

#### Separate Styles File (>= 100 lines)

For complex components, create a separate style file:

```typescript
// UserProfile.styles.ts
import type { SxProps, Theme } from '@mui/material';

export const userProfileStyles: Record<string, SxProps<Theme>> = {
  // Define styles here
};
```