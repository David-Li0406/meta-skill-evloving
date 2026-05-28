---
name: ui-components
description: Specialized skill for creating consistent UI components using shadcn/ui and TailwindCSS. Use when building forms, buttons, modals, or other reusable UI elements.
---

# UI Components Skill

This skill provides expertise in building consistent and accessible UI components using shadcn/ui and TailwindCSS in the Artiefy project.

## When to Use This Skill

- Creating new reusable UI components
- Implementing forms and form validation
- Building modals, dialogs, and overlays
- Adding buttons, inputs, and other form controls
- Ensuring design consistency across the app

## Key Technologies

- **shadcn/ui**: Component library built on Radix UI
- **TailwindCSS**: Utility-first CSS framework
- **Radix UI**: Accessible component primitives
- **Lucide Icons**: Icon library

## Patterns and Conventions

### Component Structure

- Place in `src/components/`
- Use PascalCase for component names
- Export as default from index files

### Styling

- Use TailwindCSS classes
- Follow design system colors and spacing
- Ensure responsive design

### Accessibility

- Use Radix UI primitives for accessibility
- Add proper ARIA labels and roles
- Test with screen readers

## Examples

### Button Component

```tsx
// src/components/ui/button.tsx
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?:
    | 'default'
    | 'destructive'
    | 'outline'
    | 'secondary'
    | 'ghost'
    | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
}

export function Button({
  className,
  variant = 'default',
  size = 'default',
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors',
        'focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none',
        'disabled:pointer-events-none disabled:opacity-50',
        {
          'bg-primary text-primary-foreground hover:bg-primary/90':
            variant === 'default',
          'bg-destructive text-destructive-foreground hover:bg-destructive/90':
            variant === 'destructive',
          'border border-input bg-background hover:bg-accent hover:text-accent-foreground':
            variant === 'outline',
          'bg-secondary text-secondary-foreground hover:bg-secondary/80':
            variant === 'secondary',
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
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';

const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'Contraseña debe tener al menos 6 caracteres'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data: LoginFormData) => {
    console.log(data);
  };

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
                <Input placeholder="tu@email.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Contraseña</FormLabel>
              <FormControl>
                <Input type="password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">
          Iniciar Sesión
        </Button>
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

export const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      'data-[state=open]:animate-in data-[state=closed]:animate-out fixed inset-0 z-50 bg-black/80',
      'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
      className
    )}
    {...props}
  />
));

export const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        'fixed top-[50%] left-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%]',
        'gap-4 border bg-background p-6 shadow-lg duration-200',
        'data-[state=open]:animate-in data-[state=closed]:animate-out',
        'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
        'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
        'data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%]',
        'data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]',
        'sm:rounded-lg',
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute top-4 right-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:ring-2 focus:ring-ring focus:ring-offset-2 focus:outline-none disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));
```

## Resources

- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [Radix UI Documentation](https://www.radix-ui.com/)
- Project components: `src/components/`
- Styles: `src/styles/globals.css`
