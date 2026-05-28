# Tailwind + MUI Integration

This guide covers the setup and patterns for using Tailwind CSS with Material UI in interface design projects.

---

## Philosophy

**Tailwind** handles layout, spacing, typography, and most styling through utility classes.

**Material UI** provides complex interactive components (data tables, date pickers, dialogs, autocomplete) that would be time-consuming to build from scratch.

**Both** are driven by a unified token system defined in CSS variables.

---

## Installation

```bash
# Core dependencies
npm install @mui/material @emotion/react @emotion/styled

# Optional: Data grid, date pickers
npm install @mui/x-data-grid @mui/x-date-pickers

# Tailwind (if not already installed)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

## Tailwind Configuration

Configure Tailwind to work alongside MUI:

```js
// tailwind.config.js
module.exports = {
  // Important: Increase specificity for Tailwind to override MUI
  important: '#root',

  // Disable preflight to avoid conflicts with MUI's baseline
  corePlugins: {
    preflight: false,
  },

  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],

  theme: {
    extend: {
      // Semantic color tokens
      colors: {
        canvas: 'var(--canvas)',
        surface: {
          DEFAULT: 'var(--surface)',
          elevated: 'var(--surface-elevated)',
          overlay: 'var(--surface-overlay)',
        },
        ink: {
          DEFAULT: 'var(--ink)',
          secondary: 'var(--ink-secondary)',
          muted: 'var(--ink-muted)',
        },
        edge: {
          DEFAULT: 'var(--edge)',
          subtle: 'var(--edge-subtle)',
        },
        accent: 'var(--accent)',
      },

      // Semantic spacing
      spacing: {
        'card': '1rem',
        'section': '1.5rem',
        'region': '2rem',
      },

      // Semantic border radius
      borderRadius: {
        'control': '0.375rem',
        'card': '0.5rem',
        'modal': '0.75rem',
      },

      // Custom shadows
      boxShadow: {
        'layered': `
          0 0 0 0.5px rgba(0, 0, 0, 0.05),
          0 1px 2px rgba(0, 0, 0, 0.04),
          0 2px 4px rgba(0, 0, 0, 0.03),
          0 4px 8px rgba(0, 0, 0, 0.02)
        `,
      },
    },
  },

  plugins: [],
}
```

---

## CSS Variables

Define your design tokens as CSS variables so both Tailwind and MUI can consume them:

```css
/* globals.css or styles.css */

/* Reset for MUI compatibility */
*, *::before, *::after {
  box-sizing: border-box;
}

:root {
  /* Canvas - the app background */
  --canvas: #fafafa;

  /* Surfaces - elevation levels */
  --surface: #ffffff;
  --surface-elevated: #ffffff;
  --surface-overlay: #ffffff;

  /* Ink - text hierarchy */
  --ink: #0f172a;
  --ink-secondary: #475569;
  --ink-muted: #94a3b8;

  /* Edge - borders */
  --edge: rgba(0, 0, 0, 0.08);
  --edge-subtle: rgba(0, 0, 0, 0.04);

  /* Accent - primary brand/action color */
  --accent: #2563eb;

  /* Semantic colors */
  --success: #16a34a;
  --warning: #d97706;
  --error: #dc2626;

  /* Radius tokens (for MUI sx props) */
  --radius-control: 0.375rem;
  --radius-card: 0.5rem;
  --radius-modal: 0.75rem;
}

.dark {
  --canvas: #0a0a0a;
  --surface: #141414;
  --surface-elevated: #1a1a1a;
  --surface-overlay: #1f1f1f;
  --ink: #fafafa;
  --ink-secondary: #a1a1aa;
  --ink-muted: #71717a;
  --edge: rgba(255, 255, 255, 0.08);
  --edge-subtle: rgba(255, 255, 255, 0.04);
  --accent: #3b82f6;
  --success: #22c55e;
  --warning: #f59e0b;
  --error: #ef4444;
}
```

---

## MUI Theme Bridge

Create an MUI theme that consumes your CSS variables:

```tsx
// theme.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: 'var(--accent)',
    },
    background: {
      default: 'var(--canvas)',
      paper: 'var(--surface)',
    },
    text: {
      primary: 'var(--ink)',
      secondary: 'var(--ink-secondary)',
    },
    divider: 'var(--edge)',
    error: {
      main: 'var(--error)',
    },
    success: {
      main: 'var(--success)',
    },
    warning: {
      main: 'var(--warning)',
    },
  },

  typography: {
    fontFamily: 'inherit', // Use Tailwind's font stack
  },

  shape: {
    borderRadius: 6, // Default radius in pixels
  },

  components: {
    // Disable default MUI elevation shadows
    MuiPaper: {
      defaultProps: {
        elevation: 0,
      },
    },

    // Button defaults
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },

    // Input defaults
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 'var(--radius-control)',
          '& .MuiOutlinedInput-notchedOutline': {
            borderColor: 'var(--edge)',
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: 'var(--edge)',
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: 'var(--accent)',
            borderWidth: '1px',
          },
        },
      },
    },
  },
});
```

---

## Provider Setup

Wrap your app with both providers:

```tsx
// app/layout.tsx or _app.tsx
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { theme } from './theme';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <div id="root">{children}</div>
        </ThemeProvider>
      </body>
    </html>
  );
}
```

Note: The `id="root"` on the wrapper div is required for Tailwind's `important: '#root'` configuration.

---

## Styling Patterns

### Pattern 1: Tailwind for Layout, MUI for Behavior

Use Tailwind for the container and layout, MUI for the interactive component:

```tsx
// Tailwind handles the card wrapper
<div className="bg-surface border border-edge rounded-card p-4">
  <h3 className="text-lg font-semibold text-ink mb-4">Select date range</h3>

  {/* MUI handles the date picker behavior */}
  <DatePicker
    sx={{
      '& .MuiOutlinedInput-root': {
        borderRadius: 'var(--radius-control)',
      },
    }}
  />
