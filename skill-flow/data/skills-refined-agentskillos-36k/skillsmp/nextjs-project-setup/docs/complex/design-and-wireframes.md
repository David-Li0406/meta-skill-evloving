# Phases 4-5: Design & Wireframes (Complex Path)

**Duration**: 3-6 hours total (includes user feedback iterations)
**Prerequisites**: Phase 3 (Specification complete)
**Next Phase**: Phase 6 (Implementation)

---

## Overview

This combined phase establishes the visual design system and creates implementation-ready wireframes. Design system provides the foundation (colors, typography, components), wireframes apply it to actual page layouts.

**What You'll Accomplish**:
1. Create custom design system with user feedback
2. Configure Tailwind CSS with CSS variables
3. Set up Shadcn UI component library
4. Create text-based wireframes for all pages
5. Map components to requirements
6. Validate accessibility and mobile-first approach

**Outputs**:
- `/docs/design-system.md` (complete design documentation)
- Configured `tailwind.config.ts` + `app/globals.css`
- `components.json` (Shadcn configuration)
- Base Shadcn components installed
- `/docs/wireframes.md` (text wireframes for all pages)
- `/docs/asset-inventory.md` (if images provided)

---

## Tools Required

- **Shadcn MCP**: Component search, examples, installation
- **21st Dev MCP**: Design inspiration and component discovery
- **design-ideator agent**: Brainstorm design variations (Phase 4)
- **File System**: Configuration and documentation

---

## Workflow (CoD^Σ)

```
Requirements + Research → Brainstorm_Design[3-4 options]
  ↓
Showcase ← design_ideator_agent
  ↓
User_Feedback ⇄ Iterations → Finalize_Design
  ↓
{tailwind_config, globals.css, components.json, shadcn_install}
  ↓
Spec + Design_System → Page_Inventory
  ↓
{Page_Type} → Layout_Options[2-3] ⊕ Component_Mapping
  ↓
Expert_Evaluation[UX, Conversion, A11y, Mobile, SEO] → User_Feedback
  ↓
Wireframes.md + Asset_Inventory.md → Ready_for_Implementation
```

---

## Critical Rules (Constitution-Enforced)

**Global CSS Variables**:
- ✅ ONLY use global Tailwind CSS variables
- ❌ NEVER hardcode colors in components
- ❌ NEVER use inline custom Tailwind styles
- ✅ ALL colors defined in `globals.css` via CSS variables

**Shadcn Workflow** (MANDATORY):
- ✅ ALWAYS follow: Search → View → Example → Install
- ❌ NEVER skip the Example step
- ✅ Prioritize @ui registry for core components
- ✅ Use @magicui sparingly (≤300ms animations, prefers-reduced-motion)

**Wireframes Format**:
- ✅ Text-based wireframes (NOT visual mockups)
- ✅ Reference actual Shadcn components (@ui/component-name)
- ✅ Mobile-first approach (show mobile layout first)
- ✅ Every section maps to spec.md requirements

---

## Phase 4: Design System Ideation

### Step 1: Brainstorm Design Directions

**Dispatch**: `design-ideator` agent (parallel exploration)

**Agent Task**:
1. Analyze target audience from spec
2. Review existing design trends (21st Dev MCP)
3. Generate 3-4 distinct design directions
4. Create variations for each direction

**Design Elements to Explore**:

**Color Palettes** (3-4 options):
```
Option A: Professional/Corporate
  Primary: #1e40af (blue), Secondary: #64748b (slate), Accent: #f59e0b (amber)

Option B: Modern/Vibrant
  Primary: #7c3aed (purple), Secondary: #ec4899 (pink), Accent: #06b6d4 (cyan)

Option C: Minimal/Elegant
  Primary: #18181b (zinc), Secondary: #71717a (gray), Accent: #a855f7 (purple)

Option D: Warm/Friendly
  Primary: #ea580c (orange), Secondary: #dc2626 (red), Accent: #16a34a (green)
```

