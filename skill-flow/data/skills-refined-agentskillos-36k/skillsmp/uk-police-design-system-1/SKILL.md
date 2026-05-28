---
name: uk-police-design-system
description: Build UI components, select colours, define typography, and implement visual elements for UK Police market intelligence dashboards. Apply when creating interfaces for the policing sector, implementing the "Technical Luxury" aesthetic, or needing domain-specific design guidance. This is the authoritative reference for visual design decisions including colour tokens, typography scale, spacing system, component architecture, and ADHD-specific features.
user-invocable: false
---

# UK Police Market Intelligence Design System

## Purpose

Comprehensive design system guidance for building market intelligence dashboards focused on the UK police recruitment sector. Combines domain-specific requirements with a "Technical Luxury" aesthetic philosophy.

## Related Skills

- `adhd-interface-design` — For cognitive patterns and focus modes
- `b2b-visualisation` — For chart and data display patterns
- `action-oriented-ux` — For interaction patterns
- `notification-system` — For alert severity colours

---

## Domain Context

### The UK Police Recruitment Landscape

The system serves Peel Solutions, providing managed investigator teams to UK police forces.

**Key Entities:**
- 43 territorial police forces in England & Wales
- Regional Organised Crime Units (ROCUs)
- National Crime Agency (NCA)
- British Transport Police and specialist forces

**Target Roles:**
- Police Investigators (PIP2 accredited)
- Intelligence Analysts
- Digital Forensic Examiners
- Major Crime Investigators
- Surveillance Officers

### Buying Signals in This Domain

| Signal Type | Meaning | Urgency |
|-------------|---------|---------|
| **Hiring Surge** | Force posting multiple investigator roles | High (24-48h window) |
| **HMICFRS Pressure** | "Requires Improvement" rating | Medium-High |
| **Role Cluster** | Multiple similar roles | Medium |
| **Leadership Change** | New Chief Constable, Head of Crime | Medium |
| **Contract Expiry** | Existing supplier contract ending | High |
| **Budget Cycle** | Q1/Q4 budget planning periods | Medium |

---

## Design Philosophy: Technical Luxury

"Technical Luxury" — precision engineering meets high-end elegance. Not decoration, but **rigour**.

**Design DNA:**
- Every pixel earns its place
- Speed as a feature (sub-100ms interactions)
- Determinism (predictable behaviour, consistent locations)
- Professional gravitas appropriate for policing context

### Why Dark Mode First

1. **Reduced eye strain** during extended analytical sessions
2. **Minimised visual glare** for ADHD users
3. **Professional aesthetic** appropriate for sensitive policing data

---

## Colour System

### Primary Palette (Dark Theme)

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-canvas` | `hsl(220, 20%, 7%)` | Main background |
| `--bg-surface-0` | `hsl(220, 18%, 11%)` | Card backgrounds |
| `--bg-surface-1` | `hsl(220, 16%, 15%)` | Elevated surfaces, hover |
| `--bg-surface-2` | `hsl(220, 14%, 19%)` | Highest elevation (modals) |

### Text Hierarchy

| Token | Value | Usage |
|-------|-------|-------|
| `--text-primary` | `hsl(220, 10%, 93%)` | Primary content |
| `--text-secondary` | `hsl(220, 10%, 70%)` | Secondary content |
| `--text-muted` | `hsl(220, 10%, 50%)` | De-emphasised text |

### Semantic Colours

**Use colour for only three jobs:**
1. **Status** — Success / Warning / Error / Neutral
2. **Priority** — What to look at first
3. **Interaction** — Links, primary buttons, selection

| Purpose | Colour | Hex |
|---------|--------|-----|
| **Action** | Blue | #3B82F6 |
| **Success** | Emerald | #10B981 |
| **Warning** | Amber | #F59E0B |
| **Danger** | Coral | #FF6B6B |
| **Info** | Indigo | #6366F1 |

### Critical Rules

1. **Never use pure black** (`#000000`) — causes eye strain
2. **Reserve red for "must act / error" only**
3. **Reduce saturation in dark mode**
4. **Use elevation via lightness** — not heavy shadows

---

## Typography

### Typeface Selection

| Role | Typeface | Rationale |
|------|----------|-----------|
| **UI & Body** | Inter | Designed for screens, tall x-height, highly legible |
| **Data & Metrics** | IBM Plex Mono | Monospace signals precision, tabular alignment |

### Type Scale

