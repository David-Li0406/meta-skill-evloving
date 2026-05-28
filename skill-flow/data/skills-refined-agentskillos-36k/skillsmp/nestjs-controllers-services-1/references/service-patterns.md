# NestJS Service Patterns

## Basic Service

```typescript
import { Injectable, NotFoundException } from '@nestjs/common';

@Injectable()
export class UsersService {
  constructor(
    private readonly usersRepository: UsersRepository,
    private readonly emailService: EmailService,
  ) {}

  async findAll(query: ListUsersDto): Promise<User[]> {
    return this.usersRepository.find(query);
  }

  async findOne(id: number): Promise<User> {
    const user = await this.usersRepository.findById(id);
    if (!user) {
      throw new NotFoundException(`User #${id} not found`);
    }
    return user;
  }

  async create(dto: CreateUserDto): Promise<User> {
    const user = await this.usersRepository.create(dto);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}
```

## Provider Scopes

```typescript
import { Injectable, Scope } from '@nestjs/common';

// Singleton (default) - shared across all requests
@Injectable()
export class SingletonService {}

// Request scope - new instance per request
@Injectable({ scope: Scope.REQUEST })
export class RequestScopedService {
  constructor(@Inject(REQUEST) private request: Request) {}
}

// Transient - new instance each injection
@Injectable({ scope: Scope.TRANSIENT })
export class TransientService {}
```

## Custom Providers

```typescript
// Value provider
const configProvider = {
  provide: 'CONFIG',
  useValue: { apiKey: 'xxx' },
};

// Factory provider
const dbProvider = {
  provide: 'DATABASE',
  useFactory: async (config: ConfigService) => {
    return createConnection(config.get('DATABASE_URL'));
  },
  inject: [ConfigService],
};

// Class provider
const loggerProvider = {
  provide: LoggerService,
  useClass: process.env.NODE_ENV === 'test' 
    ? MockLoggerService 
    : LoggerService,
};

// Existing provider (alias)
const aliasProvider = {
  provide: 'ALIAS',
  useExisting: RealService,
};

@Module({
  providers: [configProvider, dbProvider, loggerProvider],
})
export class AppModule {}
```

## Async Providers

```typescript
@Module({
  providers: [
    {
      provide: 'ASYNC_CONNECTION',
      useFactory: async () => {
        const connection = await createConnection();
        return connection;
      },
    },
  ],
})
export class DatabaseModule {}
```

## Circular Dependencies

```typescript
// Use forwardRef for circular deps
@Injectable()
export class CatsService {
  constructor(
    @Inject(forwardRef(() => DogsService))
    private dogsService: DogsService,
  ) {}
}

@Injectable()
export class DogsService {
  constructor(
    @Inject(forwardRef(() => CatsService))
    private catsService: CatsService,
  ) {}
}
```
