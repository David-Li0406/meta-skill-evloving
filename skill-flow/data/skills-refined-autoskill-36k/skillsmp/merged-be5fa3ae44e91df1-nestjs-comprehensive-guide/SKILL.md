---
name: nestjs-comprehensive-guide
description: Use this skill when building comprehensive NestJS applications, integrating databases, implementing authentication, and following best practices for architecture and testing.
---

# Comprehensive NestJS Guide

This skill provides a detailed framework for building production-grade NestJS applications, covering architecture patterns, database integration, authentication, testing, and best practices.

## When to Use
- Building REST APIs or GraphQL servers with NestJS
- Setting up authentication and authorization
- Implementing middleware, guards, or interceptors
- Working with databases (Drizzle ORM, TypeORM)
- Creating microservices architecture
- Writing unit and integration tests
- Setting up OpenAPI/Swagger documentation

## Core Architecture

### Module Structure
```typescript
import { Module } from '@nestjs/common';

@Module({
  imports: [/* other modules */],
  controllers: [/* controllers */],
  providers: [/* providers */],
  exports: [/* exported providers */],
})
export class FeatureModule {}
```

### Controller Pattern
```typescript
import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';

@Controller('users')
export class UsersController {
  @Get()
  findAll(@Query() query: any) {
    return 'This returns all users';
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return `This returns user #${id}`;
  }

  @Post()
  create(@Body() createUserDto: any) {
    return 'This creates a user';
  }
}
```

### Service with Dependency Injection
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class UsersService {
  constructor(/* inject dependencies */) {}

  findAll() {
    return 'Users service logic';
  }
}
```

## ORM Selection (CRITICAL)

**ALWAYS detect and use the project's existing ORM. Never switch ORMs mid-project.**

| Detection Method | ORM |
|------------------|-----|
| `drizzle.config.ts` or `drizzle-orm` in package.json | **Drizzle** |
| `prisma/schema.prisma` or `@prisma/client` in package.json | **Prisma** |
| `typeorm` in package.json or `ormconfig.json` | **TypeORM** |

```bash
# Quick detection commands
grep -l "drizzle" package.json   # Drizzle
ls prisma/schema.prisma 2>/dev/null  # Prisma
grep -l "typeorm" package.json   # TypeORM
```

**If no ORM exists yet**, ask the user which they prefer before proceeding.

## Database Integration

### Setup with Drizzle ORM

#### Installation
```bash
# Using npm
npm install drizzle-orm pg
npm install -D drizzle-kit tsx @types/pg

# Using yarn
yarn add drizzle-orm pg
yarn add -D drizzle-kit tsx @types/pg
```

#### Configuration
```typescript
// drizzle.config.ts
import 'dotenv/config';
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  out: './drizzle',
  schema: './src/db/schema.ts',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### Database Schema
```typescript
// src/db/schema.ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

### User Repository with Drizzle
```typescript
// src/users/user.repository.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../db/database.service';
import { users } from '../db/schema';
import { eq } from 'drizzle-orm';

@Injectable()
export class UserRepository {
  constructor(private db: DatabaseService) {}

  async findAll() {
    return this.db.database.select().from(users);
  }

  async findOne(id: number) {
    const result = await this.db.database
      .select()
      .from(users)
      .where(eq(users.id, id))
      .limit(1);
    return result[0];
  }

  async create(data: typeof users.$inferInsert) {
    const result = await this.db.database
      .insert(users)
      .values(data)
      .returning();
    return result[0];
  }

  async update(id: number, data: Partial<typeof users.$inferInsert>) {
    const result = await this.db.database
      .update(users)
      .set(data)
      .where(eq(users.id, id))
      .returning();
    return result[0];
  }

  async remove(id: number) {
    const result = await this.db.database
      .delete(users)
      .where(eq(users.id, id))
      .returning();
    return result[0];
  }
}
```

## Authentication & Authorization

### JWT Strategy
```typescript
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private readonly configService: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.getOrThrow('JWT_SECRET'),
    });
  }

  async validate(payload: JwtPayload): Promise<AuthUser> {
    return {
      id: payload.sub,
      email: payload.email,
      roles: payload.roles,
    };
  }
}
```

