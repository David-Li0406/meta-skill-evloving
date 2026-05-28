---
name: dark-theme-components
description: Dark theme UI component patterns with zinc/emerald color scheme. Use when creating or styling UI components that need to match the app's dark theme aesthetic. Includes design tokens, component patterns, and styling guidelines for consistent dark mode interfaces.
---

# Dark Theme UI Components

Reusable patterns and design tokens for building consistent dark theme interfaces with zinc backgrounds and emerald accents.

## Design System

See [design-tokens.md](references/design-tokens.md) for complete reference:

- **Colors:** Zinc backgrounds (950/900/800), emerald accents (500/400)
- **Border Radius:** lg (8px), xl (12px), 2xl (16px)
- **Spacing:** Consistent gaps and padding
- **Typography:** Sizes, weights, line heights
- **Shadows:** Elevation and accent glows
- **Transitions:** Smooth color and state changes

## Quick Reference

### Input Field
```tsx
<input className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors" />
```

### Primary Button
```tsx
<button className="bg-emerald-500 hover:bg-emerald-400 text-black font-bold px-6 py-3 rounded-xl transition-colors">
    Action
</button>
```

### Secondary Button
```tsx
<button className="bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-white font-medium px-6 py-3 rounded-xl transition-colors">
    Action
</button>
```

### Card
```tsx
<div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
    {/* Content */}
</div>
```

### Label
```tsx
<label className="text-sm font-medium text-zinc-300">
    Field Name
</label>
```

### Error State
```tsx
<div className="flex items-center gap-2 text-red-400 text-sm">
    <AlertCircle className="h-4 w-4" />
    Error message
</div>
```

## Color Palette

**Backgrounds:**
- `bg-zinc-950` - Primary (darkest)
- `bg-zinc-900` - Secondary
- `bg-zinc-800` - Tertiary/hover

**Borders:**
- `border-zinc-800` - Default
- `border-emerald-500` - Focus/active
- `border-red-500` - Error

**Text:**
- `text-white` - Primary
- `text-zinc-300` - Labels
- `text-zinc-400` - Descriptions
- `text-zinc-500` - Placeholders

**Accents:**
- `bg-emerald-500` - Primary action
- `bg-emerald-400` - Hover
- `text-emerald-500` - Accent text
- `bg-emerald-500/10` - Subtle background

## Common Patterns

### Form Field with Validation
```tsx
<div className="space-y-2">
    <label className="text-sm font-medium text-zinc-300">Name</label>
    <input
        className={cn(
            "w-full bg-zinc-950 border rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors",
            error ? "border-red-500" : "border-zinc-800"
        )}
    />
    {error && (
        <div className="flex items-center gap-2 text-red-400 text-sm">
            <AlertCircle className="h-4 w-4" />
            {error}
        </div>
    )}
</div>
```

### Icon Header
```tsx
<div className="flex items-center gap-3">
    <div className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-500">
        <Icon size={20} />
    </div>
    <div>
        <h2 className="text-2xl font-bold">Title</h2>
        <p className="text-zinc-400">Description</p>
    </div>
</div>
```

### Select Dropdown
```tsx
<select className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors">
    <option value="">Select...</option>
    <option value="1">Option 1</option>
</select>
```

### Disabled State
```tsx
<input
    disabled
    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-white outline-none opacity-50 cursor-not-allowed"
/>
```

## Best Practices

1. **Consistent spacing** - Use gap-3 (12px) for default spacing
2. **Focus states** - Always use emerald-500 for focus borders
3. **Transitions** - Add transition-colors for smooth state changes
4. **Disabled states** - Use opacity-50 and cursor-not-allowed
5. **Error states** - Red border + red text with icon
6. **Rounded corners** - xl (12px) for inputs/buttons, 2xl (16px) for cards
7. **Text hierarchy** - white for primary, zinc-300 for labels, zinc-400 for descriptions
8. **Hover states** - Lighten background (zinc-900 → zinc-800)
9. **Shadows** - Use sparingly, shadow-lg for elevation
10. **Icons** - Use lucide-react, size 20 for headers, 16 for inline

## Accessibility

- Use semantic HTML (label, input, button)
- Ensure sufficient color contrast
- Provide focus indicators (emerald-500 border)
- Include aria-labels where needed
- Support keyboard navigation
