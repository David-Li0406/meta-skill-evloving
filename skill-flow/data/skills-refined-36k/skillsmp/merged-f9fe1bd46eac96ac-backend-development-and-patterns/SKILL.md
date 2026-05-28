---
name: backend-development-and-patterns
description: Use this skill when you need to implement robust backend systems, covering API design, authentication, error handling, security, and common backend patterns.
---

# Backend Development and Patterns Skill

## 📋 Table of Contents

1. [Overview](#overview)
2. [Detailed Guide](#detailed-guide)
3. [When to Use](#when-to-use)
4. [API Design](#api-design)
5. [Authentication and Authorization](#authentication-and-authorization)
6. [Error Handling](#error-handling)
7. [Security](#security)
8. [Common Patterns](#common-patterns)
9. [Practical Examples](#practical-examples)

---

## Overview

This skill covers the fundamentals of backend development, including:

- **API Design** - RESTful API, GraphQL
- **Authentication and Authorization** - JWT, OAuth
- **Error Handling** - Custom error classes, global error handlers
- **Security** - SQL Injection, XSS, CSRF prevention
- **Common Patterns** - Repository pattern, service layer, caching strategies

---

## Detailed Guide

### 1. API Design

#### RESTful API Design

```typescript
// Endpoint Design
GET    /api/users          # List users
GET    /api/users/:id      # Get user details
POST   /api/users          # Create user
PUT    /api/users/:id      # Update user
DELETE /api/users/:id      # Delete user
```

#### Response Format

```typescript
// Success Response
type SuccessResponse<T> = {
  success: true;
  data: T;
};

// Error Response
type ErrorResponse = {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
};

type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;
```

### 2. Authentication and Authorization

#### JWT (JSON Web Token)

```typescript
// Token Generation
import jwt from 'jsonwebtoken';

function generateToken(userId: string) {
  return jwt.sign({ userId }, process.env.JWT_SECRET!, { expiresIn: '7d' });
}

// Token Verification
function verifyToken(token: string) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET!);
  } catch (error) {
    throw new Error('Invalid token');
  }
}
```

### 3. Error Handling

#### Custom Error Classes

```typescript
class AppError extends Error {
  constructor(public statusCode: number, public code: string, message: string, public details?: any) {
    super(message);
    this.name = 'AppError';
  }
}

class ValidationError extends AppError {
  constructor(message: string, details?: any) {
    super(400, 'VALIDATION_ERROR', message, details);
  }
}
```

### 4. Security

#### SQL Injection Prevention

```typescript
// Good Example (Using Prisma)
const user = await prisma.user.findUnique({ where: { id: userId } });
```

### 5. Common Patterns

#### Repository Pattern

```typescript
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}

class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }
}
```

#### Service Layer

```typescript
class CreateUserUseCase {
  constructor(private userRepository: UserRepository) {}

  async execute(input: CreateUserInput): Promise<User> {
    const validated = CreateUserSchema.parse(input);
    const user = User.create(validated);
    return this.userRepository.save(user);
  }
}
```

#### Caching Strategy

```typescript
async function getUser(id: string): Promise<User> {
  const cached = await cache.get(`user:${id}`);
  if (cached) return cached;

  const user = await userRepository.findById(id);
  await cache.set(`user:${id}`, user, { ttl: 3600 });
  return user;
}
```

---

## Practical Examples

### Example 1: User CRUD API

```typescript
// routes/users.ts
import express from 'express';
import { prisma } from '../lib/prisma';

const router = express.Router();

router.get('/', async (req, res) => {
  const users = await prisma.user.findMany();
  res.json({ data: users });
});

// Additional CRUD operations...
```

### Example 2: Authentication API

```typescript
router.post('/register', async (req, res) => {
  const data = req.body; // Validate and process input
  const user = await prisma.user.create({ data });
  const token = generateToken(user.id);
  res.status(201).json({ data: user, token });
});
```

---

## When to Use

### 🎯 Essential Timing

- [ ] When creating new API endpoints
- [ ] During database schema design
- [ ] When implementing authentication features
- [ ] During security reviews

---

## Related Skills

- **nodejs-development** - Detailed Node.js/Express skills
- **python-development** - Detailed Python/FastAPI skills
- **database-design** - Detailed database design skills
- **api-design** - Detailed API design skills

---

_Last updated: 2025-12-24_