# NestJS Cache Patterns

## Basic Setup

```typescript
import { CacheModule } from '@nestjs/cache-manager';

@Module({
  imports: [
    CacheModule.register({
      ttl: 5000, // 5 seconds
      max: 100, // max items
    }),
  ],
})
export class AppModule {}
```

## Cache Interceptor

```typescript
import { CacheInterceptor, CacheKey, CacheTTL } from '@nestjs/cache-manager';

@Controller('users')
@UseInterceptors(CacheInterceptor)
export class UsersController {
  @Get()
  @CacheTTL(30000) // 30 seconds
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  @CacheKey('user')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }
}
```

## Programmatic Caching

```typescript
import { CACHE_MANAGER } from '@nestjs/cache-manager';
import { Cache } from 'cache-manager';

@Injectable()
export class UsersService {
  constructor(@Inject(CACHE_MANAGER) private cacheManager: Cache) {}

  async findOne(id: string): Promise<User> {
    // Check cache
    const cached = await this.cacheManager.get<User>(`user:${id}`);
    if (cached) return cached;

    // Fetch from DB
    const user = await this.usersRepository.findById(id);

    // Store in cache
    await this.cacheManager.set(`user:${id}`, user, 60000);

    return user;
  }

  async update(id: string, data: UpdateUserDto): Promise<User> {
    const user = await this.usersRepository.update(id, data);
    
    // Invalidate cache
    await this.cacheManager.del(`user:${id}`);
    
    return user;
  }

  async clearAllUsers(): Promise<void> {
    await this.cacheManager.reset();
  }
}
```

## Redis Store

```typescript
import { CacheModule } from '@nestjs/cache-manager';
import * as redisStore from 'cache-manager-redis-store';

@Module({
  imports: [
    CacheModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        store: redisStore,
        host: config.get('REDIS_HOST'),
        port: config.get('REDIS_PORT'),
        ttl: 60,
      }),
    }),
  ],
})
export class AppModule {}
```

## Custom Cache Key

```typescript
@Injectable()
export class CustomCacheInterceptor extends CacheInterceptor {
  trackBy(context: ExecutionContext): string | undefined {
    const request = context.switchToHttp().getRequest();
    const { method, url } = request;
    
    // Don't cache POST, PUT, DELETE
    if (method !== 'GET') return undefined;
    
    // Include user in cache key
    const userId = request.user?.id || 'anonymous';
    return `${userId}:${url}`;
  }
}
```

## Cache-Aside Pattern

```typescript
@Injectable()
export class ProductsService {
  constructor(
    @Inject(CACHE_MANAGER) private cache: Cache,
    private productsRepo: ProductsRepository,
  ) {}

  async getProduct(id: string): Promise<Product> {
    const cacheKey = `product:${id}`;
    
    // Try cache first
    let product = await this.cache.get<Product>(cacheKey);
    
    if (!product) {
      // Cache miss - fetch from DB
      product = await this.productsRepo.findById(id);
      
      if (product) {
        // Populate cache
        await this.cache.set(cacheKey, product, 300000); // 5 min
      }
    }
    
    return product;
  }
}
```

## Bulk Cache Operations

```typescript
async getProducts(ids: string[]): Promise<Product[]> {
  const products: Product[] = [];
  const missingIds: string[] = [];

  // Check cache for each
  for (const id of ids) {
    const cached = await this.cache.get<Product>(`product:${id}`);
    if (cached) {
      products.push(cached);
    } else {
      missingIds.push(id);
    }
  }

  // Fetch missing from DB
  if (missingIds.length > 0) {
    const dbProducts = await this.productsRepo.findByIds(missingIds);
    
    // Cache and add to result
    for (const product of dbProducts) {
      await this.cache.set(`product:${product.id}`, product);
      products.push(product);
    }
  }

  return products;
}
```
