# Board Dashboard Layout Templates

## ⚠️ CRITICAL: Dark Theme Required

**All components MUST use the platform's dark theme.** The Board Dashboard is part of the existing MI Platform React app and must match visually.

### Required Colour Tokens

| Token | HSL Value | Usage |
|-------|-----------|-------|
| Canvas | `hsl(220, 20%, 7%)` | Page background |
| Surface 0 | `hsl(220, 18%, 11%)` | Card backgrounds |
| Surface 1 | `hsl(220, 16%, 15%)` | Elevated surfaces, borders, hover |
| Surface 2 | `hsl(220, 14%, 19%)` | Highest elevation (modals) |
| Text Primary | `hsl(220, 10%, 93%)` | Main content |
| Text Secondary | `hsl(220, 10%, 70%)` | Secondary content |
| Text Muted | `hsl(220, 10%, 50%)` | De-emphasised text |

### Semantic Colours

| Status | Colour | Hex | Icon |
|--------|--------|-----|------|
| Success | Emerald | #10B981 | ✓ |
| Warning | Amber | #F59E0B | ⚡ |
| Danger | Coral | #FF6B6B | ⚠ |
| Action | Blue | #3B82F6 | — |
| Info | Indigo | #6366F1 | ℹ️ |

---

## 5-Tab Information Architecture

```
TAB 1: EXECUTIVE SNAPSHOT (Home)
├── 6 KPI cards with status indicators
├── Top signal this week
├── Signal feed (recent 5)
└── "Last updated" timestamp

TAB 2: MARKET LANDSCAPE
├── Geographic map with opportunity heat
├── Priority ranking table
├── Status tracker (e.g., HMICFRS ratings)
└── Budget cycle indicator

TAB 3: COMPETITIVE INTELLIGENCE
├── Competitor summary cards
├── Recent activity feed (wins, awards)
├── Contract renewal calendar (18-month view)
├── Competitor activity feed

TAB 4: PIPELINE & REVENUE
├── Pipeline scorecard
├── Revenue forecast (3/6/12 month)
├── Deal risk summary
├── Conversion trends

TAB 5: STRATEGIC SIGNALS
├── Signal feed (chronological, filterable)
├── Trend summary
├── Policy/regulatory tracker
└── Recommended actions
```

---

## Tab 1: Executive Snapshot Layout (Dark Theme)

