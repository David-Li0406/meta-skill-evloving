---
name: bun-dev
description: Use this skill when working with the Bun runtime, including bun:sqlite, Bun.serve, bun:test, or any Bun-specific patterns.
---

# Bun Development

Bun runtime → native APIs → zero-dependency patterns.

## When to Use

- Bun runtime development
- SQLite database with bun:sqlite
- HTTP server with Bun.serve
- Testing with bun:test
- File operations with Bun.file/Bun.write
- Shell operations with $ template
- Password hashing with Bun.password
- Environment variable handling
- Building and bundling

**NOT for:** Node.js-only patterns, cross-runtime libraries, non-Bun projects

## Runtime Basics

**Package Management:**

```bash
bun install          # Install dependencies
bun add zod          # Add package
bun remove zod       # Remove package
bun update           # Update all packages
```

**Script Execution:**

```bash
bun run dev          # Run package.json script
bun run src/index.ts # Execute TypeScript directly
bun --watch index.ts # Watch mode
```

**Testing:**

```bash
bun test             # Run all tests
bun test src/        # Run tests in a directory
bun test --watch     # Watch mode for tests
bun test --coverage  # Run tests with coverage
```

**Building:**

```bash
bun build ./index.ts --outfile dist/bundle.js
bun build ./index.ts --compile --outfile myapp  # Create standalone executable
```

## File Operations

```typescript
// Read file (lazy, efficient)
const file = Bun.file('./data.json');
if (!(await file.exists())) throw new Error('File not found');

// Read formats
const text = await file.text();
const json = await file.json();
const buffer = await file.arrayBuffer();
const stream = file.stream(); // For large files

// Metadata
console.log(file.size, file.type);

// Write operations
await Bun.write('./output.txt', 'content');
await Bun.write('./data.json', JSON.stringify(data));
await Bun.write('./blob.txt', new Blob(['data']));
```

## SQLite (bun:sqlite)

```typescript
import { Database } from 'bun:sqlite';

const db = new Database('app.db', { create: true, readwrite: true, strict: true });

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
const createUser = db.prepare('INSERT INTO users (id, email, name) VALUES (?, ?, ?)');
```