# Patterns (NNRC)

## Where things live

- **Server actions**: `src/app/actions/*`
  - Small orchestration layer: auth/role checks + input parsing + calls services + `revalidatePath`
- **Services**: `src/services/*`
  - Business logic and Prisma queries
- **Prisma**: `src/lib/prisma.ts`
- **Auth**: `src/lib/auth.ts`, `src/lib/auth.config.ts`, `src/lib/admin.ts`

## Input parsing

- Prefer explicit parsing over implicit casting:
  - `const daysCount = parseInt(formData.get("daysCount") as string, 10);`
- Validate required fields before DB writes.
- Normalize strings (trim, lowercase emails when appropriate).

## Revalidation

- If a server-rendered route reads mutated data, call `revalidatePath("/route")`.
- Prefer revalidating the narrowest path(s) impacted.

## Admin-only flows

- Use `withAdminAuth` in server actions and any privileged route handlers.
- Keep admin functionality server-side; don’t rely on client-only hiding.
