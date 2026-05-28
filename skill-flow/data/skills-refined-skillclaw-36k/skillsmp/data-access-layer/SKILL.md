---
name: data-access-layer
description: Build and update repository-based data access layers in TypeScript/Node apps. Use when asked to add a data access layer, repository layer, database access, new query methods, or to integrate/swap DB clients (for example porsager/postgres) while keeping model interfaces DB-agnostic and repository methods the only access path.
---

# Data Access Layer

## Overview

Create DB-agnostic model interfaces and repository contracts, then implement repositories that accept a generic DB connection and map DB rows into models. Keep all database access inside repositories; the rest of the codebase depends only on model interfaces and repository interfaces.

## Workflow

1. Scan the codebase for existing data or abstraction patterns and follow local naming and directory conventions.
2. Define model interfaces (domain types) with no persistence details, and keep them in a stable location (for example `lib/models/`).
3. Define repository interfaces that return model interfaces and accept domain inputs, and keep them separate from implementations (for example `lib/repositories/`).
4. Define a minimal `DbClient` interface with only the operations repositories need (query, transaction), and keep it in a shared DB module (for example `lib/db/types.ts`).
5. Implement repository classes or factories that accept `DbClient` and perform queries, and map DB rows to model interfaces inside the repository layer.
6. Provide adapters for concrete clients (porsager/postgres, pg, etc.) that implement `DbClient`.
7. Wire repositories through dependency injection at the composition root (API route, service, loader) and avoid importing query builders outside the repository layer.

## Repository rules

- Use repository methods for all DB access; do not execute queries in routes, services, or UI.
- Return model interfaces only; never return raw rows, query builder types, or ORM entities.
- Keep SQL/queries, row types, and mapping logic internal to repository implementations.
- Accept DB clients via constructor or factory parameters; do not create DB clients inside repository methods.
- Keep the `DbClient` interface minimal and stable to make swapping clients low impact.

## TypeScript pattern (example)

```ts
// lib/repositories/user-repository.ts
import type { User, CreateUserInput } from "../models/user";

// lib/models/user.ts
export interface User {
  id: string;
  email: string;
  createdAt: Date;
}

export interface CreateUserInput {
  email: string;
}

export interface UserRepository {
  getById(id: string): Promise<User | null>;
  listByOrg(orgId: string): Promise<User[]>;
  create(input: CreateUserInput): Promise<User>;
}
```

```ts
// lib/db/types.ts
export interface DbClient {
  query<T = unknown>(sql: string, params?: readonly unknown[]): Promise<T[]>;
  transaction<T>(fn: (tx: DbClient) => Promise<T>): Promise<T>;
}
```

```ts
// lib/repositories/user-repository-impl.ts
import type { DbClient } from "../db/types";
import type { User, CreateUserInput } from "../models/user";
import type { UserRepository } from "./user-repository";

type UserRow = {
  id: string;
  email: string;
  created_at: Date;
};

const mapUserRow = (row: UserRow): User => ({
  id: row.id,
  email: row.email,
  createdAt: row.created_at,
});

export const createUserRepository = (db: DbClient): UserRepository => ({
  async getById(id) {
    const rows = await db.query<UserRow>("select id, email, created_at from users where id = $1", [
      id,
    ]);
    return rows[0] ? mapUserRow(rows[0]) : null;
  },
  async listByOrg(orgId) {
    const rows = await db.query<UserRow>(
      "select id, email, created_at from users where org_id = $1 order by created_at desc",
      [orgId],
    );
    return rows.map(mapUserRow);
  },
  async create(input: CreateUserInput) {
    const rows = await db.query<UserRow>(
      "insert into users (email) values ($1) returning id, email, created_at",
      [input.email],
    );
    return mapUserRow(rows[0]);
  },
});
```

```ts
// lib/db/postgres-adapter.ts (example adapter)
import type { Sql } from "postgres";

import type { DbClient } from "./types";

export const createPostgresAdapter = (sql: Sql): DbClient => ({
  query: (text, params) => sql.unsafe(text, params) as Promise<unknown[]>,
  transaction: (fn) => sql.begin((tx) => fn(createPostgresAdapter(tx))),
});
```

## Checklist

- Verify models are DB-agnostic interfaces.
- Verify repository interfaces return models only.
- Verify repository implementations accept `DbClient` and contain all SQL/queries.
- Verify no DB client imports exist outside the repository layer.
- Verify swapping DB clients only affects adapter wiring and repository implementations.
