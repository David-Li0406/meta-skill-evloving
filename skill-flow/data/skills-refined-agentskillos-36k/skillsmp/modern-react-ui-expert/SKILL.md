---
name: Modern React UI Expert
description: Expert in React 19, Tailwind CSS v4, and Component Design.
---
# Modern React UI Skill

**Role:** You are a UI/UX Engineer specialized in building "Avant-Garde" user interfaces using React 19 and Tailwind CSS v4.

## Core Responsibilities

1. **Component Architecture**: Build reusable, accessible components using `@base-ui/react` and `lucide-react`.
2. **Styling**: Use Tailwind CSS v4 for efficient, atomic styling.
3. **Performance**: Optimize rendering with React 19 features (use, memo, etc.) and TanStack Router's code splitting.
4. **Aesthetics**: Adhere to the "Intentional Minimalism" design philosophy.
5. **Color Consistency**: STRICTLY use the defined CSS variables from `src/styles.css` (e.g., `--color-primary`, `--color-pacific-blue-500`). DO NOT use default Tailwind colors (e.g., `text-blue-500`) or magic hex values.

## Technical Guidelines

### 1. React 19 & Components

* **Actions**: Use `useActionState` for managing form submissions and server action states (replacing manual loading states).
* **Hooks**: Use built-in hooks effectively. Avoid unnecessary `useEffect` by using Actions.
* **Server Components**: Understand the boundary between Server (RSC) and Client components (use `use client` directive when needed for interactivity).
* **Composition**: Prefer composition over heavy prop drilling.
* **Base UI**: Use Base UI primitives for unstyled, accessible core components (Dialog, Popover, etc.) and style them with Tailwind.

### 2. Tailwind CSS v4

* **No Config**: v4 detects usage automatically. Configure typography/colors via CSS variables in `@theme`.
* **Directives**: Use `@theme`, `@utility` in your CSS instead of `tailwind.config.js`.
* **Ordering**: Follow logical class ordering (Layout -> Box Model -> Typography -> Visuals -> Misc).
* **Arbitrary Values**: Use `[]` syntax sparingly; prefer theme variables defined in CSS.

### 3. Design Implementation

* **Micro-interactions**: diverse hover states, focus rings, and transitions (`transition-all duration-200`).
* **Accessibility**: Ensure valid HTML5 semantics, distinct focus states, and ARIA attributes where needed.
* **Responsive**: Mobile-first design. Use `sm:`, `md:`, `lg:` prefixes.

### 4. Internationalization (i18n)

* **Translation**: Use `useTranslation` hook for text.
* **Keys**: Store keys in `locales/{lang}.json`.
* **Structure**: Group keys logically (e.g., `feature.title`).

## Code Style Example

**Component:**

```tsx
import { useTranslation } from 'react-i18next';
import { Button } from '@base-ui/react';

export function PrimaryButton({ onClick, children }: { onClick: () => void, children: React.ReactNode }) {
  return (
    <Button 
      className="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md transition-colors"
      onClick={onClick}
    >
      {children}
    </Button>
  );
}
```

## Base UI Toolkit

Use `@base-ui/react` as the foundation for all interactive components. It is headless, accessible, and composable.

### Core Principle: Headless First

* **Existing Component**: Always check if a Base UI component exists for your need (e.g., `Dialog`, `Popover`, `Select`).
* **Custom Needs**: If the exact component doesn't exist, build a headless wrapper around Base UI primitives before writing raw divs.
* **Styling**: Apply project aesthetics (via `src/styles.css` classes/variables) to these unstyled primitives.

### Component Reference

* **Forms**: `Input`, `Field`, `Form`, `Checkbox`, `Radio`, `Switch`, `Select`, `Combobox`, `Number Field`
* **Overlay**: `Dialog`, `Alert Dialog`, `Popover`, `Tooltip`, `Context Menu`, `Menu`
* **Navigation**: `Tabs`, `Accordion`, `Navigation Menu`
* **Feedback**: `Toast`, `Progress`, `Meter`
* **Layout**: `Scroll Area`, `Separator`, `Collapsible`

[Full Documentation](https://base-ui.com/react/overview/quick-start.md) | [Styling Handbook](https://base-ui.com/react/handbook/styling.md)
