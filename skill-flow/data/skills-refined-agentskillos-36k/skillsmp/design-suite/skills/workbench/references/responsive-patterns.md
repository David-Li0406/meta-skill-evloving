# Responsive Design Patterns

Mobile-first, content-driven responsive design for interface applications.

---

## Core Principles

### Mobile-First

Write base styles for mobile, then add complexity for larger screens:

```tsx
// Mobile-first: base is mobile, md: adds tablet/desktop
className="p-4 md:p-6 lg:p-8"

// NOT desktop-first (harder to maintain)
className="p-8 md:p-6 sm:p-4"
```

### Content-Driven Breakpoints

Don't design for devices. Design for content. When does the content break? That's your breakpoint.

Tailwind's defaults are sensible starting points:
- `sm:` 640px — Small tablets, large phones landscape
- `md:` 768px — Tablets
- `lg:` 1024px — Small laptops, tablets landscape
- `xl:` 1280px — Desktops
- `2xl:` 1536px — Large desktops

### Touch Considerations

Mobile interfaces need larger touch targets:

```tsx
// Minimum 44px touch targets
className="min-h-[44px] min-w-[44px]"

// Generous padding for tap areas
className="p-3"  // 12px — comfortable for fingers

// Interactive elements need breathing room
className="gap-2"  // Minimum gap between tappable items
```

---

## Sidebar Pattern

The most common dashboard layout. Sidebar visible on desktop, collapsible drawer on mobile.

### Implementation

```tsx
import { useState } from 'react';
import { Menu, X } from 'lucide-react';

function DashboardLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-canvas">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed inset-y-0 left-0 z-50 w-64 bg-canvas border-r border-edge
          transform transition-transform duration-200 ease-out
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
          md:translate-x-0 md:static md:z-auto
        `}
      >
        {/* Mobile close button */}
        <div className="flex items-center justify-between p-4 border-b border-edge md:hidden">
          <span className="text-lg font-semibold text-ink">Menu</span>
          <button
            onClick={() => setSidebarOpen(false)}
            className="p-2 -mr-2 rounded-md hover:bg-surface"
          >
            <X className="h-5 w-5 text-ink-muted" />
          </button>
        </div>

        {/* Logo - desktop */}
        <div className="hidden md:flex h-14 px-4 items-center border-b border-edge">
          <span className="text-lg font-semibold text-ink">Acme</span>
        </div>

        {/* Navigation */}
        <nav className="p-3 space-y-1">
          {/* Nav items */}
        </nav>
      </aside>

      {/* Main content area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile header */}
        <header className="flex items-center gap-4 h-14 px-4 border-b border-edge md:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 -ml-2 rounded-md hover:bg-surface"
          >
            <Menu className="h-5 w-5 text-ink" />
          </button>
          <span className="text-lg font-semibold text-ink">Acme</span>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto p-4 md:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
```

### Key Decisions

- **`fixed` on mobile, `static` on desktop:** Mobile sidebar overlays content; desktop sidebar is part of the flow.
- **`z-50` for sidebar, `z-40` for overlay:** Sidebar above overlay, both above content.
- **`min-w-0` on main area:** Prevents flex child from overflowing when content is wide.
- **`overflow-auto` on main:** Content scrolls independently from sidebar.

---

## Data Table Pattern

Tables become cards on mobile. Row data stacks vertically.

### Implementation

```tsx
interface Transaction {
  id: string;
  date: string;
  description: string;
  amount: string;
  status: 'completed' | 'pending' | 'failed';
}

