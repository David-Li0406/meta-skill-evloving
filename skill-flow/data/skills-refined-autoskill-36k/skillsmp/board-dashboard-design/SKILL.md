---
name: board-dashboard-design
description: 5-second rule patterns for executive board dashboards with 6-8 KPIs
---

# Board Dashboard Design Skill

## Purpose

Design dashboards that **drive decisions, not just display data**. Board members check weekly, not daily — every element must justify its presence.

## Related Skills

- **UK Police Design System Skill** — **MANDATORY** visual tokens and components
- ADHD Interface Design Skill — Cognitive load principles apply universally
- B2B Visualisation Skill — Data display patterns


## The Two Fundamental Rules

### Rule 1: The 5-Second Rule

A board member must answer two questions within 5 seconds of viewing the home screen:

1. **"Is the business healthy?"**
2. **"Where is the fire?"**

If they must click, scroll, or hover to answer these, the design has failed.

### Rule 2: The 6-8 Metric Limit

More than 8 KPIs on a home view creates decision paralysis. Every metric must map directly to a board decision. If you can't articulate what decision a metric supports, remove it.


## The Decision Hierarchy

Organise dashboards around decisions, not data categories:

```
Level 1: Strategic Position
├─ Are we winning/losing in core segments?
├─ Where are emerging opportunities?
└─ What are top threats?

Level 2: Market Intelligence  
├─ What are competitors doing?
├─ How are customer needs shifting?
└─ What regulatory changes are coming?

Level 3: Pipeline Health
├─ Which deals are at risk?
├─ What's the revenue impact?
└─ What actions would help?
```


## KPI Card Pattern (Dark Theme)

Every KPI card must use Surface 0 background with proper contrast:

```
┌─────────────────────────────────────────────┐
│ Pipeline Health                    📊       │  ← Label (muted text)
│ £1.2M                                       │  ← Value (primary text, IBM Plex Mono)
│ ↑ 12% vs last month    ✓ ON TRACK          │  ← Change + Status badge
│ (Target: £1.0M)                             │  ← Context (muted text)
└─────────────────────────────────────────────┘
Background: hsl(220, 18%, 11%) — Surface 0
Border: hsl(220, 16%, 15%) — Surface 1 (1px)
```

**Required elements:**
- Metric name (what it is) — `--text-secondary`
- Value (the number) — `--text-primary`, IBM Plex Mono, large
- Direction indicator (↑ ↓ →) — coloured by direction
- Comparison (vs target, vs last period)
- Status (badge with icon + text)
- Context (target, benchmark) — `--text-muted`


## Refresh Cadence Guidelines

| Data Type | Refresh | Rationale |
|-----------|---------|-----------|
| Pipeline/CRM | Real-time | Critical metric |
| Contract awards | Daily | Notices publish throughout day |
| Market signals | Daily | Sufficient for strategic use |
| Competitor activity | Weekly | Strategic, not operational |
| Policy/regulatory | As released | Manual curation |

**For board meetings:** Freeze data at Sunday 23:59 before Monday meetings so all members see identical numbers.


## React/Next.js Implementation Patterns

### Component Structure

The Board Dashboard is a **page within the existing React app**, not a separate application:

```
app/
├── board/
│   └── page.tsx           # /board route — Tab navigation
├── components/
│   ├── board/
│   │   ├── kpi-card.tsx           # KPI display component
│   │   ├── status-badge.tsx       # RAG status indicator
│   │   ├── signal-feed.tsx        # Signal list
│   │   ├── metric-trend.tsx       # Sparkline
│   │   └── executive-snapshot.tsx # Tab 1 layout
│   └── ui/                        # Shared shadcn components
```

### Using Existing Design Tokens

```tsx
// Use CSS variables from globals.css — already defined in the app
<div className="bg-[hsl(220,18%,11%)] border border-[hsl(220,16%,15%)] rounded-lg p-4">
  <span className="text-[hsl(220,10%,70%)] text-sm uppercase tracking-wider">
    Pipeline Health
  </span>
  <span className="text-[hsl(220,10%,93%)] font-mono text-3xl font-semibold">
    £1.2M
  </span>
</div>

// Or use the existing Tailwind config if tokens are mapped
<div className="bg-surface-0 border-surface-1 text-primary">...</div>
```

### KPI Card Component

```tsx
interface KPICardProps {
  label: string
  value: string
  change: string
  changeDirection: 'up' | 'down' | 'flat'
  status: 'success' | 'warning' | 'danger' | 'neutral' | 'pending'
  context: string
  icon?: React.ReactNode
}

export function KPICard({ label, value, change, changeDirection, status, context, icon }: KPICardProps) {
  const statusConfig = {
    success: { bg: 'bg-emerald-500/10', text: 'text-emerald-400', label: 'ON TRACK', icon: '✓' },
    warning: { bg: 'bg-amber-500/10', text: 'text-amber-400', label: 'CAUTION', icon: '⚡' },
    danger: { bg: 'bg-red-500/10', text: 'text-red-400', label: 'AT RISK', icon: '⚠' },
    neutral: { bg: 'bg-slate-500/10', text: 'text-slate-400', label: '', icon: '' },
    pending: { bg: 'bg-slate-500/10', text: 'text-slate-400', label: 'PENDING', icon: '⏳' },
  }
  
  const config = statusConfig[status]
  const directionIcon = changeDirection === 'up' ? '↑' : changeDirection === 'down' ? '↓' : '→'
  
  return (
    <div className="bg-[hsl(220,18%,11%)] border border-[hsl(220,16%,15%)] rounded-lg p-4">
      <div className="flex justify-between items-start mb-2">
        <span className="text-[hsl(220,10%,70%)] text-sm">{label}</span>
        {icon && <span className="text-xl">{icon}</span>}
      </div>
      <div className="text-[hsl(220,10%,93%)] font-mono text-3xl font-semibold mb-2">
        {value}
      </div>
      <div className="flex items-center gap-2 text-sm">
        <span className={changeDirection === 'up' ? 'text-emerald-400' : changeDirection === 'down' ? 'text-amber-400' : 'text-slate-400'}>
          {directionIcon} {change}
        </span>
        {status !== 'neutral' && (
          <span className={`${config.bg} ${config.text} px-2 py-0.5 rounded text-xs font-medium`}>
            {config.icon} {config.label}
          </span>
        )}
      </div>
      <div className="text-[hsl(220,10%,50%)] text-sm mt-1">{context}</div>
    </div>
  )
}
```

### Chart Libraries

| Library | Use For |
|---------|---------|
| Recharts | 80% of charts (Line, Bar, Area) |
| Tremor | Pre-styled dashboard components |

Configure dark theme for all charts:
```tsx
<ResponsiveContainer>
  <LineChart data={data}>
    <XAxis stroke="hsl(220, 10%, 50%)" />
    <YAxis stroke="hsl(220, 10%, 50%)" />
    <Line stroke="#3B82F6" strokeWidth={2} />
  </LineChart>
</ResponsiveContainer>
```

### Performance

- Aggregate data server-side via API routes
- Use React Query / SWR for caching
- Target: home page loads in <3 seconds


## Cognitive Load Audit

Before launch, verify:

| Check | Target |
|-------|--------|
| Uses platform dark theme? | Yes — mandatory |
| KPIs on home screen | 3-6 |
| Time to answer "Are we on track?" | <30 seconds |
| Most important metric largest? | Yes |
| Colour used only for status? | Yes |
| Every viz maps to a decision? | Yes |
| Works without training? | Yes |
| All metrics have context? | Yes |
| Matches rest of MI Platform visually? | Yes |

