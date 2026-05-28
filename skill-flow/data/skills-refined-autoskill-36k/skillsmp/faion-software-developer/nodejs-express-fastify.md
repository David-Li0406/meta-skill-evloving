---
id: nodejs-express-fastify
name: "Express/Fastify Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Express/Fastify Patterns

## Overview

Express and Fastify are the two leading Node.js web frameworks. This methodology covers setup, routing, middleware, and best practices for building production-grade APIs with both frameworks.

## When to Use

- **Express**: Maximum ecosystem compatibility, mature middleware
- **Fastify**: High performance, built-in validation, TypeScript-first
- Both: REST APIs, microservices, web applications

## Key Principles

1. **Middleware composition** - Build features through composable middleware
2. **Centralized error handling** - Single error handler for consistency
3. **Input validation** - Validate all incoming data
4. **Structured logging** - JSON logs for production
5. **Graceful shutdown** - Handle process termination properly

## Best Practices

### Express Application Setup

```typescript
// app.ts
import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { rateLimit } from 'express-rate-limit';
import { pinoHttp } from 'pino-http';
import { router } from './routes';
import { errorHandler } from './middleware/errorHandler';
import { notFoundHandler } from './middleware/notFound';
import { config } from './config';

export function createApp(): Express {
  const app = express();

  // Trust proxy for rate limiting behind reverse proxy
  app.set('trust proxy', 1);

  // Security headers
  app.use(helmet());

  // CORS
  app.use(cors({
    origin: config.corsOrigins,
    credentials: true,
  }));

  // Compression
  app.use(compression());

  // Body parsing
  app.use(express.json({ limit: '10kb' }));
  app.use(express.urlencoded({ extended: true, limit: '10kb' }));

  // Logging
  app.use(pinoHttp({
    logger: config.logger,
    autoLogging: true,
  }));

  // Rate limiting
  app.use(rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100,
    standardHeaders: true,
    legacyHeaders: false,
  }));

  // Health check (before auth)
  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  // API routes
  app.use('/api/v1', router);

  // 404 handler
  app.use(notFoundHandler);

  // Error handler (must be last)
  app.use(errorHandler);

  return app;
}

// server.ts
import http from 'node:http';
import { createApp } from './app';
import { config } from './config';
import { logger } from './utils/logger';

const app = createApp();
const server = http.createServer(app);

// Graceful shutdown
function shutdown(signal: string) {
  logger.info(`${signal} received, shutting down gracefully`);

  server.close(() => {
    logger.info('HTTP server closed');
    process.exit(0);
  });

  // Force close after 30s
  setTimeout(() => {
    logger.error('Could not close connections in time, forcefully shutting down');
    process.exit(1);
  }, 30000);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

server.listen(config.port, () => {
  logger.info(`Server running on port ${config.port}`);
});
```

### Express Router Organization

```typescript
// routes/index.ts
import { Router } from 'express';
import usersRouter from './users.routes';
import ordersRouter from './orders.routes';
import authRouter from './auth.routes';
import { authenticate } from '../middleware/auth';

const router = Router();

// Public routes
router.use('/auth', authRouter);

// Protected routes
router.use('/users', authenticate, usersRouter);
router.use('/orders', authenticate, ordersRouter);

export { router };

// routes/users.routes.ts
import { Router } from 'express';
import { userController } from '../container';
import { validate } from '../middleware/validate';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/users';

const router = Router();

router.get('/', userController.getUsers);
router.get('/:id', userController.getUser);
router.post('/', validate(CreateUserSchema), userController.createUser);
router.patch('/:id', validate(UpdateUserSchema), userController.updateUser);
router.delete('/:id', userController.deleteUser);

export default router;
```

### Fastify Application Setup

