# Component Patterns

## Table of Contents
- [Imports](#imports)
- [Button Variants](#button-variants)
- [Cards](#cards)
- [Modals](#modals)
- [Navigation](#navigation)
- [Data Display](#data-display)
- [Feedback](#feedback)

## Imports

```tsx
// UI components from shared package
import { Button } from "@ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@ui/dialog";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@ui/sheet";
import { Input } from "@ui/input";
import { Label } from "@ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@ui/tabs";
import { ScrollArea } from "@ui/scroll-area";
import { Skeleton } from "@ui/skeleton";

// Icons
import { Home, Search, Settings, ChevronRight, X, Check } from "lucide-react";

// Utilities
import { cn } from "@/lib/utils";
```

## Button Variants

```tsx
// Primary action
<Button>Save Changes</Button>

// Secondary action
<Button variant="secondary">Cancel</Button>

// Destructive action
<Button variant="destructive">Delete</Button>

// Ghost (no background)
<Button variant="ghost" size="icon">
  <Settings className="h-4 w-4" />
</Button>

// Outline
<Button variant="outline">Learn More</Button>

// Link style
<Button variant="link">View Details</Button>

// Loading state
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Saving...
</Button>

// With icon
<Button>
  <Plus className="mr-2 h-4 w-4" />
  Add Item
</Button>

// Icon only (use size="icon")
<Button variant="ghost" size="icon">
  <X className="h-4 w-4" />
  <span className="sr-only">Close</span>
</Button>
```

## Cards

```tsx
// Basic card
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description text</CardDescription>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
  <CardFooter className="flex justify-end gap-2">
    <Button variant="outline">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>

// Interactive card
<Card className="cursor-pointer hover:bg-accent/50 transition-colors">
  <CardContent className="p-4">
    <div className="flex items-center gap-3">
      <div className="flex-1">
        <h3 className="font-medium">Item Title</h3>
        <p className="text-sm text-muted-foreground">Subtitle</p>
      </div>
      <ChevronRight className="h-4 w-4 text-muted-foreground" />
    </div>
  </CardContent>
</Card>

// Stats card
<Card>
  <CardContent className="p-6">
    <div className="text-2xl font-bold">1,234</div>
    <p className="text-xs text-muted-foreground">Total Users</p>
  </CardContent>
</Card>
```

## Modals

### Dialog (Desktop-optimized)
```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
      <DialogDescription>
        Make changes to your profile here.
      </DialogDescription>
    </DialogHeader>
    <div className="grid gap-4 py-4">
      {/* Form fields */}
    </div>
    <DialogFooter>
      <Button type="submit">Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Sheet (Side panel)
```tsx
<Sheet>
  <SheetTrigger asChild>
    <Button variant="outline">Open Menu</Button>
  </SheetTrigger>
  <SheetContent side="right" className="w-[300px] sm:w-[400px]">
    <SheetHeader>
      <SheetTitle>Navigation</SheetTitle>
    </SheetHeader>
    <nav className="flex flex-col gap-2 mt-4">
      {/* Nav items */}
    </nav>
  </SheetContent>
</Sheet>

// Mobile bottom sheet
<SheetContent side="bottom" className="h-[85vh] rounded-t-xl">
  <div className="mx-auto w-12 h-1.5 bg-muted rounded-full mb-4" />
  {/* Content */}
</SheetContent>
```

### Alert Dialog (Confirmation)
```tsx
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction>Delete</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

## Navigation

### Tabs
```tsx
<Tabs defaultValue="tab1" className="w-full">
  <TabsList className="grid w-full grid-cols-3">
    <TabsTrigger value="tab1">Tab 1</TabsTrigger>
    <TabsTrigger value="tab2">Tab 2</TabsTrigger>
    <TabsTrigger value="tab3">Tab 3</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">Content 1</TabsContent>
  <TabsContent value="tab2">Content 2</TabsContent>
  <TabsContent value="tab3">Content 3</TabsContent>
</Tabs>
```

### Breadcrumb
```tsx
<Breadcrumb>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbPage>Current Page</BreadcrumbPage>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumb>
```

### Dropdown Menu
```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="icon">
      <MoreVertical className="h-4 w-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuItem>
      <Edit className="mr-2 h-4 w-4" />
      Edit
    </DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem className="text-destructive">
      <Trash className="mr-2 h-4 w-4" />
      Delete
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## Data Display

### List with ScrollArea
```tsx
<ScrollArea className="h-[300px]">
  <div className="space-y-2 p-4">
    {items.map((item) => (
      <div key={item.id} className="flex items-center gap-3 p-2 rounded-md hover:bg-accent">
        <Avatar className="h-8 w-8">
          <AvatarImage src={item.avatar} />
          <AvatarFallback>{item.initials}</AvatarFallback>
        </Avatar>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium truncate">{item.name}</p>
          <p className="text-xs text-muted-foreground">{item.email}</p>
        </div>
      </div>
    ))}
  </div>
</ScrollArea>
```

### Loading Skeleton
```tsx
// Card skeleton
<Card>
  <CardHeader>
    <Skeleton className="h-4 w-[200px]" />
    <Skeleton className="h-3 w-[150px]" />
  </CardHeader>
  <CardContent>
    <Skeleton className="h-20 w-full" />
  </CardContent>
</Card>

// List skeleton
<div className="space-y-3">
  {[...Array(5)].map((_, i) => (
    <div key={i} className="flex items-center gap-3">
      <Skeleton className="h-10 w-10 rounded-full" />
      <div className="flex-1 space-y-2">
        <Skeleton className="h-4 w-[200px]" />
        <Skeleton className="h-3 w-[150px]" />
      </div>
    </div>
  ))}
</div>
```

### Empty State
```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <div className="rounded-full bg-muted p-4 mb-4">
    <Inbox className="h-8 w-8 text-muted-foreground" />
  </div>
  <h3 className="text-lg font-medium">No items yet</h3>
  <p className="text-sm text-muted-foreground mt-1 mb-4">
    Get started by creating your first item.
  </p>
  <Button>
    <Plus className="mr-2 h-4 w-4" />
    Create Item
  </Button>
</div>
```

## Feedback

### Toast Notifications
```tsx
import { toast } from "sonner";

// Success
toast.success("Changes saved successfully");

// Error
toast.error("Failed to save changes");

// With description
toast("Event created", {
  description: "Your event has been scheduled for tomorrow.",
});

// With action
toast("Item deleted", {
  action: {
    label: "Undo",
    onClick: () => restoreItem(),
  },
});
```

### Badge
```tsx
<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
```

### Progress
```tsx
<Progress value={65} className="w-full" />
```
