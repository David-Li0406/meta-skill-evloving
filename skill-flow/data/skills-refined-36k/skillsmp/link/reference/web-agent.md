# Web Package Agent Reference

Reference to `.claude/agent/web.md` for packages/web development.

## When to Use Web Agent

Use the web agent when working on:
- React components
- UI/UX implementation
- Forms and validation
- Frontend routing
- Styling with Tailwind CSS v4
- shadcn/ui component integration

## Critical Rules Summary

### 1. Imports - Always use `@/` alias
```typescript
// ✅ CORRECT
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

// ❌ WRONG
import { Button } from "../../../components/ui/button"
```

### 2. Classes - Always use `cn()`
```typescript
// ✅ CORRECT
<div className={cn("flex", className, isActive && "bg-primary")} />

// ❌ WRONG
<div className={`flex ${className}`} />
```

### 3. UI Text - Always Spanish
```typescript
// ✅ CORRECT
<Button>Guardar Cambios</Button>
toast.success("Perfil actualizado")

// ❌ WRONG
<Button>Save Changes</Button>
```

### 4. Theme - Use CSS variables
```typescript
// ✅ CORRECT
<div className="bg-background text-foreground" />

// ❌ WRONG
<div className="bg-white text-black" />
```

### 5. Forms - React Hook Form + Zod
```typescript
const schema = z.object({
  name: z.string().min(2, { message: "Mínimo 2 caracteres." })
})

<Form {...form}>
  <FormField control={form.control} name="name" render={({ field }) => (
    <FormItem>
      <FormLabel>Nombre</FormLabel>
      <FormControl><Input {...field} /></FormControl>
      <FormMessage />
    </FormItem>
  )} />
</Form>
```

### 6. Data Fetching - TanStack Query
```typescript
const { data, isLoading } = useQuery({
  queryKey: ["profiles"],
  queryFn: async () => {
    const { data, error } = await api.api.profiles.get()
    if (error) throw error
    return data
  },
})
```

## Full Agent Documentation

See `.claude/agent/web.md` for complete reference.