```typescript
// app.ts
import Fastify, { FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox';
import { userRoutes } from './routes/users.routes';
import { authRoutes } from './routes/auth.routes';
import { errorHandler } from './plugins/errorHandler';
import { config } from './config';

export async function createApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: config.logLevel,
      transport: config.isDevelopment
        ? { target: 'pino-pretty' }
        : undefined,
    },
  }).withTypeProvider<TypeBoxTypeProvider>();

  // Plugins
  await app.register(helmet);
  await app.register(cors, {
    origin: config.corsOrigins,
    credentials: true,
  });
  await app.register(rateLimit, {
    max: 100,
    timeWindow: '15 minutes',
  });

  // Custom error handler
  app.setErrorHandler(errorHandler);

  // Health check
  app.get('/health', async () => ({
    status: 'ok',
    timestamp: new Date().toISOString(),
  }));

  // Routes
  await app.register(authRoutes, { prefix: '/api/v1/auth' });
  await app.register(userRoutes, { prefix: '/api/v1/users' });

  return app;
}

// server.ts
import { createApp } from './app';
import { config } from './config';

async function start() {
  const app = await createApp();

  try {
    await app.listen({ port: config.port, host: '0.0.0.0' });
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
}

start();
```

### Fastify Routes with TypeBox

```typescript
// routes/users.routes.ts
import { FastifyPluginAsync } from 'fastify';
import { Type, Static } from '@sinclair/typebox';

const UserSchema = Type.Object({
  id: Type.String(),
  email: Type.String({ format: 'email' }),
  name: Type.String(),
  createdAt: Type.String({ format: 'date-time' }),
});

const CreateUserSchema = Type.Object({
  email: Type.String({ format: 'email' }),
  name: Type.String({ minLength: 1, maxLength: 100 }),
  password: Type.String({ minLength: 8 }),
});

const UpdateUserSchema = Type.Partial(
  Type.Object({
    email: Type.String({ format: 'email' }),
    name: Type.String({ minLength: 1, maxLength: 100 }),
  })
);

const ParamsSchema = Type.Object({
  id: Type.String(),
});

const QuerySchema = Type.Object({
  page: Type.Optional(Type.Number({ minimum: 1, default: 1 })),
  limit: Type.Optional(Type.Number({ minimum: 1, maximum: 100, default: 20 })),
  search: Type.Optional(Type.String()),
});

type User = Static<typeof UserSchema>;
type CreateUser = Static<typeof CreateUserSchema>;
type UpdateUser = Static<typeof UpdateUserSchema>;

export const userRoutes: FastifyPluginAsync = async (app) => {
  // GET /users
  app.get<{
    Querystring: Static<typeof QuerySchema>;
    Reply: { users: User[]; total: number; page: number; limit: number };
  }>(
    '/',
    {
      schema: {
        querystring: QuerySchema,
        response: {
          200: Type.Object({
            users: Type.Array(UserSchema),
            total: Type.Number(),
            page: Type.Number(),
            limit: Type.Number(),
          }),
        },
      },
      preHandler: [app.authenticate],
    },
    async (request, reply) => {
      const { page = 1, limit = 20, search } = request.query;
      const result = await app.userService.getUsers(page, limit, search);
      return result;
    }
  );

  // GET /users/:id
  app.get<{
    Params: Static<typeof ParamsSchema>;
    Reply: { data: User };
  }>(
    '/:id',
    {
      schema: {
        params: ParamsSchema,
        response: {
          200: Type.Object({ data: UserSchema }),
        },
      },
      preHandler: [app.authenticate],
    },
    async (request) => {
      const user = await app.userService.getUser(request.params.id);
      return { data: user };
    }
  );

  // POST /users
  app.post<{
    Body: CreateUser;
    Reply: { data: User };
  }>(
    '/',
    {
      schema: {
        body: CreateUserSchema,
        response: {
          201: Type.Object({ data: UserSchema }),
        },
      },
    },
    async (request, reply) => {
      const user = await app.userService.createUser(request.body);
      reply.status(201);
      return { data: user };
    }
  );

  // PATCH /users/:id
  app.patch<{
    Params: Static<typeof ParamsSchema>;
    Body: UpdateUser;
    Reply: { data: User };
  }>(
    '/:id',
    {
      schema: {
        params: ParamsSchema,
        body: UpdateUserSchema,
        response: {
          200: Type.Object({ data: UserSchema }),
        },
      },
      preHandler: [app.authenticate],
    },
    async (request) => {
      const user = await app.userService.updateUser(
        request.params.id,
        request.body
      );
      return { data: user };
    }
  );

  // DELETE /users/:id
  app.delete<{
    Params: Static<typeof ParamsSchema>;
  }>(
    '/:id',
    {
      schema: {
        params: ParamsSchema,
        response: {
          204: Type.Null(),
        },
      },
      preHandler: [app.authenticate],
    },
    async (request, reply) => {
      await app.userService.deleteUser(request.params.id);
      reply.status(204).send();
    }
  );
};
```

