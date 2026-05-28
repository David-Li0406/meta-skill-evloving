# NestJS Logging & Metrics

## Built-in Logger

```typescript
import { Logger, Injectable } from '@nestjs/common';

@Injectable()
export class UsersService {
  private readonly logger = new Logger(UsersService.name);

  async findOne(id: string) {
    this.logger.log(`Finding user ${id}`);
    this.logger.debug('Debug info');
    this.logger.warn('Warning message');
    this.logger.error('Error occurred', error.stack);
    
    return user;
  }
}
```

## Custom Logger

```typescript
import { LoggerService } from '@nestjs/common';
import * as winston from 'winston';

export class WinstonLogger implements LoggerService {
  private logger: winston.Logger;

  constructor() {
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json(),
      ),
      transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'app.log' }),
      ],
    });
  }

  log(message: string, context?: string) {
    this.logger.info(message, { context });
  }

  error(message: string, trace?: string, context?: string) {
    this.logger.error(message, { trace, context });
  }

  warn(message: string, context?: string) {
    this.logger.warn(message, { context });
  }
}

// main.ts
const app = await NestFactory.create(AppModule, {
  logger: new WinstonLogger(),
});
```

## Request Logging Middleware

```typescript
@Injectable()
export class LoggingMiddleware implements NestMiddleware {
  private readonly logger = new Logger('HTTP');

  use(req: Request, res: Response, next: NextFunction) {
    const { method, originalUrl } = req;
    const requestId = req.headers['x-request-id'] || uuid();
    
    const start = Date.now();
    
    res.on('finish', () => {
      const duration = Date.now() - start;
      this.logger.log(
        `${method} ${originalUrl} ${res.statusCode} ${duration}ms`,
        { requestId },
      );
    });
    
    next();
  }
}
```

## Health Checks

```typescript
import { TerminusModule, HealthCheckService, HttpHealthIndicator, TypeOrmHealthIndicator } from '@nestjs/terminus';

@Controller('health')
export class HealthController {
  constructor(
    private health: HealthCheckService,
    private http: HttpHealthIndicator,
    private db: TypeOrmHealthIndicator,
  ) {}

  @Get()
  check() {
    return this.health.check([
      () => this.db.pingCheck('database'),
      () => this.http.pingCheck('api', 'https://api.example.com'),
    ]);
  }

  @Get('liveness')
  liveness() {
    return { status: 'ok' };
  }

  @Get('readiness')
  readiness() {
    return this.health.check([
      () => this.db.pingCheck('database'),
    ]);
  }
}
```

## Prometheus Metrics

```typescript
import { PrometheusModule, makeCounterProvider, makeHistogramProvider } from '@willsoto/nestjs-prometheus';

@Module({
  imports: [
    PrometheusModule.register({
      path: '/metrics',
      defaultMetrics: { enabled: true },
    }),
  ],
  providers: [
    makeCounterProvider({
      name: 'http_requests_total',
      help: 'Total HTTP requests',
      labelNames: ['method', 'path', 'status'],
    }),
    makeHistogramProvider({
      name: 'http_request_duration_seconds',
      help: 'HTTP request duration',
      labelNames: ['method', 'path'],
      buckets: [0.1, 0.5, 1, 2, 5],
    }),
  ],
})
export class MetricsModule {}

// Usage in interceptor
@Injectable()
export class MetricsInterceptor implements NestInterceptor {
  constructor(
    @InjectMetric('http_requests_total') private counter: Counter,
    @InjectMetric('http_request_duration_seconds') private histogram: Histogram,
  ) {}

  intercept(context: ExecutionContext, next: CallHandler) {
    const req = context.switchToHttp().getRequest();
    const start = Date.now();

    return next.handle().pipe(
      tap(() => {
        const duration = (Date.now() - start) / 1000;
        this.counter.inc({ method: req.method, path: req.path, status: 200 });
        this.histogram.observe({ method: req.method, path: req.path }, duration);
      }),
    );
  }
}
```
