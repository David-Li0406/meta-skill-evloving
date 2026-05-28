---
name: bun-development
description: Use this skill when working with the Bun runtime, including bun:sqlite, Bun.serve, bun:test, and other Bun-specific patterns.
---

# Bun Development

Bun runtime → native APIs → zero-dependency patterns.

<when_to_use>

- Bun runtime development
- SQLite database with bun:sqlite
- HTTP server with Bun.serve
- Testing with bun:test
- File operations with Bun.file/Bun.write
- Shell operations with $ template
- Password hashing with Bun.password
- Environment variable handling
- Building and bundling

NOT for: Node.js-only patterns, cross-runtime libraries, non-Bun projects

</when_to_use>

<runtime_basics>

**Package management**:

```bash
bun install          # Install deps
bun add <package>    # Add package
bun remove <package> # Remove package
bun update           # Update all
```

**Script execution**:

```bash
bun run <script>     # Run package.json script
bun run <file>       # Execute TypeScript directly
bun --watch <file>   # Watch mode
```

**Testing**:

```bash
bun test             # All tests
bun test <directory> # Directory
bun test --watch     # Watch mode
bun test --coverage  # With coverage
```

**Building**:

```bash
bun build <file> --outfile <output>  # Build with output
bun build <file> --compile --outfile <executable>  # Standalone executable
```

</runtime_basics>

## File Operations

<file_operations>

```typescript
// Read file (lazy, efficient)
const file = Bun.file('<path>');
if (!(await file.exists())) throw new Error('File not found');

// Read formats
const text = await file.text();
const json = await file.json();
const buffer = await file.arrayBuffer();
const stream = file.stream(); // Large files

// Metadata
console.log(file.size, file.type);

// Write
await Bun.write('<output_path>', 'content');
await Bun.write('<data_path>', JSON.stringify(data));
await Bun.write('<blob_path>', new Blob(['data']));
```

</file_operations>

## SQLite (bun:sqlite)

<sqlite>

```typescript
import { Database } from 'bun:sqlite';

const db = new Database('<database>', { create: true, readwrite: true, strict: true });

// Create tables
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

// Prepared statements (always use these)
const getUser = db.prepare('SELECT * FROM users WHERE id = ?');
const createUser = db.prepare('INSERT INTO users (id, email, name) VALUES (?, ?, ?) RETURNING *');

// Execution
const user = getUser.get('<user_id>');                    // Single row
const all = db.prepare('SELECT * FROM users').all();     // All rows
db.prepare('DELETE FROM users WHERE id = ?').run('<id>');  // No return

// Named parameters
const stmt = db.prepare('SELECT * FROM users WHERE email = $email');
stmt.get({ $email: '<email>' });

// Transactions (atomic, auto-rollback on error)
const transfer = db.transaction((fromId: string, toId: string, amount: number) => {
  db.run('UPDATE accounts SET balance = balance - ? WHERE id = ?', [amount, fromId]);
  db.run('UPDATE accounts SET balance = balance + ? WHERE id = ?', [amount, toId]);
});
transfer('<from_id>', '<to_id>', <amount>);

db.close(); // When done
```

</sqlite>

## Password Hashing

<password>

```typescript
// Hash (argon2id recommended)
const hash = await Bun.password.hash('<password>', {
  algorithm: 'argon2id',
  memoryCost: 65536,  // 64 MB
  timeCost: 3
});

// Or bcrypt
const bcryptHash = await Bun.password.hash('<password>', {
  algorithm: 'bcrypt',
  cost: 12
});

// Verify
const isValid = await Bun.password.verify('<password>', hash);
if (!isValid) throw new Error('Invalid password');
```

**Auth flow example**:

```typescript
app.post('/auth/register', zValidator('json', RegisterSchema), async (c) => {
  const { email, password } = c.req.valid('json');
  const db = c.get('db');

  if (db.prepare('SELECT id FROM users WHERE email = ?').get(email)) {
    throw new HTTPException(409, { message: 'Email already registered' });
  }

  const hashedPassword = await Bun.password.hash(password, { algorithm: 'argon2id' });
  const user = db.prepare(`
    INSERT INTO users (id, email, password) VALUES (?, ?, ?) RETURNING id, email
  `).get(crypto.randomUUID(), email, hashedPassword);

  return c.json({ user }, 201);
});
```

</password>

## HTTP Server

<http_server>

```typescript
Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === '/') return new Response('Hello');
    if (url.pathname === '/json') return Response.json({ ok: true });
    return new Response('Not found', { status: 404 });
  },
  error(err) {
    return new Response(`Error: ${err.message}`, { status: 500 });
  }
});
```

**With Hono** (recommended for APIs):

```typescript
import { Hono } from 'hono';

const app = new Hono()
  .get('/', (c) => c.text('Hello'))
  .get('/json', (c) => c.json({ ok: true }));

Bun.serve({ port: 3000, fetch: app.fetch });
```

</http_server>

