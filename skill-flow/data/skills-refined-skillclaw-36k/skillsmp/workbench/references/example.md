# Craft in Action

This shows how systematic precision translates to real decisions using Tailwind + MUI. Learn the thinking, not just the code. Your values will differ — the approach won't.

---

## The Subtle Layering Mindset

Before looking at any example, internalize this: **you should barely notice the system working.**

When you look at Stripe's dashboard, you don't think "nice borders." You just understand the structure. When you look at Airwallex, you don't think "good surface elevation." You just know what's above what. The craft is invisible — that's how you know it's working.

---

## Example: Stripe-Style Metric Card

Stripe's metric cards aren't just numbers in boxes. They provide context, comparison, and meaning.

### The Token Foundation

First, establish your tokens in `tailwind.config.js`:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        canvas: 'var(--canvas)',
        surface: {
          DEFAULT: 'var(--surface)',
          elevated: 'var(--surface-elevated)',
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
      borderRadius: {
        control: '0.375rem',
        card: '0.5rem',
      },
    },
  },
}
```

```css
/* globals.css */
:root {
  --canvas: #fafafa;
  --surface: #ffffff;
  --surface-elevated: #ffffff;
  --ink: #0f172a;
  --ink-secondary: #475569;
  --ink-muted: #94a3b8;
  --edge: rgba(0, 0, 0, 0.08);
  --edge-subtle: rgba(0, 0, 0, 0.04);
  --accent: #635bff; /* Stripe purple */
}
```

### The Component

```tsx
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string;
  change: number;
  changeLabel: string;
  context?: string;
}

function MetricCard({ label, value, change, changeLabel, context }: MetricCardProps) {
  const isPositive = change >= 0;

  return (
    <div className="bg-surface border border-edge rounded-card p-5">
      {/* Label */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-medium text-ink-muted uppercase tracking-wide">
          {label}
        </span>
        {context && (
          <span className="text-xs text-ink-muted">
            {context}
          </span>
        )}
      </div>

      {/* Value */}
      <div className="mb-2">
        <span className="text-2xl font-semibold tracking-tight text-ink tabular-nums">
          {value}
        </span>
      </div>

      {/* Change indicator */}
      <div className="flex items-center gap-1.5">
        {isPositive ? (
          <TrendingUp className="h-3.5 w-3.5 text-green-600" />
        ) : (
          <TrendingDown className="h-3.5 w-3.5 text-red-600" />
        )}
        <span className={`text-xs font-medium tabular-nums ${
          isPositive ? 'text-green-600' : 'text-red-600'
        }`}>
          {isPositive ? '+' : ''}{change}%
        </span>
        <span className="text-xs text-ink-muted">
          {changeLabel}
        </span>
      </div>
    </div>
  );
}

// Usage
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
  <MetricCard
    label="Gross volume"
    value="$142,384"
    change={12.5}
    changeLabel="vs last month"
    context="This month"
  />
  <MetricCard
    label="Successful payments"
    value="1,247"
    change={8.2}
    changeLabel="vs last month"
  />
  <MetricCard
    label="New customers"
    value="89"
    change={-3.1}
    changeLabel="vs last month"
  />
  <MetricCard
    label="Refund rate"
    value="0.8%"
    change={-0.2}
    changeLabel="vs last month"
  />
</div>
```

### Why These Decisions

**Why `p-5` not `p-4`?** Stripe cards breathe. The extra 4px creates comfortable spacing without feeling loose. Metric cards benefit from slightly more padding than action cards.

**Why uppercase label with `tracking-wide`?** Labels are metadata, not content. Uppercase with wide tracking creates visual distinction without using color — the hierarchy emerges from typographic treatment.

**Why `tabular-nums` on value and change?** Numbers in adjacent cards should align vertically when values change. Tabular figures ensure $142,384 and $89 use the same width per digit.

**Why subtle change indicators?** The change percentage tells the story. The icon reinforces it visually. Neither needs to scream — together they're clear without being loud.

---

## Example: Airwallex-Style Data Table

Airwallex handles dense financial data with clarity. Tables need to breathe even when packed with information.

### Using MUI DataGrid with Tailwind

```tsx
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Chip } from '@mui/material';

