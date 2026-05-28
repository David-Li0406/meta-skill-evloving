# Phase 5: Wireframes and Layout (Complex Path)

**Duration**: 1-2 hours
**Prerequisites**: Phase 4 (Design System complete)
**Next Phase**: Phase 6 (Implementation)

---

## Overview

**Purpose**: Create text-based wireframes mapping specification to design system components with layout structure

**Inputs**:
- User stories from spec.md (Phase 3)
- Design system from design-system.md (Phase 4)
- Component inventory from components.json
- User-provided assets (optional: images, logos, icons)

**Outputs**:
- `/docs/wireframes.md` (text wireframes for all pages)
- `/docs/asset-inventory.md` (if assets provided)
- Component-to-requirement mapping
- Layout hierarchy per page type

---

## Overview Philosophy

**CRITICAL**: This phase creates **text wireframes** NOT visual mockups.

**Text Wireframe** := Structured component layout descriptions mapping design system components to page sections

**Why Text Wireframes**:
- Token-efficient (500-1000 tokens vs 10K+ for generated visual mockups)
- Directly implementable (references actual Shadcn components)
- Version control friendly (pure markdown)
- Iterative (easy to modify and compare options)
- AI-native (optimized for Claude Code implementation)

**Format Example**:
```markdown
## Page: Dashboard

### Hero Section
- Layout: Grid 2-column (lg) → Stack (mobile)
- Left Column:
  - @ui/card (variant: default, padding: 8)
    - Heading: h1 text-4xl font-bold (design-system: primary)
    - Body: text-lg text-muted-foreground
    - CTA: @ui/button (variant: default, size: lg)
- Right Column:
  - @asset/hero-dashboard.png (placeholder: w-full h-auto)
```

---

## Tools Required

- **Shadcn MCP**: Component inventory verification
- **21st Dev MCP**: Layout inspiration (optional)
- **File System**: Wireframe documentation
- **Asset Management**: Image placeholder generation

---

## Workflow (CoD^Σ)

```
Spec.md + Design_System → Page_Inventory
  ↓
{Page_Type} → Layout_Options[2-3] ⊕ Component_Mapping
  ↓
Expert_Evaluation[UX, Conversion, A11y, Mobile, SEO] → Recommendations
  ↓
User_Feedback ⇄ Iteration → Finalize
  ↓
Wireframes.md + Asset_Inventory.md
```

---

## Detailed Steps

### Step 1: Page Inventory

Extract page types from specification:

**Common Page Types**:
- Landing/Home page (marketing)
- Authentication pages (login, signup, password reset)
- Dashboard/App shell (authenticated)
- Profile/Settings pages
- Feature-specific pages (from user stories)
- Error pages (404, 500, 403)

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
1. 404 Not Found
2. 500 Server Error
3. 403 Unauthorized
```

### Step 2: Asset Inventory (If Provided)

**IF user provides assets** (images, logos, icons), create inventory:

**Asset Categories**:
- **Brand**: Logo variations (light/dark, size variants)
- **Hero Images**: Marketing page visuals
- **Product Screenshots**: Dashboard, feature demos
- **Icons**: Custom SVG icons (beyond Lucide)
- **Illustrations**: Empty states, onboarding

**Inventory Format**:
```markdown
## Asset Inventory

### Brand Assets
- @assets/logo-light.svg (header, footer - light mode)
- @assets/logo-dark.svg (header, footer - dark mode)
- @assets/logo-icon.svg (favicon, mobile nav)

### Hero Images
- @assets/hero-dashboard.png (landing page, 1920x1080)
- @assets/hero-features.png (features section, 1200x800)

### Product Screenshots
- @assets/screenshot-dashboard.png (dashboard demo, 1440x900)
- @assets/screenshot-analytics.png (analytics feature, 1440x900)

### Placeholders
- Use unsplash.com/photos/[id] for missing images
- Specify dimensions and aspect ratios
```

**Storage**:
- Place in `/public/assets/` directory
- Reference via `@assets/filename.ext` in wireframes
- Generate responsive image variants during implementation

### Step 3: Create Layout Options (Per Page Type)

For EACH page type, generate 2-3 layout options with expert evaluation.

**Process**:
1. Map user story requirements to page sections
2. Propose 2-3 layout structures (different component hierarchies)
3. Map design system components to each section
4. Expert evaluation (5 dimensions: UX, Conversion, A11y, Mobile, SEO)
5. Present to user with recommendations

**Layout Option Format**:
```markdown
## Landing Page - Option A: Hero-First

