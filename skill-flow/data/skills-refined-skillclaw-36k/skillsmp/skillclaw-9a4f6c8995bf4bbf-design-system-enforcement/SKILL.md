---
name: design-system-enforcement
description: Use this skill to enforce consistent, accessible, and beautiful UI across projects using shadcn/ui or shadcn-svelte with Tailwind CSS v4. All agents must validate against the design system before generating any UI code.
---

# Design System Enforcement

**Purpose:** Enforce consistent, accessible, and beautiful UI across projects using shadcn/ui or shadcn-svelte with Tailwind CSS v4.

**Activation Triggers:**

- Creating new components or pages
- Generating UI elements
- Styling React or Svelte components
- Setting up project design system
- Before ANY UI code generation
- Component library initialization
- Design system validation needed

## Core Design Principles (MANDATORY)

### 1. Typography: 4 Sizes, 2 Weights ONLY

**STRICTLY ENFORCED:**

| Size   | Tailwind Class | Pixels | Use Case               |
|--------|----------------|--------|------------------------|
| Size 1 | `text-3xl`     | 32px   | Large headings         |
| Size 2 | `text-2xl`     | 24px   | Subheadings            |
| Size 3 | `text-base`    | 16px   | Body text              |
| Size 4 | `text-sm`      | 14px   | Small text/labels      |

**Weights:**
- ✅ `font-semibold` - Headings and emphasis
- ✅ `font-normal` - Body text and UI

**❌ FORBIDDEN:**
- Additional font sizes or weights beyond specified

### 2. 8pt Grid System

**STRICTLY ENFORCED:** All spacing MUST be divisible by 8 or 4.

**Allowed Tailwind Spacing:**
```
p-1 (4px)   | m-1 (4px)   | gap-1 (4px)
p-2 (8px)   | m-2 (8px)   | gap-2 (8px)
p-3 (12px)  | m-3 (12px)  | gap-3 (12px)
p-4 (16px)  | m-4 (16px)  | gap-4 (16px)
p-5 (20px)  | m-5 (20px)  | gap-5 (20px)
p-6 (24px)  | m-6 (24px)  | gap-6 (24px)
p-8 (32px)  | m-8 (32px)  | gap-8 (32px)
```

**❌ FORBIDDEN:** Custom spacing values not divisible by 4 or 8.

### 3. 60/30/10 Color Rule

**STRICTLY ENFORCED:**

- **60% Neutral** - `bg-background` - White/dark backgrounds
- **30% Complementary** - `text-foreground`, `text-muted-foreground` - Text/icons
- **10% Accent** - `bg-primary`, `text-primary` - CTAs and highlights ONLY

**❌ FORBIDDEN:**
- Overusing accent colors (>10%)
- Hardcoded colors
- Multiple competing accent colors

### 4. OKLCH Color Variables (globals.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Define OKLCH color variables here */
  }
}
```

## Setup Workflow

### 1. Initialize Design System

Run the setup script to configure the design system for your project.
```bash
bash scripts/setup-design-system.sh
```

### 2. Validate Design System

Use the validation script to ensure compliance with the design system.
```bash
bash scripts/validate-design-system.sh
```