const columns: GridColDef[] = [
  {
    field: 'id',
    headerName: 'Transaction ID',
    width: 160,
    renderCell: (params) => (
      <span className="font-mono text-xs text-ink-secondary">
        {params.value}
      </span>
    ),
  },
  {
    field: 'date',
    headerName: 'Date',
    width: 120,
    renderCell: (params) => (
      <span className="text-sm text-ink-secondary tabular-nums">
        {params.value}
      </span>
    ),
  },
  {
    field: 'description',
    headerName: 'Description',
    flex: 1,
    minWidth: 200,
    renderCell: (params) => (
      <span className="text-sm text-ink truncate">
        {params.value}
      </span>
    ),
  },
  {
    field: 'amount',
    headerName: 'Amount',
    width: 120,
    align: 'right',
    headerAlign: 'right',
    renderCell: (params) => (
      <span className="font-mono text-sm text-ink tabular-nums">
        {params.value}
      </span>
    ),
  },
  {
    field: 'currency',
    headerName: 'Currency',
    width: 80,
    renderCell: (params) => (
      <span className="text-xs font-medium text-ink-muted uppercase">
        {params.value}
      </span>
    ),
  },
  {
    field: 'status',
    headerName: 'Status',
    width: 120,
    renderCell: (params) => {
      const statusStyles = {
        completed: 'bg-green-50 text-green-700 border-green-200',
        pending: 'bg-amber-50 text-amber-700 border-amber-200',
        failed: 'bg-red-50 text-red-700 border-red-200',
      };
      return (
        <span className={`
          inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border
          ${statusStyles[params.value as keyof typeof statusStyles]}
        `}>
          {params.value}
        </span>
      );
    },
  },
];

function TransactionTable({ rows }: { rows: any[] }) {
  return (
    <div className="bg-surface border border-edge rounded-card overflow-hidden">
      <DataGrid
        rows={rows}
        columns={columns}
        disableRowSelectionOnClick
        hideFooterSelectedRowCount
        className="border-none"
        sx={{
          // Remove default MUI styling conflicts
          '& .MuiDataGrid-root': {
            border: 'none',
          },
          // Header styling
          '& .MuiDataGrid-columnHeaders': {
            backgroundColor: 'var(--canvas)',
            borderBottom: '1px solid var(--edge)',
            minHeight: '44px !important',
            maxHeight: '44px !important',
          },
          '& .MuiDataGrid-columnHeaderTitle': {
            fontSize: '0.75rem',
            fontWeight: 500,
            color: 'var(--ink-muted)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
          },
          // Cell styling
          '& .MuiDataGrid-cell': {
            borderBottom: '1px solid var(--edge-subtle)',
            padding: '0 16px',
            display: 'flex',
            alignItems: 'center',
          },
          // Row hover
          '& .MuiDataGrid-row:hover': {
            backgroundColor: 'var(--surface)',
          },
          // Footer styling
          '& .MuiDataGrid-footerContainer': {
            borderTop: '1px solid var(--edge)',
            backgroundColor: 'var(--canvas)',
          },
          // Remove cell focus outline
          '& .MuiDataGrid-cell:focus': {
            outline: 'none',
          },
          '& .MuiDataGrid-cell:focus-within': {
            outline: 'none',
          },
        }}
      />
    </div>
  );
}
```

### Why These Decisions

**Why card wrapper with `overflow-hidden`?** The DataGrid needs containment. The border-radius on the card should clip the table edges cleanly.

**Why uppercase column headers?** Column headers are labels, not content. The uppercase treatment with muted color creates hierarchy — headers recede, data advances.

**Why `tabular-nums` on amounts and dates?** Financial data must align. $1,234.56 and $89.00 should have their decimal points line up.

**Why custom status badges instead of MUI Chip?** MUI Chips carry too much visual weight for inline status. Lighter badges with semantic colors communicate status without competing for attention.

**Why `var(--edge-subtle)` for row borders?** Row separation should be whisper-quiet. If you can clearly see every line, the table feels like a spreadsheet. Subtle borders create just enough definition.

---

## Example: Dashboard with Sidebar

Complete layout showing navigation context.

```tsx
import { Home, CreditCard, Users, Settings, ChevronDown } from 'lucide-react';

function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-canvas">
      {/* Sidebar */}
      <aside className="w-64 border-r border-edge bg-canvas flex flex-col">
        {/* Logo */}
        <div className="h-14 px-4 flex items-center border-b border-edge">
          <span className="text-lg font-semibold text-ink">Acme</span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-3 space-y-1">
          <NavItem icon={Home} label="Dashboard" active />
          <NavItem icon={CreditCard} label="Transactions" />
          <NavItem icon={Users} label="Customers" />
          <NavItem icon={Settings} label="Settings" />
        </nav>

        {/* User section */}
        <div className="p-3 border-t border-edge">
          <button className="w-full flex items-center gap-3 px-3 py-2 rounded-md hover:bg-surface transition-colors">
            <div className="h-8 w-8 rounded-full bg-accent/10 flex items-center justify-center">
              <span className="text-sm font-medium text-accent">JD</span>
            </div>
            <div className="flex-1 text-left">
              <div className="text-sm font-medium text-ink">John Doe</div>
              <div className="text-xs text-ink-muted">john@acme.com</div>
            </div>
            <ChevronDown className="h-4 w-4 text-ink-muted" />
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}

