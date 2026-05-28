# Backend Best Practices (Next.js + Prisma + PostgreSQL)

## API Endpoints

### RESTful Design

- **Resource-Based URLs**: Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
- **Naming**: Consistent lowercase, hyphenated or underscored
- **Versioning**: URL path or headers for breaking changes
- **Plural Nouns**: Use for resource endpoints (e.g., `/users`, `/products`)
- **Nested Resources**: Limit depth to 2-3 levels max
- **Query Parameters**: Use for filtering, sorting, pagination, search

### HTTP Status Codes

| Code | Use Case                       |
| ---- | ------------------------------ |
| 200  | Success                        |
| 201  | Created                        |
| 400  | Bad request / Validation error |
| 401  | Unauthorized                   |
| 403  | Forbidden                      |
| 404  | Not found                      |
| 500  | Server error                   |

---

## Authentication & Authorization

- **JWT or OAuth**: With HTTPS; verify tokens on every request
- **RBAC**: Role-based access control enforced in app and database layers

---

## File & Media Handling

- **Blurhash Generation**: Generate blurhash for all uploaded images and videos
- **Storage**: Return URLs and metadata (size, dimensions, format, blurhash) in API responses

---

## API Security

- **SQL Injection**: Use parameterized queries
- **File Uploads**: Validate type, size, and scan for malware
- **Secrets**: Never expose in client code; use environment variables only
- **CORS**: Explicitly configure and validate
- **HTTPS**: Enforce for all network requests in production
- **Certificate Pinning**: Pin expected certificates to prevent MITM attacks
- **Rate Limiting**: Per-user and per-IP limits with headers
- **CSRF Protection**: Anti-CSRF tokens for mutations
- **CSP Headers**: Define allowed content sources
- **Auditing**: Log all sensitive operations

---

## Database Models (Prisma)

### Naming Conventions

- **Models**: Singular (e.g., `User`, `Product`)
- **Tables**: Plural snake_case (configured via `@@map`)

### Standard Fields

```prisma
model Example {
  id         String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  publicId   String    @unique @default(cuid()) @map("public_id")
  createdAt  DateTime  @default(now()) @map("created_at") @db.Timestamptz
  updatedAt  DateTime  @updatedAt @map("updated_at") @db.Timestamptz
  deletedAt  DateTime? @map("deleted_at") @db.Timestamptz

  @@map("examples")
}
```

### Best Practices

- **Primary Keys**: UUID v4 with `DEFAULT gen_random_uuid()`
- **Public IDs**: Add unique `publicId` for entities in public URLs (nanoid, slugs)
- **Timestamps**: Include `createdAt` and `updatedAt` as `TIMESTAMPTZ`
- **Soft Deletes**: Add nullable `deletedAt TIMESTAMPTZ` for data retention
- **Appropriate Types**: Match data types to purpose and size requirements
- **Constraints**: Use NOT NULL, UNIQUE, foreign keys, CHECK to enforce rules
- **Relationships**: Define clearly with appropriate cascade behaviors
- **Multi-Layer Validation**: Validate at both model and database levels

### Indexing Strategy

- **Foreign Keys**: Always index
- **Frequently Queried**: Index columns used in WHERE, JOIN, ORDER BY
- **Partial Unique**: For soft-deletes
- **GIN**: For full-text search

### Normalization

- Target 3NF, balance with query performance
- Avoid derived values
- Use junction tables for many-to-many

### Row Level Security

Enable RLS for user/tenant data isolation.

---

## Database Queries (Prisma)

### Security

- **SQL Injection**: Use Prisma's query builder; never interpolate user input
- **Parameterized Queries**: Always use prepared statements

### Performance

- **N+1 Prevention**: Use `include` for eager loading

```typescript
// ❌ BAD - N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { userId: user.id } });
}

// ✅ GOOD - Single query with include
const users = await prisma.user.findMany({
  include: { posts: true },
});
```

- **Select Specific**: Request only needed columns

```typescript
// ✅ Select only what you need
const users = await prisma.user.findMany({
  select: { id: true, name: true, email: true },
});
```

- **Timeouts**: Implement to prevent runaway queries
- **Bulk Operations**: Use `createMany` and `updateMany` for batch operations
- **Cursor Pagination**: Use for large datasets over offset methods

```typescript
// ✅ Cursor pagination
const posts = await prisma.post.findMany({
  take: 10,
  skip: 1,
  cursor: { id: lastPostId },
  orderBy: { createdAt: "desc" },
});
```

- **Transactions**: Wrap related operations

```typescript
await prisma.$transaction([
  prisma.user.update({
    where: { id },
    data: { balance: { decrement: amount } },
  }),
  prisma.transaction.create({ data: { userId: id, amount, type: "DEBIT" } }),
]);
```

### Caching & Monitoring

- **Caching**: Cache expensive queries with short TTLs (1–5m), invalidate on writes
- **Monitoring**: Analyze slow queries with `EXPLAIN ANALYZE` and `pg_stat_statements`

---

## Database Migrations (Prisma)

### Best Practices

- **Reversible**: Always consider rollback scenarios
- **Small Changes**: One logical change per migration
- **Separate Concerns**: Keep schema changes separate from data migrations
- **Clear Names**: Descriptive names indicating what migration does
- **Version Control**: Commit all migrations; never modify applied migrations
- **Zero-Downtime**: Consider deployment order and backwards compatibility
- **Index Management**: Use concurrent options to avoid locks on large tables
- **Test First**: Test on staging before production

### Migration Workflow

```bash
# Generate migration
npx prisma migrate dev --name add_user_profile

# Apply to production
npx prisma migrate deploy

# Reset database (dev only)
npx prisma migrate reset
```

### RLS After Migration

Enable Row Level Security and define CRUD policies after creating tables.

---

## Anti-Patterns

| Pattern              | Problem            | Solution                |
| -------------------- | ------------------ | ----------------------- |
| `SELECT *`           | Over-fetching      | Select specific columns |
| No indexes on FKs    | Slow joins         | Index foreign keys      |
| String interpolation | SQL injection      | Parameterized queries   |
| No pagination        | Memory issues      | Cursor pagination       |
| Missing transactions | Data inconsistency | Wrap related ops        |
| No soft deletes      | Data loss          | Add deletedAt           |
| Hardcoded secrets    | Security risk      | Environment variables   |
