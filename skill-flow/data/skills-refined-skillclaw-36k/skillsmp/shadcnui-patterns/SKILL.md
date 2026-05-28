---
name: shadcn/ui Patterns
description: Build polished, accessible UI with shadcn/ui components following FrankX design system
version: 1.0.0
---

# shadcn/ui Patterns for FrankX

## Purpose
Create distinctive, production-grade interfaces using shadcn/ui components with FrankX's glassmorphic design system. This skill ensures consistent component usage, proper accessibility, and avoidance of generic AI aesthetics.

## FrankX Project Configuration

```json
{
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "baseColor": "neutral",
  "cssVariables": true,
  "iconLibrary": "lucide",
  "aliases": {
    "ui": "@/components/ui",
    "utils": "@/lib/utils"
  }
}
```

## Core Principles

### 1. Design-First Approach
Before coding any component:
- Establish a bold aesthetic direction (glassmorphic, aurora gradients, etc.)
- Choose typography that elevates (not defaults)
- Avoid generic AI aesthetics - make intentional creative choices

### 2. Component Structure
```
components/
├── ui/
│   ├── primitives/     # shadcn base components (button, input, etc.)
│   ├── magic-ui/       # Enhanced motion components
│   └── [Custom].tsx    # FrankX-specific components
```

## Installing New Components

```bash
# Add shadcn components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add toast
```

## Essential Patterns

### Button Variants
```tsx
import { Button } from "@/components/ui/primitives/button"

// FrankX uses premium button styling
<Button variant="default">Primary Action</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Destructive</Button>

// With loading state
<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  Submit
</Button>
```

### Cards with Glassmorphic Styling
```tsx
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

// FrankX glassmorphic card pattern
<Card className="bg-white/5 backdrop-blur-xl border-white/10 hover:border-white/20 transition-all">
  <CardHeader>
    <CardTitle className="text-xl font-semibold">Title</CardTitle>
    <CardDescription className="text-neutral-400">Description</CardDescription>
  </CardHeader>
  <CardContent>
    {/* Content */}
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### Form with Validation
```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  email: z.string().email("Invalid email address"),
  name: z.string().min(2, "Name must be at least 2 characters"),
})

function EmailForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", name: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Subscribe</Button>
      </form>
    </Form>
  )
}
```

### Dialog / Modal
```tsx
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open</Button>
  </DialogTrigger>
  <DialogContent className="bg-neutral-900/95 backdrop-blur-xl border-white/10">
    <DialogHeader>
      <DialogTitle>Modal Title</DialogTitle>
      <DialogDescription>Description text here.</DialogDescription>
    </DialogHeader>
    {/* Content */}
  </DialogContent>
</Dialog>
```

### Toast Notifications
```tsx
import { toast } from "sonner"

// Success
toast.success("Changes saved successfully")

// Error
toast.error("Something went wrong")

// Promise handling
toast.promise(saveData(), {
  loading: "Saving...",
  success: "Saved!",
  error: "Failed to save"
})
```

## FrankX Design System Integration

### Color Tokens (CSS Variables)
```css
/* Aurora gradient colors */
--aurora-1: #00d4ff;
--aurora-2: #7c3aed;
--aurora-3: #f472b6;

/* Glass effects */
--glass-bg: rgba(255, 255, 255, 0.05);
--glass-border: rgba(255, 255, 255, 0.1);
--glass-hover: rgba(255, 255, 255, 0.15);
```

### Glassmorphic Utilities
```tsx
// Standard glass card
className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-xl"

// Elevated glass
className="bg-white/10 backdrop-blur-2xl border border-white/20 shadow-2xl rounded-2xl"

// Interactive glass
className="bg-white/5 backdrop-blur-xl border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all duration-300"
```

### Typography Classes
```tsx
// Headlines
className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-white via-aurora-1 to-aurora-2 bg-clip-text text-transparent"

// Body text
className="text-neutral-300 leading-relaxed"

// Muted text
className="text-neutral-500 text-sm"
```

## Accessibility Requirements

1. **Focus States**: All interactive elements must have visible focus rings
   ```tsx
   className="focus-visible:ring-2 focus-visible:ring-aurora-1 focus-visible:ring-offset-2"
   ```

2. **Color Contrast**: Ensure 4.5:1 minimum for body text, 3:1 for large text

3. **Screen Reader Support**: Use proper ARIA labels
   ```tsx
   <Button aria-label="Close dialog">
     <X className="h-4 w-4" />
   </Button>
   ```

4. **Keyboard Navigation**: All components must be keyboard accessible

## What to Avoid

- Generic purple gradients without purpose
- Cookie-cutter layouts lacking FrankX character
- Overused typefaces (use Inter sparingly, prefer distinctive choices)
- Missing loading/error states
- Components without hover/focus feedback
- Non-responsive designs

## When to Use This Skill

- Building new UI components for FrankX.AI
- Creating forms, modals, or interactive elements
- Implementing design system components
- Ensuring accessibility compliance

## Related Skills

- `ui-ux-design-expert` - High-level design decisions
- `nextjs-react-expert` - React patterns and Next.js specifics
- `framer-expert` - Animation and motion design

## Resources

- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Radix UI Primitives](https://radix-ui.com)
- [Tailwind CSS](https://tailwindcss.com)
- FrankX Design System: `docs/DESIGN_SYSTEM_GUIDE.md`
