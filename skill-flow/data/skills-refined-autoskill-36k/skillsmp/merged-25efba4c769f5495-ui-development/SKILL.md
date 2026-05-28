---
name: ui-development
description: Use this skill when building, styling, or refactoring UI components, forms, and layouts with shadcn/ui and Tailwind CSS, ensuring accessibility and progressive enhancement.
---

# UI Development Guide

## When to Use This Skill

Use this skill when:
- Building or modifying UI components
- Creating forms and handling form validation
- Working with shadcn/ui components
- Styling with Tailwind CSS
- Implementing progressive enhancement
- Ensuring accessibility in UI design
- User mentions: "UI", "component", "form", "styling", "Tailwind", "shadcn", "button", "input"

## Key Technologies

- **shadcn/ui**: Component library built on Radix UI
- **Tailwind CSS**: Utility-first CSS framework
- **Radix UI**: Accessible component primitives
- **Lucide Icons**: Icon library

## Critical UI Rules

1. **Server Components first**: Default to Server Components, use "use client" only for interactivity.
2. **Progressive enhancement**: Forms must work without JavaScript.
3. **shadcn/ui only**: No MUI components.
4. **Direct Server Action references**: No inline wrappers in forms.
5. **Dropdown Server Actions**: Use `onSelect`, not forms.
6. **Tailwind CSS**: Use CSS variables, no hardcoded hex colors.

## Component Structure

- Place components in `src/components/`
- Use PascalCase for component names
- Export as default from index files

## Styling Guidelines

- Use Tailwind CSS classes
- Follow design system colors and spacing
- Ensure responsive design
- Organize classes consistently: layout → sizing → spacing → typography → colors → effects

## Accessibility Patterns

- Use Radix UI primitives for accessibility
- Add proper ARIA labels and roles
- Test with screen readers
- Use semantic HTML for better accessibility

## Examples

### Button Component

```tsx
// src/components/ui/button.tsx
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
}

export function Button({ className, variant = 'default', size = 'default', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors',
        {
          'bg-primary text-primary-foreground hover:bg-primary/90': variant === 'default',
          'bg-destructive text-destructive-foreground hover:bg-destructive/90': variant === 'destructive',
          'border border-input bg-background hover:bg-accent hover:text-accent-foreground': variant === 'outline',
          'bg-secondary text-secondary-foreground hover:bg-secondary/80': variant === 'secondary',
          'hover:bg-accent hover:text-accent-foreground': variant === 'ghost',
          'text-primary underline-offset-4 hover:underline': variant === 'link',
        },
        {
          'h-10 px-4 py-2': size === 'default',
          'h-9 rounded-md px-3': size === 'sm',
          'h-11 rounded-md px-8': size === 'lg',
          'h-10 w-10': size === 'icon',
        },
        className
      )}
      {...props}
    />
  );
}
```

### Form with Validation

```tsx
// src/components/forms/LoginForm.tsx
'use client';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl>
              <Input placeholder="your@email.com" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <FormField control={form.control} name="password" render={({ field }) => (
          <FormItem>
            <FormLabel>Password</FormLabel>
            <FormControl>
              <Input type="password" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit" className="w-full">Log In</Button>
      </form>
    </Form>
  );
}
```

### Modal Component

```tsx
// src/components/ui/dialog.tsx
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

export const Dialog = DialogPrimitive.Root;
export const DialogTrigger = DialogPrimitive.Trigger;
export const DialogPortal = DialogPrimitive.Portal;
export const DialogClose = DialogPrimitive.Close;

export const DialogOverlay = React.forwardRef(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn('fixed inset-0 z-50 bg-black/80', className)}
    {...props}
  />
));

export const DialogContent = React.forwardRef(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn('fixed top-[50%] left-[50%] z-50 max-w-lg p-6 bg-background shadow-lg', className)}
      {...props}
    >
      {children}
      <DialogClose className="absolute top-4 right-4">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogClose>
    </DialogPrimitive.Content>
  </DialogPortal>
));
```

## UI Checklist

Before committing UI code:
- [ ] Server Components by default (only "use client" when needed)
- [ ] Forms work without JavaScript
- [ ] Direct Server Action references (no inline wrappers)
- [ ] Dropdowns use `onSelect` for Server Actions
- [ ] CSS variables, no hardcoded colors
- [ ] `cn()` used for className merging
- [ ] Semantic HTML (nav, main, article, etc.)
- [ ] ARIA labels for icon-only buttons
- [ ] Responsive design (mobile-first)
- [ ] shadcn/ui components only (no MUI)

## Additional Resources

- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Radix UI Documentation](https://www.radix-ui.com/)
- Project components: `src/components/`
- Styles: `src/styles/globals.css`