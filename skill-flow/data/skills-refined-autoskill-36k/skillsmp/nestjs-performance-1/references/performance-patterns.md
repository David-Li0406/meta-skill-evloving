# NestJS Performance Patterns

## Compression

```typescript
import compression from 'compression';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(compression());
  await app.listen(3000);
}
```

## Response Caching Interceptor

```typescript
import { CacheInterceptor, CacheKey, CacheTTL } from '@nestjs/cache-manager';

@Controller('products')
@UseInterceptors(CacheInterceptor)
export class ProductsController {
  @Get()
  @CacheKey('all-products')
  @CacheTTL(300) // 5 minutes
  findAll() {
    return this.productsService.findAll();
  }
}
```

## Request Timeout

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { timeout } from 'rxjs/operators';

@Injectable()
export class TimeoutInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler) {
    return next.handle().pipe(timeout(5000));
  }
}
```

## Database Query Optimization

```typescript
@Injectable()
export class UsersService {
  // Pagination
  async findAll(page = 1, limit = 20) {
    return this.userRepo.find({
      skip: (page - 1) * limit,
      take: limit,
      select: ['id', 'name', 'email'], // Select only needed fields
    });
  }

  // Eager loading
  async findWithOrders(id: string) {
    return this.userRepo.findOne({
      where: { id },
      relations: ['orders', 'orders.items'],
    });
  }
}
```

## Clustering

```typescript
// main.ts
import cluster from 'cluster';
import os from 'os';

if (cluster.isPrimary) {
  const numCPUs = os.cpus().length;
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  cluster.on('exit', (worker) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork();
  });
} else {
  bootstrap();
}
```

## Lazy Loading Modules

```typescript
@Module({})
export class AppModule {
  static forRoot(): DynamicModule {
    return {
      module: AppModule,
      imports: [
        LazyModuleLoader.forFeature([
          () => import('./reports/reports.module').then(m => m.ReportsModule),
        ]),
      ],
    };
  }
}
```
