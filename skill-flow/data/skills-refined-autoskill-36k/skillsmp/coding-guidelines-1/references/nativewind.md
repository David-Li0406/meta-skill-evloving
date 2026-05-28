# NativeWind Patterns

Principles and research guidance for projects using NativeWind (Tailwind CSS for React Native).

## Core Principles

### Tailwind in React Native
NativeWind enables Tailwind CSS utility classes in React Native via the `className` prop. Not all Tailwind utilities translate to React Native - research compatibility before using.

### Research Before Implementation
NativeWind has specific limitations compared to web Tailwind. Always verify:
- Use context7 to query NativeWind documentation
- Search for: supported utilities, platform differences, configuration

## Usage Patterns

### className Prop
Apply Tailwind classes via the `className` prop on React Native components. Research which components support className.

### Conditional Classes
Use array join pattern for conditional styling:

```tsx
className={[
  "base-classes",
  condition ? "true-classes" : "false-classes",
].join(" ")}
```

### State Variants
Research which state variants are supported:
- Some variants work differently than web (e.g., `active:` on Pressable)
- Some web variants may not be supported
- Platform-specific behavior may differ

## Key Differences from Web Tailwind

### Compatibility Research Required
Before using any Tailwind utility, verify NativeWind support:
- Flexbox utilities - research current support level
- Grid utilities - research if supported
- Pseudo-classes - research which ones work
- Responsive breakpoints - research mobile behavior

### Platform Differences
Styles may behave differently on iOS vs Android. Research:
- Shadow utilities (iOS vs Android elevation)
- Font rendering differences
- Touch feedback behavior

## Configuration

### Required Setup Files
NativeWind requires specific configuration. Research current setup:
- Tailwind configuration file
- TypeScript declarations
- CSS import in root layout
- Metro bundler configuration

## Research Checklist

Before implementing, query documentation for:
- [ ] Whether the Tailwind utility is supported in NativeWind
- [ ] How the utility translates to React Native styles
- [ ] Platform-specific behavior (iOS vs Android)
- [ ] State variant support (hover, active, focus, disabled)
- [ ] Current configuration requirements
- [ ] Any breaking changes in current NativeWind version
- [ ] Workarounds for unsupported utilities
