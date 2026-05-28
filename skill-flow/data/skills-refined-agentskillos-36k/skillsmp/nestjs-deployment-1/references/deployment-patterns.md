# NestJS Deployment Patterns

## Docker Multi-Stage Build

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "dist/main.js"]
```

## PM2 Configuration

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'api',
    script: 'dist/main.js',
    instances: 'max',
    exec_mode: 'cluster',
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000,
    },
    max_memory_restart: '1G',
    error_file: './logs/error.log',
    out_file: './logs/out.log',
  }],
};
```

## Graceful Shutdown

```typescript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.enableShutdownHooks();

  await app.listen(3000);
}

// In service
@Injectable()
export class AppService implements OnModuleDestroy {
  async onModuleDestroy() {
    // Cleanup: close DB connections, finish jobs
    await this.closeConnections();
  }
}
```

## Health Checks

```typescript
import { Controller, Get } from '@nestjs/common';
import {
  HealthCheck,
  HealthCheckService,
  HttpHealthIndicator,
  TypeOrmHealthIndicator,
} from '@nestjs/terminus';

@Controller('health')
export class HealthController {
  constructor(
    private health: HealthCheckService,
    private http: HttpHealthIndicator,
    private db: TypeOrmHealthIndicator,
  ) {}

  @Get()
  @HealthCheck()
  check() {
    return this.health.check([
      () => this.db.pingCheck('database'),
      () => this.http.pingCheck('api', 'https://api.example.com'),
    ]);
  }

  @Get('live')
  liveness() {
    return { status: 'ok' };
  }

  @Get('ready')
  readiness() {
    return this.health.check([
      () => this.db.pingCheck('database'),
    ]);
  }
}
```

## Serverless (AWS Lambda)

```typescript
// lambda.ts
import { NestFactory } from '@nestjs/core';
import { ExpressAdapter } from '@nestjs/platform-express';
import serverlessExpress from '@vendia/serverless-express';
import express from 'express';
import { AppModule } from './app.module';

let cachedServer;

async function bootstrap() {
  const expressApp = express();
  const adapter = new ExpressAdapter(expressApp);
  const app = await NestFactory.create(AppModule, adapter);
  await app.init();
  return serverlessExpress({ app: expressApp });
}

export const handler = async (event, context) => {
  if (!cachedServer) {
    cachedServer = await bootstrap();
  }
  return cachedServer(event, context);
};
```
