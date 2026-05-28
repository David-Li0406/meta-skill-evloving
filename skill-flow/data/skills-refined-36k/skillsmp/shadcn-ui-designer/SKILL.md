---
name: shadcn-ui-designer
description: Expert frontend design and implementation using shadcn/ui components for Next.js and React applications. Use when building user interfaces, implementing UI features, creating forms, dashboards, data tables, modals, navigation, or any frontend component work. Covers component selection, composition patterns, responsive design, theming, and accessibility best practices with shadcn/ui.
---

# shadcn/ui Designer

Build modern, accessible user interfaces with shadcn/ui components in Next.js/React.

## Quick Start Workflow

1. **Understand requirements** - Identify what UI needs to be built
2. **Select components** - Choose appropriate shadcn components (see [component-catalog.md](references/component-catalog.md))
3. **Install components** - Run `npx shadcn@latest add <component-name>`
4. **Compose UI** - Build the interface using composition patterns (see [composition-patterns.md](references/composition-patterns.md))
5. **Test and refine** - Ensure responsiveness and accessibility

## Component Selection

Use [references/component-catalog.md](references/component-catalog.md) to find the right component for your needs.

### Quick Decision Tree

**Building a form?**
- Simple → Input + Label + Button
- With validation → Form component + react-hook-form + zod
- See: Form Patterns in [composition-patterns.md](references/composition-patterns.md)

**Need a modal?**
- General modal → Dialog
- Confirmation → Alert Dialog
- Side panel → Sheet
- Hover info → Tooltip
- Click info → Popover

**Displaying data?**
- Simple table → Table
- Advanced table with sorting/filtering → Data Table (tanstack/react-table)
- List of items → Card Grid
- Stats/metrics → Stats Grid (Cards)

**Navigation?**
- Desktop nav → Navigation Menu
- Mobile nav → Sheet (drawer)
- Tabs → Tabs component
- Full layout → Sidebar Pattern

**User feedback?**
- Temporary notification → Toast/Sonner
- Persistent message → Alert
- Loading state → Skeleton, Progress, or Loader2 icon

## Installation Commands

```bash
# Install shadcn in new project
npx shadcn@latest init

# Add single component
npx shadcn@latest add button

# Add multiple components
npx shadcn@latest add button input label card dialog

# Common starter set
npx shadcn@latest add button input label card dialog toast
```

## Implementation Patterns

### Pattern 1: Simple Form
```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

<form>
  <div className="space-y-4">
    <div className="space-y-2">
      <Label htmlFor="email">Email</Label>
      <Input id="email" type="email" />
    </div>
    <Button type="submit">Submit</Button>
  </div>
</form>
```

### Pattern 2: Form with Validation
```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form"

const schema = z.object({
  email: z.string().email(),
})

const form = useForm({
  resolver: zodResolver(schema),
})

<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    <FormField
      control={form.control}
      name="email"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Email</FormLabel>
          <FormControl><Input {...field} /></FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  </form>
</Form>
```

### Pattern 3: Modal with Form
```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button>Add Item</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Create Item</DialogTitle>
    </DialogHeader>
    {/* Form content here */}
  </DialogContent>
</Dialog>
```

### Pattern 4: Data Table with Actions
```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { MoreHorizontal } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Actions</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {data.map((item) => (
      <TableRow key={item.id}>
        <TableCell>{item.name}</TableCell>
        <TableCell>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem>Edit</DropdownMenuItem>
              <DropdownMenuItem>Delete</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

## Responsive Design

### Mobile-First Approach
Use Tailwind responsive prefixes:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Grid adapts from 1 col mobile, 2 tablet, 3 desktop */}
</div>
```

### Mobile Navigation
```tsx
{/* Mobile: Sheet drawer */}
<Sheet>
  <SheetTrigger className="md:hidden">
    <Menu />
  </SheetTrigger>
  <SheetContent side="left">
    <nav>{/* items */}</nav>
  </SheetContent>
</Sheet>

{/* Desktop: Regular nav */}
<nav className="hidden md:flex gap-4">
  {/* items */}
</nav>
```

## Theming and Customization

### Dark Mode Setup
```bash
npm install next-themes
```

```tsx
// app/layout.tsx
import { ThemeProvider } from "next-themes"

<ThemeProvider attribute="class" defaultTheme="system">
  {children}
</ThemeProvider>
```

### Theme Toggle
```tsx
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
import { Moon, Sun } from "lucide-react"

const { theme, setTheme } = useTheme()

<Button
  variant="outline"
  size="icon"
  onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
>
  <Sun className="h-5 w-5 rotate-0 scale-100 dark:-rotate-90 dark:scale-0" />
  <Moon className="absolute h-5 w-5 rotate-90 scale-0 dark:rotate-0 dark:scale-100" />
</Button>
```

