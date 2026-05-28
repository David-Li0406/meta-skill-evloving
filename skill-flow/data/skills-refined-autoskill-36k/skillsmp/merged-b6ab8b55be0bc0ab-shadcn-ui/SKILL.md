---
name: shadcn-ui
description: Use this skill when building modern React UIs with accessible, customizable components from the shadcn/ui library, utilizing Tailwind CSS for styling and Radix UI for accessibility.
---

# shadcn/ui Component Library

shadcn/ui is a collection of beautifully-designed, accessible components built with TypeScript, Tailwind CSS, and Radix UI primitives. It supports multiple frameworks including Next.js, Vite, Remix, Astro, and more. This skill provides guidelines for installation, configuration, and implementation of UI components.

## Key Principles

- **Copy, Don't Install**: Components are copied into your project, not installed as dependencies.
- **Customizable**: Modify components directly in your codebase.
- **Accessible**: Built on Radix UI primitives with ARIA support.
- **Type-Safe**: Full TypeScript support.
- **Composable**: Build complex UIs from simple primitives.

## Quick Start

### Installation

```bash
# Initialize shadcn/ui in your project
npx shadcn@latest init

# Add components
npx shadcn@latest add button input form card dialog select
```

### Project Structure

```
src/
├── components/
│   └── ui/           # shadcn components
│       ├── button.tsx
│       ├── card.tsx
│       └── input.tsx
├── lib/
│   └── utils.ts      # cn() utility
└── app/
    └── globals.css   # CSS variables
```

## Core Components

### Button Component

Basic usage:

```tsx
import { Button } from "@/components/ui/button";

export function ButtonDemo() {
  return <Button>Click me</Button>;
}
```

Button variants:

```tsx
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
```

### Input Component

Basic input:

```tsx
import { Input } from "@/components/ui/input";

export function InputDemo() {
  return <Input type="email" placeholder="Email" />;
}
```

### Form with Validation

Using React Hook Form and Zod for validation:

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <FormField
        control={form.control}
        name="email"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl>
              <Input {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <Button type="submit">Submit</Button>
    </form>
  );
}
```

### Dialog Component

Basic dialog:

```tsx
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";

export function DialogDemo() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Open Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <h2>Edit profile</h2>
        {/* Form or content goes here */}
      </DialogContent>
    </Dialog>
  );
}
```

## Theming with CSS Variables

shadcn/ui uses CSS variables for theming. Configure in `globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    /* ... other variables ... */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... other dark mode variables ... */
  }
}
```

## Accessibility Checklist

- [ ] All interactive elements are keyboard accessible.
- [ ] Focus states are visible.
- [ ] Color contrast meets WCAG AA standards.
- [ ] ARIA labels on icon-only buttons.
- [ ] Form inputs have associated labels.
- [ ] Error messages are announced to screen readers.

## Common Patterns

### Form with Multiple Fields

```tsx
const formSchema = z.object({
  username: z.string().min(2),
  email: z.string().email(),
  // ... other fields ...
});

export function AdvancedForm() {
  const form = useForm({
    resolver: zodResolver(formSchema),
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields go here */}
      <Button type="submit">Submit</Button>
    </form>
  );
}
```

## References

- Official Docs: [shadcn/ui Documentation](https://ui.shadcn.com)
- Radix UI: [Radix UI](https://www.radix-ui.com)
- React Hook Form: [React Hook Form](https://react-hook-form.com)
- Zod: [Zod](https://zod.dev)
- Tailwind CSS: [Tailwind CSS](https://tailwindcss.com)