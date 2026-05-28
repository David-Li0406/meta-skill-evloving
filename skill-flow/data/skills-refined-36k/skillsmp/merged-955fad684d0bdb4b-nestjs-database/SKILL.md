---
name: nestjs-database
description: Use this skill for implementing data access patterns, scaling strategies, migrations, and ORM selection in NestJS applications.
---

# NestJS Database Standards

## **Priority: P0 (FOUNDATIONAL)**

Database integration patterns and ORM standards for NestJS applications.

## Selection Strategy

### 1. Data Structure Analysis (The "What")

- **Structured & Highly Related**: Users, Orders, Inventory, Financials.
  - **Choice**: **PostgreSQL** (Default).
  - _Why_: Strict schema validation, ACID transactions, complex generic queries (Joins).
- **Unstructured / Polymorphic**: Product Catalogs, CMS Content, Raw JSON blobs.
  - **Choice**: **MongoDB**.
  - _Why_: Schema flexibility, fast development speed for flexible data models.
- **Time-Series / Metrics**: IoT Sensor Data, Stock Prices, Server Logs.
  - **Choice**: **TimescaleDB** (Postgres Extension).
  - _Why_: Compression, hypertable partitioning, rapid ingestion.

### 2. Access Pattern Analysis (The "How")

- **Transactional (OLTP)**: "User buys items to cart".
  - **Requirement**: Strong Consistency (ACID). **SQL** is mandatory.
- **Analytical (OLAP)**: "Dashboard showing sales trends".
  - **Requirement**: Aggregation speed. Columnar storage (ClickHouse) or Read Replicas.
- **High Throughput Write**: "1M events/sec".
  - **Requirement**: Append-only speed. **Cassandra** / **DynamoDB** (Leaderless replication).

### 3. Decision Matrix

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

## Scaling & Production

- **Read Replicas**: Configure separate `replication` connections (Master for Write, Slaves for Read) in TypeORM/Prisma to distribute load.
- **Connection Multiplexing**:
  - **Problem**: Scaling K8s pods to 100+ exhausts DB connection limits.
  - **Solution**: Use **PgBouncer** (Postgres) or **ProxySQL** (MySQL) in transaction mode. Do NOT rely solely on ORM pooling.
- **Migrations**:
  - **NEVER** run `synchronize: true` in production.
  - **Execution**: Run migrations via a dedicated "init container" or CD job step. Do **NOT** auto-run inside the main app process on startup.
- **Soft Deletes**: Use `@DeleteDateColumn` (TypeORM) or middleware (Prisma) to preserve data integrity.

## Architectures (Multi-Tenancy & Sharding)

- **Column-Based (SaaS Standard)**: Single DB, `tenant_id` column.
  - _Scale_: High. _Isolation_: Low.
- **Schema-Based**: One DB, one Schema per Tenant.
  - _Scale_: Medium. _Isolation_: Medium.
- **Database-Based**: One DB per Tenant.
  - _Scale_: Low. _Isolation_: High.
- **Horizontal Sharding**: Shard massive tables by a key across physical nodes to exceed single-node write limits.
- **Partitioning (Postgres)**: Use native Table Partitioning for massive tables.

## Migrations & Data Evolution

- **Separation**:
  - **Schema Migrations (DDL)**: Structural changes. Fast. Run before app deploy.
  - **Data Migrations (DML)**: Transforming data. Slow. Run as background jobs.
- **Zero-Downtime Field Migration (Expand-Contract Pattern)**:
  1. **Expand**: Add new column (nullable). Deploy App v1.
  2. **Migrate**: Backfill data in batches.
  3. **Contract**: Deploy App v2. Drop old field in next schema migration.
- **Seeding**:
  - **Dev**: Use factories to generate mock data.
  - **Prod**: Only seed static dictionaries using "Upsert" logic.

## Best Practices

1. **Pagination**: Mandatory. Use limit/offset or cursor-based pagination.
2. **Indexing**: Define indexes in code for frequently filtered columns.
3. **Transactions**: Use `QueryRunner` (TypeORM) or `$transaction` (Prisma) for all multi-step mutations to ensure atomicity.