function NavItem({
  icon: Icon,
  label,
  active = false
}: {
  icon: any;
  label: string;
  active?: boolean;
}) {
  return (
    <a
      href="#"
      className={`
        flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors
        ${active
          ? 'bg-surface text-ink font-medium'
          : 'text-ink-secondary hover:bg-surface hover:text-ink'
        }
      `}
    >
      <Icon className="h-4 w-4" />
      {label}
    </a>
  );
}
```

### Why These Decisions

**Why same background for sidebar and content?** Fragmenting visual space with different backgrounds creates "sidebar world" and "content world." Same background, subtle border separation. The sidebar is part of the app, not a separate region.

**Why `h-14` for the logo area?** Matches the comfortable height of a top bar. Creates visual anchor at the top of the sidebar.

**Why `rounded-md` for nav items, not `rounded-lg`?** Nav items are small, functional elements. Smaller radius feels more precise. Save larger radius for cards and containers.

**Why user section at the bottom?** Navigation flows down in order of importance. User account is accessed occasionally — it belongs at the edge, not competing with primary navigation.

---

## Example: Form with MUI Components

```tsx
import { TextField, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';

function PaymentForm() {
  return (
    <div className="bg-surface border border-edge rounded-card p-6 max-w-md">
      <h2 className="text-lg font-semibold text-ink mb-6">Payment details</h2>

      <form className="space-y-4">
        {/* Amount */}
        <div>
          <label className="block text-sm font-medium text-ink mb-1.5">
            Amount
          </label>
          <div className="flex gap-2">
            <TextField
              variant="outlined"
              size="small"
              placeholder="0.00"
              className="flex-1"
              InputProps={{
                startAdornment: <span className="text-ink-muted mr-1">$</span>,
              }}
              sx={textFieldStyles}
            />
            <Select
              size="small"
              defaultValue="USD"
              className="w-24"
              sx={selectStyles}
            >
              <MenuItem value="USD">USD</MenuItem>
              <MenuItem value="EUR">EUR</MenuItem>
              <MenuItem value="GBP">GBP</MenuItem>
            </Select>
          </div>
        </div>

        {/* Recipient */}
        <div>
          <label className="block text-sm font-medium text-ink mb-1.5">
            Recipient email
          </label>
          <TextField
            variant="outlined"
            size="small"
            placeholder="email@example.com"
            fullWidth
            sx={textFieldStyles}
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-ink mb-1.5">
            Description
            <span className="text-ink-muted font-normal ml-1">(optional)</span>
          </label>
          <TextField
            variant="outlined"
            size="small"
            placeholder="What's this payment for?"
            fullWidth
            multiline
            rows={2}
            sx={textFieldStyles}
          />
        </div>

        {/* Actions */}
        <div className="flex gap-3 pt-2">
          <Button
            variant="outlined"
            className="flex-1 normal-case font-medium text-ink border-edge hover:bg-canvas"
            sx={buttonOutlinedStyles}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            className="flex-1 normal-case font-medium bg-accent hover:bg-accent/90 shadow-none"
            disableElevation
          >
            Send payment
          </Button>
        </div>
      </form>
    </div>
  );
}

// Shared MUI style overrides
const textFieldStyles = {
  '& .MuiOutlinedInput-root': {
    borderRadius: '0.375rem',
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
    padding: '8px 12px',
    fontSize: '0.875rem',
  },
};

const selectStyles = {
  borderRadius: '0.375rem',
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
  '& .MuiSelect-select': {
    padding: '8px 12px',
    fontSize: '0.875rem',
  },
};

const buttonOutlinedStyles = {
  borderColor: 'var(--edge)',
  '&:hover': {
    borderColor: 'var(--edge)',
    backgroundColor: 'var(--canvas)',
  },
};
```

### Why These Decisions

**Why custom labels instead of MUI's built-in?** MUI's floating labels add visual complexity. Simple top-aligned labels are clearer and more consistent with the minimal approach.

**Why `space-y-4` for form spacing?** 16px between form fields is comfortable without being loose. Dense enough to feel like a cohesive form, spacious enough to not feel cramped.

**Why `pt-2` before actions?** Slight extra breathing room separates the action buttons from the form fields. They're related but distinct — the visual separation reinforces this.

**Why `flex-1` on both buttons?** Equal width buttons when there are two options. Neither action dominates visually — the color difference (outlined vs contained) creates hierarchy.

---

## The Craft Check

Apply the squint test to your work:

1. Blur your eyes or step back
2. Can you still perceive hierarchy?
3. Is anything jumping out at you?
4. Can you tell where regions begin and end?

If hierarchy is visible and nothing is harsh — the subtle layering is working.

## Adapt to Context

Your product might need:
- Warmer hues (slight yellow/orange tint to grays)
- Cooler hues (blue-gray base)
- Different density (more or less padding)
- Light mode variations (principles apply, values change)

**The principle is constant:** barely different, still distinguishable. Consistent tokens, systematic spacing, quiet structure. The values adapt to context — the discipline doesn't.
