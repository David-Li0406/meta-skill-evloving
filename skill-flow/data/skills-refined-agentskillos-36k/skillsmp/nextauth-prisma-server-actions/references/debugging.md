# Debugging checklist (NNRC)

## Auth/session issues

- Check `src/lib/auth.ts` callbacks:
  - `jwt`: populates `token.id` and `token.role`
  - `session`: copies those onto `session.user`
- Check `src/types/next-auth.d.ts` so TS knows `session.user.id` exists.
- Check sign-in provisioning logic (user creation/lookup) in `UserService`.

## Authorization issues (admin)

- Verify role propagation:
  - Role is written to DB (`user.role`)
  - Role is put into JWT (`token.role`)
  - Role is attached to session (`session.user.role`)
- Use `withAdminAuth` for server actions that mutate or expose sensitive data.

## Prisma/query issues

- Confirm all DB access uses `prisma` from `src/lib/prisma.ts` (singleton).
- Look for N+1 queries in loops; refactor to batched queries or `include`.
- For multi-step writes, use `prisma.$transaction`.

## “UI didn’t update after mutation”

- If the data is read in a Server Component route, add `revalidatePath` in the server action.
- If the UI is client state, ensure you update state / refetch after awaiting the action.

## “Works locally, fails on Vercel”

- Confirm migrations run in production (`prisma migrate deploy`).
- Confirm environment vars are set (auth provider, DB URL).
- Watch for data shape differences (nullable fields, unexpected rows).
