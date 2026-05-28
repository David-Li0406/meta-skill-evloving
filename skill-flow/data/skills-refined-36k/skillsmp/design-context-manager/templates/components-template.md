# Component Guidelines

## Component Library

**Primary Library:** [e.g., shadcn/ui, Radix UI, Material UI]
**Location:** `[e.g., components/ui/]`
**Styling:** [e.g., Tailwind CSS, CSS Modules]

## Button Patterns

### Variants
| Variant | Usage | Style |
|---------|-------|-------|
| Primary | Main actions, CTAs | Solid background, high contrast |
| Secondary | Alternative actions | Outlined or muted background |
| Ghost | Tertiary actions | Transparent, text only |
| Destructive | Delete, remove | Red/danger color |
| Link | Navigation-style | Underline on hover |

### Sizes
| Size | Height | Padding | Font Size |
|------|--------|---------|-----------|
| sm | 32px | 12px 16px | 14px |
| default | 40px | 16px 20px | 14px |
| lg | 48px | 20px 24px | 16px |
| icon | 40px | 10px | - |

### States
- **Hover:** Slight lightening/darkening
- **Active/Pressed:** Further contrast change
- **Disabled:** 50% opacity, cursor not-allowed
- **Loading:** Spinner replaces content or inline

## Form Patterns

### Input Fields
- **Height:** 40px (default), 48px (large)
- **Padding:** 12px horizontal
- **Border:** 1px, neutral-300
- **Border radius:** 6px or 8px
- **Focus:** Ring with primary color

### Labels
- **Position:** Above input
- **Spacing:** 8px below label
- **Font:** 14px, medium weight
- **Required indicator:** Red asterisk after label

### Validation
- **Error state:** Red border, error icon
- **Error message:** Below input, 12px, red text
- **Success state:** Green check icon (optional)

### Field Spacing
- **Between fields:** 16px
- **Between sections:** 32px

## Card Patterns

### Default Card
- **Padding:** 24px
- **Border:** 1px neutral-200 or shadow-sm
- **Border radius:** 8px or 12px
- **Background:** Surface secondary

### Interactive Card
- **Hover:** Slight lift (shadow-md) or border highlight
- **Clickable:** cursor-pointer, focus ring

### Card Header
- **Padding bottom:** 16px
- **Border bottom:** Optional divider

## Modal / Dialog

### Structure
- **Overlay:** Black at 50% opacity
- **Container:** Centered, max-width 500px (default)
- **Padding:** 24px
- **Border radius:** 12px

### Header
- **Title:** h3 or h4
- **Close button:** Top right

### Footer
- **Button alignment:** Right
- **Button order:** Cancel (secondary), Confirm (primary)

## Navigation

### Top Navigation
- **Height:** 64px
- **Sticky:** Yes
- **Background:** Surface primary or blur backdrop

### Sidebar
- **Width:** 240px (expanded), 64px (collapsed)
- **Item height:** 40px
- **Item padding:** 8px 16px

### Breadcrumbs
- **Separator:** `/` or `>`
- **Current page:** Not a link, bold or different color

## Data Display

### Tables
- **Header:** Bold, background neutral-100
- **Row height:** 48px minimum
- **Cell padding:** 12px 16px
- **Borders:** Horizontal only, or full grid
- **Hover:** Row highlight

### Lists
- **Item spacing:** 8px or 12px
- **Bullet style:** Circle, disc, or none

### Badges / Tags
- **Padding:** 4px 8px
- **Border radius:** 4px or full
- **Font size:** 12px

## Loading States

### Skeleton
- **Background:** Animated gradient, neutral-200 to neutral-100
- **Border radius:** Match content shape

### Spinner
- **Size:** 16px (inline), 24px (default), 48px (page)
- **Color:** Primary or neutral

### Progress
- **Height:** 4px or 8px
- **Background:** Neutral-200
- **Fill:** Primary color

## Empty States

### Structure
- **Icon:** 48px, muted color
- **Title:** h4, centered
- **Description:** Body text, muted
- **Action:** Primary button

### Placement
- **Center vertically and horizontally in container**

---
_Source: [e.g., Analyzed from components/ui/ directory]_
_Last Updated: [Date]_
