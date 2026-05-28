---
name: web-design-reviewer
description: Visual inspection and design quality assurance for LucidData web interface at localhost:3000. Use when reviewing responsive design, checking Tailwind CSS consistency, validating shadcn/ui component usage, testing accessibility (WCAG 2.1 AA), identifying layout issues, or verifying design system compliance. Automatically detects Next.js + Tailwind stack and captures screenshots for issue documentation.
license: MIT
compatibility: Designed for Claude Code with Playwright MCP or screenshot capability. Requires locally running dev server (npm run dev). Works with Next.js, Tailwind CSS, and shadcn/ui components.
metadata:
  author: LucidData Team
  version: "1.0"
  framework: Next.js 15 with Tailwind CSS 3.4.1
  ui_library: shadcn/ui with Radix UI primitives
  accessibility_target: WCAG 2.1 AA
allowed-tools: mcp__playwright__navigate mcp__playwright__screenshot mcp__playwright__click mcp__playwright__evaluate Read Edit Write
---

# Web Design Reviewer

Visual inspection and design quality assurance skill for the LucidData Next.js application.

## Overview

This skill provides systematic visual QA for the LucidData web interface, checking responsive design, Tailwind CSS consistency, shadcn/ui component usage, and WCAG 2.1 AA accessibility compliance. It uses automated screenshot capture and browser inspection to identify and fix design issues.

## When to Use This Skill

Activate this skill when you need to:

- **Review responsive design**: Test layouts across mobile, tablet, and desktop viewports
- **Check Tailwind consistency**: Verify consistent use of spacing, colors, typography
- **Validate components**: Ensure shadcn/ui components are used correctly
- **Test accessibility**: Check WCAG 2.1 AA compliance (contrast, focus states, ARIA)
- **Identify layout issues**: Find overflow, misalignment, z-index conflicts
- **Verify design system**: Ensure adherence to LucidData design patterns
- **Capture screenshots**: Document design issues or create visual records

## Four-Phase Workflow

### Phase 1: Information Gathering

**Objective**: Understand the current state and identify what to review

**Actions**:
1. Confirm dev server is running at `http://localhost:3000`
2. Identify the framework and styling approach (already known: Next.js 15 + Tailwind CSS 3.4.1)
3. Understand the pages to review (landing, auth, dashboard, vault, consent, audit)
4. Review the component structure (`components/ui/` for shadcn/ui, `components/*/` for features)

**Example**:
```
User: "Review the dashboard layout on mobile"
Assistant: Let me verify the dev server is running and navigate to the dashboard page.
```

### Phase 2: Visual Inspection

**Objective**: Capture screenshots and identify design issues

**Actions**:
1. Navigate to target pages using Playwright MCP
2. Capture screenshots at key viewports:
   - **Mobile**: 375×667 (iPhone SE), 390×844 (iPhone 12)
   - **Tablet**: 768×1024 (iPad), 1024×1366 (iPad Pro)
   - **Desktop**: 1920×1080 (HD), 2560×1440 (QHD)
3. Identify issues by category:
   - **Layout**: Overflow, misalignment, z-index conflicts, whitespace
   - **Responsive**: Breaking points, text truncation, image scaling, mobile menu
   - **Accessibility**: Color contrast, focus indicators, ARIA labels, keyboard navigation
   - **Consistency**: Inconsistent spacing, font sizes, color usage, button styles

**Example**:
```typescript
// Navigate to dashboard
await mcp__playwright__navigate({ url: 'http://localhost:3000/dashboard' });

// Set mobile viewport (iPhone 12)
await mcp__playwright__evaluate({
  script: 'window.resizeTo(390, 844)'
});

// Capture screenshot
await mcp__playwright__screenshot({
  path: 'dashboard-mobile-390.png',
  fullPage: true
});
```

### Phase 3: Issue Fixing

**Objective**: Apply fixes following LucidData patterns

**Actions**:
1. **Prioritize issues**:
   - P1 (critical): Broken functionality, inaccessible content
   - P2 (high): Poor UX, significant visual issues
   - P3 (low): Polish, minor inconsistencies

2. **Locate source files**:
   - Use browser DevTools inspection (if available)
   - Search for components in `components/` directory
   - Check global styles in `app/globals.css` and `tailwind.config.ts`

