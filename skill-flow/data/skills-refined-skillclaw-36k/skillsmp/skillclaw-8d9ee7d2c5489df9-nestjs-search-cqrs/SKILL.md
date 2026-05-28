---
name: nestjs-search-cqrs
description: Use this skill when integrating Elasticsearch with a NestJS application using CQRS patterns for efficient data synchronization and retrieval.
---

# Skill body

## Search Engine & Full-Text

### Strategy

- **Pattern**: **CQRS (Command Query Responsibility Segregation)**.
  - **Write**: To Primary Database (Postgres/MySQL). Source of Truth.
  - **Read (Complex)**: To Search Engine (Elasticsearch, OpenSearch, MeiliSearch). Optimized for filtering, fuzzy search, and aggregation.

### Synchronization (The Hard Part)

- **Dual Write (Anti-Pattern)**: Avoid using `await db.save(); await es.index();`.
  - _Why_: Partial failures can lead to data inconsistency and slow down HTTP responses.
- **Event-Driven (Recommended)**:
  1. Service writes to the database.
  2. Service emits `EntityUpdated`.
  3. Event Handler (Async) pushes to Queue (BullMQ).
  4. Worker indexes the document to the Search Engine with retries.
- **CDC (Golden Standard)**: Use Change Data Capture (Debezium) to connect directly to the database transaction log. This method has no application conceptual overhead but comes with higher operational complexity.

### Organization

- **Module**: Encapsulate the client in a `SearchModule`.
- **Abstraction**: Create generic `SearchService<T>` helpers with methods like:
  - `indexDocument(id, body)`
  - `search(query, filters)`
- **Mapping**: Use `class-transformer` to map Entities to "Search Documents". Ensure that search documents are flatter than relational entity constraints.

### Testing

- **E2E**: Do not mock the search engine in critical end-to-end flows.
- **Docker**: Spin up an `elasticsearch:8` container in the test harness to verify that indexing works correctly.