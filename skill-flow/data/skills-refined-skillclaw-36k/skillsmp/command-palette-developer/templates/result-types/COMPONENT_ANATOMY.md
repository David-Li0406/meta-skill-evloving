# Component Anatomy Reference

Visual breakdown of each result component showing dimensions, spacing, and layout.

## PersonResult (56px height)

```
┌────────────────────────────────────────────────────────────┐
│  [  JD  ]  John Doe                                        │ 56px
│    ●      Senior Engineer                                  │
│           john@company.com • Engineering • SF              │
└────────────────────────────────────────────────────────────┘
   └─┬─┘   └───────┬────────┘
    40px          flex-1

Layout:
- Container: Full width, 56px height, horizontal flex
- Avatar: 40px circle, left-aligned, 12px gap to content
- Status: 12px dot, absolute positioned bottom-right of avatar
- Content: Flex-1, vertical stack, truncate overflow
  - Name: 14px font-semibold, truncate
  - Role: 12px text-muted-foreground, truncate
  - Metadata: 11px text-muted-foreground/75, truncate, gap with •
```

**States:**
- Default: `hover:bg-muted/50`
- Selected: `bg-primary/10 text-primary`
- Status online: green dot
- Status away: amber dot
- Status offline: gray dot

**Initials fallback:**
- 2 letters max (first letter of first two words)
- Gradient background: `from-primary/20 to-primary/10`
- Centered in circle

---

## FileResult (56px height)

```
┌────────────────────────────────────────────────────────────────┐
│  [ 📄 ]  UserService.ts                              [ TS ]    │ 56px
│           /src/services/user/UserService.ts                    │
│           12.2 KB • 2 hours ago                                │
└────────────────────────────────────────────────────────────────┘
   └─┬─┘   └─────────┬──────────┘                       └─┬─┘
    40px            flex-1                                32px

Layout:
- Container: Full width, 56px height, horizontal flex
- Icon/Thumb: 40px square, rounded, 12px gap to content
- Content: Flex-1, vertical stack, truncate overflow
  - Name: 14px font-medium, truncate
  - Path: 12px text-muted-foreground, truncate with title tooltip
  - Metadata: 11px text-muted-foreground/75, gap with •
- Badge: 32px min-width, 20px height, uppercase, monospace

Icon mapping:
- Code files: FileCode (blue accent)
- Config files: FileJson (amber accent)
- Images: FileImage (green accent)
- Video: FileVideo (purple accent)
- Archives: FileArchive (gray accent)
- Text: FileText (slate accent)
```

**States:**
- Default: `hover:bg-muted/50`
- Selected: `bg-primary/10 text-primary`
- Thumbnail: Shows if provided, lazy loaded
- Icon fallback: Muted background with icon

**Size formatting:**
- < 1KB: "X B"
- < 1MB: "X.X KB"
- < 1GB: "X.X MB"
- >= 1GB: "X.X GB"

**Time formatting:**
- Uses date-fns `formatDistanceToNow`
- Examples: "2 hours ago", "3 days ago", "about 1 month ago"

---

## ActionResult (48-56px height)

```
┌──────────────────────────────────────────────────────────────────┐
│  [ 💾 ]  Save Document                    [ ⌘ ][ S ]            │ 48px+
│           Save current changes to file                           │
└──────────────────────────────────────────────────────────────────┘
   └─┬─┘   └─────────┬───────────┘           └────┬─────┘
    32px            flex-1                      variable

Layout:
- Container: Full width, min-height 48px, horizontal flex
- Icon: 32px container (8px padding), rounded, muted background
- Content: Flex-1, vertical stack
  - Name: 14px font-medium
  - Description: 12px text-muted-foreground, truncate
- Shortcut: Auto-width, horizontal flex of kbd elements
  - Each key: min-width 24px, height 24px, border, shadow

Shortcut rendering:
- Split by '+' character
- Platform detection (Mac vs Windows)
- Special symbols: ⌘ ⌥ ⇧ ^ ↑ ↓ ← → ↵ ⎋
```

**States:**
- Default: `hover:bg-muted/50`
- Selected: `bg-primary/10 text-primary`
- Disabled: `opacity-50 cursor-not-allowed`
- Destructive: `text-destructive hover:bg-destructive/5`
- Destructive + Selected: `bg-destructive/10 text-destructive`

**Keyboard shortcut format:**
| Input | Mac Output | Windows Output |
|-------|------------|----------------|
| `Cmd+S` | `⌘ + S` | `Ctrl + S` |
| `Cmd+Shift+P` | `⌘ + ⇧ + P` | `Ctrl + Shift + P` |
| `Alt+Up` | `⌥ + ↑` | `Alt + ↑` |

---

## CardResult (Variable height, ~240px typical)

```
┌──────────────────────────────────────┐
│                                   ⭐  │
│                                      │
│         [  Image Preview  ]          │ 160px
│                                      │
│                                      │
├──────────────────────────────────────┤
│  E-commerce Dashboard                │
│  Modern analytics dashboard for...  │ ~80px
│                                      │
│  [ React ] [ TypeScript ]            │
│                                      │
│  👤 Alex Johnson                      │
└──────────────────────────────────────┘

Layout:
- Container: Full width, auto height, vertical flex, rounded border
- Image: Full width, 160px height, cover fit
  - Star icon: Absolute top-right, 8px margin, backdrop blur
- Content: Padding 12px, vertical stack, 8px gap
  - Title: 14px font-semibold, line-clamp-1
  - Description: 12px text-muted-foreground, line-clamp-2
  - Tags: Horizontal flex-wrap, 6px gap, max 3 shown + count
  - Author: Border-top, 8px padding-top, horizontal flex, 8px gap
    - Avatar: 20px circle
    - Name: 12px text-muted-foreground, truncate
```

