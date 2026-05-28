# Node.js SDK (@databricks/sql)

## Installation

```bash
npm install @databricks/sql
```

## Basic Usage

```typescript
import { DBSQLClient } from "@databricks/sql";

const client = new DBSQLClient();

await client.connect({
  host: "<workspace>.cloud.databricks.com",
  path: "/sql/1.0/warehouses/<warehouse_id>",
  token: "<token>",
});

const session = await client.openSession();
const operation = await session.executeStatement("SELECT * FROM table");
const rows = await operation.fetchAll();

await operation.close();
await session.close();
await client.close();
```

## Connection Options

```typescript
await client.connect({
  host: process.env.DATABRICKS_HOST!,
  path: process.env.SQL_WAREHOUSE_HTTP_PATH!,
  token: accessToken,
  // Optional
  socketTimeout: 60000,  // milliseconds
});

// Session options
const session = await client.openSession({
  initialCatalog: "main",
  initialSchema: "default",
});
```

## Parameter Binding

```typescript
// Named parameters
const operation = await session.executeStatement(
  "SELECT * FROM users WHERE id = :userId AND status = :status",
  {
    namedParameters: {
      userId: { value: "123", type: "STRING" },
      status: { value: "active", type: "STRING" },
    },
  }
);
```

## Fetching Results

```typescript
// Fetch all rows
const rows = await operation.fetchAll();

// Fetch chunk
const chunk = await operation.fetchChunk({ maxRows: 1000 });

// Get schema
const schema = await operation.getSchema();
```

## Fastify Implementation Example

```typescript
import Fastify from "fastify";
import { DBSQLClient } from "@databricks/sql";

const fastify = Fastify({ logger: true });

const DATABRICKS_HOST = process.env.DATABRICKS_HOST!;
const SQL_WAREHOUSE_PATH = process.env.SQL_WAREHOUSE_HTTP_PATH!;

fastify.get("/api/users", async (request, reply) => {
  const accessToken = request.headers["x-forwarded-access-token"] as string;
  if (!accessToken) {
    return reply.status(401).send({ error: "No access token" });
  }

  const client = new DBSQLClient();

  try {
    await client.connect({
      host: DATABRICKS_HOST,
      path: SQL_WAREHOUSE_PATH,
      token: accessToken,
    });

    const session = await client.openSession();
    const operation = await session.executeStatement(
      "SELECT * FROM catalog.schema.users LIMIT 100"
    );
    const rows = await operation.fetchAll();

    await operation.close();
    await session.close();

    return rows;
  } finally {
    await client.close();
  }
});

fastify.listen({ port: 8000 });
```

## Reusable Helper

```typescript
import { DBSQLClient, IDBSQLSession, IOperation } from "@databricks/sql";

interface QueryResult<T> {
  rows: T[];
  schema: { name: string; type: string }[];
}

export async function executeQuery<T = Record<string, unknown>>(
  token: string,
  sql: string,
  params?: Record<string, { value: string; type: string }>
): Promise<QueryResult<T>> {
  const client = new DBSQLClient();
  let session: IDBSQLSession | null = null;
  let operation: IOperation | null = null;

  try {
    await client.connect({
      host: process.env.DATABRICKS_HOST!,
      path: process.env.SQL_WAREHOUSE_HTTP_PATH!,
      token,
    });

    session = await client.openSession();
    operation = await session.executeStatement(sql, {
      namedParameters: params,
    });

    const [rows, schema] = await Promise.all([
      operation.fetchAll(),
      operation.getSchema(),
    ]);

    return {
      rows: rows as T[],
      schema: schema?.columns?.map((c) => ({ name: c.name, type: c.type })) ?? [],
    };
  } finally {
    if (operation) await operation.close();
    if (session) await session.close();
    await client.close();
  }
}

// Usage example
const result = await executeQuery<{ id: string; name: string }>(
  accessToken,
  "SELECT id, name FROM users WHERE status = :status",
  { status: { value: "active", type: "STRING" } }
);
```

## Error Handling

```typescript
import { DBSQLClient } from "@databricks/sql";

try {
  const client = new DBSQLClient();
  await client.connect({ ... });
  // ...
} catch (error) {
  if (error instanceof Error) {
    // Determine cause from error message
    if (error.message.includes("AUTHENTICATION")) {
      console.error("Authentication error:", error.message);
    } else if (error.message.includes("INVALID_PARAMETER")) {
      console.error("Parameter error:", error.message);
    } else if (error.message.includes("timeout")) {
      console.error("Timeout:", error.message);
    } else {
      console.error("Error:", error.message);
    }
  }
}
```

## Important Notes

- Always `close()` client, session, and operation
- Adjust timeout settings for long-running queries
- Use `fetchChunk()` for large data retrieval
