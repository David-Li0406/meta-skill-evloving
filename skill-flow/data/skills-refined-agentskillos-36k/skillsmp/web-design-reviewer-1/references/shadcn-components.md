# shadcn/ui Components Reference

Catalog of shadcn/ui components used in LucidData with usage patterns and customization guidelines.

## Installed Components

Located in `components/ui/`:

- **alert-dialog.tsx** - Confirmation dialogs
- **badge.tsx** - Status indicators
- **button.tsx** - Interactive buttons
- **card.tsx** - Content containers
- **checkbox.tsx** - Form checkboxes
- **dialog.tsx** - Modal dialogs
- **input.tsx** - Text inputs
- **label.tsx** - Form labels
- **radio-group.tsx** - Radio button groups
- **select.tsx** - Dropdown selects
- **table.tsx** - Data tables
- **textarea.tsx** - Multi-line inputs
- **toast.tsx** - Notifications

## Button

**Variants**: `default` | `destructive` | `outline` | `secondary` | `ghost` | `link`

**Sizes**: `default` | `sm` | `lg` | `icon`

```tsx
import { Button } from '@/components/ui/button';

// Primary action
<Button>Save</Button>

// Destructive action
<Button variant="destructive">Delete</Button>

// Secondary action
<Button variant="outline">Cancel</Button>

// Icon button
<Button variant="ghost" size="icon">
  <TrashIcon className="h-4 w-4" />
</Button>

// Loading state
<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  {isLoading ? 'Saving...' : 'Save'}
</Button>
```

## Dialog

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';

<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Create Entry</DialogTitle>
      <DialogDescription>
        Add a new vault entry
      </DialogDescription>
    </DialogHeader>

    {/* Form content */}

    <DialogFooter>
      <Button variant="outline" onClick={() => setIsOpen(false)}>
        Cancel
      </Button>
      <Button onClick={handleSave}>Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

## Alert Dialog

```tsx
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';

<AlertDialog open={showConfirm} onOpenChange={setShowConfirm}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone. This will permanently delete the entry.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

## Form Components

```tsx
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';

// Input with label
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" placeholder="you@example.com" />
</div>

// Textarea
<div className="space-y-2">
  <Label htmlFor="description">Description</Label>
  <Textarea id="description" rows={4} />
</div>

// Select
<div className="space-y-2">
  <Label>Category</Label>
  <Select value={category} onValueChange={setCategory}>
    <SelectTrigger>
      <SelectValue placeholder="Select category" />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="identity">Identity</SelectItem>
      <SelectItem value="financial">Financial</SelectItem>
      <SelectItem value="health">Health</SelectItem>
    </SelectContent>
  </Select>
</div>

// Checkbox
<div className="flex items-center space-x-2">
  <Checkbox id="agree" checked={agreed} onCheckedChange={setAgreed} />
  <Label htmlFor="agree">I agree to the terms</Label>
</div>
```

## Card

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>Vault Entry</CardTitle>
    <CardDescription>Personal identification data</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content goes here</p>
  </CardContent>
  <CardFooter className="justify-end gap-2">
    <Button variant="outline">Edit</Button>
    <Button variant="destructive">Delete</Button>
  </CardFooter>
</Card>
```

## Table

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Label</TableHead>
      <TableHead>Category</TableHead>
      <TableHead>Created</TableHead>
      <TableHead className="text-right">Actions</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {entries.map((entry) => (
      <TableRow key={entry.id}>
        <TableCell className="font-medium">{entry.label}</TableCell>
        <TableCell>{entry.category}</TableCell>
        <TableCell>{formatDate(entry.createdAt)}</TableCell>
        <TableCell className="text-right">
          <Button variant="ghost" size="sm">Edit</Button>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

## Toast

```tsx
import { useToast } from '@/lib/hooks/use-toast';

function Component() {
  const { toast } = useToast();

  const handleAction = () => {
    toast({
      title: "Success",
      description: "Entry created successfully",
    });
  };

  const handleError = () => {
    toast({
      title: "Error",
      description: "Failed to create entry",
      variant: "destructive",
    });
  };
}
```

## Badge

```tsx
import { Badge } from '@/components/ui/badge';

// Default badge
<Badge>Active</Badge>

// Destructive badge
<Badge variant="destructive">Revoked</Badge>

// Outline badge
<Badge variant="outline">Pending</Badge>

// Secondary badge
<Badge variant="secondary">Draft</Badge>
```

## Customization Guidelines

### Extending Components

```tsx
// Create variant
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export function PrimaryButton({ className, ...props }) {
  return (
    <Button
      className={cn("bg-primary hover:bg-primary/90", className)}
      {...props}
    />
  );
}
```

### Theming

Colors are defined in `tailwind.config.ts` and referenced via CSS variables:

```css
/* app/globals.css */
:root {
  --primary: ...;
  --secondary: ...;
  --destructive: ...;
  --muted: ...;
}
```

Use in components:
```tsx
<div className="bg-primary text-primary-foreground">
```

### Accessibility

All shadcn/ui components include:
- Proper ARIA attributes
- Keyboard navigation
- Focus management
- Screen reader support

**Best practices**:
- Always provide labels for form fields
- Use semantic HTML
- Test with keyboard navigation
- Verify with screen reader

---

**For more information:**
- [Tailwind Patterns](tailwind-patterns.md)
- [Accessibility Guide](accessibility.md)
- [shadcn/ui Documentation](https://ui.shadcn.com)
