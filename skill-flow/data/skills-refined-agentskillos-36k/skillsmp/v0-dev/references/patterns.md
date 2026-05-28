# v0.dev

## Patterns


---
  #### **Name**
Effective Prompting
  #### **Description**
Structure prompts for best results
  #### **When To Use**
Any v0 generation
  #### **Implementation**
    # Prompt Structure for Best Results:
    
    ## 1. Be Specific About Components
    # BAD
    "Create a login form"
    
    # GOOD
    "Create a login form with:
    - Email input with validation
    - Password input with show/hide toggle
    - 'Remember me' checkbox
    - Submit button (disabled until valid)
    - 'Forgot password' link
    - Social login buttons (Google, GitHub)
    Use shadcn/ui Card, Input, Button, Checkbox components"
    
    ## 2. Specify Design Constraints
    # BAD
    "Make it look nice"
    
    # GOOD
    "Design constraints:
    - Max width 400px, centered
    - Dark mode support
    - Mobile-first responsive
    - Subtle shadows, rounded corners
    - Primary color for submit button"
    
    ## 3. Include Behavior
    # BAD
    "Add form handling"
    
    # GOOD
    "Behavior:
    - Show loading spinner on submit
    - Display error message below form on failure
    - Disable form while submitting
    - Redirect on success (placeholder)"
    
    ## 4. Reference Existing Patterns
    # BAD
    "Like a modern app"
    
    # GOOD
    "Similar to:
    - Vercel dashboard login
    - Linear app onboarding
    - Stripe checkout form style"
    
    ## 5. Mention Accessibility
    "Ensure:
    - Proper label associations
    - Focus states visible
    - Error messages announced to screen readers
    - Keyboard navigation works"
    

---
  #### **Name**
Component Iteration
  #### **Description**
Refine components through conversation
  #### **When To Use**
Improving generated output
  #### **Implementation**
    # Iteration Strategy:
    
    ## Step 1: Generate Base Component
    "Create a pricing card with:
    - Plan name and price
    - Feature list with check icons
    - CTA button
    Use shadcn Card and Button"
    
    ## Step 2: Refine Specific Elements
    "Update the pricing card:
    - Make the 'Pro' plan highlighted with a border
    - Add 'Most Popular' badge
    - Show annual/monthly toggle price"
    
    ## Step 3: Add States
    "Add to the pricing card:
    - Hover state with subtle scale
    - Loading state for CTA button
    - Disabled state for unavailable plans"
    
    ## Step 4: Improve Responsive
    "Make pricing cards:
    - Stack vertically on mobile
    - 3 columns on desktop
    - Equal heights in row"
    
    ## Step 5: Polish Details
    "Final touches:
    - Add subtle gradient to highlighted card
    - Animate feature list on hover
    - Add tooltip for 'i' icons"
    
    # Tips for Iteration:
    # - Reference specific parts: "the submit button"
    # - Be precise: "change padding to 24px" not "add more space"
    # - Ask for variants: "create hover and active states"
    # - Request alternatives: "show 3 different layouts"
    

---
  #### **Name**
Export and Integration
  #### **Description**
Move v0 components to your codebase
  #### **When To Use**
Using generated components
  #### **Implementation**
    # Step 1: Export from v0
    # Click "Code" tab, then "Copy"
    # Or use CLI: npx v0 add <component-url>
    
    # Step 2: Set Up shadcn/ui (if not done)
    npx shadcn-ui@latest init
    
    # Step 3: Add Required Components
    # v0 will tell you which components are needed
    npx shadcn-ui@latest add button card input
    
    # Step 4: Create Component File
    # components/pricing-card.tsx
    import { Button } from "@/components/ui/button"
    import { Card, CardContent, CardHeader } from "@/components/ui/card"
    
    interface PricingCardProps {
      plan: string
      price: number
      features: string[]
      isPopular?: boolean
      onSelect: () => void
    }
    
    export function PricingCard({
      plan,
      price,
      features,
      isPopular = false,
      onSelect
    }: PricingCardProps) {
      // v0 generated code here, adapted with props
      return (
        <Card className={isPopular ? "border-primary" : ""}>
          {/* ... */}
        </Card>
      )
    }
    
    # Step 5: Customize for Your Design System
    # - Replace hardcoded colors with CSS variables
    # - Use your typography scale
    # - Match your spacing conventions
    # - Add your animation preferences
    
    # Step 6: Add Tests
    import { render, screen } from "@testing-library/react"
    import { PricingCard } from "./pricing-card"
    
    test("renders plan name", () => {
      render(<PricingCard plan="Pro" price={29} features={[]} onSelect={() => {}} />)
      expect(screen.getByText("Pro")).toBeInTheDocument()
    })
    

---
  #### **Name**
Complex Layouts
  #### **Description**
Generate multi-component layouts
  #### **When To Use**
