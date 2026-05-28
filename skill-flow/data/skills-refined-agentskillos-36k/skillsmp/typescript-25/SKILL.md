---
name: typescript
description: >
  TypeScript strict patterns and best practices.
  Trigger: When implementing or refactoring TypeScript in .ts/.tsx (types, interfaces, generics, const maps, type guards, removing any, tightening unknown).
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [root, web, api]
  auto_invoke: 'Writing TypeScript types/interfaces'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Const Types Pattern (REQUIRED)

```typescript
// ✅ ALWAYS: Create const object first, then extract type
const CLIENT_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  PENDING: 'pending',
} as const;

type ClientStatus = (typeof CLIENT_STATUS)[keyof typeof CLIENT_STATUS];

// ❌ NEVER: Direct union types
type ClientStatus = 'active' | 'inactive' | 'pending';
```

**Why?** Single source of truth, runtime values, autocomplete, easier refactoring.

## Flat Interfaces (REQUIRED)

```typescript
// ✅ ALWAYS: One level depth, nested objects → dedicated interface
interface ClientAddress {
  street: string;
  city: string;
}

interface Client {
  id: string;
  name: string;
  address: ClientAddress;
}

interface Admin extends Client {
  permissions: string[];
}

// ❌ NEVER: Inline nested objects
interface Client {
  address: { street: string; city: string }; // NO!
}
```

## Never Use `any`

```typescript
// ✅ Use unknown for truly unknown types
function parse(input: unknown): Client {
  if (isClient(input)) return input;
  throw new Error('Invalid input');
}

// ✅ Use generics for flexible types
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// ❌ NEVER
function parse(input: any): any {}
```

## Utility Types

```typescript
Pick<Client, 'id' | 'name'>; // Select fields
Omit<Client, 'id'>; // Exclude fields
Partial<Client>; // All optional
Required<Client>; // All required
Readonly<Client>; // All readonly
Record<string, Client>; // Object type
Extract<Union, 'a' | 'b'>; // Extract from union
Exclude<Union, 'a'>; // Exclude from union
NonNullable<T | null>; // Remove null/undefined
ReturnType<typeof fn>; // Function return type
Parameters<typeof fn>; // Function params tuple
```

## Type Guards

```typescript
function isClient(value: unknown): value is Client {
  return typeof value === 'object' && value !== null && 'id' in value && 'name' in value;
}
```

## Import Types

```typescript
import type { Client } from './types';
import { createClient, type Config } from './utils';
```

## Strict Mode

TypeScript strict mode is enabled. No implicit any, strict null checks.

```typescript
// ✅ Explicit types
function greet(name: string): string {
  return `Hello, ${name}`;
}

// ❌ Implicit any (not allowed)
function greet(name) {
  // Error!
  return `Hello, ${name}`;
}
```

## Prisma Types

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

type PrismaClient = typeof prisma;
type Client = PrismaClient['client'];

// Prisma input types
import { Prisma } from '@prisma/client';

type ClientCreateInput = Prisma.ClientCreateInput;
type ClientUpdateInput = Prisma.ClientUpdateInput;
```

## Commands

```bash
npm run typecheck              # Type check all
npm run typecheck --workspace=@migestion/api   # API only
npm run typecheck --workspace=@migestion/web   # Web only
```
