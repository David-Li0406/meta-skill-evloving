# 4. Prisma Tools & Telemetry

**Impact: MEDIUM**

Managing your database in 2026 requires modern tools.

## 4.1 Prisma Studio (2026 Edition)

The new Prisma Studio is faster and supports:
- **Direct SQL Execution**: Run TypedSQL queries directly.
- **Data Export**: Export results to CSV/JSON/SQL inserts.
- **Relational Navigation**: Deep-link between related records.

## 4.2 Telemetry and Monitoring

Prisma 7 includes native OpenTelemetry support.

```typescript
// prisma.config.ts
import { defineConfig } from '@prisma/config';

export default defineConfig({
  telemetry: {
    enabled: true,
    provider: 'otel', // Exports to Honeycomb, Datadog, etc.
  }
});
```

## 4.3 Migration Workflows

Never run `prisma db push` in production. Use versioned migrations.

1.  **Dev**: `bun prisma migrate dev --name init`
2.  **CI/CD**: `bun prisma migrate deploy`

**Pro Tip**: Use `prisma migrate diff` to generate SQL between two states for manual review before applying.