</div>
```

### Pattern 2: Tailwind Classes on MUI Components

Use Tailwind's `className` for simple styling:

```tsx
<Button
  variant="contained"
  className="bg-accent hover:bg-accent/90 px-4 py-2"
>
  Submit
</Button>
```

### Pattern 3: MUI sx for Complex Overrides

Use MUI's `sx` prop when you need to override internal MUI styles:

```tsx
<DataGrid
  sx={{
    '& .MuiDataGrid-cell': {
      borderColor: 'var(--edge-subtle)',
    },
    '& .MuiDataGrid-columnHeaders': {
      backgroundColor: 'var(--canvas)',
    },
  }}
/>
```

### Pattern 4: Shared Style Objects

Create reusable style objects for consistent MUI overrides:

```tsx
// styles/mui-overrides.ts
export const inputStyles = {
  '& .MuiOutlinedInput-root': {
    borderRadius: 'var(--radius-control)',
    '& fieldset': {
      borderColor: 'var(--edge)',
    },
    '&:hover fieldset': {
      borderColor: 'var(--edge)',
    },
    '&.Mui-focused fieldset': {
      borderColor: 'var(--accent)',
      borderWidth: '1px',
    },
  },
};

export const selectStyles = {
  borderRadius: 'var(--radius-control)',
  '& .MuiOutlinedInput-notchedOutline': {
    borderColor: 'var(--edge)',
  },
};

// Usage
<TextField sx={inputStyles} />
<Select sx={selectStyles} />
```

---

## Component Examples

### Styled TextField

```tsx
import { TextField } from '@mui/material';

function StyledInput({ label, ...props }) {
  return (
    <div>
      <label className="block text-sm font-medium text-ink mb-1.5">
        {label}
      </label>
      <TextField
        variant="outlined"
        size="small"
        fullWidth
        sx={{
          '& .MuiOutlinedInput-root': {
            borderRadius: 'var(--radius-control)',
            backgroundColor: 'var(--canvas)',
            '& fieldset': {
              borderColor: 'var(--edge)',
            },
            '&:hover fieldset': {
              borderColor: 'var(--edge)',
            },
            '&.Mui-focused fieldset': {
              borderColor: 'var(--accent)',
              borderWidth: '1px',
            },
          },
          '& .MuiOutlinedInput-input': {
            padding: '10px 12px',
            fontSize: '0.875rem',
          },
        }}
        {...props}
      />
    </div>
  );
}
```

### Styled Dialog

```tsx
import { Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';

function StyledDialog({ open, onClose, title, children, actions }) {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      PaperProps={{
        className: "bg-surface border border-edge rounded-modal",
        sx: {
          maxWidth: '480px',
          width: '100%',
        },
      }}
    >
      <DialogTitle className="text-lg font-semibold text-ink px-6 py-4 border-b border-edge">
        {title}
      </DialogTitle>
      <DialogContent className="px-6 py-4">
        {children}
      </DialogContent>
      <DialogActions className="px-6 py-4 border-t border-edge gap-3">
        {actions}
      </DialogActions>
    </Dialog>
  );
}
```

### Styled Autocomplete

```tsx
import { Autocomplete, TextField } from '@mui/material';

function StyledAutocomplete({ label, options, ...props }) {
  return (
    <div>
      <label className="block text-sm font-medium text-ink mb-1.5">
        {label}
      </label>
      <Autocomplete
        options={options}
        renderInput={(params) => (
          <TextField
            {...params}
            variant="outlined"
            size="small"
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 'var(--radius-control)',
                '& fieldset': {
                  borderColor: 'var(--edge)',
                },
                '&.Mui-focused fieldset': {
                  borderColor: 'var(--accent)',
                  borderWidth: '1px',
                },
              },
            }}
          />
        )}
        PaperComponent={({ children, ...props }) => (
          <div
            {...props}
            className="bg-surface-elevated border border-edge rounded-card shadow-lg mt-1"
          >
            {children}
          </div>
        )}
        {...props}
      />
    </div>
  );
}
```

---

## When to Use What

| Need | Use |
|------|-----|
| Layout (flex, grid, positioning) | Tailwind |
| Spacing (padding, margin, gap) | Tailwind |
| Typography (size, weight, color) | Tailwind |
| Simple buttons | Either (Tailwind preferred) |
| Form inputs | MUI with Tailwind styling |
| Data tables | MUI DataGrid |
| Date/time pickers | MUI DatePicker |
| Autocomplete/combobox | MUI Autocomplete |
| Dialogs/modals | MUI Dialog |
| Complex selects | MUI Select |
| Tooltips | MUI Tooltip |
| Tabs | Either |
| Cards | Tailwind |
| Navigation | Tailwind |

---

## Troubleshooting

### Tailwind classes not applying

Ensure `important: '#root'` is set in tailwind.config.js and your app has a wrapper with `id="root"`.

### MUI styles bleeding through

Use more specific selectors in sx props or increase Tailwind specificity with `!important` utilities (e.g., `!bg-surface`).

### Dark mode not switching

Ensure CSS variables are defined for both `:root` and `.dark` selectors, and that your dark mode toggle adds/removes the `dark` class on the html or body element.

### Fonts not matching

Set `fontFamily: 'inherit'` in MUI theme to use Tailwind's font stack.
