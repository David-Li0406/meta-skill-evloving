# SaaS Dashboard Template

A starting point for SaaS analytics dashboards. Adapt to your product — don't use as-is.

---

## When to Use

- Analytics/metrics dashboards
- Admin panels with data overview
- SaaS product main interfaces
- Internal tools with KPIs

---

## Example Data Notice

> **This template includes realistic example data** to make the first iteration viewable. Look for `// -- EXAMPLE DATA --` comments marking data you should replace with your own content.

## Structure

```
1. Sidebar — Navigation, user context
2. Top Bar — Page title, actions, search
3. Metrics Row — Key KPIs at a glance
4. Primary Content — Main data visualization
5. Secondary Content — Supporting tables/lists
```

---

## Direction Prompts

Before using this template, answer:

1. **Who uses this daily?** Their role shapes information hierarchy.
2. **What's the first thing they need to see?** That's your metrics row.
3. **What action do they take most?** That needs to be one click away.
4. **What's the data density?** Dense (trading terminal) vs spacious (consumer app)?

---

## Token Foundation

Establish tokens before building:

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
  --accent: #2563eb;
}
```

---

## Section Blueprints

### 1. Sidebar

```tsx
<aside className="w-64 border-r border-edge bg-canvas flex flex-col">
  {/* Logo */}
  <div className="h-14 px-4 flex items-center border-b border-edge">
    <span className="text-lg font-semibold text-ink">
      {/* -- EXAMPLE DATA -- */}
      Acme Analytics
      {/* -- END EXAMPLE DATA -- */}
    </span>
  </div>

  {/* Navigation */}
  <nav className="flex-1 p-3 space-y-1">
    <NavItem icon={Home} label="Dashboard" active />
    <NavItem icon={BarChart} label="Analytics" />
    <NavItem icon={Users} label="Customers" />
    <NavItem icon={Settings} label="Settings" />
  </nav>

  {/* User section */}
  <div className="p-3 border-t border-edge">
    <UserMenu />
  </div>
</aside>
```

**Customize:**
- Navigation items based on your product's information architecture
- Consider collapsible sidebar for more content space

### 2. Top Bar

```tsx
<header className="h-14 px-6 flex items-center justify-between border-b border-edge bg-surface">
  <div>
    <h1 className="text-lg font-semibold text-ink">
      {/* -- EXAMPLE DATA -- */}
      Overview
      {/* -- END EXAMPLE DATA -- */}
    </h1>
  </div>

  <div className="flex items-center gap-4">
    {/* Search */}
    <div className="relative">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-ink-muted" />
      <input
        type="text"
        placeholder="Search..."
        className="pl-9 pr-4 py-2 bg-canvas border border-edge rounded-control text-sm w-64 focus:outline-none focus:ring-2 focus:ring-accent/20"
      />
    </div>

    {/* Actions */}
    <Button variant="contained" size="small">
      {/* -- EXAMPLE DATA -- */}
      Export Report
      {/* -- END EXAMPLE DATA -- */}
    </Button>
  </div>
</header>
```

**Customize:**
- Page-specific actions on the right
- Breadcrumbs for deep navigation

### 3. Metrics Row

**Metrics Data:**
```tsx
// -- EXAMPLE DATA --
const metrics = [
  { label: 'Total Revenue', value: '$142,384', change: 12.5, changeLabel: 'vs last month' },
  { label: 'Active Users', value: '8,429', change: 8.2, changeLabel: 'vs last month' },
  { label: 'Conversion Rate', value: '3.24%', change: -0.8, changeLabel: 'vs last month' },
  { label: 'Avg. Order Value', value: '$64.50', change: 4.1, changeLabel: 'vs last month' },
];
// -- END EXAMPLE DATA --
```

```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
  {metrics.map((metric) => (
    <MetricCard
      key={metric.label}
      label={metric.label}
      value={metric.value}
      change={metric.change}
      changeLabel={metric.changeLabel}
    />
  ))}
