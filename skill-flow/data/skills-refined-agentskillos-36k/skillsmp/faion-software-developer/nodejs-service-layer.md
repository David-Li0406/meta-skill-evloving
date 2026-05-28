---
id: nodejs-service-layer
name: "Node.js Service Layer"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Node.js Service Layer

## Overview

The service layer pattern in Node.js separates business logic from HTTP handling, creating testable, reusable code. This methodology covers the Controller-Service-Repository pattern, dependency injection, and best practices for enterprise Node.js applications.

## When to Use

- Building REST APIs with Express/Fastify
- Applications with complex business logic
- Projects requiring high testability
- Microservices architecture
- Applications needing clear separation of concerns

## Key Principles

1. **Thin controllers** - Only handle HTTP request/response
2. **Fat services** - Contain all business logic
3. **Repository pattern** - Abstract data access
4. **Dependency injection** - Enable testability
5. **Single responsibility** - Each layer has one job

## Best Practices

### Layer Responsibilities

```
┌─────────────────────────────────────┐
│           Controllers               │  HTTP handling, validation
│   (Request → Response)              │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│            Services                 │  Business logic, orchestration
│   (Business Logic)                  │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│          Repositories               │  Data access, queries
│   (Data Access)                     │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│           Database                  │
└─────────────────────────────────────┘
```

### Project Structure

```
src/
├── app.ts                  # Express app setup
├── server.ts               # Server entry point
├── config/
│   ├── index.ts           # Configuration
│   └── database.ts        # DB connection
│
├── controllers/
│   ├── index.ts
│   ├── users.controller.ts
│   └── orders.controller.ts
│
├── services/
│   ├── index.ts
│   ├── users.service.ts
│   └── orders.service.ts
│
├── repositories/
│   ├── index.ts
│   ├── users.repository.ts
│   └── orders.repository.ts
│
├── models/
│   ├── user.model.ts
│   └── order.model.ts
│
├── middleware/
│   ├── auth.ts
│   ├── errorHandler.ts
│   └── validate.ts
│
├── routes/
│   ├── index.ts
│   └── users.routes.ts
│
├── types/
│   └── index.ts
│
└── utils/
    ├── errors.ts
    └── logger.ts
```

### Repository Layer

```typescript
// repositories/users.repository.ts
import { PrismaClient, User, Prisma } from '@prisma/client';

export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  findAll(params: FindAllParams): Promise<{ users: User[]; total: number }>;
  create(data: CreateUserData): Promise<User>;
  update(id: string, data: UpdateUserData): Promise<User>;
  delete(id: string): Promise<void>;
}

interface FindAllParams {
  page: number;
  limit: number;
  search?: string;
}

interface CreateUserData {
  email: string;
  name: string;
  hashedPassword: string;
}

interface UpdateUserData {
  email?: string;
  name?: string;
}

export class UserRepository implements IUserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { id },
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
    });
  }

  async findAll(params: FindAllParams): Promise<{ users: User[]; total: number }> {
    const { page, limit, search } = params;
    const skip = (page - 1) * limit;

    const where: Prisma.UserWhereInput = search
      ? {
          OR: [
            { name: { contains: search, mode: 'insensitive' } },
            { email: { contains: search, mode: 'insensitive' } },
          ],
        }
      : {};

    const [users, total] = await Promise.all([
      this.prisma.user.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.user.count({ where }),
    ]);

    return { users, total };
  }

  async create(data: CreateUserData): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserData): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }
}
```

### Service Layer

```typescript
// services/users.service.ts
import { User } from '@prisma/client';
import { IUserRepository } from '../repositories/users.repository';
import { hashPassword, comparePasswords } from '../utils/password';
import { NotFoundError, ConflictError, UnauthorizedError } from '../utils/errors';

export interface IUserService {
  getUser(id: string): Promise<User>;
  getUsers(page: number, limit: number, search?: string): Promise<PaginatedUsers>;
  createUser(data: CreateUserDto): Promise<User>;
  updateUser(id: string, data: UpdateUserDto): Promise<User>;
  deleteUser(id: string): Promise<void>;
  authenticateUser(email: string, password: string): Promise<User>;
}

interface CreateUserDto {
  email: string;
  name: string;
  password: string;
}

interface UpdateUserDto {
  email?: string;
  name?: string;
}

interface PaginatedUsers {
  users: User[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export class UserService implements IUserService {
  constructor(private userRepository: IUserRepository) {}

  async getUser(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);

    if (!user) {
      throw new NotFoundError(`User with id ${id} not found`);
    }

    return user;
  }

  async getUsers(
    page: number,
    limit: number,
    search?: string
  ): Promise<PaginatedUsers> {
    const { users, total } = await this.userRepository.findAll({
      page,
      limit,
      search,
    });

    return {
      users,
      total,
      page,
      limit,
      pages: Math.ceil(total / limit),
    };
  }

  async createUser(data: CreateUserDto): Promise<User> {
    // Check for existing user
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      throw new ConflictError('User with this email already exists');
    }

    // Hash password
    const hashedPassword = await hashPassword(data.password);

    // Create user
    return this.userRepository.create({
      email: data.email,
      name: data.name,
      hashedPassword,
    });
  }

  async updateUser(id: string, data: UpdateUserDto): Promise<User> {
    // Verify user exists
    await this.getUser(id);

    // Check email uniqueness if updating email
    if (data.email) {
      const existing = await this.userRepository.findByEmail(data.email);
      if (existing && existing.id !== id) {
        throw new ConflictError('Email already in use');
      }
    }

    return this.userRepository.update(id, data);
  }

  async deleteUser(id: string): Promise<void> {
    await this.getUser(id); // Verify exists
    await this.userRepository.delete(id);
  }

  async authenticateUser(email: string, password: string): Promise<User> {
    const user = await this.userRepository.findByEmail(email);

    if (!user) {
      throw new UnauthorizedError('Invalid credentials');
    }

    const isValid = await comparePasswords(password, user.hashedPassword);

    if (!isValid) {
      throw new UnauthorizedError('Invalid credentials');
    }

    return user;
  }
}
```

