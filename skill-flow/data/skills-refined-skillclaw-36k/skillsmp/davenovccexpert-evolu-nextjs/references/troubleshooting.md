# Troubleshooting

Common issues and solutions when working with Evolu and Next.js.

## Sync Failures

Evolu handles offline operation automatically. No action required for temporary network loss.

For persistent sync issues:
- Check sync URL configuration
- Verify mnemonic validity
- Check browser console for WebSocket errors
- Ensure sync server is reachable

## Validation Errors

Always wrap mutations in validation checks:

```typescript
const result = BrandedType.from(input);
if (!result.ok) {
  // Handle error - don't proceed with mutation
  return;
}
// Safe to use result.value
```

## Hydration Mismatches

If you see hydration errors with Evolu:

1. **Ensure Client Components**: All Evolu code must be in components with `"use client"` directive
2. **Use Suspense**: Wrap components using `useQuery` with Suspense boundaries
3. **Disable SSR**: For problematic components, use `next/dynamic`:

```tsx
import dynamic from "next/dynamic";

const TodoApp = dynamic(
  () => import("@/components/TodoApp").then((mod) => mod.TodoApp),
  { ssr: false }
);
```

## TypeScript Errors

### "Property does not exist on type"

Ensure `tsconfig.json` has:
```json
{
  "compilerOptions": {
    "strict": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### "Type 'string' is not assignable to type 'NonEmptyString100'"

You must use `.from()` to validate and parse:
```typescript
// Wrong
create("todo", { title: userInput });

// Correct
const result = NonEmptyString100.from(userInput);
if (result.ok) {
  create("todo", { title: result.value });
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `"use client"` | Add directive to all files using Evolu |
| Missing Suspense boundary | Wrap EvoluProvider children with Suspense |
| Not filtering `isDeleted` | Add `.where("isDeleted", "is not", evolu.sqliteTrue)` to queries |
| Using undefined instead of null | Use `nullOr()` for optional fields |
| Logging mnemonic | Never log in production - security risk |
