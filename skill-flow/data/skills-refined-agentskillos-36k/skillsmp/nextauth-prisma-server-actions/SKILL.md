---
name: nextauth-prisma-server-actions
description: Build and debug data mutations and protected access in this No Name Running Club app using Next.js App Router server actions + Prisma + NextAuth v5. Use when implementing/repairing server actions, route handlers, admin-only flows, session/role propagation, Prisma queries/transactions, or caching/revalidation behavior.
---

# NextAuth + Prisma + Server Actions (NNRC)

This skill is opinionated to this repo’s patterns:

- **Auth**: `auth()` / `signIn()` / `signOut()` from `src/lib/auth.ts`
- **Admin auth**: `withAdminAuth()` / helpers in `src/lib/admin.ts`
- **DB**: `prisma` singleton from `src/lib/prisma.ts`
- **Server actions**: `src/app/actions/*` with `"use server"`

## Default patterns

### Server action shape

- Put the mutation in `src/app/actions/<domain>.ts`
- Start with `"use server"`
- Authenticate early
- Validate/parse inputs (especially `FormData`)
- Delegate business logic to `src/services/*` where appropriate
- Revalidate paths after mutations that affect server-rendered pages

### Auth & role checks

- **User-required**: `const session = await auth(); if (!session?.user?.id) throw new Error("Not authenticated");`
- **Admin-required**: wrap the body with `withAdminAuth(async () => { ... })`
- Don’t trust client-provided user ids/roles; derive from the session.

### Prisma query hygiene

- Prefer `select` over returning whole models when you don’t need all fields.
- Watch for accidental N+1 loops; batch with `where: { id: { in: ... } }` or use `include`.
- For multi-write invariants, use `prisma.$transaction(...)`.

## Debugging playbook

### “Session.user.id is undefined”

- Confirm `src/lib/auth.ts` sets it in the `session` callback.
- Confirm the `jwt` callback is populating `token.id` from DB.
- Confirm types in `src/types/next-auth.d.ts` include `session.user.id`.

### “Admin pages/actions not protected”

- Server actions should use `withAdminAuth(...)`.
- Pages/layouts should gate data fetching and rendering based on role (server-side).
- Confirm admin role is being set (see `src/lib/auth.ts` sign-in callback + `shouldBeAdmin`).

### “Mutation works but UI doesn’t update”

- If the UI is server-rendered, add `revalidatePath("/the-path")` in the server action after the write.
- If the UI is client state, ensure you update local state or refetch after the action resolves.

### “Prisma errors in production”

- Ensure migrations are deployed (`yarn build` runs `prisma migrate deploy`).
- Avoid relying on dev-only behavior (e.g., using `migrate dev` semantics).
- Validate all nullable fields before use; production data often has more edge cases.

## References

- Patterns: `references/patterns.md`
- Debugging checklist: `references/debugging.md`
