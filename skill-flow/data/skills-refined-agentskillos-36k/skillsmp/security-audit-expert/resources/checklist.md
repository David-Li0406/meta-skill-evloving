# Security Review Checklist

## Server Functions (TanStack Start)

- [ ] **Input Validation**: Does every `createServerFn` have a `.validator(z.object(...))`?
- [ ] **Method Definition**: Is `{ method: 'POST' }` used for mutations to prevent CSRF in GET requests?
- [ ] **Sensitive Return**: Does the handler *explicitly* select fields to return? (Avoid returning full user objects with hashed passwords).
- [ ] **Authorization**: Is there a check (e.g., `if (!context.user) throw ...`) at the start of the handler?

## Database Access (Prisma)

- [ ] **Raw Queries**: Is `$queryRaw` used? If so, are parameters passed securely (not concatenated strings)?
- [ ] **Row-Level Access**: Do queries include `where: { ownerId: user.id }` to prevent IDOR?
- [ ] **Pagination**: Are `take` and `skip` limits enforced to prevent DoS via massive queries?

## Client-Side (React)

- [ ] **XSS**: Is `dangerouslySetInnerHTML` used? If yes, is the content sanitized (DOMPurify)?
- [ ] **URLs**: Are user-provided URLs validated to prevention `javascript:` schemes?
- [ ] **State**: Is sensitive data (like tokens) kept out of `localStorage` if possible? (HttpOnly cookies preferred).

## General

- [ ] **Secrets**: Are `process.env` secrets checked to ensure they aren't leaked to the client bundle?
- [ ] **Dependencies**: `npm audit` check passed?
