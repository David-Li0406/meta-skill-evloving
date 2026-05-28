---
name: design-system-enforcement
description: Use this skill to enforce mandatory design system guidelines for projects using either Next.js with shadcn/ui or SvelteKit with shadcn-svelte and Tailwind CSS v4. It ensures consistent, accessible UI across all components and pages.
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

| Size | Tailwind Class | Pixels | Use Case |
|------|----------------|--------|----------|
| Size 1 | `text-3xl` or `text-2xl` | 32px or 24px | Large headings |
| Size 2 | `text-2xl` or `text-xl` | 24px or 20px | Subheadings |
| Size 3 | `text-base` | 16px | Body text |
| Size 4 | `text-sm` | 14px | Small text/labels |

**Weights:**
- ✅ `font-semibold` - Headings and emphasis
- ✅ `font-normal` - Body text and UI

**❌ FORBIDDEN:**
- More than 4 font sizes
- Additional font weights (bold, light, etc.)
- Inconsistent size application

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

**❌ FORBIDDEN:** Custom spacing like `p-[13px]`, `m-[7px]`

### 3. 60/30/10 Color Rule

**STRICTLY ENFORCED:**

- **60% Neutral** - `bg-background` - White/dark backgrounds
- **30% Complementary** - `text-foreground`, `text-muted-foreground` - Text/icons
- **10% Accent** - `bg-primary`, `text-primary` - CTAs and highlights ONLY

**❌ FORBIDDEN:**
- Overusing accent colors (>10%)
- Hardcoded colors
- Multiple competing accent colors

### 4. OKLCH Color Variables

**Configuration Example:**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.623 0.214 259.815);
}
```

## Setup Workflow

### 1. Initialize Design System

Run setup script during project initialization:

```bash
# Interactive setup
./scripts/setup-design-system.sh
```

### 2. Validate Existing Code

Check if existing code follows design system:

```bash
# Validate all components
./scripts/validate-design-system.sh
```

### 3. Before Creating UI

**MANDATORY AGENT WORKFLOW:**

```bash
# 1. Read design system (REQUIRED)
cat design-system.md

# 2. Understand constraints
# - Only 4 font sizes from config
# - Only 2 font weights
# - All spacing divisible by 8/4
# - Color distribution 60/30/10
# - OKLCH colors only
# - shadcn/ui or shadcn-svelte components only

# 3. Generate code following design system

# 4. Self-validate before completion
./scripts/validate-design-system.sh app/components/MyNewComponent.tsx
```

## Agent Enforcement Rules

### Before Generating ANY UI Code

**MANDATORY CHECKLIST:**

1. [ ] Read `design-system.md` file
2. [ ] Understand font size constraints (4 only)
3. [ ] Understand font weight constraints (2 only)
4. [ ] Understand spacing constraints (divisible by 8/4)
5. [ ] Understand color distribution (60/30/10)
6. [ ] Know OKLCH color variables
7. [ ] Use only shadcn/ui or shadcn-svelte components

### During Code Generation

**ENFORCE:**

- Use only configured font sizes
- Use only Semibold or Regular weights
- All spacing values divisible by 8 or 4
- 60% `bg-background`, 30% `text-foreground`, 10% `bg-primary`
- OKLCH colors from globals.css
- Proper accessibility (ARIA labels, keyboard nav)

### After Code Generation

**VALIDATE:**

```bash
# Self-validation
./scripts/validate-design-system.sh path/to/component.tsx
```

**❌ AUTOMATIC REJECTION:**

- More than 4 font sizes
- Font weights other than Semibold/Regular
- Spacing not divisible by 4 or 8
- Accent color usage > 10%
- Custom CSS instead of Tailwind
- Non-shadcn/ui or shadcn-svelte components

## Example Component (Compliant)

```tsx
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function ExampleComponent() {
  return (
    <Card className="p-6 bg-background">
      <CardHeader className="mb-4">
        <CardTitle className="text-2xl font-semibold">Welcome to TaskFlow</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-base font-normal text-foreground">Manage your tasks efficiently with AI-powered workflows.</p>
        <div className="flex gap-4">
          <Button className="bg-primary text-primary-foreground">Get Started</Button>
          <Button variant="outline" className="text-foreground">Learn More</Button>
        </div>
      </CardContent>
    </Card>
  );
}
```

## Resources

**Scripts:** `scripts/` directory:

- `setup-design-system.sh` - Interactive configuration
- `validate-design-system.sh` - Code validation

**Templates:** `templates/` directory:

- `design-system-template.md` - Base template with placeholders

---

**Frameworks:** Next.js 13+ with App Router or SvelteKit + Tailwind CSS v4
**UI Libraries:** shadcn/ui or shadcn-svelte
**Color Format:** OKLCH
**Enforcement:** Mandatory for all agents
**Version:** 1.0.0