**Typography Systems** (2-3 options):
```
Option A: Classic (Georgia serif + system sans)
Option B: Modern (Inter for all, weight variations)
Option C: Humanist (Poppins headings + Open Sans body)
```

**Component Styles** (2-3 directions):
```
Direction A: Sharp/Geometric (0.25rem radius, 2px borders, sharp shadows)
Direction B: Soft/Rounded (0.75rem radius, minimal borders, soft shadows)
Direction C: Brutalist/Bold (0 radius, 3px borders, heavy shadows)
```

**Layout Patterns**:
```
Pattern A: Full-width sections with contained content
Pattern B: Card-based layouts with whitespace
Pattern C: Asymmetric/editorial layouts
Pattern D: Grid-based systematic layouts
```

### Step 2: Create Design Showcase

**Dispatch**: `design-ideator` agent to create showcase page

Create `/app/design-showcase/page.tsx` presenting ALL variations:

```typescript
// Design Showcase - Present ALL variations to user
export default function DesignShowcase() {
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-4xl font-bold mb-8">Design System Options</h1>

      {/* Option A: Professional/Corporate */}
      <section className="mb-16 p-8 rounded-lg bg-gray-50">
        <h2 className="text-2xl font-bold mb-4">Option A: Professional</h2>
        <div className="space-y-4">
          <div className="flex gap-4">
            <Button className="bg-blue-600">Primary</Button>
            <Button variant="outline">Secondary</Button>
          </div>
          <Card className="p-6">
            <h3 className="text-xl font-semibold mb-2">Card Component</h3>
            <Input className="mt-4" placeholder="Input field" />
          </Card>
        </div>
      </section>

      {/* Option B, C... similar structure */}
    </div>
  )
}
```

**Use template**: `@templates/design-showcase.md` for structure

### Step 3: User Feedback Loop

**Present showcase** and gather feedback:

**Questions to Ask**:
1. Which color palette resonates with your brand?
2. Which typography feels most appropriate?
3. Which component style matches your aesthetic?
4. Any specific inspirations or examples?
5. What mood/feeling should the design convey?

**21st Dev MCP Integration**:
```typescript
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
- xs: 0.75rem (12px), sm: 0.875rem (14px), base: 1rem (16px)
- lg: 1.125rem (18px), xl: 1.25rem (20px), 2xl: 1.5rem (24px)
- 3xl: 1.875rem (30px), 4xl: 2.25rem (36px)

## Spacing System
Based on 4px baseline (0.25rem increments):
- xs: 0.25rem (4px), sm: 0.5rem (8px), md: 1rem (16px)
- lg: 1.5rem (24px), xl: 2rem (32px), 2xl: 3rem (48px)

## Components

### Shadows
- sm: 0 1px 2px rgba(0,0,0,0.05)
- md: 0 4px 6px rgba(0,0,0,0.1)
- lg: 0 10px 15px rgba(0,0,0,0.1)

### Border Radius
- sm: 0.25rem, md: 0.5rem, lg: 0.75rem, full: 9999px

### Animations
- Duration: 150-300ms (fast interactions)
- Easing: cubic-bezier(0.4, 0, 0.2, 1)
- Respects prefers-reduced-motion

## Component Library
Core Shadcn UI components (@ui registry):
- button, card, input, label, textarea
- dropdown-menu, select, dialog, sheet
- toast, alert, badge
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
    extend: {
      colors: {
        // Use CSS variables only (no hardcoded values)
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
        // ... additional colors
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
    --accent: 38 92% 50%; /* #f59e0b amber */

    /* Semantic colors */
    --muted: 210 40% 96.1%;
    --destructive: 0 84.2% 60.2%;
    --border: 214.3 31.8% 91.4%;
    --radius: 0.5rem;
  }

  .dark {
    /* Dark mode variants */
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark mode colors */
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
        </CardContent>
      </Card>
    </div>
  )
}
```