function ResponsiveTable({ data }: { data: Transaction[] }) {
  return (
    <div className="bg-surface border border-edge rounded-card overflow-hidden">
      {/* Desktop: Traditional table */}
      <table className="hidden md:table w-full">
        <thead>
          <tr className="border-b border-edge bg-canvas">
            <th className="px-4 py-3 text-left text-xs font-medium text-ink-muted uppercase tracking-wide">
              ID
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-ink-muted uppercase tracking-wide">
              Date
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-ink-muted uppercase tracking-wide">
              Description
            </th>
            <th className="px-4 py-3 text-right text-xs font-medium text-ink-muted uppercase tracking-wide">
              Amount
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-ink-muted uppercase tracking-wide">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id} className="border-b border-edge-subtle last:border-0">
              <td className="px-4 py-3 font-mono text-xs text-ink-secondary">
                {row.id}
              </td>
              <td className="px-4 py-3 text-sm text-ink-secondary tabular-nums">
                {row.date}
              </td>
              <td className="px-4 py-3 text-sm text-ink">
                {row.description}
              </td>
              <td className="px-4 py-3 text-right font-mono text-sm text-ink tabular-nums">
                {row.amount}
              </td>
              <td className="px-4 py-3">
                <StatusBadge status={row.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Mobile: Card list */}
      <div className="md:hidden divide-y divide-edge-subtle">
        {data.map((row) => (
          <div key={row.id} className="p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs text-ink-secondary">{row.id}</span>
              <StatusBadge status={row.status} />
            </div>
            <div className="text-sm text-ink">{row.description}</div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-ink-muted">{row.date}</span>
              <span className="font-mono font-medium text-ink tabular-nums">{row.amount}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles = {
    completed: 'bg-green-50 text-green-700 border-green-200',
    pending: 'bg-amber-50 text-amber-700 border-amber-200',
    failed: 'bg-red-50 text-red-700 border-red-200',
  };

  return (
    <span className={`
      inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border
      ${styles[status as keyof typeof styles]}
    `}>
      {status}
    </span>
  );
}
```

### Key Decisions

- **`hidden md:table` / `md:hidden`:** Complete swap between table and cards at md breakpoint.
- **Important data first on mobile:** ID and status at top, amount prominent at bottom.
- **`divide-y` for mobile cards:** Simpler than managing border-b on each card.

---

## Metric Grid Pattern

Metrics stack on mobile, expand to grid on larger screens.

### Implementation

```tsx
function MetricGrid({ metrics }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric) => (
        <MetricCard key={metric.id} {...metric} />
      ))}
    </div>
  );
}