### Color Customization
Edit `app/globals.css`:
```css
:root {
  --primary: 220 70% 50%;  /* Custom blue */
  --secondary: 280 60% 50%;  /* Custom purple */
}
```

## Accessibility Best Practices

1. **Always pair inputs with labels**
   ```tsx
   <Label htmlFor="email">Email</Label>
   <Input id="email" />
   ```

2. **Use semantic HTML**
   - Dialog for modals (handles focus trap)
   - Button for actions (not div with onClick)

3. **Add ARIA labels where needed**
   ```tsx
   <Button aria-label="Close menu">
     <X className="h-4 w-4" />
   </Button>
   ```

4. **Keyboard navigation**
   - All shadcn components support keyboard navigation by default
   - Test with Tab, Enter, Escape keys

5. **Focus management**
   - Dialog/Sheet components handle focus automatically
   - Use `autoFocus` sparingly

## Common Use Cases

### Building a Todo App
See complete example: [assets/examples/todo-app.tsx](assets/examples/todo-app.tsx)

Key components: Card, Checkbox, Button, Input, Dialog

### Building a Dashboard
Components needed:
- Stats Grid: Card components
- Navigation: Sheet (mobile) + Sidebar (desktop)
- Data Display: Table or Card Grid
- Actions: DropdownMenu, Button

See Dashboard patterns in [composition-patterns.md](references/composition-patterns.md)

### Building a Form
Simple form: Input + Label + Button
Complex form: Form + react-hook-form + zod

See Form patterns in [composition-patterns.md](references/composition-patterns.md)

### Building a Data Table
Basic: Table component
Advanced: Data Table with tanstack/react-table

See Data Display patterns in [composition-patterns.md](references/composition-patterns.md)

## Icons

shadcn/ui uses Lucide React:
```bash
npm install lucide-react
```

```tsx
import { Check, X, Loader2, Plus, Trash2 } from "lucide-react"

<Button>
  <Plus className="mr-2 h-4 w-4" />
  Add Item
</Button>

{/* Loading spinner */}
<Loader2 className="h-4 w-4 animate-spin" />
```

## Loading States

### Button Loading
```tsx
<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  Submit
</Button>
```

### Content Loading
```tsx
import { Skeleton } from "@/components/ui/skeleton"

{isLoading ? (
  <Skeleton className="h-12 w-full" />
) : (
  <div>{content}</div>
)}
```

## Notifications

### Toast
```tsx
import { useToast } from "@/components/ui/use-toast"

const { toast } = useToast()

toast({
  title: "Success",
  description: "Item created successfully",
})

toast({
  variant: "destructive",
  title: "Error",
  description: "Something went wrong",
})
```

Remember to add `<Toaster />` to layout.

## Reference Files

- **[component-catalog.md](references/component-catalog.md)** - Complete list of all shadcn components with use cases and installation
- **[composition-patterns.md](references/composition-patterns.md)** - Common UI patterns (forms, tables, dashboards, navigation)
- **[setup-guide.md](references/setup-guide.md)** - Complete setup instructions, configuration, theming, and troubleshooting

## Setup Information

If the project doesn't have shadcn/ui set up yet, see [setup-guide.md](references/setup-guide.md) for complete installation and configuration instructions.

## General Guidelines

1. **Install only needed components** - Don't add all components upfront
2. **Use the `cn()` utility** - Properly merge Tailwind classes
3. **Follow responsive patterns** - Mobile-first design with Tailwind breakpoints
4. **Maintain accessibility** - Use semantic HTML and proper labels
5. **Leverage composition** - Combine simple components into complex UIs
6. **Keep components clean** - Extract reusable patterns into separate components
7. **Test interactivity** - Verify keyboard navigation and screen reader support

## Example Workflow

User request: "Build a todo app"

1. **Analyze requirements**
   - List of tasks
   - Add/delete tasks
   - Mark complete
   - Empty state

2. **Select components** (check component-catalog.md)
   - Card (container)
   - Checkbox (complete tasks)
   - Button (add, delete)
   - Input + Label (task input)
   - Dialog (add task modal)

3. **Install components**
   ```bash
   npx shadcn@latest add card checkbox button input label dialog
   ```

4. **Compose UI** (reference composition-patterns.md and todo-app.tsx example)
   - Create Card wrapper
   - Map tasks with Checkbox
   - Dialog for add form
   - Empty state with prompt

5. **Add interactivity**
   - useState for tasks
   - Add/delete/toggle handlers
   - Form submission

6. **Refine**
   - Add icons (lucide-react)
   - Responsive styling
   - Loading states
   - Toast notifications

Result: Fully functional, accessible todo app with shadcn/ui components.