### Controller Layer

```typescript
// controllers/users.controller.ts
import { Request, Response, NextFunction } from 'express';
import { IUserService } from '../services/users.service';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/users';

export class UserController {
  constructor(private userService: IUserService) {}

  getUsers = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 20;
      const search = req.query.search as string | undefined;

      const result = await this.userService.getUsers(page, limit, search);

      res.json(result);
    } catch (error) {
      next(error);
    }
  };

  getUser = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { id } = req.params;
      const user = await this.userService.getUser(id);

      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  createUser = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const data = CreateUserSchema.parse(req.body);
      const user = await this.userService.createUser(data);

      res.status(201).json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  updateUser = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { id } = req.params;
      const data = UpdateUserSchema.parse(req.body);
      const user = await this.userService.updateUser(id, data);

      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  deleteUser = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { id } = req.params;
      await this.userService.deleteUser(id);

      res.status(204).send();
    } catch (error) {
      next(error);
    }
  };
}
```

### Dependency Injection

```typescript
// container.ts
import { PrismaClient } from '@prisma/client';
import { UserRepository } from './repositories/users.repository';
import { UserService } from './services/users.service';
import { UserController } from './controllers/users.controller';

// Database client
const prisma = new PrismaClient();

// Repositories
const userRepository = new UserRepository(prisma);

// Services
const userService = new UserService(userRepository);

// Controllers
const userController = new UserController(userService);

export { prisma, userRepository, userService, userController };

// routes/users.routes.ts
import { Router } from 'express';
import { userController } from '../container';
import { authenticate } from '../middleware/auth';

const router = Router();

router.get('/', authenticate, userController.getUsers);
router.get('/:id', authenticate, userController.getUser);
router.post('/', userController.createUser);
router.patch('/:id', authenticate, userController.updateUser);
router.delete('/:id', authenticate, userController.deleteUser);

export default router;
```

### Error Handling

```typescript
// utils/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR',
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class ConflictError extends AppError {
  constructor(message = 'Resource conflict') {
    super(message, 409, 'CONFLICT');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ValidationError extends AppError {
  constructor(
    message = 'Validation failed',
    public errors: Record<string, string[]> = {}
  ) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

// middleware/errorHandler.ts
import { ErrorRequestHandler } from 'express';
import { ZodError } from 'zod';
import { AppError } from '../utils/errors';
import { logger } from '../utils/logger';

export const errorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  logger.error({ err, path: req.path, method: req.method });

  if (err instanceof ZodError) {
    return res.status(400).json({
      error: 'Validation failed',
      code: 'VALIDATION_ERROR',
      details: err.flatten().fieldErrors,
    });
  }

  if (err instanceof AppError && err.isOperational) {
    return res.status(err.statusCode).json({
      error: err.message,
      code: err.code,
    });
  }

  // Unknown error
  return res.status(500).json({
    error: 'Internal server error',
    code: 'INTERNAL_ERROR',
  });
};
```

## Anti-patterns

### Avoid: Business Logic in Controllers

```typescript
// BAD
app.post('/users', async (req, res) => {
  const existing = await prisma.user.findUnique({ where: { email: req.body.email }});
  if (existing) return res.status(409).json({ error: 'Exists' });
  const hashedPassword = await bcrypt.hash(req.body.password, 10);
  const user = await prisma.user.create({ data: { ...req.body, hashedPassword }});
  res.json(user);
});

// GOOD - delegate to service
app.post('/users', async (req, res, next) => {
  try {
    const user = await userService.createUser(req.body);
    res.json(user);
  } catch (error) {
    next(error);
  }
});
```

### Avoid: Direct Database Access in Services

```typescript
// BAD - service uses Prisma directly
class UserService {
  async getUser(id: string) {
    return prisma.user.findUnique({ where: { id }});
  }
}

// GOOD - service uses repository
class UserService {
  constructor(private userRepository: IUserRepository) {}

  async getUser(id: string) {
    return this.userRepository.findById(id);
  }
}
```

## References

- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Express.js Documentation](https://expressjs.com/)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