3. **Apply fixes** following LucidData patterns:
   - Use Tailwind utility classes (avoid inline styles)
   - Follow shadcn/ui component structure
   - Use `cn()` utility for className merging
   - Maintain responsive breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px)
   - Ensure proper Server/Client component usage

**Example fix for mobile overflow**:
```tsx
// Before (overflow on mobile)
<div className="flex gap-4">
  <Button>Action 1</Button>
  <Button>Action 2</Button>
  <Button>Action 3</Button>
</div>

// After (responsive stacking)
<div className="flex flex-col sm:flex-row gap-2 sm:gap-4">
  <Button className="w-full sm:w-auto">Action 1</Button>
  <Button className="w-full sm:w-auto">Action 2</Button>
  <Button className="w-full sm:w-auto">Action 3</Button>
</div>
```

### Phase 4: Re-verification

**Objective**: Verify fixes and test for regressions

**Actions**:
1. Capture after screenshots at same viewports
2. Compare before/after screenshots
3. Test for regressions in other areas
4. Iterate if needed (max 3 attempts before consulting user)

**Example**:
```
✅ Fixed: Mobile menu overflow at 375px
✅ Fixed: Button text truncation on tablet
⚠️  New issue: Footer alignment shifted on desktop
```

## LucidData Design System

### Color Palette

Defined in [tailwind.config.ts](../../../tailwind.config.ts):

```typescript
{
  colors: {
    primary: // Brand color for CTAs
    secondary: // Supporting actions
    destructive: // Delete/revoke actions
    muted: // Backgrounds, disabled states
    accent: // Highlights, badges
    // ... other colors
  }
}
```

**Usage**:
- Primary buttons: `bg-primary text-primary-foreground`
- Secondary buttons: `bg-secondary text-secondary-foreground`
- Destructive buttons: `bg-destructive text-destructive-foreground`
- Muted backgrounds: `bg-muted text-muted-foreground`

### Typography

**Font Family**: Default sans-serif stack

**Heading Sizes**:
- H1: `text-3xl md:text-4xl font-bold`
- H2: `text-2xl md:text-3xl font-semibold`
- H3: `text-xl md:text-2xl font-semibold`
- H4: `text-lg md:text-xl font-medium`

**Body Text**:
- Base: `text-base` (16px)
- Small: `text-sm` (14px)
- Extra small: `text-xs` (12px)

**Labels**: `text-sm font-medium text-muted-foreground`

### Spacing

Use Tailwind spacing scale consistently:
- Padding: `p-4`, `p-6`, `p-8`
- Margin: `m-4`, `m-6`, `m-8`
- Gap: `gap-2`, `gap-4`, `gap-6`
- Space between: `space-y-4`, `space-x-4`

**Common patterns**:
- Card padding: `p-6`
- Section spacing: `space-y-6` or `space-y-8`
- Button groups: `gap-2`
- Form fields: `space-y-4`

### Components (shadcn/ui)

All components located in [components/ui/](../../../components/ui/):

**Button** variants:
- `default`: Primary actions
- `destructive`: Delete, revoke
- `outline`: Secondary actions
- `secondary`: Less emphasis
- `ghost`: Minimal styling
- `link`: Text link style

**Button** sizes:
- `default`: Standard size
- `sm`: Compact
- `lg`: Large
- `icon`: Square icon button

**Dialog**: For modals (create, edit, view)
**Alert Dialog**: For confirmations (delete)
**Toast**: For notifications
**Badge**: For status indicators
**Table**: For data lists

### Icons

**Library**: Lucide React

**Standard sizes**:
- Small: `h-4 w-4`
- Medium: `h-5 w-5`
- Large: `h-6 w-6`

**Usage**: Always wrap in `<Icon className="h-4 w-4" />`

## Common Issues in LucidData

### 1. Mobile Menu Overflow

**Issue**: Horizontal overflow on mobile causing side scroll

**Fix**:
```tsx
// Add overflow-x-hidden to layout
<body className="overflow-x-hidden">
```

### 2. Form Layout on Small Screens

**Issue**: Form inputs too narrow or overlapping on mobile

**Fix**:
```tsx
// Use responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <div className="space-y-2">
    <Label>Field 1</Label>
    <Input />
  </div>
  <div className="space-y-2">
    <Label>Field 2</Label>
    <Input />
  </div>
</div>
```

### 3. Table Responsiveness

**Issue**: Tables overflow on mobile