## WebSocket

<websocket>

```typescript
import type { ServerWebSocket } from 'bun';

type WsData = { userId: string };

Bun.serve<WsData>({
  port: 3000,
  fetch(req, server) {
    const url = new URL(req.url);
    if (url.pathname === '/ws') {
      const userId = url.searchParams.get('userId') || 'anon';
      return server.upgrade(req, { data: { userId } }) ? undefined
        : new Response('Upgrade failed', { status: 400 });
    }
    return new Response('Hello');
  },
  websocket: {
    open(ws: ServerWebSocket<WsData>) {
      ws.subscribe('chat');
      ws.send(JSON.stringify({ type: 'connected' }));
    },
    message(ws: ServerWebSocket<WsData>, msg: string | Buffer) {
      ws.publish('chat', msg);
    },
    close(ws: ServerWebSocket<WsData>) {
      ws.unsubscribe('chat');
    }
  }
});
```

</websocket>

## Shell Operations

<shell>

```typescript
import { $ } from 'bun';

// Run commands
const result = await $`<command>`;
console.log(result.text());

// Variables (auto-escaped)
const dir = '<directory>';
await $`find ${dir} -name "*.ts"`;

// Check exit code
const { exitCode } = await $`npm test`.nothrow();
if (exitCode !== 0) console.error('Tests failed');

// Spawn process
const proc = Bun.spawn(['<command>', '<args>']);
await proc.exited;

// Capture output
const proc2 = Bun.spawn(['echo', 'Hello'], { stdout: 'pipe' });
const output = await new Response(proc2.stdout).text();
```

</shell>

## Testing (bun:test)

<testing>

```typescript
import { describe, test, expect, beforeEach, afterEach } from 'bun:test';

describe('feature', () => {
  let db: Database;

  beforeEach(() => { db = new Database(':memory:'); });
  afterEach(() => { db.close(); });

  test('behavior', () => {
    expect(result).toBe(expected);
    expect(arr).toContain(item);
    expect(fn).toThrow();
    expect(obj).toEqual({ foo: 'bar' });
  });

  test('async', async () => {
    const result = await asyncFn();
    expect(result).toBeDefined();
  });

  test.todo('pending feature');
  test.skip('temporarily disabled');
});
```

```bash
bun test                    # All tests
bun test <file>            # Specific file
bun test --watch            # Watch mode
bun test --coverage         # With coverage
```

</testing>

## Environment Variables

<environment>

```typescript
// Access
console.log(Bun.env.NODE_ENV);
console.log(Bun.env.DATABASE_URL);

// Zod validation
import { z } from 'zod';

const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  DATABASE_URL: z.string(),
  PORT: z.coerce.number().int().positive().default(3000),
  API_KEY: z.string().min(32)
});

export const env = EnvSchema.parse(Bun.env);
```

Bun auto-loads `.env`, `.env.local`, `.env.production`.

</environment>

## Performance Utilities

<performance>

```typescript
// High-resolution timing
const start = Bun.nanoseconds();
await doWork();
console.log(`Took ${(Bun.nanoseconds() - start) / 1_000_000}ms`);

// Hashing
const hash = Bun.hash(data);
const crc32 = Bun.hash.crc32(data);
const sha256 = Bun.CryptoHasher.hash('sha256', data);

// Sleep
await Bun.sleep(1000);

// Memory
const { rss, heapUsed } = process.memoryUsage();
console.log('RSS:', rss / 1024 / 1024, 'MB');
```

</performance>

## Building & Bundling

<building>

```bash
# Production bundle
bun build <file> --outfile <output> --minify --sourcemap

# External deps
bun build <file> --outfile <output> --external <dep1> --external <dep2>

# Standalone executable
bun build <file> --compile --outfile <executable>

# Cross-compile
bun build <file> --compile --target=<target> --outfile <output>
```

</building>

<rules>

ALWAYS:
- Use Bun APIs when available (faster, native)
- Prepared statements for database queries
- Transactions for multi-statement operations
- argon2id for password hashing
- Validate environment variables at startup
- Close database connections when done

NEVER:
- String interpolation in SQL (use parameters)
- Plaintext passwords
- Ignore async disposal cleanup
- Deprecated Node.js APIs when Bun native exists

PREFER:
- Bun.file over fs.readFile
- Bun.write over fs.writeFile
- bun:sqlite over external SQLite libraries
- Bun.password over bcrypt/argon2 packages
- $ shell template over child_process

</rules>

<references>

- [sqlite-patterns.md](references/sqlite-patterns.md) — migrations, pooling, repository, FTS
- [server-patterns.md](references/server-patterns.md) — HTTP, WebSocket, streaming, compression
- [testing.md](references/testing.md) — assertions, mocking, snapshots, best practices

**Examples:**
- [database-crud.md](examples/database-crud.md) — SQLite CRUD patterns
- [file-uploads.md](examples/file-uploads.md) — streaming file handling

</references>