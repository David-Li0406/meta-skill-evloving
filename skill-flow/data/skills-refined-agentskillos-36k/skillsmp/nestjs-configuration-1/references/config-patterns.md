# NestJS Configuration Patterns

## Basic Setup

```typescript
import { ConfigModule, ConfigService } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: ['.env.local', '.env'],
    }),
  ],
})
export class AppModule {}

// Usage
@Injectable()
export class AppService {
  constructor(private configService: ConfigService) {}

  getDatabaseUrl(): string {
    return this.configService.get<string>('DATABASE_URL');
  }
}
```

## Validation with Joi

```typescript
import * as Joi from 'joi';

@Module({
  imports: [
    ConfigModule.forRoot({
      validationSchema: Joi.object({
        NODE_ENV: Joi.string()
          .valid('development', 'production', 'test')
          .default('development'),
        PORT: Joi.number().default(3000),
        DATABASE_URL: Joi.string().required(),
        JWT_SECRET: Joi.string().required(),
        JWT_EXPIRATION: Joi.string().default('1h'),
      }),
      validationOptions: {
        abortEarly: true,
      },
    }),
  ],
})
export class AppModule {}
```

## Configuration Namespaces

```typescript
// config/database.config.ts
import { registerAs } from '@nestjs/config';

export default registerAs('database', () => ({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT, 10) || 5432,
  name: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
}));

// config/jwt.config.ts
export default registerAs('jwt', () => ({
  secret: process.env.JWT_SECRET,
  expiresIn: process.env.JWT_EXPIRATION || '1h',
}));

// app.module.ts
@Module({
  imports: [
    ConfigModule.forRoot({
      load: [databaseConfig, jwtConfig],
    }),
  ],
})
export class AppModule {}

// Usage
@Injectable()
export class DatabaseService {
  constructor(private configService: ConfigService) {}

  getConfig() {
    return {
      host: this.configService.get<string>('database.host'),
      port: this.configService.get<number>('database.port'),
    };
  }
}
```

## Type-Safe Configuration

```typescript
// config/configuration.ts
export interface DatabaseConfig {
  host: string;
  port: number;
  name: string;
}

export interface AppConfig {
  database: DatabaseConfig;
  port: number;
}

export default (): AppConfig => ({
  port: parseInt(process.env.PORT, 10) || 3000,
  database: {
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT, 10) || 5432,
    name: process.env.DB_NAME,
  },
});

// Type-safe access
@Injectable()
export class AppService {
  constructor(private configService: ConfigService<AppConfig, true>) {}

  getPort(): number {
    return this.configService.get('port', { infer: true });
  }

  getDbHost(): string {
    return this.configService.get('database.host', { infer: true });
  }
}
```

## Environment Files

```bash
# .env
DATABASE_URL=postgres://localhost:5432/myapp
JWT_SECRET=your-secret-key

# .env.development
DEBUG=true
LOG_LEVEL=debug

# .env.production
LOG_LEVEL=error

# .env.test
DATABASE_URL=postgres://localhost:5432/myapp_test
```

```typescript
ConfigModule.forRoot({
  envFilePath: process.env.NODE_ENV === 'test' 
    ? '.env.test' 
    : [`.env.${process.env.NODE_ENV}`, '.env'],
})
```

## Async Configuration

```typescript
@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        host: config.get('database.host'),
        port: config.get('database.port'),
        database: config.get('database.name'),
        autoLoadEntities: true,
        synchronize: config.get('NODE_ENV') !== 'production',
      }),
    }),
  ],
})
export class DatabaseModule {}
```
