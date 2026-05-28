# UI Design

## Patterns


---
  #### **Name**
8-Point Grid System
  #### **Description**
Use multiples of 8px for all spacing, sizing, and layout to create visual rhythm and consistency
  #### **When**
Setting up spacing, component sizing, and layout systems
  #### **Example**
    Spacing scale (multiples of 8):
    - 4px (0.5): Tight internal padding
    - 8px (1): Default internal spacing
    - 16px (2): Between related elements
    - 24px (3): Between component groups
    - 32px (4): Section padding
    - 48px (6): Large section spacing
    - 64px (8): Major layout divisions
    
    Component heights: 32px, 40px, 48px (buttons, inputs)
    Benefits: Pixel-perfect at 2x, easier math, consistent rhythm
    

---
  #### **Name**
Type Scale Hierarchy
  #### **Description**
Establish clear typographic hierarchy using size, weight, and spacing
  #### **When**
Designing content-heavy interfaces, dashboards, or documentation
  #### **Example**
    Type scale (1.25 ratio):
    - Display: 48px/52px (hero headings)
    - H1: 40px/44px (page titles)
    - H2: 32px/36px (section headings)
    - H3: 24px/28px (subsections)
    - Body Large: 18px/28px (hero copy, intros)
    - Body: 16px/24px (default text)
    - Body Small: 14px/20px (captions, metadata)
    - Label: 12px/16px (form labels, tags)
    
    Weight hierarchy: Display (700), Headings (600), Body (400), Metadata (500)
    

---
  #### **Name**
Accessible Color Contrast
  #### **Description**
Ensure all text and interactive elements meet WCAG AA contrast requirements minimum
  #### **When**
Defining color systems, creating themes, designing components
  #### **Example**
    Contrast ratios required:
    - Normal text: 4.5:1 minimum (WCAG AA)
    - Large text (18px+): 3:1 minimum
    - Interactive elements: 3:1 against background
    - AAA standard: 7:1 (preferable for body text)
    
    Tools: Contrast checker, Stark plugin
    
    Example:
    ✓ #0066FF text on #FFFFFF background = 5.9:1 (Pass AA)
    ✗ #6B7280 text on #F3F4F6 background = 2.1:1 (Fail)
    

---
  #### **Name**
Component State Mapping
  #### **Description**
Design all interactive states for every component to ensure complete system coverage
  #### **When**
Creating design system components or designing new interactive elements
  #### **Example**
    Required states for buttons:
    - Default (resting state)
    - Hover (mouse over)
    - Focus (keyboard navigation, 2px outline)
    - Active (being clicked)
    - Disabled (not interactive, 40% opacity)
    - Loading (spinner, disabled interaction)
    
    For inputs, add:
    - Empty
    - Filled
    - Error (red border, error message)
    - Success (green checkmark)
    
    No component is complete without all states designed.
    

---
  #### **Name**
Progressive Enhancement with Motion
  #### **Description**
Use animation to clarify relationships and guide attention, never just for decoration
  #### **When**
Adding transitions, loading states, or interactive feedback
  #### **Example**
    Purposeful motion:
    - Modal entrance: Scale from 0.95 to 1.0 (shows origin)
    - Dropdown: Slide down with fade (shows hierarchy)
    - Button click: Scale to 0.98 (confirms interaction)
    - Loading: Skeleton screens → content (shows progress)
    - Page transitions: Fade content (reduces jarring switches)
    
    Duration: 150-300ms (feels instant but perceptible)
    Easing: ease-out (starts fast, ends slow)
    
    Remove motion for prefers-reduced-motion users
    

---
  #### **Name**
Design Token System
  #### **Description**
Abstract design decisions into reusable tokens that can be referenced and updated globally
  #### **When**
Building design systems that need to scale or support theming
  #### **Example**
    Color tokens:
    - Primitive: blue-500: #0066FF (raw values)
    - Semantic: color-primary: blue-500 (intent-based)
    - Component: button-bg-primary: color-primary (specific use)
    
    Spacing tokens:
    - space-xs: 4px
    - space-sm: 8px
    - space-md: 16px
    - space-lg: 24px
    
    Export as CSS variables, JavaScript objects, or platform tokens
    Benefits: Change once, update everywhere; themeable; consistent
    

## Anti-Patterns


---
  #### **Name**
Pixel Pushing Without Purpose
  #### **Description**
Obsessing over visual polish before validating that the design actually works for users
  #### **Why**
Beautiful but unusable is failure. Polish comes after proving the concept works.
  #### **Instead**
    Design progression:
    1. Low-fidelity wireframes (validate structure and flow)
    2. Prototype core interactions (test usability)
    3. Apply visual design (hierarchy, color, typography)
    4. Polish details (spacing, shadows, transitions)
    
    Test early, polish late. Don't spend 3 hours on a button no one will click.
    

---
  #### **Name**
Inconsistent Spacing
  #### **Description**
Using arbitrary spacing values instead of a consistent scale
  #### **Why**
Creates visual noise, slows development, makes the interface feel unpolished even if you can't pinpoint why.
  #### **Instead**
    Bad: 7px, 13px, 19px, 25px (random)
    Good: 8px, 16px, 24px, 32px (8pt scale)
    
    Implement with design tokens:
    margin: var(--space-md) /* 16px */
    
    Consistency creates rhythm. Rhythm creates calm.
    

---
  #### **Name**
Low-Contrast Text
  #### **Description**
Using light gray text on white backgrounds for aesthetic reasons
  #### **Why**
Fails accessibility standards, hurts readability, excludes users with vision impairments.
  #### **Instead**
    Bad: #9CA3AF text on #FFFFFF (2.8:1 - fails WCAG)
    Good: #4B5563 text on #FFFFFF (8.6:1 - passes AAA)
    
    Hierarchy through size and weight, not low contrast.
    Use color contrast checkers in design tools.
    

---
  #### **Name**
Decoration-Only Icons
  #### **Description**
Using icons without text labels to save space or look minimal
  #### **Why**
Icon meanings aren't universal. Users guess wrong, miss features, get frustrated.
  #### **Instead**
    Always pair icons with text labels, except for universally understood icons:
    - ✓ Search (magnifying glass)
    - ✓ Settings (gear)
    - ✓ Close (X)
    - ✓ Menu (hamburger)
    
    For everything else: icon + label
    Or use tooltips on hover (but not on mobile)
    

---
  #### **Name**
Over-Designed Micro-Interactions
  #### **Description**
Adding excessive animations, hover effects, and transitions everywhere
  #### **Why**
Slow, distracting, increases cognitive load. Motion should clarify, not impress.
  #### **Instead**
    Motion rules:
    - Only animate to clarify cause and effect
    - Duration <300ms (longer feels sluggish)
    - Respect prefers-reduced-motion
    - Test on low-end devices
    
    Example: Dropdown slides down from trigger (shows relationship)
    Counter-example: Button pulses on hover (pointless distraction)
    

---
  #### **Name**
Copying Popular Designs Without Context
  #### **Description**
Replicating Stripe/Linear/Apple designs because they look good, ignoring different user needs
  #### **Why**
What works for their users and use cases may not work for yours. Context matters.
  #### **Instead**
    Instead of "make it look like Linear":
    1. Understand why Linear made those choices
    2. Identify your users' needs and constraints
    3. Design for your context
    4. Borrow principles, not pixels
    
    Stripe's spacing works for sparse data. Your dense dashboard needs different hierarchy.
    