</div>
```

**MetricCard Component:**

```tsx
function MetricCard({ label, value, change, changeLabel }) {
  const isPositive = change >= 0;

  return (
    <div className="bg-surface border border-edge rounded-card p-5">
      <div className="text-xs font-medium text-ink-muted uppercase tracking-wide mb-3">
        {label}
      </div>
      <div className="text-2xl font-semibold text-ink tabular-nums mb-2">
        {value}
      </div>
      <div className="flex items-center gap-1.5 text-xs">
        <span className={isPositive ? 'text-green-600' : 'text-red-600'}>
          {isPositive ? '+' : ''}{change}%
        </span>
        <span className="text-ink-muted">{changeLabel}</span>
      </div>
    </div>
  );
}
```

**Customize:**
- 3-4 metrics maximum — more dilutes focus
- Choose metrics that answer "how is the business doing?"

### 4. Primary Content — Data Table

**Table Data:**
```tsx
// -- EXAMPLE DATA --
const columns = [
  { field: 'id', headerName: 'Order ID', width: 100 },
  { field: 'customer', headerName: 'Customer', width: 180 },
  { field: 'amount', headerName: 'Amount', width: 120 },
  { field: 'status', headerName: 'Status', width: 120 },
  { field: 'date', headerName: 'Date', width: 140 },
];

const rows = [
  { id: '#4532', customer: 'Sarah Chen', amount: '$249.00', status: 'completed', date: 'Jan 15, 2024' },
  { id: '#4531', customer: 'Marcus Johnson', amount: '$89.00', status: 'completed', date: 'Jan 15, 2024' },
  { id: '#4530', customer: 'Emily Rodriguez', amount: '$312.50', status: 'pending', date: 'Jan 14, 2024' },
  { id: '#4529', customer: 'David Kim', amount: '$178.00', status: 'completed', date: 'Jan 14, 2024' },
  { id: '#4528', customer: 'Lisa Patel', amount: '$425.00', status: 'failed', date: 'Jan 13, 2024' },
];
// -- END EXAMPLE DATA --
```

```tsx
<div className="bg-surface border border-edge rounded-card overflow-hidden">
  <div className="px-5 py-4 border-b border-edge flex items-center justify-between">
    <h2 className="text-sm font-semibold text-ink">Recent Transactions</h2>
    <div className="flex items-center gap-2">
      {/* Filters, export, etc. */}
    </div>
  </div>

  <DataGrid
    rows={rows}
    columns={columns}
    sx={{
      border: 'none',
      '& .MuiDataGrid-columnHeaders': {
        backgroundColor: 'var(--canvas)',
        borderColor: 'var(--edge)',
      },
      '& .MuiDataGrid-cell': {
        borderColor: 'var(--edge-subtle)',
      },
    }}
  />
</div>
```

**Customize:**
- Column definitions based on your data model
- Row actions (edit, delete, view)
- Pagination strategy

### 5. Secondary Content — Charts or Lists

**Activity Data:**
```tsx
// -- EXAMPLE DATA --
const activities = [
  { id: 1, icon: ShoppingCart, text: 'New order from Sarah Chen', time: '2 min ago', color: 'text-green-600' },
  { id: 2, icon: UserPlus, text: 'Marcus Johnson upgraded to Pro', time: '15 min ago', color: 'text-blue-600' },
  { id: 3, icon: AlertCircle, text: 'Payment failed for Lisa Patel', time: '1 hour ago', color: 'text-red-600' },
  { id: 4, icon: TrendingUp, text: 'Revenue milestone: $100K this month', time: '3 hours ago', color: 'text-amber-600' },
];
// -- END EXAMPLE DATA --
```

```tsx
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
  {/* Chart */}
  <div className="bg-surface border border-edge rounded-card p-5">
    <h3 className="text-sm font-semibold text-ink mb-4">Revenue Over Time</h3>
    <div className="h-64">
      {/* Chart component */}
    </div>
  </div>

  {/* Activity feed */}
  <div className="bg-surface border border-edge rounded-card p-5">
    <h3 className="text-sm font-semibold text-ink mb-4">Recent Activity</h3>
    <div className="space-y-3">
      {activities.map(item => (
        <div key={item.id} className="flex items-center gap-3 py-2 border-b border-edge-subtle last:border-0">
          <div className={`w-8 h-8 rounded-full bg-canvas flex items-center justify-center ${item.color}`}>
            <item.icon className="w-4 h-4" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm text-ink truncate">{item.text}</p>
            <p className="text-xs text-ink-muted">{item.time}</p>
          </div>
        </div>
      ))}
    </div>
  </div>
