# Phase 4: Design System Ideation (Complex Path)

**Duration**: 2-4 hours (includes user feedback iterations)
**Prerequisites**: Phase 3 (Specification complete)
**Next Phase**: Phase 5 (Wireframes)

---

## Overview

**Purpose**: Create custom design system with user feedback, configure Tailwind CSS, set up Shadcn UI components

**Inputs**:
- Product specification (`/docs/spec.md`)
- Target audience and brand requirements
- Research reports (shadcn-best-practices.md, design-systems.md)

**Outputs**:
- `/docs/design-system.md` (complete design documentation)
- Configured `tailwind.config.ts` with CSS variables
- `components.json` configured for Shadcn
- Base components installed
- Design showcase page (for user feedback)

---

## Tools Required

- **Shadcn MCP**: Component search, examples, installation
- **21st Dev MCP**: Design inspiration and component discovery
- **design-ideator agent**: Brainstorm design variations
- **File System**: Configuration and documentation

---

## Workflow (CoD^Σ)

```
Requirements ∧ Research → Brainstorm[3-4 directions]
  ↓
Showcase ← design_ideator_agent
  ↓
User_Feedback ⇄ Iterations
  ↓
Finalize → {tailwind_config, component_setup, documentation}
  ↓
Validation → Ready_for_Wireframes
```

---

## Critical Rules

**Global CSS Variables** (Constitution-enforced):
- ✅ ONLY use global Tailwind CSS variables
- ❌ NEVER hardcode colors in components
- ❌ NEVER use inline custom Tailwind styles
- ✅ ALL colors defined in `globals.css` via CSS variables

**Shadcn Workflow** (MANDATORY):
- ✅ ALWAYS follow: Search → View → Example → Install
- ❌ NEVER skip the Example step
- ✅ Prioritize @ui registry for core components
- ✅ Use @magicui sparingly (≤300ms animations, prefers-reduced-motion)

---

## Detailed Steps

### Step 1: Brainstorm Design Directions

**Dispatch**: `design-ideator` agent (parallel exploration)

**Agent Task**:
1. Analyze target audience from spec
2. Review existing design trends
3. Generate 3-4 distinct design directions
4. Create variations for each direction

**Design Elements to Explore**:

**1. Color Palettes** (3-4 options):
```
Option A: Professional/Corporate
  Primary: #1e40af (blue)
  Secondary: #64748b (slate)
  Accent: #f59e0b (amber)

Option B: Modern/Vibrant
  Primary: #7c3aed (purple)
  Secondary: #ec4899 (pink)
  Accent: #06b6d4 (cyan)

Option C: Minimal/Elegant
  Primary: #18181b (zinc)
  Secondary: #71717a (gray)
  Accent: #a855f7 (purple)

Option D: Warm/Friendly
  Primary: #ea580c (orange)
  Secondary: #dc2626 (red)
  Accent: #16a34a (green)
```

**2. Typography Systems** (2-3 options):
```
Option A: Classic
  Heading: Georgia, serif
  Body: -apple-system, sans-serif
  Code: 'Fira Code', monospace

Option B: Modern
  Heading: 'Inter', sans-serif (weight: 700)
  Body: 'Inter', sans-serif (weight: 400)
  Code: 'JetBrains Mono', monospace

Option C: Humanist
  Heading: 'Poppins', sans-serif
  Body: 'Open Sans', sans-serif
  Code: 'Source Code Pro', monospace
```

**3. Component Styles** (2-3 directions):
```
Direction A: Sharp/Geometric
  Border radius: 0.25rem (small)
  Shadows: Sharp, defined
  Borders: 2px solid

Direction B: Soft/Rounded
  Border radius: 0.75rem (large)
  Shadows: Soft, diffuse
  Borders: 1px, often borderless

Direction C: Brutalist/Bold
  Border radius: 0 (square)
  Shadows: None or heavy
  Borders: 3px solid, high contrast
```

**4. Layout Patterns**:
```
Pattern A: Full-width sections with contained content
Pattern B: Card-based layouts with whitespace
Pattern C: Asymmetric/editorial layouts
Pattern D: Grid-based systematic layouts
```

### Step 2: Create Design Showcase

**Dispatch**: `design-ideator` agent to create showcase page

**Showcase Structure**:
Create `/app/design-showcase/page.tsx`:

```typescript
// Design Showcase - Present ALL variations to user

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"

export default function DesignShowcase() {
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-4xl font-bold mb-8">Design System Options</h1>

      {/* Option A */}
      <section className="mb-16 p-8 rounded-lg bg-gray-50">
        <h2 className="text-2xl font-bold mb-4">Option A: Professional/Corporate</h2>
        <div className="space-y-4">
          <div className="flex gap-4">
            <Button className="bg-blue-600">Primary Button</Button>
            <Button variant="outline">Secondary</Button>
            <Button variant="ghost">Tertiary</Button>
          </div>
          <Card className="p-6">
            <h3 className="text-xl font-semibold mb-2">Card Component</h3>
            <p className="text-gray-600">Sample content with typography...</p>
            <Input className="mt-4" placeholder="Input field example" />
          </div>
        </div>
      </section>

      {/* Option B */}
      <section className="mb-16 p-8 rounded-lg bg-purple-50">
        <h2 className="text-2xl font-bold mb-4">Option B: Modern/Vibrant</h2>
        {/* Similar structure with different styling */}
      </section>

      {/* Option C */}
      <section className="mb-16 p-8 rounded-lg bg-zinc-50">
        <h2 className="text-2xl font-bold mb-4">Option C: Minimal/Elegant</h2>
        {/* Similar structure with different styling */}
      </section>
    </div>
  )
}
```

**Use template**: `@templates/design-showcase.md` for structure

### Step 3: User Feedback Loop

**Present showcase** and gather feedback:

**Questions to Ask**:
1. Which color palette resonates with your brand?
2. Which typography feels most appropriate for your audience?
3. Which component style matches your desired aesthetic?
4. Any specific inspirations or examples to reference?
5. What mood/feeling should the design convey?

**21st Dev MCP Integration**:
```typescript
// Find design inspiration
mcp__21st_dev__21st_magic_component_inspiration({
  searchQuery: "modern dashboard layout",
  message: "Looking for inspiration for [user's use case]"
})
```

**Iterate**:
- Combine elements from different options if user likes mixed approach
- Create refined variations based on feedback
- Present 2nd round if needed
- Continue until user approves final direction

**Evidence Collection** (Constitution Article II):
- Document user preferences: `design-system.md:feedback-notes`
- Reference inspiration sources: 21st Dev results, competitor examples
- Justify choices: Accessibility contrast ratios, WCAG compliance

### Step 4: Finalize Design System

Once user approves direction, document complete system.

**Create `/docs/design-system.md`**:

```markdown
# Design System

## Design Philosophy
[User-approved aesthetic direction and rationale]

## Color Palette

### Primary Colors
- Primary: `hsl(var(--primary))` - #1e40af - Main brand color
- Secondary: `hsl(var(--secondary))` - #64748b - Supporting color
- Accent: `hsl(var(--accent))` - #f59e0b - Highlights and CTAs

### Semantic Colors
- Destructive: `hsl(var(--destructive))` - Error states
- Muted: `hsl(var(--muted))` - Backgrounds, disabled states
- Border: `hsl(var(--border))` - Dividers and outlines

### Accessibility
- All color combinations meet WCAG 2.1 AA standards (4.5:1 contrast minimum)
- High-emphasis text on primary: AAA compliant (7:1)

## Typography

### Font Families
- Heading: Inter, -apple-system, sans-serif
- Body: Inter, -apple-system, sans-serif
- Code: 'JetBrains Mono', monospace

### Type Scale
- xs: 0.75rem (12px)
- sm: 0.875rem (14px)
- base: 1rem (16px)
- lg: 1.125rem (18px)
- xl: 1.25rem (20px)
- 2xl: 1.5rem (24px)
- 3xl: 1.875rem (30px)
- 4xl: 2.25rem (36px)

### Line Heights
- Tight: 1.25 (headings)
- Normal: 1.5 (body text)
- Relaxed: 1.75 (long-form content)

## Spacing System
Based on 4px baseline: 0.25rem increments
- xs: 0.25rem (4px)
- sm: 0.5rem (8px)
- md: 1rem (16px)
- lg: 1.5rem (24px)
- xl: 2rem (32px)
- 2xl: 3rem (48px)

## Components

### Shadows
- sm: 0 1px 2px rgba(0,0,0,0.05)
- md: 0 4px 6px rgba(0,0,0,0.1)
- lg: 0 10px 15px rgba(0,0,0,0.1)

### Border Radius
- sm: 0.25rem
- md: 0.5rem
- lg: 0.75rem
- full: 9999px

### Animations
- Duration: 150-300ms (fast interactions)
- Easing: cubic-bezier(0.4, 0, 0.2, 1)
- Respects prefers-reduced-motion

## Component Library

### Shadcn UI (@ui registry)
Core components used:
- button, card, input, label, textarea
- dropdown-menu, select, dialog, sheet
- toast, alert, badge
- [Complete list after installation]

## Design Tokens (CSS Variables)

All design tokens are defined as CSS variables in `globals.css`.
Components reference variables, never hardcode values.
```

