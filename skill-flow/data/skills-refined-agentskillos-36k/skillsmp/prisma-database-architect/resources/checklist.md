# Prisma Schema Design Checklist
  
Use this checklist before applying any schema changes.

## Naming Conventions

- [ ] **Models**: PascalCase (e.g., `UserProfile`, not `user_profile`).
- [ ] **Fields**: camelCase (e.g., `firstName`, not `first_name`).
- [ ] **Enums**: PascalCase (e.g., `UserRole`).
- [ ] **Map Names**: Use `@@map` to use snake_case for database table names (Postgres standard).

  ```prisma
  model User {
    id        String   @id
    createdAt DateTime @map("created_at")
    @@map("users")
  }
  ```

## Performance & Indexing

- [ ] **Foreign Keys**: Are all `@relation` fields indexed? (Prisma does not do this automatically for all DBs).

  ```prisma
  authorId String
  @@index([authorId])
  ```

- [ ] **Filtering**: Are fields used in `WHERE` clauses indexed?
- [ ] **Uniqueness**: Are `@@unique` constraints applied to fields that must be unique (email, slug)?
- [ ] **Composite Indexes**: Are there `@@index([fieldA, fieldB])` for common multi-field filters?

## Relations

- [ ] **Explicit Names**: Do ambiguous relations have explicit names?

  ```prisma
  sentMessages     Message[] @relation("Sender")
  receivedMessages Message[] @relation("Receiver")
  ```

- [ ] **Cascades**: Is `onDelete: Cascade` applied appropriately? (Avoid for critical data).

## Data Integrity

- [ ] **Enums**: Are native Enums used for fixed states (Status, Role)?
- [ ] **Defaults**: Are `@default(now())` or `@default(uuid())` used where possible to simplify client logic?