| Token | Size | Weight | Usage |
|-------|------|--------|-------|
| `--type-display` | 36px | 600 | Hero metrics, page titles |
| `--type-h1` | 30px | 600 | Section headers |
| `--type-h2` | 24px | 600 | Card headers |
| `--type-h3` | 20px | 500 | Subsection headers |
| `--type-body` | 16px | 400 | Body text |
| `--type-body-sm` | 14px | 400 | Secondary body, table cells |
| `--type-caption` | 12px | 500 | Labels, metadata |
| `--type-metric` | 24-40px | 600 | KPI values (tabular numerals) |

### Typographic Rules

- Use `font-variant-numeric: tabular-nums` for all data
- Labels: uppercase, 0.05em letter-spacing, muted colour
- Monospace for metrics and raw data values

---

## Spacing System

### Base Unit: 4px

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Tight padding, icon gaps |
| `--space-2` | 8px | Inline spacing |
| `--space-3` | 12px | Component internal padding |
| `--space-4` | 16px | Standard padding |
| `--space-5` | 24px | Section spacing |
| `--space-6` | 32px | Major section breaks |
| `--space-7` | 40px | Page-level spacing |
| `--space-8` | 48px | Large component spacing |

### Density Modes

| Mode | Multiplier | Use Case |
|------|------------|----------|
| **Comfortable** | 1.0 | Default |
| **Compact** | 0.875 | Power users |
| **Dense** | 0.75 | Maximum density |

---

## Component Architecture

### App Shell

```
┌─────────────────────────────────────────────────────────────────┐
│  [Logo]  Global Search (⌘K)              [Alerts] [User] [Theme]│
├────────┬────────────────────────────────────────────────────────┤
│  Nav   │                    Page Content                        │
│  Rail  │                                                        │
│ [Home] │  Page Header: Title · Timeframe · Freshness · CTA      │
│ [Leads]│                                                        │
│ [Intel]│  [ Main Content Area ]                                 │
│ [Force]│                                                        │
└────────┴────────────────────────────────────────────────────────┘
```

### Severity Levels

| Level | Colour | Icon | Usage |
|-------|--------|------|-------|
| **Critical** | Danger | ⚠️ | Requires immediate action |
| **Warning** | Warning | ⚡ | Attention needed soon |
| **Info** | Info | ℹ️ | Noteworthy but not urgent |
| **Success** | Success | ✓ | Positive development |

---

## ADHD-Specific Features

### The "Pin" System

Every card, profile, and chart has a **Pin icon**:
- Click pin → item flies into "pinned tray"
- Access without losing current place
- Prevents forgotten findings

### Quick Capture

Keyboard shortcut (`⌘K` then `n`) opens:
- Single input field
- Auto-files to inbox
- Returns to current view
- No context switch

### Focus Mode Toggle

When activated:
- Hides secondary metrics and charts
- Dims sidebar and navigation
- Expands central task list
- Mutes non-urgent notifications

### Card State Badges

```
[REVIEWING]  [ACTIONED]  [SNOOZED: Mon]  [FLAGGED]
```

Clear visual state prevents "did I already look at this?"

---

## Accessibility

- **WCAG 2.1 AA minimum** — 4.5:1 contrast
- **Never colour alone** — pair with icons, labels
- **Focus states** — visible ring using action colour
- **Touch targets** — minimum 44×44px
- **Reduced motion** — honour `prefers-reduced-motion`

---

## Empty, Loading, and Error States

### Empty State
- Illustration + friendly message
- Primary action (e.g., "Adjust Filters")
- Secondary action (e.g., "Refresh")

### Loading State
- Skeleton matching component shape
- Subtle pulse animation
- Maintain layout to prevent jank

### Error State
- Error icon with muted colour
- Brief explanation
- Retry action
- Link to support if persistent

---

## Summary: Design Principles

1. **Technical Luxury** — Precision and elegance, not decoration
2. **Dark Mode Primary** — Reduces strain, professional aesthetic
3. **Semantic Colour Only** — Status, Priority, Interaction; else neutral
4. **Progressive Disclosure** — Overview → Detail → Deep Dive
5. **Focus Mode** — One task at a time, everything else dimmed
6. **Keyboard First** — Every action accessible without mouse
7. **Domain Appropriate** — Language and patterns fit policing context
8. **ADHD Optimised** — Pin system, quick capture, clear states
9. **Trust Through Transparency** — Explain scores, show confidence
10. **Speed as Feature** — Sub-100ms interactions, instant feedback