**Layout Structure**:
```
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
  ├── Feature Card 2: [same structure]
  └── Feature Card 3: [same structure]

Social Proof (bg-muted, py-16)
  ├── Testimonials: @ui/carousel
  └── Logos: Grid 4 columns (grayscale filter)

CTA Section (py-24)
  ├── Heading: h2 text-4xl
  └── CTA: @ui/button (size: lg, variant: default)
```

**Expert Evaluation**:
- **UX** (8/10): Clear hierarchy, strong CTA visibility. Consider adding social proof earlier.
- **Conversion** (9/10): Multiple conversion points, clear value prop. Excellent CTA placement.
- **A11y** (10/10): Semantic HTML, proper heading hierarchy, keyboard navigable.
- **Mobile** (7/10): Stacks well but hero section may be too tall on mobile. Consider h-auto with min-h-[500px].
- **SEO** (9/10): Clear h1, structured content, fast-loading hero. Add meta descriptions.

**Recommendation**: **Option A** - Hero-first is best for SaaS landing pages. High conversion potential with clear value proposition above the fold.
```

**Generate 2-3 options per page type**, each with different:
- Component hierarchy
- Visual emphasis (content-first vs visual-first)
- Conversion strategy (single CTA vs multiple touchpoints)
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

### Sidebar
- Component: Custom sidebar (based on @ui/sheet for mobile)
- Variant: Fixed left, w-64 (desktop) → Sheet overlay (mobile)
- Children:
  - Nav Links: @ui/button (variant: ghost, justify: start)
  - Active State: bg-accent text-accent-foreground
  - Collapse Toggle: @ui/button (icon-only, variant: ghost)

### Main Content Area
- Component: Container max-w-7xl mx-auto
- Layout: Grid gap-6 (responsive)
- Children:
  - Stats Cards: @ui/card (grid 4 columns → 2 → 1)
    - Icon: Lucide icon (stroke-width: 1.5)
    - Title: text-sm text-muted-foreground
    - Value: text-3xl font-bold
    - Change: @ui/badge (variant: secondary)
  - Chart Card: @ui/card
    - Header: @ui/card-header + @ui/select (date range)
    - Content: Chart.js or Recharts component
  - Recent Activity: @ui/card
    - Header: @ui/card-header
    - Content: @ui/table (striped variant)
```

**Requirements**:
- Every section MUST reference actual installed or installable Shadcn components
- Use `@ui/component-name` notation for Shadcn components
- Use `@assets/filename.ext` notation for asset references
- Include variants, sizes, and styling props
- Reference design system variables (e.g., `text-primary`, `bg-accent`)

### Step 5: User Feedback Loop

Present wireframe options to user:

**Presentation Format**:
```markdown
## Page: Landing Page

I've created 3 layout options for your landing page:

### Option A: Hero-First (Recommended)
[Insert wireframe structure]
**Best for**: SaaS products, strong value prop, visual demos
**Expert Scores**: UX 8/10, Conversion 9/10, A11y 10/10, Mobile 7/10, SEO 9/10

### Option B: Feature-First
[Insert wireframe structure]
**Best for**: Complex products needing immediate feature showcase
**Expert Scores**: UX 7/10, Conversion 7/10, A11y 10/10, Mobile 9/10, SEO 8/10

### Option C: Social-Proof-First
[Insert wireframe structure]
**Best for**: Established products with strong testimonials
**Expert Scores**: UX 9/10, Conversion 8/10, A11y 10/10, Mobile 8/10, SEO 7/10

**My Recommendation**: Option A (Hero-First) because [specific rationale based on user's spec requirements]

**Questions**:
1. Which option aligns best with your brand?
2. Any sections you'd like to add/remove?
3. Should we prioritize mobile or desktop layout?
```