### Express Validation Middleware

```typescript
// middleware/validate.ts
import { Request, Response, NextFunction } from 'express';
import { z, ZodSchema } from 'zod';
import { ValidationError } from '../utils/errors';

export function validate(schema: ZodSchema) {
  return (req: Request, _res: Response, next: NextFunction) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        throw new ValidationError('Validation failed', error.flatten().fieldErrors);
      }
      throw error;
    }
  };
}

// With params and query validation
interface ValidationSchemas {
  body?: ZodSchema;
  params?: ZodSchema;
  query?: ZodSchema;
}

export function validateAll(schemas: ValidationSchemas) {
  return (req: Request, _res: Response, next: NextFunction) => {
    try {
      if (schemas.body) {
        req.body = schemas.body.parse(req.body);
      }
      if (schemas.params) {
        req.params = schemas.params.parse(req.params);
      }
      if (schemas.query) {
        req.query = schemas.query.parse(req.query);
      }
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        throw new ValidationError('Validation failed', error.flatten().fieldErrors);
      }
      throw error;
    }
  };
}
```

### Authentication Middleware

```typescript
// middleware/auth.ts (Express)
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { UnauthorizedError } from '../utils/errors';
import { config } from '../config';

interface JwtPayload {
  userId: string;
  email: string;
}

declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload;
    }
  }
}

export function authenticate(
  req: Request,
  _res: Response,
  next: NextFunction
): void {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      throw new UnauthorizedError('Missing authorization header');
    }

    const token = authHeader.slice(7);
    const payload = jwt.verify(token, config.jwtSecret) as JwtPayload;

    req.user = payload;
    next();
  } catch (error) {
    if (error instanceof jwt.JsonWebTokenError) {
      throw new UnauthorizedError('Invalid token');
    }
    throw error;
  }
}

// Fastify decorator
// plugins/auth.ts
import { FastifyPluginAsync, FastifyRequest } from 'fastify';
import fp from 'fastify-plugin';
import jwt from 'jsonwebtoken';

declare module 'fastify' {
  interface FastifyInstance {
    authenticate: (request: FastifyRequest) => Promise<void>;
  }
  interface FastifyRequest {
    user: { userId: string; email: string };
  }
}

const authPlugin: FastifyPluginAsync = async (app) => {
  app.decorate('authenticate', async (request: FastifyRequest) => {
    const authHeader = request.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      throw app.httpErrors.unauthorized('Missing authorization');
    }

    try {
      const token = authHeader.slice(7);
      const payload = jwt.verify(token, app.config.jwtSecret);
      request.user = payload as { userId: string; email: string };
    } catch {
      throw app.httpErrors.unauthorized('Invalid token');
    }
  });
};

export default fp(authPlugin, { name: 'auth' });
```

## Anti-patterns

### Avoid: Callback Hell

```typescript
// BAD
app.get('/users/:id', (req, res) => {
  User.findById(req.params.id, (err, user) => {
    if (err) return res.status(500).json({ error: err });
    Order.find({ userId: user.id }, (err, orders) => {
      if (err) return res.status(500).json({ error: err });
      res.json({ user, orders });
    });
  });
});

// GOOD - async/await
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id);
    const orders = await Order.find({ userId: user.id });
    res.json({ user, orders });
  } catch (error) {
    next(error);
  }
});
```

### Avoid: No Error Handling

```typescript
// BAD
app.post('/users', async (req, res) => {
  const user = await userService.createUser(req.body);
  res.json(user);
});

// GOOD
app.post('/users', async (req, res, next) => {
  try {
    const user = await userService.createUser(req.body);
    res.json(user);
  } catch (error) {
    next(error);
  }
});
```

## References

- [Express.js Guide](https://expressjs.com/en/guide/)
- [Fastify Documentation](https://fastify.dev/docs/latest/)
- [TypeBox](https://github.com/sinclairzx81/typebox)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