```
╔═══════════════════════════════════════════════════════════════════╗
║ Canvas background: hsl(220, 20%, 7%)                              ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║ Board Intelligence Dashboard    Last updated: 23/12/2025, 14:00   ║
║ (text-primary)                  (text-muted)                      ║
║                                                                   ║
║ ┌─────────────────────┐ ┌─────────────────────┐ ┌───────────────┐ ║
║ │ Surface 0           │ │ Surface 0           │ │ Surface 0     │ ║
║ │                     │ │                     │ │               │ ║
║ │ Pipeline Health 📊  │ │ Win Rate       📈  │ │ Intent    👁️  │ ║
║ │                     │ │                     │ │               │ ║
║ │ £1.2M               │ │ 48%                 │ │ 4 forces     │ ║
║ │ (text-primary)      │ │ (text-primary)      │ │              │ ║
║ │                     │ │                     │ │               │ ║
║ │ ↑ 12% ✓ ON TRACK   │ │ ↓ 2% ⚡ CAUTION    │ │ 🔴 Contact   │ ║
║ │ (emerald) (badge)   │ │ (amber) (badge)     │ │    this week │ ║
║ │                     │ │                     │ │               │ ║
║ │ (Target: £1.0M)     │ │ (Target: 50%)       │ │               │ ║
║ │ (text-muted)        │ │ (text-muted)        │ │               │ ║
║ └─────────────────────┘ └─────────────────────┘ └───────────────┘ ║
║                                                                   ║
║ ┌─────────────────────┐ ┌─────────────────────┐ ┌───────────────┐ ║
║ │ Engage Status   🏛️  │ │ Competitor Wins 🏆  │ │ Deals at     │ ║
║ │                     │ │                     │ │ Risk     🚨  │ ║
║ │ 3 forces           │ │ RSR: 2 wins         │ │               │ ║
║ │                     │ │ Reed: 1 win         │ │ 3 deals      │ ║
║ │ High-demand targets │ │                     │ │ £450k value  │ ║
║ │                     │ │ Coming soon         │ │               │ ║
║ │ (Phase 2)           │ │ (Phase 2)           │ │ ⚠ ACTION     │ ║
║ └─────────────────────┘ └─────────────────────┘ └───────────────┘ ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║ Surface 0 card                                                    ║
║                                                                   ║
║ 🔴 Top Signal This Week                                          ║
║                                                                   ║
║ HIRING SURGE                                          1d ago     ║
║ Thames Valley Police — High website activity                     ║
║ 23 visits this week. Intent signal active.                       ║
║                                                                   ║
║ → Review and reach out                          Source: Indeed   ║
║   (text-action)                                 (text-muted)     ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║ Signals This Week (5 new)                                        ║
║                                                                   ║
║ [Signal cards using Surface 0, stacked vertically]               ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## KPI Card Component (Dark Theme)

### Structure

```
┌─────────────────────────────────────────────────────────┐
│ Background: hsl(220, 18%, 11%) — Surface 0              │
│ Border: 1px solid hsl(220, 16%, 15%) — Surface 1        │
│ Border-radius: 8px                                       │
│ Padding: 16px                                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [LABEL]                                    [ICON]       │
│ (text-secondary, 14px)                     (24px)       │
│                                                         │
│ [PRIMARY VALUE]                                         │
│ (text-primary, IBM Plex Mono, 32px, font-semibold)     │
│                                                         │
│ [↑/↓ CHANGE]  [STATUS BADGE]                           │
│ (coloured)    (badge with bg + text + icon)            │
│                                                         │
│ ([CONTEXT])                                            │
│ (text-muted, 14px)                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Status Badge Variants

```tsx
// On Track (Success)
<span className="bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded text-xs font-medium">
  ✓ ON TRACK
</span>

// Caution (Warning)  
<span className="bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded text-xs font-medium">
  ⚡ CAUTION
</span>

// Action Required (Danger)
<span className="bg-red-500/10 text-red-400 px-2 py-0.5 rounded text-xs font-medium">
  ⚠ ACTION REQUIRED
</span>

// Pending (Neutral)
<span className="bg-slate-500/10 text-slate-400 px-2 py-0.5 rounded text-xs font-medium">
  ⏳ PENDING
</span>

// Phase indicator
<span className="bg-slate-500/10 text-slate-400 px-2 py-0.5 rounded text-xs font-medium">
  PHASE 2
</span>
```

---

## React Component: KPI Card

