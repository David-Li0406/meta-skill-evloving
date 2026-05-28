---
name: nestjs-database
description: Use this skill when you need to implement database integration patterns, ORM selection, and migration strategies in NestJS applications.
---

# NestJS Database Standards

## **Priority: P0 (FOUNDATIONAL)**

Database integration patterns and ORM standards for NestJS applications.

## Selection Strategy

### Data Structure Analysis

- **Structured & Highly Related**: Use **PostgreSQL** for strict schema validation and complex queries.
- **Unstructured / Polymorphic**: Use **MongoDB** for schema flexibility and rapid development.
- **Time-Series / Metrics**: Use **TimescaleDB** (Postgres Extension) for efficient data handling.

### Access Pattern Analysis

- **Transactional (OLTP)**: Use SQL for strong consistency.
- **Analytical (OLAP)**: Consider columnar storage solutions for aggregation speed.
- **High Throughput Write**: Use **Cassandra** or **DynamoDB** for append-only speed.

## Decision Matrix

| Feature Needed         | Primary Choice    | Alternative            |
| :--------------------- | :---------------- | :--------------------- |
| General Purpose App    | **PostgreSQL**    | MySQL                  |
| Flexible JSON Docs     | **MongoDB**       | PostgreSQL (JSONB)     |
| Search Engine          | **ElasticSearch** | PostgreSQL (Full Text) |
| Financial Transactions | **PostgreSQL**    | (None)                 |

## Patterns

- **Repository Pattern**: Isolate database logic.
  - **TypeORM**: Inject `@InjectRepository(Entity)`.
  - **Prisma**: Create a comprehensive `PrismaService`.
- **Abstraction**: Services should call Repositories, not raw SQL queries.

## Configuration (TypeORM)

- **Async Loading**: Always use `TypeOrmModule.forRootAsync` to load secrets from `ConfigService`.
- **Sync**: Set `synchronize: false` in production; use migrations instead.

## Migrations

- **Never** use `synchronize: true` in production.
- **Execution**: Run via init container or CD step.
- **Zero-Downtime**: Use Expand-Contract pattern (Add -> Backfill -> Drop).
- **Seeding**: Use factories for dev data; only static dicts for prod.

## Best Practices

1. **Pagination**: Mandatory. Use limit/offset or cursor-based pagination.
2. **Indexing**: Define indexes in code (decorators/schema) for frequently filtered columns (`where`, `order by`).
3. **Transactions**: Use `QueryRunner` (TypeORM) or `$transaction` (Prisma) for all multi-step mutations to ensure atomicity.