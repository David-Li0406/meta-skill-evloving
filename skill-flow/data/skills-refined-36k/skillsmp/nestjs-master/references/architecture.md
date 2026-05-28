# NestJS Architecture Reference

## Module Patterns

### Feature Module Structure

```
src/
├── users/
│   ├── users.module.ts
│   ├── users.controller.ts
│   ├── users.service.ts
│   ├── users.repository.ts
│   ├── dto/
│   │   ├── create-user.dto.ts
│   │   ├── update-user.dto.ts
│   │   └── user-response.dto.ts
│   ├── entities/
│   │   └── user.entity.ts
│   └── guards/
│       └── user-owner.guard.ts
├── auth/
│   ├── auth.module.ts
│   ├── auth.controller.ts
│   ├── auth.service.ts
│   └── strategies/
│       ├── jwt.strategy.ts
│       └── local.strategy.ts
└── common/
    ├── common.module.ts
    ├── decorators/
    ├── filters/
    ├── guards/
    ├── interceptors/
    └── pipes/
```

### Dynamic Modules

```typescript
// For configurable modules
@Module({})
export class DatabaseModule {
  static forRoot(options: DatabaseOptions): DynamicModule {
    return {
      module: DatabaseModule,
      global: true,
      providers: [
        {
          provide: DATABASE_OPTIONS,
          useValue: options,
        },
        {
          provide: DRIZZLE,
          useFactory: async (opts: DatabaseOptions) => {
            const pool = new Pool({ connectionString: opts.url });
            return drizzle(pool, { schema: opts.schema });
          },
          inject: [DATABASE_OPTIONS],
        },
      ],
      exports: [DRIZZLE],
    };
  }

  static forRootAsync(options: DatabaseAsyncOptions): DynamicModule {
    return {
      module: DatabaseModule,
      global: true,
      imports: options.imports || [],
      providers: [
        {
          provide: DATABASE_OPTIONS,
          useFactory: options.useFactory,
          inject: options.inject || [],
        },
        {
          provide: DRIZZLE,
          useFactory: async (opts: DatabaseOptions) => {
            const pool = new Pool({ connectionString: opts.url });
            return drizzle(pool, { schema: opts.schema });
          },
          inject: [DATABASE_OPTIONS],
        },
      ],
      exports: [DRIZZLE],
    };
  }
}

// Usage
@Module({
  imports: [
    DatabaseModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (config: ConfigService) => ({
        url: config.getOrThrow('DATABASE_URL'),
        schema: allSchema,
      }),
      inject: [ConfigService],
    }),
  ],
})
export class AppModule {}
```

## Dependency Injection

### Provider Types

```typescript
// Value provider
{
  provide: 'API_KEY',
  useValue: process.env.API_KEY,
}

// Class provider
{
  provide: LoggerService,
  useClass: process.env.NODE_ENV === 'test' ? MockLogger : ConsoleLogger,
}

// Factory provider
{
  provide: 'ASYNC_CONNECTION',
  useFactory: async (config: ConfigService) => {
    const connection = await createConnection(config.get('DB_URL'));
    return connection;
  },
  inject: [ConfigService],
}

// Existing provider (alias)
{
  provide: 'AliasedService',
  useExisting: ConcreteService,
}
```

### Injection Scopes

```typescript
// Default scope (singleton)
@Injectable()
export class SingletonService {}

// Request scope (new instance per request)
@Injectable({ scope: Scope.REQUEST })
export class RequestScopedService {
  constructor(@Inject(REQUEST) private request: Request) {}
}

// Transient scope (new instance per injection)
@Injectable({ scope: Scope.TRANSIENT })
export class TransientService {}
```

### Custom Decorators for Injection

```typescript
// Inject current user from request
export const CurrentUser = createParamDecorator(
  (data: keyof AuthUser | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user as AuthUser;
    return data ? user?.[data] : user;
  },
);

// Usage
@Get('profile')
async getProfile(@CurrentUser() user: AuthUser) {
  return this.userService.findById(user.id);
}

@Get('my-id')
async getMyId(@CurrentUser('id') userId: string) {
  return { userId };
}
```

## Circular Dependency Resolution

### Problem

