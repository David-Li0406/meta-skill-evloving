---
name: jikime-lang-javascript
description: JavaScript ES2024+ development specialist covering Node.js 22 LTS, Bun 1.x (serve, SQLite, S3, shell, test), Deno 2.x, testing (Vitest, Jest), linting (ESLint 9, Biome), and backend frameworks (Express, Fastify, Hono). Use when developing JavaScript APIs, web applications, or Node.js projects.
version: 1.0.0
tags: ["language", "javascript", "nodejs", "bun", "deno", "express", "fastify", "vitest"]
triggers:
  keywords: ["javascript", "nodejs", "bun", "deno", "express", "fastify", "자바스크립트"]
  phases: ["run"]
  agents: ["backend", "frontend"]
  languages: ["javascript"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
---

# JavaScript Development Guide

JavaScript ES2024+ / Node.js 22 개발을 위한 간결한 가이드.

## Quick Reference

| 용도 | 도구 | 특징 |
|------|------|------|
| Runtime | **Node.js 22** | LTS, 안정적 |
| Runtime | **Bun** | 빠름, 올인원 |
| Framework | **Express** | 미니멀, 유연 |
| Framework | **Fastify** | 빠름, 스키마 |
| Testing | **Vitest** | 빠름, ESM |

## Project Setup

```bash
# Node.js
npm init -y
npm install express

# Bun
bun init
bun add express
```

## Express Patterns

### Basic API

```javascript
import express from 'express';

const app = express();
app.use(express.json());

// Routes
app.get('/api/users', async (req, res) => {
  const users = await UserService.list();
  res.json(users);
});

app.get('/api/users/:id', async (req, res) => {
  const user = await UserService.get(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'Not found' });
  }
  res.json(user);
});

app.post('/api/users', async (req, res) => {
  const user = await UserService.create(req.body);
  res.status(201).json(user);
});

app.listen(3000);
```

### Middleware

```javascript
// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong' });
});

// Auth middleware
const authenticate = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'No token' });
  }

  const user = await verifyToken(token);
  if (!user) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  req.user = user;
  next();
};

app.get('/api/me', authenticate, (req, res) => {
  res.json(req.user);
});
```

## Bun Patterns

### HTTP Server

```javascript
// Bun native server
Bun.serve({
  port: 3000,
  async fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === '/api/users' && req.method === 'GET') {
      const users = await getUsers();
      return Response.json(users);
    }

    return new Response('Not Found', { status: 404 });
  },
});
```

### SQLite (Built-in)

```javascript
import { Database } from 'bun:sqlite';

const db = new Database('app.db');

db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  )
`);

const insert = db.prepare('INSERT INTO users (name, email) VALUES (?, ?)');
insert.run('John', 'john@example.com');

const users = db.query('SELECT * FROM users').all();
```

## Modern JavaScript

### ES2024 Features

```javascript
// Array grouping
const grouped = Object.groupBy(users, user => user.role);

// Promise.withResolvers
const { promise, resolve, reject } = Promise.withResolvers();

// Top-level await
const config = await loadConfig();

// Optional chaining & nullish coalescing
const name = user?.profile?.name ?? 'Anonymous';
```

### Async Patterns

```javascript
// Promise.all for parallel
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);

// Promise.allSettled for error tolerance
const results = await Promise.allSettled([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3)
]);

// Async iterator
async function* fetchPages() {
  let page = 1;
  while (true) {
    const data = await fetchPage(page++);
    if (!data.length) break;
    yield data;
  }
}

for await (const page of fetchPages()) {
  console.log(page);
}
```

## Testing with Vitest

```javascript
import { describe, it, expect, vi } from 'vitest';

describe('UserService', () => {
  it('creates user successfully', async () => {
    const user = await UserService.create({
      name: 'John',
      email: 'john@example.com'
    });

    expect(user.id).toBeDefined();
    expect(user.name).toBe('John');
  });

  it('throws on duplicate email', async () => {
    await expect(
      UserService.create({ name: 'John', email: 'existing@example.com' })
    ).rejects.toThrow('Email already exists');
  });
});

// Mocking
vi.mock('./database', () => ({
  query: vi.fn(() => Promise.resolve([{ id: 1, name: 'John' }]))
}));
```

## Project Structure

```
project/
├── src/
│   ├── index.js
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── middleware/
├── tests/
├── package.json
└── README.md
```

## Best Practices

- **ESM**: `"type": "module"` 사용
- **Async/Await**: Promise 체인 대신 async/await
- **Error Handling**: try/catch와 에러 미들웨어 사용
- **환경변수**: dotenv 또는 Bun 내장 사용
- **Validation**: Zod로 입력 검증

---

Last Updated: 2026-01-21
Version: 2.0.0
