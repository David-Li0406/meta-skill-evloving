# Common Pitfalls & Quick Checklist

When your agent is about to emit Convex code, mentally run through this list:

## 1. Functions

- [ ] Imported from `./_generated/server`?
- [ ] Using new syntax (`query({ args, handler })`)?
- [ ] Args have validators (`v.*`)?
- [ ] Using `internal*` for internal / scheduled / sensitive functions?

## 2. Indexes & Queries

- [ ] No `.filter()` – using `.withIndex()` or `.withSearchIndex()` instead?
- [ ] No custom `"by_creation_time"` index?
- [ ] No `_creationTime` in custom index fields?
- [ ] Using `.order("desc")` when needed?

## 3. Actions

- [ ] `"use node";` at top of action files that use Node modules?
- [ ] No `ctx.db` in actions – using `ctx.runQuery`/`ctx.runMutation`?
- [ ] External APIs called **only** from actions?

## 4. Scheduler

- [ ] Using function references (`internal.file.fn`) in `runAfter`?
- [ ] Not relying on auth inside scheduled job handlers?

## 5. File Storage

- [ ] Storing file IDs (`Id<"_storage">`), not URLs?
- [ ] Using `ctx.storage.generateUploadUrl` + `ctx.storage.getUrl`?

## 6. React

- [ ] No conditional `useQuery` / `useMutation`?
- [ ] Use `"skip"` pattern when you want to disable a query?
- [ ] Handling `undefined` from `useQuery` while loading?

## 7. Limits

- [ ] Not returning or passing massive blobs (> 8MiB) in args/returns?
- [ ] Not reading/writing thousands of docs in a single query/mutation in a way that might hit limits?

## 8. Secrets

- [ ] Instructed user to set env vars for keys instead of hardcoding?
- [ ] Using `process.env` for secrets?

## 9. Dynamic Imports

- [ ] No `await import()` in queries or mutations? (Only actions support dynamic imports)
- [ ] Using static imports at top of file for all query/mutation dependencies?

## 10. Convex Components (e.g., Better Auth)

- [ ] Not using `ctx.db.query('componentTable')` to query component tables?
- [ ] Using `ctx.runQuery(components.<name>.adapter.findOne, {...})` for component table lookups?
- [ ] Component table queries only from mutations/actions (which have `runQuery`)?

---

If you keep these rules in your "Convex mental model", you'll produce way fewer broken Convex apps and your users will be much happier.