Building full pages or sections
  #### **Implementation**
    # Strategy: Build in Layers
    
    ## Layer 1: Shell/Layout
    "Create a dashboard layout with:
    - Collapsible sidebar (icons only when collapsed)
    - Top header with search and user menu
    - Main content area with padding
    - Mobile: bottom navigation instead of sidebar
    Use shadcn Sheet for mobile menu"
    
    ## Layer 2: Major Sections
    "Create a stats overview section with:
    - 4 metric cards in a row (stack on mobile)
    - Each card: icon, label, value, trend indicator
    - Subtle hover effect
    Use shadcn Card"
    
    ## Layer 3: Data Components
    "Create a data table with:
    - Sortable columns
    - Row selection with checkboxes
    - Pagination
    - Empty state
    - Loading skeleton
    Use shadcn Table and Skeleton"
    
    ## Layer 4: Interactive Elements
    "Create a filter bar with:
    - Search input
    - Date range picker
    - Status dropdown (multi-select)
    - Clear all button
    Use shadcn Popover, Calendar, Command"
    
    ## Layer 5: Empty/Error States
    "Create states for the table:
    - Empty: illustration, message, CTA button
    - Error: retry button, support link
    - No results: clear filters suggestion"
    
    # Combine in Your Codebase:
    // app/dashboard/page.tsx
    import { DashboardShell } from "@/components/dashboard-shell"
    import { StatsOverview } from "@/components/stats-overview"
    import { DataTable } from "@/components/data-table"
    import { FilterBar } from "@/components/filter-bar"
    
    export default function Dashboard() {
      return (
        <DashboardShell>
          <StatsOverview />
          <FilterBar />
          <DataTable />
        </DashboardShell>
      )
    }
    

---
  #### **Name**
Design System Alignment
  #### **Description**
Match v0 output to your design system
  #### **When To Use**
Consistent brand application
  #### **Implementation**
    # Include Design Tokens in Prompts
    
    ## Color System
    "Use this color scheme:
    - Primary: blue-600 (#2563eb)
    - Secondary: slate-600
    - Accent: amber-500
    - Background: slate-50 (light) / slate-900 (dark)
    - Text: slate-900 (light) / slate-50 (dark)"
    
    ## Typography
    "Typography:
    - Headings: font-semibold, tracking-tight
    - Body: text-base, text-slate-600
    - Small: text-sm, text-slate-500
    - Use Inter font family"
    
    ## Spacing
    "Spacing:
    - Card padding: p-6
    - Section gap: gap-8
    - Inline spacing: gap-2
    - Border radius: rounded-lg (default), rounded-full (avatars)"
    
    ## Shadows
    "Shadows:
    - Cards: shadow-sm
    - Dropdowns: shadow-lg
    - Modals: shadow-xl
    - Hover: shadow-md transition"
    
    ## Motion
    "Animations:
    - Transitions: duration-200, ease-out
    - Hover scale: scale-[1.02]
    - Use Tailwind animate utilities"
    
    # After Export: CSS Variables
    /* globals.css */
    :root {
      --primary: 221.2 83.2% 53.3%;
      --primary-foreground: 210 40% 98%;
      --radius: 0.5rem;
    }
    
    # Component Customization
    // Extend shadcn components
    const Button = React.forwardRef<...>(({ className, ...props }, ref) => (
      <button
        className={cn(
          buttonVariants({ variant, size }),
          "font-semibold tracking-tight",  // Your additions
          className
        )}
        ref={ref}
        {...props}
      />
    ))
    

## Anti-Patterns


---
  #### **Name**
Vague Prompts
  #### **Description**
"Make it look good" or "create a form"
  #### **Why Bad**
    v0 guesses at requirements.
    Output needs more iteration.
    Inconsistent results.
    
  #### **What To Do Instead**
    Be specific about:
    - Exact components to use
    - Layout and spacing
    - States and interactions
    - Accessibility requirements
    

---
  #### **Name**
Generating Entire Apps
  #### **Description**
Trying to build full pages in one prompt
  #### **Why Bad**
    Hard to iterate on parts.
    Complex prompts get confused.
    Can't reuse components.
    
  #### **What To Do Instead**
    Build component by component.
    Generate reusable pieces.
    Compose in your codebase.
    

---
  #### **Name**
Copy-Paste Without Review
  #### **Description**
Using generated code directly
  #### **Why Bad**
    May have accessibility issues.
    Hardcoded values.
    Inconsistent with your codebase.
    
  #### **What To Do Instead**
    Review for accessibility.
    Replace hardcoded values with props.
    Match your naming conventions.
    Add TypeScript types.
    

---
  #### **Name**
Ignoring Mobile
  #### **Description**
Not specifying responsive behavior
  #### **Why Bad**
    v0 defaults may not match needs.
    Breakpoints might be wrong.
    Touch targets too small.
    
  #### **What To Do Instead**
    Always specify mobile behavior.
    Test at multiple breakpoints.
    Consider touch interactions.
    