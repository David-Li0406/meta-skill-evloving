---
name: agentic-jumpstart-react
description: React 19 patterns and best practices for TanStack Start applications with shadcn/ui, React Hook Form, Zod, Framer Motion, and TanStack Query. Use when building React components, forms, handling state, data fetching, animations, drag and drop, toasts, modals, or when the user mentions React, hooks, components, or UI.
---

# React 19 Best Practices

## Component Structure

### File Organization

```
src/routes/admin/courses/
├── route.tsx              # Route definition
├── -components/           # Route-specific components
│   ├── CourseList.tsx
│   ├── CourseForm.tsx
│   └── CourseCard.tsx
```

### Component Pattern

```typescript
import { type ReactNode } from "react";

interface CourseCardProps {
  course: Course;
  onEdit?: (id: number) => void;
  children?: ReactNode;
}

export function CourseCard({ course, onEdit, children }: CourseCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{course.title}</CardTitle>
        <CardDescription>{course.description}</CardDescription>
      </CardHeader>
      <CardContent>{children}</CardContent>
      {onEdit && (
        <CardFooter>
          <Button onClick={() => onEdit(course.id)}>Edit</Button>
        </CardFooter>
      )}
    </Card>
  );
}
```

## Form Handling with React Hook Form + Zod

### Basic Form Pattern

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const formSchema = z.object({
  title: z.string().min(1, "Title is required").max(100),
  description: z.string().max(500).optional(),
  isPremium: z.boolean().default(false),
});

type FormData = z.infer<typeof formSchema>;

export function CourseForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: "",
      description: "",
      isPremium: false,
    },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="title">Title</Label>
        <Input
          id="title"
          {...form.register("title")}
          aria-invalid={!!form.formState.errors.title}
        />
        {form.formState.errors.title && (
          <p className="text-sm text-red-500">
            {form.formState.errors.title.message}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="description">Description</Label>
        <Textarea id="description" {...form.register("description")} />
      </div>

      <div className="flex items-center gap-2">
        <Checkbox
          id="isPremium"
          checked={form.watch("isPremium")}
          onCheckedChange={(checked) =>
            form.setValue("isPremium", checked === true)
          }
        />
        <Label htmlFor="isPremium">Premium content</Label>
      </div>

      <Button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? "Saving..." : "Save"}
      </Button>
    </form>
  );
}
```

## Data Fetching with TanStack Query

### Query Options Pattern

```typescript
import { queryOptions, useQuery, useSuspenseQuery } from "@tanstack/react-query";

// Define query options (can be shared between components)
export const courseQueryOptions = (courseId: string) =>
  queryOptions({
    queryKey: ["course", courseId],
    queryFn: () => getCourseFn({ data: { courseId } }),
  });

// In component - with suspense
function CourseDetails({ courseId }: { courseId: string }) {
  const { data: course } = useSuspenseQuery(courseQueryOptions(courseId));
  return <div>{course.title}</div>;
}

// In component - without suspense
function CourseDetails({ courseId }: { courseId: string }) {
  const { data: course, isLoading, error } = useQuery(courseQueryOptions(courseId));

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorDisplay error={error} />;
  return <div>{course.title}</div>;
}
```

### Mutations with Optimistic Updates

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

export function useUpdateCourse() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateCourseFn,
    onSuccess: () => {
      toast.success("Course updated successfully");
      queryClient.invalidateQueries({ queryKey: ["courses"] });
    },
    onError: (error) => {
      toast.error(error.message || "Failed to update course");
    },
  });
}
```

## Loading States & Suspense

### Loading Skeleton Pattern

```typescript
function CourseSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-6 w-3/4" />
        <Skeleton className="h-4 w-1/2" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-20 w-full" />
      </CardContent>
    </Card>
  );
}

function CourseList() {
  return (
    <Suspense fallback={<CourseSkeleton />}>
      <CourseListContent />
    </Suspense>
  );
}
```

## Error Boundaries

### Route-Level Error Handling

```typescript
import { DefaultCatchBoundary } from "~/components/DefaultCatchBoundary";

export const Route = createFileRoute("/courses/$courseId")({
  component: CoursePage,
  errorComponent: DefaultCatchBoundary,
});
```

## Dialog & Modal Pattern

```typescript
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog";

function DeleteCourseDialog({
  course,
  onDelete,
}: {
  course: Course;
  onDelete: () => void;
}) {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Course</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete "{course.title}"? This action cannot
            be undone.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={() => {
              onDelete();
              setOpen(false);
            }}
          >
            Delete
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

## Toast Notifications with Sonner

```typescript
import { toast } from "sonner";

// Success toast
toast.success("Course saved successfully");

// Error toast
toast.error("Failed to save course");

// Promise toast
toast.promise(saveCourse(data), {
  loading: "Saving course...",
  success: "Course saved!",
  error: "Failed to save course",
});

// Custom toast with action
toast("Course deleted", {
  action: {
    label: "Undo",
    onClick: () => restoreCourse(courseId),
  },
});
```

## Animation with Framer Motion

### Basic Animation

```typescript
import { motion } from "framer-motion";

function FadeInCard({ children }: { children: ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.div>
  );
}
```

### Staggered List Animation

```typescript
import { motion } from "framer-motion";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

function AnimatedList({ items }: { items: Item[] }) {
  return (
    <motion.ul variants={container} initial="hidden" animate="show">
      {items.map((item) => (
        <motion.li key={item.id} variants={item}>
          {item.title}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

## Drag and Drop with @hello-pangea/dnd

```typescript
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";

function ReorderableList({
  items,
  onReorder,
}: {
  items: Item[];
  onReorder: (items: Item[]) => void;
}) {
  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const reordered = Array.from(items);
    const [removed] = reordered.splice(result.source.index, 1);
    reordered.splice(result.destination.index, 0, removed);

    onReorder(reordered);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Droppable droppableId="items">
        {(provided) => (
          <ul {...provided.droppableProps} ref={provided.innerRef}>
            {items.map((item, index) => (
              <Draggable key={item.id} draggableId={String(item.id)} index={index}>
                {(provided) => (
                  <li
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                  >
                    {item.title}
                  </li>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </ul>
        )}
      </Droppable>
    </DragDropContext>
  );
}
```

## Custom Hooks

### useLocalStorage

```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    const valueToStore = value instanceof Function ? value(storedValue) : value;
    setStoredValue(valueToStore);
    window.localStorage.setItem(key, JSON.stringify(valueToStore));
  };

  return [storedValue, setValue] as const;
}
```

### useDebounce

```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

## Component Patterns Checklist

- [ ] Components use TypeScript interfaces for props
- [ ] Forms use React Hook Form with Zod validation
- [ ] Data fetching uses TanStack Query patterns
- [ ] Loading states have skeleton placeholders
- [ ] Dialogs use shadcn/ui Dialog component
- [ ] Toasts use Sonner for notifications
- [ ] Animations use Framer Motion
- [ ] Effects clean up subscriptions
- [ ] Route-specific components in `-components/` subdirectory
- [ ] Shared components in `/src/components/`