### Step 5: Configure Tailwind CSS

**Edit `tailwind.config.ts`**:

```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      fontFamily: {
        sans: ["var(--font-inter)"],
        mono: ["var(--font-jetbrains-mono)"],
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config
```

**Edit `app/globals.css`** with user-approved color values:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* User-approved colors (example: Professional/Corporate) */
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221 83% 53%; /* #1e40af blue */
    --primary-foreground: 210 40% 98%;
    --secondary: 215 16% 47%; /* #64748b slate */
    --secondary-foreground: 210 40% 98%;
    --accent: 38 92% 50%; /* #f59e0b amber */
    --accent-foreground: 222.2 84% 4.9%;

    /* Semantic colors */
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221 83% 53%;
    --radius: 0.5rem;

    /* Card and popover */
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --accent: 38 92% 50%;
    --accent-foreground: 222.2 47.4% 11.2%;

    /* Dark mode semantic colors */
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;

    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

### Step 6: Install Base Components

**Shadcn Setup**:
```bash
npx shadcn@latest init
```

**Install core components** (following Search→View→Example→Install):

```bash
# Layout & Structure
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add separator

# Forms
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add textarea
npx shadcn@latest add select

# Navigation
npx shadcn@latest add dropdown-menu
npx shadcn@latest add navigation-menu

# Feedback
npx shadcn@latest add toast
npx shadcn@latest add alert
npx shadcn@latest add badge

# Overlays
npx shadcn@latest add dialog
npx shadcn@latest add sheet
npx shadcn@latest add popover
```

**IMPORTANT**: Install one at a time, verify each works before proceeding.

### Step 7: Verify Component Integration

Create test page `/app/component-test/page.tsx`:

```typescript
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"

export default function ComponentTest() {
  return (
    <div className="container mx-auto p-8 space-y-8">
      <h1 className="text-4xl font-bold">Component Verification</h1>

      <Card>
        <CardHeader>
          <CardTitle>Buttons</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-4">
          <Button>Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="destructive">Destructive</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Form Elements</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input placeholder="Enter text..." />
          <div className="flex gap-2">
            <Badge>Default</Badge>
            <Badge variant="secondary">Secondary</Badge>
            <Badge variant="outline">Outline</Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
```

Visit `/component-test` and verify:
- [ ] All components render
- [ ] Colors use CSS variables (inspect DevTools)
- [ ] Dark mode works (if implemented)
- [ ] Hover states function
- [ ] Responsive behavior correct

---

## Sub-Agents

### design-ideator Agent
**Dispatch for**: Brainstorming and showcase creation
**Report**: `/reports/design-ideation.md`
**Token target**: ≤2500

---

## Quality Checks

### Pre-Finalization
- [ ] User approved final design direction
- [ ] All color combinations meet WCAG 2.1 AA
- [ ] Typography tested for readability
- [ ] Component styles consistent

### Post-Configuration
- [ ] `tailwind.config.ts` uses CSS variables only
- [ ] `globals.css` defines all colors
- [ ] Shadcn components installed correctly
- [ ] Dark mode works (if applicable)
- [ ] No hardcoded colors in codebase

### Accessibility
- [ ] Contrast ratios ≥4.5:1 (text)
- [ ] Focus indicators visible
- [ ] Color not sole information carrier
- [ ] Prefers-reduced-motion respected

---

## Outputs

1. **Design System Documentation**: `/docs/design-system.md`
2. **Tailwind Configuration**: `tailwind.config.ts`
3. **CSS Variables**: `app/globals.css`
4. **Shadcn Configuration**: `components.json`
5. **Base Components**: `/components/ui/*`
6. **Design Showcase**: `/app/design-showcase/page.tsx` (can delete after approval)

---

## Next Phase Handover

**Prerequisites for Phase 5 (Wireframes)**:
- ✅ Design system documented
- ✅ Tailwind configured with CSS variables
- ✅ Shadcn components installed
- ✅ Component test page validates all components
- ✅ Accessibility standards met

**Handover Context**:
- Approved color palette and typography
- Component style guide
- Available UI components
- Design constraints and conventions

**Continue with**: `phase-5-wireframes.md`

---

## Success Criteria

- ✅ User-approved design direction
- ✅ Complete design system documentation
- ✅ Tailwind configured with CSS variables only
- ✅ Shadcn UI components installed and tested
- ✅ WCAG 2.1 AA compliance verified
- ✅ Dark mode functional (if required)
- ✅ No hardcoded colors in codebase
- ✅ Ready for wireframe creation