### Role-Based Access Control
```typescript
// roles.decorator.ts
export const ROLES_KEY = 'roles';
export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);

// roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}

// Usage
@Get('admin')
@Roles(Role.ADMIN)
@UseGuards(JwtAuthGuard, RolesGuard)
async adminOnly() {}
```

## Validation & Exception Handling

### DTO Validation
```typescript
// Always use class-validator with whitelist
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,           // Strip non-whitelisted properties
  forbidNonWhitelisted: true, // Throw on non-whitelisted
  transform: true,           // Auto-transform to DTO types
  transformOptions: {
    enableImplicitConversion: true,
  },
}));
```

### Global Exception Filter
```typescript
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  constructor(private readonly logger: Logger) {}

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const { status, message } = this.getErrorDetails(exception);

    this.logger.error(`${request.method} ${request.url}`, {
      status,
      message,
      stack: exception instanceof Error ? exception.stack : undefined,
    });

    response.status(status).json({
      statusCode: status,
      message,
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }

  private getErrorDetails(exception: unknown) {
    if (exception instanceof HttpException) {
      return {
        status: exception.getStatus(),
        message: exception.message,
      };
    }
    return {
      status: HttpStatus.INTERNAL_SERVER_ERROR,
      message: 'Internal server error',
    };
  }
}
```

## Testing Patterns

### Unit Testing Services
```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';
import { UserRepository } from './user.repository';

describe('UsersService', () => {
  let service: UsersService;
  let repository: jest.Mocked<UserRepository>;

  beforeEach(async () => {
    const mockRepository = {
      findAll: jest.fn(),
      findOne: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      remove: jest.fn(),
    } as any;

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: UserRepository,
          useValue: mockRepository,
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get(UserRepository);
  });

  it('should return all users', async () => {
    const expectedUsers = [{ id: 1, name: 'John', email: 'john@example.com' }];
    repository.findAll.mockResolvedValue(expectedUsers);

    const result = await service.findAll();
    expect(result).toEqual(expectedUsers);
    expect(repository.findAll).toHaveBeenCalled();
  });
});
```

### E2E Testing with Drizzle
```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from './../src/app.module';
import { DatabaseService } from '../src/db/database.service';

describe('UsersController (e2e)', () => {
  let app: INestApplication;
  let db: DatabaseService;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    db = moduleFixture.get<DatabaseService>(DatabaseService);

    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('/users (POST)', () => {
    const createUserDto = {
      name: 'Test User',
      email: 'test@example.com',
    };

    return request(app.getHttpServer())
      .post('/users')
      .send(createUserDto)
      .expect(201)
      .expect((res) => {
        expect(res.body).toMatchObject(createUserDto);
        expect(res.body).toHaveProperty('id');
      });
  });

  it('/users (GET)', async () => {
    return request(app.getHttpServer())
      .get('/users')
      .expect(200)
      .expect((res) => {
        expect(Array.isArray(res.body)).toBe(true);
      });
  });
});
```

## Best Practices

1. **Always use constructor injection** - Never use property injection
2. **Use DTOs for data transfer** - Define interfaces for request/response
3. **Implement proper error handling** - Use exception filters
4. **Validate all inputs** - Use validation pipes
5. **Keep modules focused** - Single responsibility principle
6. **Use environment variables** - Never hardcode credentials
7. **Write comprehensive tests** - Unit and integration tests
8. **Use transactions for complex operations** - Maintain data consistency
9. **Implement proper logging** - Use interceptors for cross-cutting concerns
10. **Use type safety** - Leverage TypeScript features

## References

For detailed patterns and examples, see:

- **[references/architecture.md](references/architecture.md)** - Module patterns, DI, circular dependency resolution
- **[references/database.md](references/database.md)** - Drizzle, TypeORM, Prisma patterns, migrations, transactions
- **[references/security.md](references/security.md)** - Guards, JWT, validation, rate limiting
- **[references/testing.md](references/testing.md)** - Jest, TestingModule, e2e with supertest