**Verify**:
- [ ] All components render
- [ ] Colors use CSS variables (inspect DevTools)
- [ ] Dark mode works (if implemented)
- [ ] Hover states function
- [ ] Responsive behavior correct

---

## Phase 5: Wireframes and Layout

### Step 1: Page Inventory

Extract page types from specification:

**Inventory Format**:
```markdown
## Page Inventory

### P1 Pages (Must Have)
1. Landing Page (/) - Marketing hero + features + CTA
2. Login (/auth/login) - Email/password form
3. Dashboard (/dashboard) - Main app interface
4. Profile (/profile) - User settings

### P2 Pages (Should Have)
1. Signup (/auth/signup) - Registration flow
2. Settings (/settings) - App configuration

### P3 Pages (Nice to Have)
1. Pricing (/pricing) - Plans comparison
2. Blog (/blog) - Content listing

### Error Pages
1. 404 Not Found, 2. 500 Server Error, 3. 403 Unauthorized
```

### Step 2: Asset Inventory (If Provided)

**IF user provides assets** (images, logos, icons), create inventory:

**Inventory Format**:
```markdown
## Asset Inventory

### Brand Assets
- @assets/logo-light.svg (header, footer - light mode)
- @assets/logo-dark.svg (header, footer - dark mode)
- @assets/logo-icon.svg (favicon, mobile nav)

### Hero Images
- @assets/hero-dashboard.png (landing page, 1920x1080)

### Product Screenshots
- @assets/screenshot-dashboard.png (dashboard demo, 1440x900)

### Placeholders
- Use unsplash.com/photos/[id] for missing images
- Specify dimensions and aspect ratios
```

**Storage**: Place in `/public/assets/` directory

### Step 3: Create Layout Options (Per Page Type)

For EACH page type, generate 2-3 layout options with expert evaluation.

**Layout Option Format**:
```markdown
## Landing Page - Option A: Hero-First

**Layout Structure**:
Hero Section (full-width, h-screen)
  ├── Background: gradient (primary → secondary)
  ├── Content: Container max-w-6xl
  │   ├── Heading: h1 text-6xl font-bold
  │   ├── Subheading: text-xl text-muted-foreground
  │   └── CTA Group: @ui/button (primary + outline)
  └── Visual: @assets/hero-dashboard.png (right 50%)

Features Section (py-24)
  ├── Grid: 3 columns (lg) → 1 column (mobile)
  ├── Feature Card 1: @ui/card
  │   ├── Icon: Lucide icon-name
  │   ├── Title: h3 text-2xl font-semibold
  │   └── Description: text-muted-foreground
  └── [Feature Cards 2-3]

CTA Section (py-24)
  ├── Heading: h2 text-4xl
  └── CTA: @ui/button (size: lg, variant: default)

**Expert Evaluation**:
- UX (8/10): Clear hierarchy, strong CTA visibility
- Conversion (9/10): Multiple conversion points, clear value prop
- A11y (10/10): Semantic HTML, proper heading hierarchy
- Mobile (7/10): Stacks well but hero may be too tall
- SEO (9/10): Clear h1, structured content

**Recommendation**: Hero-first is best for SaaS landing pages.
```

**Generate 2-3 options per page type** with different:
- Component hierarchy
- Visual emphasis (content-first vs visual-first)
- Conversion strategy
- Mobile adaptation approach

### Step 4: Component Mapping

Map each wireframe section to **actual Shadcn components**:

**Mapping Format**:
```markdown
## Component Mapping: Dashboard Page

### Navigation
- Component: Custom nav (based on @ui/navigation-menu)
- Variant: Sticky top-0 z-50
- Children:
  - Logo: @assets/logo-light.svg
  - Menu Items: @ui/navigation-menu-item (link variants)
  - User Menu: @ui/dropdown-menu + @ui/avatar

### Main Content Area
- Component: Container max-w-7xl mx-auto
- Layout: Grid gap-6 (responsive)
- Children:
  - Stats Cards: @ui/card (grid 4 columns → 2 → 1)
    - Icon: Lucide icon (stroke-width: 1.5)
    - Title: text-sm text-muted-foreground
    - Value: text-3xl font-bold
  - Chart Card: @ui/card + Chart.js/Recharts
```

**Requirements**:
- Every section MUST reference actual Shadcn components (@ui/*)
- Use `@assets/filename.ext` notation for asset references
- Include variants, sizes, and styling props
- Reference design system variables

### Step 5: User Feedback Loop

Present wireframe options to user:

```markdown
## Page: Landing Page

I've created 3 layout options:

### Option A: Hero-First (Recommended)
[Insert wireframe]
**Best for**: SaaS products, strong value prop, visual demos
**Expert Scores**: UX 8/10, Conversion 9/10, A11y 10/10

### Option B: Feature-First
[Insert wireframe]
**Best for**: Complex products needing immediate feature showcase

### Option C: Social-Proof-First
[Insert wireframe]
**Best for**: Established products with strong testimonials

**My Recommendation**: Option A because [specific rationale]

**Questions**:
1. Which option aligns best with your brand?
2. Any sections to add/remove?
3. Prioritize mobile or desktop layout?
```

**Iteration**: Maximum 3 rounds, incremental updates only

### Step 6: Finalize Wireframes Document

**Document Structure**:
```markdown
# Wireframes - [Project Name]

## Overview
- Date: YYYY-MM-DD
- Design System: @docs/design-system.md
- Specification: @docs/spec.md

## Page Inventory
[List all pages with priorities]

## Asset Inventory
[If applicable]

---

## Landing Page (Priority: P1)

### Selected Layout: Option A - Hero-First

#### Hero Section
[Detailed component breakdown]

#### Component Mapping
[Section-to-component mapping]

---

## Dashboard (Priority: P1)
[Same structure for each page]

---

## Mobile Adaptations

### Responsive Breakpoints
- sm: 640px (mobile), md: 768px (tablet)
- lg: 1024px (desktop), xl: 1280px (wide)

### Layout Changes
- Navigation: Desktop nav → Mobile drawer (@ui/sheet)
- Sidebar: Fixed → Overlay drawer
- Grid: 4 cols → 2 cols → 1 col
- Hero: Side-by-side → Stacked

---

## Implementation Notes

### Component Installation Order
1. Core layout: @ui/card, @ui/button, @ui/separator
2. Navigation: @ui/navigation-menu, @ui/dropdown-menu
3. Forms: @ui/input, @ui/label, @ui/form
4. Feedback: @ui/toast, @ui/alert
5. Advanced: @ui/carousel, @ui/chart, @ui/table

### Accessibility Checklist
- [ ] All interactive elements keyboard accessible
- [ ] Color contrast ≥4.5:1 (WCAG AA)
- [ ] Semantic HTML (header, nav, main, footer)
- [ ] ARIA labels where needed
- [ ] Focus indicators visible
```

---

## Quality Checks

### Design System Validation
- [ ] User approved final design direction
- [ ] All color combinations meet WCAG 2.1 AA
- [ ] Typography tested for readability
- [ ] Component styles consistent
- [ ] `tailwind.config.ts` uses CSS variables only
- [ ] `globals.css` defines all colors
- [ ] Shadcn components installed correctly
- [ ] Dark mode works (if applicable)
- [ ] No hardcoded colors in codebase

### Wireframes Validation
- [ ] All P1 pages have wireframes
- [ ] All components reference installable Shadcn components
- [ ] Asset inventory complete (if applicable)
- [ ] Mobile responsive strategy documented
- [ ] Expert evaluation scores documented (5 dimensions)
- [ ] User approval received on layout options
- [ ] Implementation order defined

### Accessibility
- [ ] Contrast ratios ≥4.5:1 (text)
- [ ] Focus indicators visible
- [ ] Color not sole information carrier
- [ ] Prefers-reduced-motion respected
- [ ] All interactive elements keyboard accessible
- [ ] Semantic HTML structure

---

## Outputs Summary

**Phase 4 Outputs**:
1. `/docs/design-system.md` - Complete design documentation
2. `tailwind.config.ts` - Tailwind configuration
3. `app/globals.css` - CSS variables
4. `components.json` - Shadcn configuration
5. `/components/ui/*` - Base components installed
6. `/app/design-showcase/page.tsx` - Showcase (can delete after approval)

**Phase 5 Outputs**:
1. `/docs/wireframes.md` - Text wireframes for all pages
2. `/docs/asset-inventory.md` - Asset references (if applicable)
3. Component-to-requirement mapping
4. Implementation order checklist

---

## Next Phase Handover

**Prerequisites for Phase 6 (Implementation)**:
- ✅ Design system documented and approved
- ✅ Tailwind configured with CSS variables
- ✅ Shadcn components installed and tested
- ✅ Wireframes complete and approved
- ✅ All components mapped to Shadcn registry
- ✅ Asset placeholders or references defined
- ✅ Mobile responsive strategy documented
- ✅ Accessibility standards met (WCAG 2.1 AA)

**Handover Context**:
- Approved color palette and typography
- Component style guide
- Available UI components
- Page-by-page implementation order (P1 → P2 → P3)
- Asset requirements and placeholders
- Responsive breakpoint definitions

**Continue with**: Phase 6 (Implementation)

---

## Success Criteria

### Phase 4 Success
- ✅ User-approved design direction
- ✅ Complete design system documentation
- ✅ Tailwind configured with CSS variables only
- ✅ Shadcn UI components installed and tested
- ✅ WCAG 2.1 AA compliance verified
- ✅ Dark mode functional (if required)
- ✅ No hardcoded colors in codebase

### Phase 5 Success
- ✅ Wireframes created for all P1 pages (minimum)
- ✅ All components mapped to installable Shadcn components
- ✅ Asset inventory complete (if applicable)
- ✅ Mobile responsive strategy documented
- ✅ Expert evaluation scores documented (5 dimensions)
- ✅ User approval received on layout options
- ✅ Implementation order defined

### Combined Success
- ✅ Ready to proceed with Phase 6 (Implementation)
- ✅ Design system and wireframes integrated
- ✅ All prerequisites met
- ✅ Quality checks passed

---

## Common Issues & Solutions

### Issue: Design feedback loop taking too long
**Solution**: Maximum 3 iterations, present clear recommendations, combine user-liked elements from different options

### Issue: Wireframes too detailed (approaching visual design)
**Solution**: Reference design system variables only (e.g., "text-primary" not "#000000"), keep focus on component hierarchy

### Issue: Components don't exist in Shadcn registry
**Solution**: Always check Shadcn registry first via MCP. If custom needed, specify base component

### Issue: Mobile layout not considered
**Solution**: Mobile-first wireframes. Show mobile layout FIRST, then progressive enhancement

### Issue: Asset references missing or unclear
**Solution**: Always use @assets/filename.ext notation with dimensions and aspect ratio

---

## Anti-Patterns

❌ **Visual mockups** - Token-heavy, hard to iterate, not directly implementable
❌ **Hardcoded values** - Use design system variables only
❌ **Skipping Shadcn Example step** - Always follow Search→View→Example→Install
❌ **Skipping expert evaluation** - Scores provide objective decision criteria
❌ **Undefined mobile strategy** - Mobile-first is mandatory
❌ **Vague component references** - "Some button" → "@ui/button (variant: default, size: lg)"
❌ **No asset placeholders** - Every image needs @assets/filename.ext reference
❌ **Ignoring accessibility** - WCAG 2.1 AA is minimum standard
