---
name: Create Shadcn Component
description: Workflow to create standardized, accessible, and theme-compatible UI components extending the Shadcn/UI system.
version: 1.0.0
---

# Skill: Create Shadcn Component Extension

This skill guides the creation of composite or extended UI components in ATLAS.
Unlike primitives (in `components/ui`), these are often specialized versions (e.g., a "SearchableUserSelect" or "StatusBadge") that combine logic with UI.

## Execution Steps

### 1. Identify Component Type
Is it:
- **Pure UI**: Just styling (e.g., a specific Card variant)? -> Place in `components/ui/extension/` (create if needed).
- **Logic + UI**: Connects to data? -> Place in `components/[module]/` or `components/common/`.
- **Form Element**: Input requiring validation? -> Must wrap `React.forwardRef`.

### 2. Component Template
Create the file `[kebab-case-name].tsx`. Use this standard pattern:

```typescript
"use client"

import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"
// Import primitives if needed, e.g. import { Button } from "@/components/ui/button"

// 1. Define Variants (Optional)
const componentVariants = cva(
  "base-styles-here flex items-center ...", 
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        outline: "border border-input bg-background",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

// 2. Define Props
export interface [Name]Props
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof componentVariants> {
  // Add custom props here
  customProp?: string
}

// 3. Component Definition
const [Name] = React.forwardRef<HTMLDivElement, [Name]Props>(
  ({ className, variant, size, customProp, ...props }, ref) => {
    return (
      <div
        className={cn(componentVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      >
        {/* Component Logic */}
        {children}
      </div>
    )
  }
)
[Name].displayName = "[Name]"

export { [Name], componentVariants }
```

### 3. Requirements Checklist
- [ ] **Dark Mode**: Verify manually that colors use Tailwind vars (e.g., `bg-background`, `text-primary`) and NOT hardcoded hex or slate-50/900 unless necessary for a specific effect.
- [ ] **Accessibility**: If interactive, does it use Radix primitives? Does it handle keyboard navigation?
- [ ] **Responsiveness**: Does it look broken on mobile?

### 4. Integration
If this component is meant to be global, export it from a barrel file or suggest adding it to the `components/agents.md` documentation.
