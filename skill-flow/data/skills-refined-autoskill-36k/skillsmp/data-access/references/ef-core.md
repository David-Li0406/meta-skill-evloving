# EF Core

## Configuration

- Keep DbContext in Infrastructure.
- Use explicit configuration classes for entities.
- Prefer `AsNoTracking` for read-only views.

## Migrations

- One migration per change set.
- Keep migration names descriptive.
- Avoid data seeding in migrations unless required.