**Fix**:
```tsx
// Wrap in scrollable container
<div className="overflow-x-auto">
  <Table>
    {/* table content */}
  </Table>
</div>

// Or use card layout on mobile
<div className="block md:hidden">
  {/* Card layout */}
</div>
<div className="hidden md:block">
  <Table />
</div>
```

### 4. Focus States

**Issue**: Missing focus indicators for keyboard navigation

**Fix**:
```tsx
// Add focus-visible ring (already in shadcn/ui components)
<Button className="focus-visible:ring-2 focus-visible:ring-offset-2">
  Click me
</Button>

// For custom interactive elements
<div
  tabIndex={0}
  className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
>
  Custom element
</div>
```

### 5. Color Contrast

**Issue**: Text not readable against background (WCAG fail)

**Check**: Use contrast ratio of at least 4.5:1 for normal text, 3:1 for large text

**Fix**:
```tsx
// Bad: Low contrast
<p className="text-gray-400 bg-gray-100">Text</p>

// Good: High contrast
<p className="text-gray-900 bg-gray-100">Text</p>
// Or use muted colors
<p className="text-muted-foreground">Text</p>
```

## Responsive Breakpoints

Tailwind breakpoints used in LucidData:

```typescript
{
  sm: '640px',  // Small tablets, large phones (landscape)
  md: '768px',  // Tablets
  lg: '1024px', // Small laptops, tablets (landscape)
  xl: '1280px', // Desktops
  '2xl': '1536px' // Large desktops
}
```

**Usage pattern** (mobile-first):
```tsx
// Mobile: stack vertically
// Desktop: horizontal layout
<div className="flex flex-col md:flex-row gap-4">
  {/* content */}
</div>

// Mobile: full width
// Desktop: fixed width
<div className="w-full md:w-96">
  {/* content */}
</div>

// Mobile: hidden
// Desktop: visible
<div className="hidden md:block">
  {/* desktop-only content */}
</div>
```

## Accessibility Checklist (WCAG 2.1 AA)

### Color Contrast
- [ ] Normal text (< 18px): 4.5:1 contrast ratio
- [ ] Large text (≥ 18px or 14px bold): 3:1 contrast ratio
- [ ] UI components and graphics: 3:1 contrast ratio

### Keyboard Navigation
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible and clear
- [ ] Logical tab order (matches visual order)
- [ ] No keyboard traps (can tab out of modals, dropdowns)

### Screen Reader
- [ ] Images have alt text (or empty alt="" if decorative)
- [ ] Form inputs have associated labels
- [ ] Buttons have descriptive text or aria-label
- [ ] ARIA landmarks used appropriately (main, nav, aside)
- [ ] Dialog modals have aria-labelledby and aria-describedby

### Responsive & Zoom
- [ ] Content reflows at 400% zoom without horizontal scroll
- [ ] Text can be resized up to 200% without loss of functionality
- [ ] Touch targets are at least 44×44px on mobile

## References

For more detailed information, see:

- [Tailwind Patterns](references/tailwind-patterns.md) - LucidData-specific Tailwind conventions
- [shadcn Components](references/shadcn-components.md) - Component catalog and customization
- [Accessibility Guide](references/accessibility.md) - WCAG 2.1 AA checklist and testing

## Viewport Test Sizes

Use the [viewport-sizes.json](assets/viewport-sizes.json) asset for standardized test viewports.

## Quick Reference

| Task | Viewport | Screenshot Command |
|------|----------|-------------------|
| Mobile review | 375×667 | Capture at iPhone SE size |
| Mobile review | 390×844 | Capture at iPhone 12 size |
| Tablet review | 768×1024 | Capture at iPad size |
| Desktop review | 1920×1080 | Capture at HD size |
| Wide review | 2560×1440 | Capture at QHD size |

| Issue Type | Priority | Common Fix |
|------------|----------|------------|
| Overflow | P1 | Add `overflow-x-hidden` or responsive layout |
| Poor contrast | P1 | Adjust text/background colors (4.5:1 ratio) |
| Missing focus | P1 | Add `focus-visible:ring-2` |
| Text truncation | P2 | Add `truncate` or responsive font sizes |
| Inconsistent spacing | P3 | Standardize to `gap-4`, `p-6`, etc. |

---

**Version**: 1.0
**Last Updated**: 2026-01-13
**Maintained by**: LucidData Team
