# shadcn/ui Methodology

## shadcn/ui Component Architecture

### Principles

1. **Copy, don't install** - Components are copied to your codebase, not npm packages
2. **Composition over inheritance** - Build complex UIs from simple primitives
3. **Design separate from implementation** - Headless behavior + styled presentation

### Directory Structure

```
src/
├── components/
│   ├── ui/              # shadcn primitives (Button, Card, Dialog)
│   ├── forms/           # Form-specific compositions
│   ├── layout/          # Layout components
│   └── [feature]/       # Feature-specific components
├── lib/
│   └── utils.ts         # cn() helper
└── styles/
    └── globals.css      # CSS variables, @tailwind directives
```

### Component Patterns

**1. Primitive + Composition:**
```tsx
// ui/button.tsx - primitive
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      {...props}
    />
  )
)

// components/submit-button.tsx - composition
export function SubmitButton({ loading, children }: SubmitButtonProps) {
  return (
    <Button type="submit" disabled={loading}>
      {loading ? <Spinner /> : children}
    </Button>
  )
}
```

**2. Variant Management (CVA):**
```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

**3. Compound Components:**
```tsx
// Card with subcomponents
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

### Installation

```bash
# Init shadcn in project
npx shadcn@latest init

# Add components
npx shadcn@latest add button card dialog form

# Add multiple
npx shadcn@latest add button card input label
```

### MCP Integration

With shadcn MCP server installed, use natural language:
- "Add a dialog component"
- "Install the form components"
- "What props does Button accept?"

### Best Practices

| Do | Don't |
|----|-------|
| Extend via composition | Modify ui/ files directly |
| Use CSS variables for theming | Hardcode colors |
| Keep ui/ as primitives | Add business logic to ui/ |
| Use cn() for class merging | String concatenation |
| Implement accessibility | Skip ARIA attributes |

### Accessibility Checklist

- [ ] Semantic HTML (button, not div)
- [ ] ARIA labels where needed
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Focus management in modals
- [ ] Color contrast ratios

### Theming

```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    /* ... */
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... */
  }
}
```

### Anti-patterns

1. **Don't:** Inline everything without extraction
2. **Don't:** Ignore the variant system
3. **Don't:** Mix Tailwind arbitrary values with design tokens
4. **Don't:** Skip forwardRef for DOM components
5. **Don't:** Forget displayName for debugging

---

*shadcn/ui Component Architecture*
*Sources: [shadcn/ui docs](https://ui.shadcn.com/docs), [Anatomy of shadcn/ui](https://manupa.dev/blog/anatomy-of-shadcn-ui)*
