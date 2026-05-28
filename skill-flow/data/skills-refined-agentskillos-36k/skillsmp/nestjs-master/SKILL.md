---
name: nestjs-master
description: Comprehensive NestJS framework mastery with Drizzle ORM, TypeORM, Prisma, BullMQ queues, and 40 best practice rules. Use for NestJS applications, APIs, authentication, database integration, queue processing, microservices, testing, and architectural decisions.
---

# NestJS Master Skill

Authoritative guide for building production-grade NestJS applications. Consolidates architecture patterns, database integration, authentication, queues, and testing best practices.

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

See **[references/database.md](references/database.md)** for patterns specific to each ORM.

## Core Architecture

### Module Organization

```typescript
// Feature module pattern - one module per domain
@Module({
  imports: [
    DrizzleModule,
    ConfigModule.forFeature(userConfig),
  ],
  controllers: [UserController],
  providers: [UserService, UserRepository],
  exports: [UserService], // Only export what other modules need
})
export class UserModule {}
```

### Dependency Injection Patterns

```typescript
// Constructor injection (preferred)
@Injectable()
export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly configService: ConfigService,
  ) {}
}

// Custom providers for flexibility
const providers = [
  {
    provide: 'DATABASE_CONNECTION',
    useFactory: async (config: ConfigService) => {
      return drizzle(config.get('DATABASE_URL'));
    },
    inject: [ConfigService],
  },
];
```

### Controller Best Practices

```typescript
@Controller('users')
@UseGuards(JwtAuthGuard)
@ApiTags('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  async findOne(
    @Param('id', ParseUUIDPipe) id: string,
  ): Promise<UserResponseDto> {
    const user = await this.userService.findById(id);
    if (!user) throw new NotFoundException(`User ${id} not found`);
    return plainToInstance(UserResponseDto, user);
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  async create(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
    return this.userService.create(dto);
  }
}
```

## Database Integration

All three ORMs are fully supported. **Use whichever the project already has.**

### Quick Comparison

| Feature | Drizzle | Prisma | TypeORM |
|---------|---------|--------|---------|
| Type Safety | Excellent (schema-first) | Excellent (generated) | Good (decorators) |
| Query Builder | SQL-like, composable | Fluent API | QueryBuilder |
| Migrations | `drizzle-kit` | `prisma migrate` | Built-in CLI |
| Performance | Lightweight, fast | Good (query engine) | Good |
| Learning Curve | Low (SQL knowledge helps) | Low | Medium |

### Repository Pattern (ORM-Agnostic Interface)

```typescript
// Define interface - implementation varies by ORM
export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserDto): Promise<User>;
  update(id: string, data: UpdateUserDto): Promise<User | null>;
  delete(id: string): Promise<boolean>;
}

// Inject by token for flexibility
@Injectable()
export class UserService {
  constructor(
    @Inject('USER_REPOSITORY') 
    private readonly userRepository: IUserRepository,
  ) {}
}
```

### ORM-Specific Implementations

See **[references/database.md](references/database.md)** for complete patterns:
- **Drizzle**: Schema definition, module setup, queries, transactions
- **Prisma**: Schema, PrismaService, queries, transactions  
- **TypeORM**: Entities, repositories, QueryBuilder, transactions

### Transaction Pattern (All ORMs)

```typescript
// Drizzle
await this.db.transaction(async (tx) => { /* use tx */ });

// Prisma  
await this.prisma.$transaction(async (tx) => { /* use tx */ });

// TypeORM
await this.dataSource.transaction(async (manager) => { /* use manager */ });
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

// Example DTO
export class CreateUserDto {
  @IsEmail()
  @Transform(({ value }) => value?.toLowerCase())
  email: string;

  @IsString()
  @MinLength(8)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, {
    message: 'Password must contain uppercase, lowercase, and number',
  })
  password: string;

  @IsOptional()
  @IsString()
  @MaxLength(100)
  name?: string;
}
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

## Quick Reference: 40 Best Practice Rules

| ID | Rule | Category |
|----|------|----------|
| **arch-01** | One module per domain/feature | Architecture |
| **arch-02** | Keep controllers thin, logic in services | Architecture |
| **arch-03** | Use repository pattern for data access | Architecture |
| **arch-04** | Avoid circular dependencies with forwardRef | Architecture |
| **arch-05** | Export only what other modules need | Architecture |
| **di-01** | Prefer constructor injection | Dependency Injection |
| **di-02** | Use custom providers for complex setup | Dependency Injection |
| **di-03** | Scope providers appropriately (default, request, transient) | Dependency Injection |
| **di-04** | Use injection tokens for non-class dependencies | Dependency Injection |
| **error-01** | Use built-in HTTP exceptions | Error Handling |
| **error-02** | Implement global exception filter | Error Handling |
| **error-03** | Log errors with context (request ID, user) | Error Handling |
| **error-04** | Never expose internal errors to clients | Error Handling |
| **security-01** | Always validate input (see `validation` skill) | Security |
| **security-02** | Use whitelist: true in ValidationPipe | Security |
| **security-03** | Implement rate limiting on public endpoints | Security |
| **security-04** | Hash passwords with bcrypt (cost 12+) | Security |
| **security-05** | Use helmet for HTTP headers | Security |
| **security-06** | Validate JWT with proper expiration | Security |
| **perf-01** | Use pagination for list endpoints | Performance |
| **perf-02** | Implement caching with CacheModule | Performance |
| **perf-03** | Use database indexes for frequent queries | Performance |
| **perf-04** | Lazy load modules when possible | Performance |
| **perf-05** | Use connection pooling | Performance |
| **test-01** | Unit test services with mocked dependencies | Testing |
| **test-02** | Use TestingModule.compile() for integration | Testing |
| **test-03** | E2E test with supertest and test database | Testing |
| **test-04** | Mock external services in tests | Testing |
| **test-05** | Test guards and interceptors in isolation | Testing |
| **db-01** | Use project's existing ORM consistently | Database |
| **db-02** | Define schema with proper constraints | Database |
| **db-03** | Use transactions for multi-step operations | Database |
| **db-04** | Implement soft deletes where appropriate | Database |
| **db-05** | Use migrations for schema changes | Database |
| **api-01** | Version APIs (/v1/, /v2/) | API Design |
| **api-02** | Use proper HTTP methods and status codes | API Design |
| **api-03** | Document with OpenAPI/Swagger | API Design |
| **api-04** | Implement consistent response format | API Design |
| **micro-01** | Use message patterns for microservices | Microservices |
| **devops-01** | Use ConfigService for environment variables | DevOps |

## References

For detailed patterns and examples, see:

- **[references/architecture.md](references/architecture.md)** - Module patterns, DI, circular dependency resolution
- **[references/database.md](references/database.md)** - Drizzle, TypeORM, Prisma patterns, migrations, transactions
- **[references/queues.md](references/queues.md)** - BullMQ patterns, job processing, retry strategies
- **[references/security.md](references/security.md)** - Guards, JWT, validation, rate limiting
- **[references/testing.md](references/testing.md)** - Jest, TestingModule, e2e with supertest

## When to Use This Skill

Load this skill when:
- Building new NestJS applications or features
- Integrating databases (Drizzle, Prisma, or TypeORM - match existing)
- Implementing authentication/authorization
- Setting up queue processing with BullMQ
- Writing tests for NestJS components
- Making architectural decisions
- Debugging dependency injection issues