**States:**
- Default: `hover:bg-muted/30 border-border shadow-sm`
- Selected: `bg-primary/5 border-primary shadow-md`
- Image loading: Pulse animation on gray background
- Image error: "No preview" text on muted background
- Star filled: Amber color with fill

**Tag styling:**
- Pill shape: rounded-full
- Primary tags: `bg-primary/10 text-primary`
- Max visible: 3 tags + count (e.g., "+2")
- Small text: 11px font-medium

---

## NavigationResult (56px height)

```
┌────────────────────────────────────────────────────────────────────┐
│  [ 🏠 ]  Dashboard  ⏱                    App / Dashboard          │ 56px
│           /app/dashboard                                           │
│           Main                                                     │
└────────────────────────────────────────────────────────────────────┘
   └─┬─┘   └────┬─────┘                    └────────┬──────┘
    36px      flex-1                              responsive

Layout:
- Container: Full width, 56px height, horizontal flex
- Icon: 36px container, rounded, muted background or gradient
- Content: Flex-1, vertical stack, truncate overflow
  - Name row: Horizontal flex, gap 8px
    - Name: 14px font-medium, truncate
    - Recent icon: 12px clock, flex-shrink-0
    - External icon: 12px external link, flex-shrink-0
  - Path: 12px text-muted-foreground, truncate, monospace, title tooltip
  - Section: 11px text-muted-foreground/75
- Breadcrumbs: Hidden on mobile (sm:flex), horizontal flex, gap 4px

Breadcrumb generation:
1. Split path by '/'
2. Filter empty segments
3. Capitalize each segment
4. Replace - and _ with spaces
5. Show max 3 segments + "..." if more
```

**States:**
- Default: `hover:bg-muted/50`
- Selected: `bg-primary/10 text-primary`
- Recent: Clock icon shown
- External: External link icon shown
- No icon: First letter of path in gradient circle

**Path formatting:**
- Truncation: Shows start + "..." + end
- Max length: 60 characters
- Examples:
  - `/app/user-settings/profile` → kept as-is
  - `/app/very/long/path/to/settings` → `/app/.../settings`

**Breadcrumb display:**
| Path | Breadcrumbs |
|------|-------------|
| `/app/dashboard` | `App / Dashboard` |
| `/app/team/members` | `App / Team / Members` |
| `/very/long/path/here` | `Very / Long / ... / Here` |

---

## Responsive Breakpoints

All components adapt to screen size:

```
Mobile (< 640px):
- Hide breadcrumbs in NavigationResult
- Hide tertiary metadata
- Maintain touch-friendly 48px minimum height

Tablet (640px - 1024px):
- Show essential metadata
- Abbreviated breadcrumbs
- 56px height for better content display

Desktop (> 1024px):
- Full metadata display
- Complete breadcrumb trails
- Expanded spacing for readability
```

## Spacing System

Consistent spacing across all components:

```
Padding:
- Container: 12px horizontal, 8px vertical
- Content groups: 8px gap
- Metadata items: 8px gap with • separator

Gaps:
- Icon to content: 12px
- Metadata to content: 4px (mt-1)
- Between metadata items: 8px

Heights:
- Standard result: 56px (14rem)
- Compact result: 48px (12rem)
- Card result: Variable (~240px)
- Avatar/icon: 40px circle
- Small icon: 20px square
- Badge: 20px height
```

## Color Tokens

Using Tailwind v4 semantic tokens:

```css
/* Backgrounds */
--background        /* Base surface */
--muted            /* Secondary surface */
--primary          /* Accent/selection */
--destructive      /* Danger/delete */

/* Text */
--foreground       /* Primary text */
--muted-foreground /* Secondary text */
--primary          /* Accent text */
--destructive      /* Danger text */

/* Borders */
--border           /* Default borders */
--primary          /* Selected borders */

/* Status colors */
--green-500        /* Online */
--amber-500        /* Away */
--gray-400         /* Offline */
```

## Typography Scale

```
Primary text:   14px, font-semibold (600)
Secondary text: 12px, font-normal (400)
Tertiary text:  11px, font-normal (400)
Monospace:      12px, font-mono (shortcuts, paths)
```

## Shadow & Border

```
Default card:   shadow-sm (0 1px 2px)
Hover card:     shadow (0 1px 3px)
Selected card:  shadow-md (0 4px 6px)

Border width:   1px
Border radius:
  - Cards: 8px (rounded-lg)
  - Avatar: 9999px (rounded-full)
  - Icons: 6px (rounded)
  - Badges: 4px (rounded) or 9999px (rounded-full)
```

## Animation & Transitions

All components use consistent timing:

```css
transition-colors duration-150 ease-out

/* States */
hover: 150ms ease-out
selected: instant (no transition)
loading: pulse animation (2s infinite)
```

## Accessibility

Every component includes:

```tsx
role="option"                  // ARIA role
aria-selected={selected}       // Selection state
aria-disabled={disabled}       // Disabled state (ActionResult)
aria-label={description}       // Icon descriptions
title={fullText}              // Tooltip for truncated text
```

Focus indicators:
```css
focus:outline-none            /* Remove default */
focus-visible:ring-2          /* Keyboard focus only */
focus-visible:ring-primary    /* Brand color */
```

## Print Layout

For printing command palettes:

```css
@media print {
  .result-component {
    page-break-inside: avoid;  /* Keep component together */
    box-shadow: none;          /* Remove shadows */
    border: 1px solid #000;    /* Clear borders */
  }
}
```
