---
name: design-system
description: design system with Tailwind v4.0, accessibility patterns, and project-specific UI/UX rules. Use for all KKOOKK frontend development.
---

# Design System

## When to Use

- Styling KKOOKK components with Tailwind CSS v4.0
- Implementing KKOOKK-specific layouts and interactions
- Adding accessibility (a11y) features
- Building mobile-optimized web UI

---

## Core Design Principles

1. **Tactile Certainty (물리적 확신)**: Mimic physical stamp sensation through visual feedback
2. **Paperless Freedom (지갑의 자유)**: Light, mobile-first, no-install PWA experience
3. **Human Bridge (연결의 가치)**: Warm digital connection between owners and customers

---

## UI Component Library

- **Base**: [shadcn/ui](https://ui.shadcn.com/) (Radix UI primitives + Tailwind)
- Install components as needed: `npx shadcn@latest add button dialog ...`
- Components are copied to `src/components/ui/` — customize freely to match KKOOKK design tokens
- **Do NOT** install other UI libraries (MUI, Chakra, Ant Design, etc.) without explicit approval

### When to Use shadcn/ui

| Use shadcn/ui | Build from scratch |
|---------------|-------------------|
| Dialog, Modal, Sheet | Simple presentational components |
| Dropdown, Select, Combobox | KKOOKK-specific stamp card UI |
| Toast, Alert | Custom animations with Framer Motion |
| Form inputs (with validation) | Layout components |

---

## Tailwind CSS v4.0 Rules

### ⚠️ Configuration Method

**All custom colors defined in `index.css` using `@theme`, NOT `tailwind.config.js`**

```css
@import "tailwindcss";

@theme {
  /* KKOOKK Orange Scale */
  --color-kkookk-orange-50: #fff7ed;
  --color-kkookk-orange-200: #fed7aa;
  --color-kkookk-orange-500: #ff4d00; /* Primary CTA */
  --color-kkookk-orange-600: #ea580c;
  --color-kkookk-orange-900: #7c2d12; /* Text on white */

  /* Status */
  --color-kkookk-red: #dc2626;
  --color-kkookk-amber: #f59e0b;

  /* Global */
  --color-kkookk-paper: #faf9f6;
  --color-kkookk-navy: #1a1c1e;

  /* Owner Persona */
  --color-kkookk-indigo: #2e58ff;
  --color-kkookk-steel: #64748b;

  /* Customer Persona */
  --color-kkookk-sand: #f5f5f0;
  --color-kkookk-yellow: #ffd600;

  /* Typography */
  --font-family-pretendard: "Pretendard Variable", -apple-system, sans-serif;
}
```

### Mobile-First Approach

- Start with mobile styles (default)
- Use responsive prefixes for larger screens: `md:`, `lg:`, `xl:`
- KKOOKK is mobile-web-first: optimize for mobile viewport

### Class Organization Order (Critical for Consistency)

Always write Tailwind classes in this order:

1. **Layout** (flex/grid, position, display)
2. **Spacing** (p/m/gap)
3. **Size** (w/h)
4. **Typography** (text-_, font-_)
5. **Colors** (bg-_, text-_, border-\*)
6. **Effects** (shadow, rounded, opacity)
7. **States** (hover:, focus:, active:, disabled:)

**Example:**

```tsx
<button className="flex items-center justify-center gap-2 h-14 px-6 text-base font-semibold bg-kkookk-orange-500 text-white rounded-2xl shadow-md hover:shadow-lg active:scale-95 transition-all">
```

### Conditional Classes

Use `clsx` or `tailwind-merge` for dynamic class combinations:

```tsx
import { twMerge } from 'tailwind-merge';

<div className={twMerge(
    "flex items-center p-4 rounded-xl transition-all",
    isActive ? "bg-kkookk-orange-500 text-white" : "bg-gray-100 text-gray-700",
    isDisabled && "opacity-50 cursor-not-allowed"
)}>
```

### Pattern Extraction Rule

- If a class combination appears **3+ times**, extract it into:
  - A reusable component, OR
  - A custom Tailwind utility in `@layer utilities`

**Example:**

```css
/* index.css */
@layer utilities {
  .btn-primary {
    @apply h-14 px-6 rounded-2xl bg-kkookk-orange-500 text-white font-semibold active:scale-95 transition-all;
  }
}
```

### Spacing Scale

- Use Tailwind's 4px-based scale: `p-2`, `p-4`, `gap-2`, `gap-6`, etc.
- **Avoid inline `style={}`** - always use Tailwind classes
- KKOOKK standard:
  - Safe margin: `px-4` (16px)
  - Section spacing: `gap-6` (24px)
  - Group spacing: `gap-2` (8px)

---

## Color System (KKOOKK-Specific)

### Color Usage Rules

- **Primary CTA**: `bg-kkookk-orange-500` (#FF4D00)
- **Text on white backgrounds**: `text-kkookk-orange-900` (#7C2D12) for readability
- **Owner UI**: Trust Indigo (#2E58FF) + Steel Gray (#64748B)
- **Customer UI**: Warm Sand (#F5F5F0) + Sunny Yellow (#FFD600) with Navy Black text
- **Global background**: Soft Paper White (#FAF9F6)
- **Body text**: Deep Navy Black (#1A1C1E)
- **Error**: `text-kkookk-red` (#DC2626)
- **Warning**: `text-kkookk-amber` (#F59E0B)

### WCAG Compliance

- **Minimum**: WCAG AAA (7:1 contrast ratio)
- Test under outdoor lighting (400+ lux)
- Navy Black on Paper White provides 7:1+ contrast

---

## Typography (Pretendard Required)

### Font Configuration

```tsx
<body className="font-pretendard">
```

### Type Scale

| Category     | Class       | Size | Weight          | Usage                  |
| ------------ | ----------- | ---- | --------------- | ---------------------- |
| Display Hero | `text-6xl`  | 60px | ExtraBold (800) | Stamp count emphasis   |
| Display Sub  | `text-4xl`  | 36px | ExtraBold (800) | Reward achievement     |
| Heading 1    | `text-2xl`  | 24px | SemiBold (600)  | Page title, store name |
| Heading 2    | `text-xl`   | 20px | SemiBold (600)  | Section titles         |
| Body 1       | `text-base` | 16px | Medium (500)    | Main body text         |
| Body 2       | `text-sm`   | 14px | Regular (400)   | Supporting text        |
| Caption      | `text-xs`   | 12px | Regular (400)   | Timestamps, micro-copy |

### Weight Guidelines

- **Display**: ExtraBold (800)
- **Owner UI**: SemiBold (600) for professional tone
- **Customer UI**: Medium (500) for body, Regular (400) for supporting text

---

## Component Specifications

### KKOOKK Stamp Card

```tsx
<div className="p-4 rounded-2xl shadow-lg bg-white">{/* Card content */}</div>
```

### Core CTA Button (Critical)

```tsx
<button className="h-14 px-6 rounded-2xl bg-kkookk-orange-500 text-white font-semibold active:scale-95 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
  스탬프 적립
</button>
```

**Key Requirements:**

- Height: `h-14` (56px) - prevents accidental taps
- Corner radius: `rounded-2xl` (16px)
- Active state: `active:scale-95` for tactile feedback
- Transition: `transition-all duration-200`
- **Anti-double-tap**: Disable for 300ms after click (see Interactions section)

### Button Variants

```tsx
// Primary CTA
<button className="h-14 bg-kkookk-orange-500 text-white active:scale-95 transition-all">

// Secondary (Owner)
<button className="h-14 bg-kkookk-indigo text-white active:scale-95 transition-all">

// Outline
<button className="h-14 border-2 border-kkookk-orange-500 text-kkookk-orange-600 active:scale-95 transition-all">

// Ghost
<button className="h-14 text-kkookk-orange-600 hover:bg-kkookk-orange-50 active:scale-95 transition-all">
```

---

## Interactions & Animations

### Stamp Impact (Signature Animation)

```tsx
import { motion } from "framer-motion";

<motion.div
  animate={{ scale: [0.8, 1.1, 1.0] }}
  transition={{ duration: 0.2, times: [0, 0.6, 1] }}
>
  {/* Stamp element */}
</motion.div>;
```

### Page Transitions

```tsx
// New page: Slide-in from right
<motion.div
  initial={{ x: '100%' }}
  animate={{ x: 0 }}
  exit={{ x: '100%' }}
  transition={{ duration: 0.3, ease: 'easeOut' }}
>
```

### Modal Animations

```tsx
// Slide-up from bottom
<motion.div
  initial={{ y: '100%' }}
  animate={{ y: 0 }}
  exit={{ y: '100%' }}
  transition={{ duration: 0.3, ease: 'easeOut' }}
  className="fixed inset-x-0 bottom-0 rounded-t-3xl bg-white"
>
```

### Toast Notifications

```tsx
<motion.div
  initial={{ y: 100, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
  exit={{ y: 100, opacity: 0 }}
  className="fixed bottom-20 left-4 right-4 p-4 bg-kkookk-navy text-white rounded-xl"
>
  {/* Auto-dismiss after 2 seconds */}
</motion.div>
```

### Polling Pulse (Approval Waiting)

```tsx
<motion.div
  animate={{
    scale: [1, 1.05, 1],
    opacity: [1, 0.8, 1]
  }}
  transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
  className="bg-kkookk-orange-500"
>
```

### Double-Tap Prevention (Mandatory for CTAs)

```tsx
const [isProcessing, setIsProcessing] = useState(false);

const handleClick = async () => {
  if (isProcessing) return;

  setIsProcessing(true);

  try {
    await performAction();
  } finally {
    setTimeout(() => setIsProcessing(false), 300);
  }
};

<button
  disabled={isProcessing}
  onClick={handleClick}
  className="h-14 disabled:opacity-50 disabled:cursor-not-allowed"
>
```

---

## State Matrix

| State    | Tailwind Classes                                                | Usage            |
| -------- | --------------------------------------------------------------- | ---------------- |
| Default  | `shadow-md rounded-2xl`                                         | Idle state       |
| Hover    | `hover:shadow-lg hover:brightness-105`                          | Desktop only     |
| Active   | `active:scale-95 active:brightness-90`                          | Touch feedback   |
| Loading  | `animate-pulse opacity-70`                                      | Data processing  |
| Error    | `border-kkookk-red text-kkookk-red`                             | Failed action    |
| Warning  | `bg-kkookk-amber/10 text-kkookk-amber`                          | Needs attention  |
| Disabled | `bg-kkookk-orange-50 text-kkookk-orange-200 cursor-not-allowed` | Unmet conditions |
| Success  | `bg-kkookk-orange-500 text-white`                               | Confirmed action |

---

## Accessibility (A11y)

### Minimum Requirements

| Requirement      | Implementation                                  |
| ---------------- | ----------------------------------------------- |
| Labels           | `<label htmlFor="id">`                          |
| Focus visibility | `focus:ring-4 focus:ring-kkookk-orange-500/50`  |
| ARIA attributes  | `aria-label`, `aria-modal`, `aria-labelledby`   |
| Touch targets    | Minimum 44x44px, KKOOKK standard: 56px (`h-14`) |
| Color contrast   | WCAG AAA (7:1+)                                 |

### Keyboard Navigation

- All interactive elements must be focusable
- Tab order must be logical (use `tabIndex` if needed)
- Escape key closes modals
- Enter/Space activates buttons

### Focus States

```tsx
<button className="focus:outline-none focus:ring-4 focus:ring-kkookk-orange-500/50 focus:ring-offset-2">
  Click me
</button>
```

### ARIA Examples

**Dialog/Modal:**

```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  className="fixed inset-0 z-50"
>
  <h2 id="dialog-title">Confirm Redemption</h2>
  {/* Modal content */}
</div>
```

**Form Labels:**

```tsx
<label htmlFor="store-name" className="text-sm font-medium">
  매장 이름
</label>
<input
  id="store-name"
  type="text"
  className="border-gray-300 focus:border-kkookk-orange-500 focus:ring-2 focus:ring-kkookk-orange-200"
/>
```

**Icon Buttons:**

```tsx
<button aria-label="닫기" className="...">
  <CloseIcon />
</button>
```

### High Contrast Mode (Optional)

```tsx
const prefersHighContrast = window.matchMedia(
  "(prefers-contrast: high)",
).matches;

// If true, switch to:
// - Background: #FFFFFF
// - Borders: 2px instead of 1px
// - Text: #000000
```

---

## Edge Cases

### Empty State

Provide actionable CTA, not just "No data":

```tsx
<div className="flex flex-col items-center gap-4 py-8 text-center text-slate-400">
  <EmptyIcon className="w-16 h-16" />
  <p className="text-base">아직 적립된 스탬프가 없어요</p>
  <button className="h-14 px-6 bg-kkookk-orange-500 text-white rounded-2xl">
    첫 도장을 찍으러 가볼까요?
  </button>
</div>
```

### Camera Permission Denied

```tsx
Toast.show({
  message: "카메라 권한이 필요해요. 설정에서 허용해주세요",
  type: "warning",
});
```

### Location Mismatch

```tsx
<div className="p-4 bg-kkookk-amber/10 border border-kkookk-amber text-kkookk-amber rounded-xl">
  ⚠️ 매장 위치와 현재 위치가 달라요
</div>
```

---

## Mobile Web Optimization

### Outdoor Visibility

- Test under 400+ lux (bright sunlight)
- Use high-contrast pairs: Navy Black on Paper White
- Avoid light gray text on white backgrounds

### Touch Optimization

- All interactive elements: minimum 48x48px tap area
- Main CTAs: 56px (`h-14`) for reliability
- Spacing between touch targets: minimum 8px

### Performance

- Prefer Tailwind classes over inline styles
- Extract repeated patterns (3+ occurrences rule)
- Use `transition-all` sparingly (only for interactive elements)

---

## UI Benchmarks & Philosophy

- **Owner (SaaS)**: Toss - Simple, clear hierarchy, professional
- **Customer (Wallet)**: Daangn - Local, friendly, warm
- **Common**: iOS - Smooth animations, rounded corners, depth

### KPI Goals

- **Recognition speed**: `text-6xl` for critical numbers
- **Error prevention**: High contrast + large touch targets (`h-14`)
- **Drop-off reduction**: Engaging animations (polling pulse, stamp impact)

---

## Instructions for Claude

1. **Always check `index.css` @theme section** for KKOOKK colors (NOT tailwind.config.js)
2. When asked to "Create X" or "Design Y", automatically apply these rules
3. Follow class organization order for every component
4. Use `twMerge` for conditional classes
5. Extract patterns after 3+ repetitions
6. Every CTA needs anti-double-tap protection (300ms disable)
7. All interactive elements need proper focus states
8. Mobile-first: design for 375px width, enhance for larger screens
9. If request violates accessibility or KKOOKK guidelines, suggest compliant alternative