```tsx
interface KPICardProps {
  label: string
  value: string
  change?: string
  changeDirection?: 'up' | 'down' | 'flat'
  status: 'success' | 'warning' | 'danger' | 'neutral' | 'pending' | 'phase'
  statusLabel?: string
  context?: string
  icon?: React.ReactNode
  details?: string[]
}

const statusConfig = {
  success: { 
    bg: 'bg-emerald-500/10', 
    text: 'text-emerald-400', 
    defaultLabel: 'ON TRACK', 
    icon: '✓' 
  },
  warning: { 
    bg: 'bg-amber-500/10', 
    text: 'text-amber-400', 
    defaultLabel: 'CAUTION', 
    icon: '⚡' 
  },
  danger: { 
    bg: 'bg-red-500/10', 
    text: 'text-red-400', 
    defaultLabel: 'ACTION REQUIRED', 
    icon: '⚠' 
  },
  neutral: { 
    bg: 'bg-slate-500/10', 
    text: 'text-slate-400', 
    defaultLabel: '', 
    icon: '' 
  },
  pending: { 
    bg: 'bg-slate-500/10', 
    text: 'text-slate-400', 
    defaultLabel: 'PENDING', 
    icon: '⏳' 
  },
  phase: { 
    bg: 'bg-slate-500/10', 
    text: 'text-slate-400', 
    defaultLabel: 'PHASE 2', 
    icon: '' 
  },
}

export function KPICard({ 
  label, 
  value, 
  change, 
  changeDirection, 
  status, 
  statusLabel,
  context, 
  icon,
  details 
}: KPICardProps) {
  const config = statusConfig[status]
  const directionIcon = changeDirection === 'up' ? '↑' : changeDirection === 'down' ? '↓' : '→'
  const directionColor = changeDirection === 'up' 
    ? 'text-emerald-400' 
    : changeDirection === 'down' 
      ? 'text-amber-400' 
      : 'text-slate-400'
  
  return (
    <div className="bg-[hsl(220,18%,11%)] border border-[hsl(220,16%,15%)] rounded-lg p-4">
      {/* Header */}
      <div className="flex justify-between items-start mb-3">
        <span className="text-[hsl(220,10%,70%)] text-sm">{label}</span>
        {icon && <span className="text-xl opacity-70">{icon}</span>}
      </div>
      
      {/* Value */}
      <div className="text-[hsl(220,10%,93%)] font-mono text-3xl font-semibold mb-3">
        {value}
      </div>
      
      {/* Change + Status */}
      <div className="flex items-center gap-2 text-sm mb-2">
        {change && (
          <span className={directionColor}>
            {directionIcon} {change}
          </span>
        )}
        {(status !== 'neutral' || statusLabel) && (
          <span className={`${config.bg} ${config.text} px-2 py-0.5 rounded text-xs font-medium`}>
            {config.icon} {statusLabel || config.defaultLabel}
          </span>
        )}
      </div>
      
      {/* Context */}
      {context && (
        <div className="text-[hsl(220,10%,50%)] text-sm">{context}</div>
      )}
      
      {/* Optional details list */}
      {details && details.length > 0 && (
        <ul className="mt-3 text-[hsl(220,10%,50%)] text-sm space-y-1">
          {details.map((detail, i) => (
            <li key={i}>• {detail}</li>
          ))}
        </ul>
      )}
    </div>
  )
}
```

---

## React Component: Signal Card

