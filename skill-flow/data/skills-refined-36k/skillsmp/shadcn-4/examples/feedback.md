# Feedback Patterns

Examples for alerts, toasts, dialogs, and loading states.

## Alert Messages

```tsx
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle, CheckCircle2, Info, AlertTriangle } from "lucide-react";

// Success Alert
<Alert className="border-green-500 bg-green-50 dark:bg-green-950">
  <CheckCircle2 className="h-4 w-4 text-green-600" />
  <AlertTitle className="text-green-800 dark:text-green-200">Success</AlertTitle>
  <AlertDescription className="text-green-700 dark:text-green-300">
    Your changes have been saved successfully.
  </AlertDescription>
</Alert>

// Error Alert
<Alert variant="destructive">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>
    Something went wrong. Please try again later.
  </AlertDescription>
</Alert>

// Warning Alert
<Alert className="border-yellow-500 bg-yellow-50 dark:bg-yellow-950">
  <AlertTriangle className="h-4 w-4 text-yellow-600" />
  <AlertTitle className="text-yellow-800 dark:text-yellow-200">Warning</AlertTitle>
  <AlertDescription className="text-yellow-700 dark:text-yellow-300">
    Your session will expire in 5 minutes.
  </AlertDescription>
</Alert>

// Info Alert
<Alert>
  <Info className="h-4 w-4" />
  <AlertTitle>Note</AlertTitle>
  <AlertDescription>
    This feature is currently in beta.
  </AlertDescription>
</Alert>
```

## Toast Notifications (Sonner)

```tsx
// Setup: Add Toaster to layout
import { Toaster } from "@/components/ui/sonner";

// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  );
}

// Usage
import { toast } from "sonner";

// Basic toasts
toast("Event created");
toast.success("Successfully saved!");
toast.error("Something went wrong");
toast.warning("Please review your input");
toast.info("New update available");

// With description
toast.success("Task completed", {
  description: "Your task has been marked as done.",
});

// With action
toast("File uploaded", {
  action: {
    label: "View",
    onClick: () => router.push("/files"),
  },
});

// With cancel
toast("Delete item?", {
  action: {
    label: "Delete",
    onClick: () => deleteItem(),
  },
  cancel: {
    label: "Cancel",
    onClick: () => {},
  },
});

// Promise toast (loading → success/error)
toast.promise(saveData(), {
  loading: "Saving...",
  success: "Data saved successfully!",
  error: "Failed to save data",
});

// Custom duration
toast.success("Saved!", { duration: 5000 }); // 5 seconds

// Dismiss programmatically
const toastId = toast.loading("Loading...");
// Later:
toast.dismiss(toastId);
```

## Confirmation Dialog

```tsx
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

export function DeleteConfirmation({ onConfirm, itemName }) {
  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button variant="destructive" size="sm">
          <Trash2 className="mr-2 h-4 w-4" />
          Delete
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This will permanently delete "{itemName}". This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={onConfirm}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
```

## Form Dialog

```tsx
export function CreateTaskDialog({ onSubmit }) {
  const [open, setOpen] = useState(false);

  function handleSubmit(data: FormData) {
    onSubmit(data);
    setOpen(false);
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Task
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create Task</DialogTitle>
          <DialogDescription>
            Add a new task to your list.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="title">Title</Label>
              <Input id="title" name="title" required />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Textarea id="description" name="description" />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit">Create</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

## Loading States

### Button Loading

```tsx
import { Loader2 } from "lucide-react";

export function LoadingButton({ loading, children, ...props }) {
  return (
    <Button disabled={loading} {...props}>
      {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {children}
    </Button>
  );
}

// Usage
<LoadingButton loading={isSubmitting}>
  {isSubmitting ? "Saving..." : "Save"}
</LoadingButton>
```

### Full Page Loading

```tsx
export function PageLoading() {
  return (
    <div className="flex h-screen items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">Loading...</p>
      </div>
    </div>
  );
}
```

### Skeleton Loading

```tsx
import { Skeleton } from "@/components/ui/skeleton";

export function CardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-5 w-1/2" />
        <Skeleton className="h-4 w-3/4" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-24 w-full" />
      </CardContent>
      <CardFooter>
        <Skeleton className="h-9 w-24" />
      </CardFooter>
    </Card>
  );
}

export function TableSkeleton({ rows = 5 }) {
  return (
    <div className="space-y-2">
      <Skeleton className="h-10 w-full" /> {/* Header */}
      {Array.from({ length: rows }).map((_, i) => (
        <Skeleton key={i} className="h-12 w-full" />
      ))}
    </div>
  );
}
```

### Progress Indicator

```tsx
import { Progress } from "@/components/ui/progress";

export function UploadProgress({ progress }) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span>Uploading...</span>
        <span>{progress}%</span>
      </div>
      <Progress value={progress} className="h-2" />
    </div>
  );
}
```

## Error Boundary

```tsx
"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex h-[50vh] flex-col items-center justify-center gap-4">
      <div className="rounded-full bg-destructive/10 p-4">
        <AlertCircle className="h-8 w-8 text-destructive" />
      </div>
      <h2 className="text-xl font-semibold">Something went wrong!</h2>
      <p className="text-sm text-muted-foreground max-w-md text-center">
        {error.message || "An unexpected error occurred."}
      </p>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}
```

## Tooltip

```tsx
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

// Wrap app in TooltipProvider
<TooltipProvider>
  <App />
</TooltipProvider>

// Usage
<Tooltip>
  <TooltipTrigger asChild>
    <Button variant="ghost" size="icon">
      <Info className="h-4 w-4" />
    </Button>
  </TooltipTrigger>
  <TooltipContent>
    <p>More information about this feature</p>
  </TooltipContent>
</Tooltip>

// With delay
<Tooltip delayDuration={300}>
  <TooltipTrigger>Hover me</TooltipTrigger>
  <TooltipContent>Shows after 300ms</TooltipContent>
</Tooltip>
```

## Popover

```tsx
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

export function InfoPopover() {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Open Popover</Button>
      </PopoverTrigger>
      <PopoverContent className="w-80">
        <div className="grid gap-4">
          <div className="space-y-2">
            <h4 className="font-medium leading-none">Dimensions</h4>
            <p className="text-sm text-muted-foreground">
              Set the dimensions for the layer.
            </p>
          </div>
          <div className="grid gap-2">
            <div className="grid grid-cols-3 items-center gap-4">
              <Label htmlFor="width">Width</Label>
              <Input id="width" defaultValue="100%" className="col-span-2 h-8" />
            </div>
            <div className="grid grid-cols-3 items-center gap-4">
              <Label htmlFor="height">Height</Label>
              <Input id="height" defaultValue="25px" className="col-span-2 h-8" />
            </div>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
```