**Iteration Process**:
- User selects option or requests modifications
- Make incremental updates (don't regenerate entire wireframe)
- Re-evaluate expert scores if layout changes significantly
- Maximum 3 iteration rounds (avoid infinite refinement)

### Step 6: Finalize Wireframes Document

**Document Structure**:
```markdown
# Wireframes - [Project Name]

## Overview
- Date: YYYY-MM-DD
- Design System: @docs/design-system.md
- Specification: @docs/spec.md

## Page Inventory
[List of all pages with priorities]

## Asset Inventory
[If applicable - list of provided assets]

---

## Landing Page (Priority: P1)

### Selected Layout: Option A - Hero-First

#### Hero Section
[Detailed component breakdown]

#### Features Section
[Detailed component breakdown]

#### CTA Section
[Detailed component breakdown]

#### Component Mapping
[Section-to-component mapping]

---

## Dashboard (Priority: P1)

[Same structure]

---

## Mobile Adaptations

### Responsive Breakpoints
- sm: 640px (mobile)
- md: 768px (tablet)
- lg: 1024px (desktop)
- xl: 1280px (wide desktop)

### Layout Changes
- **Navigation**: Desktop nav → Mobile drawer (@ui/sheet)
- **Sidebar**: Fixed → Overlay drawer
- **Grid**: 4 cols → 2 cols → 1 col
- **Hero**: Side-by-side → Stacked (image below text)

---

## Implementation Notes

### Component Installation Order
1. Core layout: @ui/card, @ui/button, @ui/separator
2. Navigation: @ui/navigation-menu, @ui/dropdown-menu
3. Forms: @ui/input, @ui/label, @ui/form
4. Feedback: @ui/toast, @ui/alert
5. Advanced: @ui/carousel, @ui/chart, @ui/table

### Asset Optimization
- Images: Use Next.js Image component with priority flag
- Icons: Prefer Lucide icons (tree-shakeable)
- Fonts: Already optimized via Geist Sans/Mono

### Accessibility Checklist
- [ ] All interactive elements keyboard accessible
- [ ] Color contrast ≥4.5:1 (WCAG AA)
- [ ] Semantic HTML (header, nav, main, footer)
- [ ] ARIA labels where needed
- [ ] Focus indicators visible

---

## Next Steps

1. Review and approve wireframes
2. Proceed to Phase 6: Implementation
3. Follow component installation order
4. Implement page-by-page (P1 → P2 → P3)
```

---

## Sub-Agents

**None required** - Orchestrator handles layout generation directly

**Optional**: If domain-specific layout expertise needed, dispatch specialist agent (e.g., e-commerce layout expert, SaaS dashboard expert)

---

## Quality Checks

### Pre-Finalization Checklist
- [ ] All pages from spec.md have wireframes
- [ ] All components reference actual Shadcn components (@ui/*)
- [ ] All assets have placeholders or references (@assets/*)
- [ ] Mobile responsive strategy documented
- [ ] Accessibility considerations noted
- [ ] Expert evaluation scores documented (UX, Conversion, A11y, Mobile, SEO)

### Component Verification
- [ ] Every component exists in Shadcn registry OR is custom with clear base
- [ ] Component variants specified (size, variant, color)
- [ ] Design system variables referenced (no hardcoded colors)
- [ ] Layout responsive breakpoints defined

### Completeness Check
- [ ] Landing page (if marketing project)
- [ ] Auth pages (if authentication required)
- [ ] Dashboard (if app project)
- [ ] Error pages (404, 500, 403)
- [ ] All P1 user story pages covered

---

## Outputs

### 1. Wireframes Document
**Location**: `/docs/wireframes.md`
**Content**: Text wireframes for all pages with component mapping
**Token Size**: 500-1000 tokens per page type

### 2. Asset Inventory
**Location**: `/docs/asset-inventory.md` (if assets provided)
**Content**: Categorized list of images, logos, icons with references
**Storage**: `/public/assets/` directory

### 3. Component Installation Checklist
**Location**: Embedded in wireframes.md footer
**Content**: Ordered list of Shadcn components to install

---

## Next Phase Handover

**Prerequisites for Phase 6 (Implementation)**:
- ✅ Wireframes complete and approved
- ✅ All components mapped to Shadcn registry
- ✅ Asset placeholders or references defined
- ✅ Mobile responsive strategy documented
- ✅ Accessibility checklist reviewed

**Handover Context**:
- Page-by-page implementation order (P1 → P2 → P3)
- Component installation sequence
- Asset requirements and placeholders
- Design system integration points
- Responsive breakpoint definitions

**Continue with**: `phase-6-implement.md`

---

## Common Issues & Solutions

### Issue: Too many layout options causing decision paralysis
**Cause**: Presenting 4+ options without clear recommendation
**Solution**: Maximum 3 options, always provide expert-backed recommendation with specific rationale tied to user's requirements.

### Issue: Wireframes too detailed (approaching visual design)
**Cause**: Including exact spacing, colors, font sizes
**Solution**: Reference design system variables only (e.g., "text-primary" not "#000000", "spacing-4" not "16px"). Keep focus on component hierarchy.

### Issue: Components don't exist in Shadcn registry
**Cause**: Proposing custom components without base
**Solution**: Always check Shadcn registry first via MCP. If custom needed, specify base component (e.g., "Custom sidebar based on @ui/sheet").

### Issue: Asset references missing or unclear
**Cause**: Vague placeholder descriptions ("image here")
**Solution**: Always use @assets/filename.ext notation with dimensions and aspect ratio (e.g., "@assets/hero.png (1920x1080, 16:9)").

### Issue: Mobile layout not considered
**Cause**: Desktop-first thinking
**Solution**: Mobile-first wireframes. Show mobile layout FIRST, then progressive enhancement for larger screens.

---

## Success Criteria

- ✅ Wireframes created for all P1 pages (minimum)
- ✅ All components mapped to installable Shadcn components
- ✅ Asset inventory complete (if applicable)
- ✅ Mobile responsive strategy documented
- ✅ Expert evaluation scores documented (5 dimensions)
- ✅ User approval received on layout options
- ✅ Implementation order defined
- ✅ Ready to proceed with Phase 6 (Implementation)

---

## Evidence Requirements (Constitution Article II)

**All wireframes MUST document**:
- **Requirements mapping**: Each page section traced to spec.md user story (file:line)
- **Component rationale**: Why this component vs alternatives (UX, A11y, performance)
- **Design system consistency**: References to design-system.md variables
- **Expert evaluation**: Scores with specific rationale per dimension

**Example Good Evidence**:
"Dashboard hero section (spec.md:line 45 - User Story P1) uses @ui/card with stats grid because: (1) Scannable metrics critical per requirements (spec.md:67), (2) Card component provides semantic grouping for screen readers (A11y score 10/10), (3) Grid layout responsive to mobile (Mobile score 9/10 - tested at 3 breakpoints)."

---

## Anti-Patterns

❌ **Visual mockups** - Token-heavy, hard to iterate, not directly implementable
❌ **Hardcoded values** - Use design system variables only
❌ **Skipping expert evaluation** - Scores provide objective decision criteria
❌ **Undefined mobile strategy** - Mobile-first is mandatory
❌ **Vague component references** - "Some button" → "@ui/button (variant: default, size: lg)"
❌ **No asset placeholders** - Every image needs @assets/filename.ext or unsplash.com reference
❌ **Ignoring accessibility** - WCAG 2.1 AA is minimum standard, not optional

---

## Wireframe Example (Reference)

**Page**: Authentication Login

```markdown
## Login Page (/auth/login)

**Layout**: Centered card on gradient background (full-height viewport)

### Structure
```
Container (h-screen flex items-center justify-center)
  ├── Background: gradient (--background → --muted)
  └── Card: @ui/card (max-w-md w-full p-8)
      ├── Header
      │   ├── Logo: @assets/logo-dark.svg (h-8 mb-4)
      │   ├── Title: h2 text-2xl font-bold
      │   └── Subtitle: text-sm text-muted-foreground
      ├── Form: @ui/form
      │   ├── Email Field
      │   │   ├── Label: @ui/label
      │   │   └── Input: @ui/input (type: email, autocomplete: email)
      │   ├── Password Field
      │   │   ├── Label: @ui/label (with "Forgot?" link)
      │   │   └── Input: @ui/input (type: password)
      │   └── Submit: @ui/button (full-width, variant: default)
      ├── Divider: @ui/separator (text: "or continue with")
      ├── Social Auth
      │   ├── Google: @ui/button (variant: outline, icon: Google logo)
      │   └── GitHub: @ui/button (variant: outline, icon: GitHub logo)
      └── Footer
          └── Link: "Don't have an account? Sign up"
```

**Expert Scores**:
- UX: 9/10 - Clear, focused, minimal friction
- Conversion: 8/10 - Social auth options increase conversion
- A11y: 10/10 - Semantic form, proper labels, keyboard flow
- Mobile: 10/10 - Card scales perfectly, touch-friendly buttons
- SEO: N/A (authenticated page)

**Mobile Adaptations**:
- Card: max-w-md → full-width with px-4
- Button spacing: Increase touch targets to 44x44px minimum
- Social buttons: Stack vertically on mobile

**Components Required**:
- @ui/card, @ui/form, @ui/input, @ui/label, @ui/button, @ui/separator

**Assets Required**:
- @assets/logo-dark.svg (header logo)
```

This example shows the level of detail expected in wireframes without crossing into visual design territory.
