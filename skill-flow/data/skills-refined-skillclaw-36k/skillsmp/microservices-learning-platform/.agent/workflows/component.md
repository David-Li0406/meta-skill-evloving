---
description: How to create a new component following project standards
---

# Creating New Components

1. Create the component file in `src/components/[ComponentName].jsx`

2. Follow this structure:
```jsx
/**
 * ComponentName - Brief description
 * @param {Object} props - Component props
 */
export default function ComponentName({ ...props }) {
  return (
    // JSX here
  );
}
```

3. Use Tailwind classes following our design system:
   - Dark backgrounds: `bg-slate-900`, `bg-slate-800`
   - Accent colors: `bg-purple-500`, `text-purple-400`
   - Glassmorphism: `backdrop-blur-lg bg-white/5`
   - Rounded corners: `rounded-2xl`
   - Shadows: `shadow-lg shadow-purple-500/10`

4. Add animations for interactive elements:
   - Hover states with `transition-all duration-300`
   - Scale effects: `hover:scale-105`
   - Glow effects: `hover:shadow-purple-500/20`

5. Export from component and import where needed