</div>
```

---

## Layout Patterns

### Full Layout

```tsx
function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen bg-canvas">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar />
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

### Responsive Sidebar

```tsx
// Mobile: drawer overlay
// Desktop: fixed sidebar

const [sidebarOpen, setSidebarOpen] = useState(false);

<aside className={`
  fixed inset-y-0 left-0 z-50 w-64 bg-canvas border-r border-edge
  transform transition-transform duration-200
  ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
  md:translate-x-0 md:static
`}>
```

---

## Component Patterns

### Card Header with Actions

```tsx
<div className="px-5 py-4 border-b border-edge flex items-center justify-between">
  <h2 className="text-sm font-semibold text-ink">Title</h2>
  <div className="flex items-center gap-2">
    <Button variant="outlined" size="small">Export</Button>
    <Button variant="contained" size="small">Add New</Button>
  </div>
</div>
```

### Empty State

```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <div className="w-12 h-12 rounded-full bg-canvas flex items-center justify-center mb-4">
    <Icon className="h-6 w-6 text-ink-muted" />
  </div>
  <h3 className="text-sm font-medium text-ink mb-1">No data yet</h3>
  <p className="text-sm text-ink-muted mb-4">Get started by creating your first item.</p>
  <Button variant="contained" size="small">Create Item</Button>
</div>
```

### Status Badge

```tsx
const statusStyles = {
  active: 'bg-green-50 text-green-700 border-green-200',
  pending: 'bg-amber-50 text-amber-700 border-amber-200',
  inactive: 'bg-gray-50 text-gray-700 border-gray-200',
};

<span className={`
  inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border
  ${statusStyles[status]}
`}>
  {status}
</span>
```

---

## Depth Strategy

Choose ONE and commit:

**Borders-only (recommended for data-dense):**
```tsx
className="bg-surface border border-edge rounded-card"
```

**Subtle shadows (for lighter feel):**
```tsx
className="bg-surface rounded-card shadow-sm"
```

---

## Common Customizations

### For Financial/Analytics
- Denser spacing (`p-4` instead of `p-5`)
- More metrics (up to 6)
- Monospace for numbers throughout
- Darker/cooler palette

### For Admin Panels
- Larger touch targets
- More prominent actions
- Status indicators everywhere
- Warmer, friendlier palette

### For Internal Tools
- Maximum data density
- Keyboard shortcuts
- Bulk actions
- Minimal decoration

---

## Anti-Patterns to Avoid

- **Harsh borders** — Keep `border-edge` subtle (rgba, not gray-300)
- **Mixed depth** — Don't use shadows AND borders randomly
- **Crowded metrics** — 4 max, each with clear purpose
- **Generic icons** — Icons should clarify, not decorate
- **Inconsistent spacing** — Stick to your scale

---

## Next Steps

1. Answer the direction prompts
2. Set up your token foundation
3. Build sidebar → top bar → metrics → content
4. Run the squint test before showing
5. Offer to save patterns to `.workbench/system.md`

This template is a scaffold. The goal is systematic precision that emerges from your specific product.

---

## Customization Checklist

Replace the example data with your own content:

- [ ] **Product Name** — Your app name in the sidebar
- [ ] **Navigation** — Your product's actual pages and sections
- [ ] **Metrics** — Your key KPIs (3-4 that answer "how is the business doing?")
- [ ] **Table Data** — Your primary data model (users, orders, etc.)
- [ ] **Activity Feed** — Events relevant to your product
- [ ] **Colors** — Adjust tokens to match your brand
- [ ] **Page Title** — Context-appropriate titles for each view