```typescript
// UserService needs AuthService
@Injectable()
export class UserService {
  constructor(private authService: AuthService) {} // Circular!
}

// AuthService needs UserService
@Injectable()
export class AuthService {
  constructor(private userService: UserService) {} // Circular!
}
```

### Solution 1: forwardRef

```typescript
// user.service.ts
@Injectable()
export class UserService {
  constructor(
    @Inject(forwardRef(() => AuthService))
    private authService: AuthService,
  ) {}
}

// auth.service.ts
@Injectable()
export class AuthService {
  constructor(
    @Inject(forwardRef(() => UserService))
    private userService: UserService,
  ) {}
}

// In modules too
@Module({
  imports: [forwardRef(() => AuthModule)],
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}
```

### Solution 2: Refactor to Shared Service (Preferred)

```typescript
// Extract shared logic to avoid circular dependency
@Injectable()
export class UserAuthSharedService {
  // Contains logic needed by both
}

@Module({
  providers: [UserAuthSharedService],
  exports: [UserAuthSharedService],
})
export class SharedModule {}

// Both UserModule and AuthModule import SharedModule
```

### Solution 3: Event-Based Communication

```typescript
// Use EventEmitter2 for decoupled communication
@Injectable()
export class UserService {
  constructor(private eventEmitter: EventEmitter2) {}

  async createUser(dto: CreateUserDto) {
    const user = await this.userRepository.create(dto);
    this.eventEmitter.emit('user.created', new UserCreatedEvent(user));
    return user;
  }
}

@Injectable()
export class AuthService {
  @OnEvent('user.created')
  async handleUserCreated(event: UserCreatedEvent) {
    await this.createDefaultPermissions(event.user.id);
  }
}
```

## Interceptors

### Response Transformation

```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, ApiResponse<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<ApiResponse<T>> {
    return next.handle().pipe(
      map((data) => ({
        success: true,
        data,
        timestamp: new Date().toISOString(),
      })),
    );
  }
}
```

### Timing/Logging Interceptor

```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger('HTTP');

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url } = request;
    const start = Date.now();

    return next.handle().pipe(
      tap(() => {
        const duration = Date.now() - start;
        this.logger.log(`${method} ${url} - ${duration}ms`);
      }),
    );
  }
}
```

### Caching Interceptor

```typescript
@Injectable()
export class CacheInterceptor implements NestInterceptor {
  constructor(
    @Inject(CACHE_MANAGER) private cacheManager: Cache,
    private reflector: Reflector,
  ) {}

  async intercept(context: ExecutionContext, next: CallHandler): Promise<Observable<any>> {
    const ttl = this.reflector.get<number>('cache_ttl', context.getHandler()) ?? 60;
    const key = this.generateCacheKey(context);

    const cached = await this.cacheManager.get(key);
    if (cached) {
      return of(cached);
    }

    return next.handle().pipe(
      tap((data) => this.cacheManager.set(key, data, ttl * 1000)),
    );
  }

  private generateCacheKey(context: ExecutionContext): string {
    const request = context.switchToHttp().getRequest();
    return `${request.method}:${request.url}`;
  }
}
```

## Middleware

```typescript
// Function middleware
export function loggerMiddleware(req: Request, res: Response, next: NextFunction) {
  console.log(`[${req.method}] ${req.url}`);
  next();
}

// Class middleware
@Injectable()
export class AuthMiddleware implements NestMiddleware {
  constructor(private readonly authService: AuthService) {}

  async use(req: Request, res: Response, next: NextFunction) {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (token) {
      try {
        req['user'] = await this.authService.validateToken(token);
      } catch {
        // Token invalid, continue without user
      }
    }
    next();
  }
}

// Apply in module
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(AuthMiddleware)
      .exclude({ path: 'health', method: RequestMethod.GET })
      .forRoutes('*');
  }
}
```

## Lifecycle Hooks

```typescript
@Injectable()
export class DatabaseService implements OnModuleInit, OnModuleDestroy {
  private pool: Pool;

  async onModuleInit() {
    // Called after module initialization
    this.pool = new Pool({ connectionString: process.env.DATABASE_URL });
    await this.pool.connect();
    console.log('Database connected');
  }

  async onModuleDestroy() {
    // Called during graceful shutdown
    await this.pool.end();
    console.log('Database disconnected');
  }
}

// Enable graceful shutdown in main.ts
app.enableShutdownHooks();
```
