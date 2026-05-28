---
name: zod-form-validation
description: Use this skill when implementing type-safe form validation with Zod schemas and React Hook Form in TypeScript frontends.
---

# Zod Form Validation Skill

Implements type-safe form validation using Zod schemas with React Hook Form integration in TypeScript frontends.

## Quick Reference

### Form Setup Pattern

```typescript
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '~/components/ui/form';

// 1. Define schema
const MySchema = z.object({
  email: z.string().email('Invalid email'),
  name: z.string().min(2, 'Name too short'),
});

// 2. Create form with zodResolver
const form = useForm<z.infer<typeof MySchema>>({
  resolver: zodResolver(MySchema),
  defaultValues: { email: '', name: '' },
});

// 3. Handle submission
const onSubmit = (data: z.infer<typeof MySchema>) => {
  toast.promise(apiCall(data), {
    loading: 'Saving...',
    success: 'Saved!',
    error: (err) => `Failed: ${err?.response?.data ?? String(err)}`,
  });
};
```

### Form Field Pattern

```typescript
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
```

## Project Conventions

### Schema Location

Define schemas in `~/components/<feature>/schemas.ts`:
- `UserSchema` in `~/components/user/schemas.ts`
- `TeamSchema` in `~/components/team/schemas.ts`
- `GameSchema` in `~/components/game/schemas.ts`

### Type Extraction

Always use `z.infer<typeof Schema>` for types instead of manual interfaces:

```typescript
export const UserSchema = z.object({ /* ... */ });
export type UserType = z.infer<typeof UserSchema>;
```

### Error Handling

Wrap mutations in `toast.promise()` for consistent user feedback:

```typescript
import { toast } from 'sonner';
import { getLogger } from '~/lib/logger';

const log = getLogger('FormComponent');

toast.promise(apiCall(data), {
  loading: 'Processing...',
  success: (response) => {
    setData(response);
    return 'Success!';
  },
  error: (err) => {
    log.error('API call failed', err);
    return `Failed: ${err?.response?.data ?? String(err)}`;
  },
});
```