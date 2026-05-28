---
name: styling-ui
description: |
  Use when implementing frontend UI components, styling, or visual design for this todo application.
  Provides Tailwind CSS classes, Alpine.js patterns, and accessibility requirements.
  Invoke for: creating templates, styling components, adding transitions, accessibility compliance.
---

# UI Styling Guide

This skill provides UI design system guidance for the todo-me application. All frontend work must follow these specifications for consistency.

## Quick Reference

### Colors
- **Primary**: `indigo-600` (hover: `indigo-700`, light: `indigo-50`)
- **Success**: `green-600` / `green-100`
- **Warning**: `yellow-500` / `yellow-100`
- **Error**: `red-600` / `red-100`
- **Neutrals**: `gray-50` through `gray-900`

### Typography
- **Font**: System stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, ...`)
- **Default size**: `text-sm` (14px)
- **Buttons**: `text-sm font-semibold`
- **Headings**: `text-lg font-semibold` (page), `text-base font-medium` (section)

### Spacing
- **Base unit**: 4px (Tailwind scale)
- **Card padding**: `p-4`
- **Standard gap**: `gap-4`
- **Form spacing**: `space-y-4`

### Common Component Classes

**Primary Button**:
```html
<button class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors">
```

**Form Input**:
```html
<input class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
```

**Card**:
```html
<div class="bg-white shadow rounded-lg p-4 hover:shadow-md transition-shadow">
```

**Badge**:
```html
<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-indigo-100 text-indigo-700">
```

## Alpine.js Patterns

**Dropdown**:
```html
<div x-data="{ open: false }">
  <button @click="open = !open" @click.away="open = false">Toggle</button>
  <div x-show="open" x-transition class="...">Content</div>
</div>
```

**Modal**:
```html
<div x-data="{ open: false }">
  <div x-show="open" class="fixed inset-0 z-50">
    <div class="fixed inset-0 bg-gray-500/75" @click="open = false"></div>
    <div class="fixed inset-0 flex items-center justify-center p-4">
      <div x-show="open" x-transition class="bg-white rounded-lg shadow-xl max-w-lg w-full p-6">
        <!-- Content -->
      </div>
    </div>
  </div>
</div>
```

## Transitions
- **Dropdowns**: `duration-100 ease-out` (enter), `duration-75 ease-in` (leave)
- **Modals**: `duration-300 ease-out` (enter), `duration-200 ease-in` (leave)
- **Hover effects**: `transition-colors` or `transition-shadow`

## Accessibility Requirements
- Minimum 4.5:1 contrast ratio for text
- All interactive elements keyboard accessible
- `sr-only` labels for icon-only buttons
- `aria-labelledby` for modals
- Focus states must be visible (`focus:ring-2`)

## Additional Resources

For detailed specifications, read these files:

1. **Component Details**: Read `COMPONENTS.md` in this skill folder for:
   - Task card styling
   - Priority indicators
   - Project/tag chips
   - Form patterns

2. **Interaction Patterns**: Read `PATTERNS.md` in this skill folder for:
   - Toast notifications
   - Loading states
   - Empty states
   - Error handling UI

3. **Complete Reference**: For comprehensive specifications, read:
   - `docs/UI-DESIGN-SYSTEM.md` - Full 1300+ line design system
   - `docs/UI-PHASE-MODIFICATIONS.md` - Phase-specific UI requirements
