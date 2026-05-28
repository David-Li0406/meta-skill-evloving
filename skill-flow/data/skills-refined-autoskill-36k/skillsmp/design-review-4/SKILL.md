---
name: design-review
description: Evaluate a React component against the Design System and propose UX/UI improvements based on Figma best practices. Use when reviewing components for design compliance, checking UI consistency, or improving user experience.
allowed-tools: Read, Glob, Grep, Edit
---

# Design System Review

Evaluate React components against the Bilavnova Design System (`src/Design System.md`) and propose UX/UI improvements.

## Instructions

### Step 1: Read the Files

1. Read the target component file provided by the user
2. Read `src/Design System.md` for reference standards

### Step 2: Analyze for Violations

Check the component against these compliance categories:

#### Typography
- **VIOLATION:** `text-[10px]` or smaller (minimum is `text-xs`/12px)
- **VIOLATION:** Missing dark mode text pairs (e.g., `text-slate-900` without `dark:text-white`)
- **CHECK:** Heading hierarchy follows `text-2xl` > `text-xl` > `text-lg` > `text-sm`

#### Colors
- **VIOLATION:** Arbitrary colors when Design System colors exist (use `lavpop-blue`, `lavpop-green`, slate scale)
- **VIOLATION:** Missing dark mode pairs for `bg-*`, `border-*`, `text-*` classes
- **CHECK:** Semantic colors used correctly (emerald=success, red=error, amber=warning)

#### Spacing & Layout
- **VIOLATION:** Arbitrary z-index like `z-[1050]` (use semantic: `z-40`, `z-50`, `z-[60]`, `z-[70]`)
- **CHECK:** Consistent spacing scale (gap-1 through gap-8, p-1 through p-8)
- **CHECK:** Responsive breakpoints applied (xs:, sm:, md:, lg:, xl:)

#### Mobile & Touch
- **VIOLATION:** Touch targets under 44px (buttons, links, interactive elements need `min-h-[44px] min-w-[44px]`)
- **VIOLATION:** Hover-only interactions without tap fallback
- **CHECK:** Fixed bottom elements have `pb-24 lg:pb-6` clearance for bottom nav
- **CHECK:** Safe area classes used for notched devices (`safe-area-top`, `bottom-nav-safe`)

#### Component Patterns
- **CHECK:** Buttons follow Design System patterns (primary: gradient, secondary: slate bg, icon: p-2.5)
- **CHECK:** Cards use standard styling (`bg-white dark:bg-slate-800 rounded-xl border`)
- **CHECK:** KPI displays use correct component: `HeroKPICard`, `SecondaryKPICard`, or `KPICardGrid`
- **CHECK:** Modals implement: escape key close, click-outside close, body scroll lock, portal rendering

#### Accessibility
- **VIOLATION:** Interactive elements without `aria-label` or visible text
- **VIOLATION:** Missing focus states (`focus:ring-2 focus:ring-lavpop-blue`)
- **CHECK:** Proper heading structure (h1 > h2 > h3)
- **CHECK:** Color contrast meets WCAG AA (4.5:1 for text)

#### Animations
- **CHECK:** Standard transitions used (`transition-all duration-200`)
- **CHECK:** Button active states present (`active:scale-95` or `active:scale-[0.98]`)

### Step 3: Propose Design Enhancements

Beyond violations, suggest improvements based on Figma/UI best practices:

#### Visual Hierarchy
- Primary actions should be visually dominant (larger, bolder, colored)
- Secondary actions should be subdued (outline or ghost buttons)
- Suggest `font-bold`, `shadow-lg`, or size increases for CTAs

#### Whitespace & Breathing Room
- Cramped layouts need more padding (`p-4` → `p-6`)
- Add spacing between sections (`space-y-4`, `space-y-6`)
- Cards should have generous internal padding

#### Consistency
- Flag inconsistent border-radius within same component
- Flag inconsistent padding/margin patterns
- Suggest alignment improvements

#### Micro-interactions
- Suggest hover states for interactive cards (`hover:shadow-lg`, `hover:-translate-y-1`)
- Suggest transition effects where missing
- Recommend loading/skeleton states for async content

#### Component Composition
- Large JSX blocks (>100 lines) should be split into sub-components
- Repeated patterns should use shared components
- Complex conditionals should be extracted

#### Icon & Border Refinement
- Icons should be 16px, 20px, or 24px (standard sizes)
- Suggest soft shadows (`shadow-soft`) over harsh ones
- Recommend subtle borders for depth

### Step 4: Output Format

Present findings in this format:

```
## Design Review: [ComponentName].jsx

### Violations Found (N)

1. **[Category]** (line X): [Description]
   Fix: `[code change]`

2. **[Category]** (line Y): [Description]
   Fix: `[code change]`

### Design Enhancements (N)

1. **[Category]** (line X-Y): [Description]
   Suggestion: `[code change]`

---
Apply violations fixes? [Yes/No]
Apply enhancements? [Yes/No]
```

### Step 5: Apply Changes

If user approves:
1. Apply violation fixes first (these are required for compliance)
2. Apply enhancements if user accepts them (these are optional improvements)
3. Use the Edit tool to make changes
4. Summarize changes made

## Quick Reference

### Must-Have Dark Mode Pairs
| Light | Dark |
|-------|------|
| `bg-white` | `dark:bg-slate-800` or `dark:bg-slate-900` |
| `bg-slate-50` | `dark:bg-slate-800` |
| `bg-slate-100` | `dark:bg-slate-800` |
| `text-slate-900` | `dark:text-white` |
| `text-slate-700` | `dark:text-slate-300` |
| `text-slate-600` | `dark:text-slate-400` |
| `border-slate-200` | `dark:border-slate-700` |

### Standard Button Patterns
```jsx
// Primary
className="bg-gradient-to-r from-lavpop-blue to-blue-600 text-white font-bold rounded-xl px-6 py-3.5 shadow-lg active:scale-[0.98] transition-all"

// Secondary
className="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl px-4 py-2 transition-all"

// Icon
className="p-2.5 rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all active:scale-95"
```

### Touch Target Minimum
```jsx
className="min-h-[44px] min-w-[44px]"
// or use utility class
className="touch-target"
```

### Z-Index Scale
| Use Case | Value |
|----------|-------|
| Sidebar/Dropdown | `z-40` |
| Primary Modal | `z-50` |
| Child Modal | `z-[60]` |
| Alert | `z-[70]` |
| Toast | `z-[80]` |