```tsx
interface SignalCardProps {
  type: string
  headline: string
  detail?: string
  action: string
  timeAgo: string
  source: string
  severity: 'critical' | 'warning' | 'info'
}

const severityConfig = {
  critical: { dot: 'bg-red-500', badge: 'text-red-400' },
  warning: { dot: 'bg-amber-500', badge: 'text-amber-400' },
  info: { dot: 'bg-blue-500', badge: 'text-blue-400' },
}

export function SignalCard({ 
  type, 
  headline, 
  detail, 
  action, 
  timeAgo, 
  source,
  severity 
}: SignalCardProps) {
  const config = severityConfig[severity]
  
  return (
    <div className="bg-[hsl(220,18%,11%)] border border-[hsl(220,16%,15%)] rounded-lg p-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-2">
        <div className="flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full ${config.dot}`} />
          <span className={`text-sm font-medium uppercase tracking-wide ${config.badge}`}>
            {type}
          </span>
        </div>
        <span className="text-[hsl(220,10%,50%)] text-sm">{timeAgo}</span>
      </div>
      
      {/* Content */}
      <div className="text-[hsl(220,10%,93%)] font-medium mb-1">{headline}</div>
      {detail && (
        <div className="text-[hsl(220,10%,70%)] text-sm mb-3">{detail}</div>
      )}
      
      {/* Footer */}
      <div className="flex justify-between items-center">
        <span className="text-[#3B82F6] text-sm">→ {action}</span>
        <span className="text-[hsl(220,10%,50%)] text-sm">{source}</span>
      </div>
    </div>
  )
}
```

---

## Page Layout Component

```tsx
export function BoardDashboardPage() {
  return (
    <div className="min-h-screen bg-[hsl(220,20%,7%)]">
      {/* Header */}
      <div className="px-6 py-4 border-b border-[hsl(220,16%,15%)]">
        <div className="flex justify-between items-center">
          <h1 className="text-[hsl(220,10%,93%)] text-2xl font-semibold">
            Board Intelligence Dashboard
          </h1>
          <span className="text-[hsl(220,10%,50%)] text-sm">
            Last updated: 23/12/2025, 14:00
          </span>
        </div>
      </div>
      
      {/* KPI Grid */}
      <div className="px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <KPICard
            label="Pipeline Health"
            value="£1.2M"
            change="12% vs last month"
            changeDirection="up"
            status="success"
            context="(Target: £1.0M)"
            icon="📊"
          />
          <KPICard
            label="Win Rate"
            value="48%"
            change="2% vs Q3"
            changeDirection="down"
            status="warning"
            context="(Target: 50%)"
            icon="📈"
          />
          {/* ... more cards */}
        </div>
      </div>
      
      {/* Top Signal */}
      <div className="px-6 pb-6">
        <h2 className="flex items-center gap-2 text-[hsl(220,10%,93%)] text-lg font-semibold mb-4">
          <span className="w-2 h-2 rounded-full bg-red-500" />
          Top Signal This Week
        </h2>
        <SignalCard
          type="HIRING SURGE"
          headline="Thames Valley Police — High website activity"
          detail="23 visits this week. Intent signal active. No contact in 45 days."
          action="Review and reach out"
          timeAgo="1d ago"
          source="Indeed Intel"
          severity="critical"
        />
      </div>
      
      {/* Signal Feed */}
      <div className="px-6 pb-6">
        <h2 className="text-[hsl(220,10%,93%)] text-lg font-semibold mb-4">
          Signals This Week <span className="text-[hsl(220,10%,50%)]">(5 new)</span>
        </h2>
        <div className="space-y-3">
          {/* Signal cards */}
        </div>
      </div>
      
      {/* Footer */}
      <div className="px-6 py-4 border-t border-[hsl(220,16%,15%)] text-center">
        <span className="text-[hsl(220,10%,50%)] text-sm">
          Data sourced from Airtable and HubSpot. Refresh rate: 60 seconds.
        </span>
      </div>
    </div>
  )
}
```

---

## Mobile Responsive Breakpoints

### Desktop (1024px+)
- Full 3-column KPI grid
- All 6 KPIs visible
- Side-by-side panels

### Tablet (768-1023px)
- 2-column KPI grid
- All 6 KPIs visible
- Stacked panels

### Mobile (320-767px)
- 1-column layout
- Top 4 KPIs only (most critical)
- Collapsed signal feed with "View all"

```tsx
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

---

## Accessibility Requirements

| Requirement | Implementation |
|-------------|----------------|
| Contrast | 4.5:1 minimum for all text |
| Colour | Never colour alone — pair with icon/text |
| Focus | 2px ring using `--color-action` |
| Touch targets | Minimum 44×44px |
| Motion | Honour `prefers-reduced-motion` |

---

## Summary Checklist

Before implementing, verify:

- [ ] Using Canvas background `hsl(220, 20%, 7%)`
- [ ] Using Surface 0 for cards `hsl(220, 18%, 11%)`
- [ ] Using platform text colours (not white/black)
- [ ] Status badges use semi-transparent backgrounds (`bg-emerald-500/10`)
- [ ] IBM Plex Mono for numeric values
- [ ] All colours paired with icons or text labels
- [ ] Matches visual style of Focus page and Leads page
- [ ] No white or light grey backgrounds anywhere