function MetricCard({ label, value, change, changeLabel }) {
  return (
    <div className="bg-surface border border-edge rounded-card p-4 sm:p-5">
      <div className="text-xs font-medium text-ink-muted uppercase tracking-wide mb-2 sm:mb-3">
        {label}
      </div>
      <div className="text-xl sm:text-2xl font-semibold text-ink tabular-nums mb-1 sm:mb-2">
        {value}
      </div>
      <div className="flex items-center gap-1.5 text-xs">
        <span className={change >= 0 ? 'text-green-600' : 'text-red-600'}>
          {change >= 0 ? '+' : ''}{change}%
        </span>
        <span className="text-ink-muted">{changeLabel}</span>
      </div>
    </div>
  );
}
```

### Breakpoint Logic

- **Mobile (base):** 1 column — cards stack full width
- **`sm:` (640px+):** 2 columns — pairs of metrics
- **`lg:` (1024px+):** 4 columns — all metrics in one row

---

## Form Layout Pattern

Forms need different treatment at different sizes.

### Implementation

```tsx
function ResponsiveForm() {
  return (
    <div className="bg-surface border border-edge rounded-card p-4 sm:p-6 max-w-2xl">
      <h2 className="text-lg font-semibold text-ink mb-4 sm:mb-6">
        Payment details
      </h2>

      <form className="space-y-4 sm:space-y-5">
        {/* Full-width on all sizes */}
        <FormField label="Recipient email" />

        {/* Side by side on larger screens */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <FormField label="Amount" />
          <FormField label="Currency" />
        </div>

        {/* Full-width textarea */}
        <FormField label="Description" multiline />

        {/* Actions: stack on mobile, inline on larger */}
        <div className="flex flex-col-reverse sm:flex-row gap-3 pt-2">
          <button className="flex-1 sm:flex-none px-4 py-2.5 sm:py-2 border border-edge rounded-control text-sm font-medium text-ink hover:bg-canvas transition-colors">
            Cancel
          </button>
          <button className="flex-1 sm:flex-none px-4 py-2.5 sm:py-2 bg-accent rounded-control text-sm font-medium text-white hover:bg-accent/90 transition-colors">
            Send payment
          </button>
        </div>
      </form>
    </div>
  );
}
```

### Key Decisions

- **`flex-col-reverse` for mobile buttons:** Primary action (Send) appears first visually on mobile.
- **`py-2.5` on mobile, `py-2` on desktop:** Larger touch targets on mobile.
- **`flex-none` on desktop buttons:** Prevents buttons from stretching in flex row.

---

## Navigation Pattern

Top nav on mobile, sidebar on desktop. Or: simplified nav on mobile, full nav on desktop.

### Tab Navigation

```tsx
function TabNav({ tabs, activeTab, onChange }) {
  return (
    <div className="border-b border-edge">
      {/* Mobile: Horizontal scroll */}
      <nav className="flex overflow-x-auto scrollbar-hide -mb-px">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`
              flex-shrink-0 px-4 py-3 text-sm font-medium border-b-2 transition-colors
              ${activeTab === tab.id
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-secondary hover:text-ink hover:border-edge'
              }
            `}
          >
            {tab.label}
          </button>
        ))}
      </nav>
    </div>
  );
}
```

### Bottom Navigation (Mobile-First)

```tsx
function MobileNav({ items, activeItem, onChange }) {
  return (
    <nav className="fixed bottom-0 inset-x-0 bg-surface border-t border-edge md:hidden">
      <div className="flex items-center justify-around">
        {items.map((item) => (
          <button
            key={item.id}
            onClick={() => onChange(item.id)}
            className={`
              flex flex-col items-center gap-1 py-2 px-3 min-w-[64px]
              ${activeItem === item.id
                ? 'text-accent'
                : 'text-ink-muted'
              }
            `}
          >
            <item.icon className="h-5 w-5" />
            <span className="text-xs font-medium">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}
```

---

## Modal/Dialog Pattern

Full-screen on mobile, centered dialog on desktop.

```tsx
function ResponsiveModal({ open, onClose, title, children }) {
  if (!open) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 z-40"
        onClick={onClose}
      />

      {/* Modal */}
      <div className={`
        fixed z-50
        inset-0 sm:inset-auto
        sm:top-1/2 sm:left-1/2 sm:-translate-x-1/2 sm:-translate-y-1/2
        sm:max-w-lg sm:w-full sm:max-h-[90vh]
        bg-surface sm:rounded-modal sm:border sm:border-edge
        flex flex-col
      `}>
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-edge">
          <h2 className="text-lg font-semibold text-ink">{title}</h2>
          <button
            onClick={onClose}
            className="p-2 -mr-2 rounded-md hover:bg-canvas"
          >
            <X className="h-5 w-5 text-ink-muted" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-4">
          {children}
        </div>
      </div>
    </>
  );
}
```

### Key Decisions

- **`inset-0` on mobile:** Full screen coverage
- **Centered positioning on `sm:`:** Traditional modal behavior
- **`max-h-[90vh]` on desktop:** Prevents modal from being taller than viewport
- **`overflow-auto` on content:** Long content scrolls within modal

---

## Hiding/Showing Content

Sometimes different content is appropriate at different sizes.

```tsx
// Show only on mobile
className="block md:hidden"

// Show only on desktop
className="hidden md:block"

// Different text at different sizes
<span className="md:hidden">Save</span>
<span className="hidden md:inline">Save changes</span>

// Icon-only on mobile, icon + text on desktop
<button className="flex items-center gap-2 px-3 py-2">
  <SaveIcon className="h-4 w-4" />
  <span className="hidden sm:inline">Save</span>
</button>
```

---

## Testing Responsive Designs

1. **Use browser DevTools:** Chrome/Firefox device mode
2. **Test actual devices:** Simulators miss touch behavior nuances
3. **Test orientations:** Portrait and landscape both matter
4. **Test intermediate sizes:** Not just the breakpoint boundaries
5. **Test content extremes:** Very long text, very short text, missing content

### Common Issues to Check

- Touch targets too small (< 44px)
- Horizontal scroll where it shouldn't be
- Text too small on mobile (< 14px for body)
- Clickable elements too close together
- Forms difficult to use on touch devices
- Modals that can't be dismissed on mobile
