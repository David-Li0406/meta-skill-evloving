# Testcontainers Integration Guide

## 설치

```bash
pnpm add -D testcontainers @testcontainers/postgresql @testcontainers/redis
```

## PostgreSQL 통합 테스트

```typescript
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { Test, TestingModule } from '@nestjs/testing';
import { TypeOrmModule } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';

describe('UserRepository (Integration)', () => {
  let container: StartedPostgreSqlContainer;
  let dataSource: DataSource;
  let repository: UserRepository;

  beforeAll(async () => {
    // 1. PostgreSQL 컨테이너 시작
    container = await new PostgreSqlContainer('postgres:15-alpine')
      .withDatabase('test_db')
      .withUsername('test')
      .withPassword('test')
      .start();

    // 2. NestJS 모듈 생성 (동적 DB 설정)
    const module: TestingModule = await Test.createTestingModule({
      imports: [
        TypeOrmModule.forRoot({
          type: 'postgres',
          host: container.getHost(),
          port: container.getPort(),
          username: container.getUsername(),
          password: container.getPassword(),
          database: container.getDatabase(),
          entities: [User],
          synchronize: true,
        }),
        TypeOrmModule.forFeature([User]),
      ],
      providers: [UserRepository],
    }).compile();

    repository = module.get(UserRepository);
    dataSource = module.get(DataSource);
  });

  afterAll(async () => {
    await dataSource?.destroy();
    await container?.stop();
  });

  beforeEach(async () => {
    // 각 테스트 전 DB 초기화
    await dataSource.synchronize(true);
  });

  it('should save and retrieve user', async () => {
    // Arrange
    const user = { name: 'Test User', email: 'test@example.com' };

    // Act
    const saved = await repository.save(user);
    const found = await repository.findById(saved.id);

    // Assert
    expect(found).toMatchObject(user);
  });
});
```

## Redis 통합 테스트

```typescript
import { RedisContainer, StartedRedisContainer } from '@testcontainers/redis';
import { CacheModule } from '@nestjs/cache-manager';
import * as redisStore from 'cache-manager-redis-store';

describe('CacheService (Integration)', () => {
  let container: StartedRedisContainer;

  beforeAll(async () => {
    container = await new RedisContainer().start();

    const module = await Test.createTestingModule({
      imports: [
        CacheModule.register({
          store: redisStore,
          host: container.getHost(),
          port: container.getPort(),
        }),
      ],
      providers: [CacheService],
    }).compile();
  });

  afterAll(async () => {
    await container?.stop();
  });
});
```

## 테스트 격리 패턴

### 트랜잭션 롤백

```typescript
describe('with transaction rollback', () => {
  let queryRunner: QueryRunner;

  beforeEach(async () => {
    queryRunner = dataSource.createQueryRunner();
    await queryRunner.startTransaction();
  });

  afterEach(async () => {
    await queryRunner.rollbackTransaction();
    await queryRunner.release();
  });
});
```

### 테이블 Truncate

```typescript
beforeEach(async () => {
  const entities = dataSource.entityMetadatas;
  for (const entity of entities) {
    const repo = dataSource.getRepository(entity.name);
    await repo.query(`TRUNCATE "${entity.tableName}" CASCADE`);
  }
});
```

## 성능 최적화

### 컨테이너 재사용 (Reusable)

```typescript
const container = await new PostgreSqlContainer()
  .withReuse()  // 컨테이너 재사용 활성화
  .start();
```

### 병렬 테스트용 네트워크 격리

```typescript
const network = await new Network().start();

const postgres = await new PostgreSqlContainer()
  .withNetwork(network)
  .withNetworkAliases('postgres')
  .start();

const redis = await new RedisContainer()
  .withNetwork(network)
  .withNetworkAliases('redis')
  .start();
```

## Jest 설정

```javascript
// jest.integration.config.js
module.exports = {
  ...require('./jest.config'),
  testRegex: '.*\\.integration\\.spec\\.ts$',
  testTimeout: 60000,  // 컨테이너 시작 시간 고려
  maxWorkers: 1,       // 순차 실행 (리소스 관리)
};
```

```json
// package.json
{
  "scripts": {
    "test:integration": "jest --config jest.integration.config.js"
  }
}
```
