---
name: podverse-development-patterns
description: Use this skill for common development patterns in the Podverse API and ORM applications.
---

# Podverse Development Patterns

This skill provides quick reference for common patterns used in the Podverse API and ORM applications.

## Monorepo Context

- **API app location**: `apps/api/`
- **ORM package location**: `packages/orm/`
- **Shared helpers**: `@podverse/helpers` (from `packages/helpers/`)
- **Message queue**: `@podverse/mq` (from `packages/mq/`)
- **Feed parsing**: `@podverse/parser` (from `packages/parser/`)
- **Database migrations**: `infra/database/main/migrations/`

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `@podverse/helpers` | Types, DTOs, utilities |
| `@podverse/orm` | Database entities and services |
| `@podverse/mq` | Message queue operations |
| `@podverse/parser` | Feed parsing |
| `@podverse/external-services` | Third-party service integrations |
| `@podverse/notifications` | Push notifications |
| `typeorm` | ORM framework |

## Patterns

### Route Definition

```typescript
// apps/api/src/routes/podcast.ts
import { Router } from 'express'
import { PodcastController } from '../controllers/podcast'
import { asyncHandler } from '../lib/asyncHandler'

const router = Router()

router.get('/:id', asyncHandler(PodcastController.getById))
router.post('/', asyncHandler(PodcastController.create))

export default router
```

### Controller Pattern

```typescript
// apps/api/src/controllers/podcast.ts
import { Request, Response } from 'express'
import { PodcastService } from '@podverse/orm'

export const PodcastController = {
  async getById(req: Request, res: Response) {
    const { id } = req.params
    const podcast = await PodcastService.getById(id)
    
    if (!podcast) {
      return res.status(404).json({ error: 'Podcast not found' })
    }
    
    res.json(podcast)
  },

  async create(req: Request, res: Response) {
    const data = req.body
    const podcast = await PodcastService.create(data)
    res.status(201).json(podcast)
  }
}
```

### Entity Definition

```typescript
// packages/orm/src/entities/Podcast.ts
import { Entity, PrimaryGeneratedColumn, Column, OneToMany, CreateDateColumn, UpdateDateColumn } from 'typeorm'
import { Episode } from './Episode'

@Entity('podcast')
export class Podcast {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column()
  title: string

  @Column({ nullable: true })
  description?: string

  @Column({ unique: true })
  feedUrl: string

  @Column({ nullable: true })
  imageUrl?: string

  @OneToMany(() => Episode, (episode) => episode.podcast)
  episodes: Episode[]

  @CreateDateColumn()
  createdAt: Date

  @UpdateDateColumn()
  updatedAt: Date
}
```

### Service Pattern

```typescript
// packages/orm/src/services/PodcastService.ts
import { getRepository } from 'typeorm'
import { Podcast } from '../entities/Podcast'

export const PodcastService = {
  async getById(id: string): Promise<Podcast | null> {
    const repo = getRepository(Podcast)
    return repo.findOne({ where: { id } })
  },

  async create(data: Partial<Podcast>): Promise<Podcast> {
    const repo = getRepository(Podcast)
    const podcast = repo.create(data)
    return repo.save(podcast)
  },

  async update(id: string, data: Partial<Podcast>): Promise<Podcast | null> {
    const repo = getRepository(Podcast)
    await repo.update(id, data)
    return this.getById(id)
  },

  async delete(id: string): Promise<void> {
    const repo = getRepository(Podcast)
    await repo.delete(id)
  }
}
```

### Rate Limiting

```typescript
// apps/api/src/lib/rateLimiter.ts
import { rateLimitAuthEndpoint, rateLimitEndpoint } from '@api/lib/rateLimiter'

// For authenticated endpoints (per-user rate limiting)
router.get('/download-data', 
  rateLimitAuthEndpoint({ windowMs: 24 * 60 * 60 * 1000, max: 3 }), 
  asyncHandler(AccountController.downloadData)
)

// For public endpoints (IP-based rate limiting)
router.post('/create', 
  rateLimitEndpoint({ windowMs: 10 * 60 * 1000, max: 3 }), 
  asyncHandler(AccountController.create)
)
```

### Query Builder Pattern

```typescript
// For complex queries
async findWithFilters(filters: PodcastFilters): Promise<Podcast[]> {
  const repo = getRepository(Podcast)
  const qb = repo.createQueryBuilder('podcast')

  if (filters.searchTerm) {
    qb.where('podcast.title ILIKE :term', { term: `%${filters.searchTerm}%` })
  }

  qb.orderBy('podcast.createdAt', 'DESC')
    .skip(filters.offset || 0)
    .take(filters.limit || 20)

  return qb.getMany()
}
```

### Error Handling

```typescript
// Use asyncHandler to catch errors automatically
import { asyncHandler } from '../lib/asyncHandler'

router.get('/:id', asyncHandler(async (req, res) => {
  const result = await riskyOperation()
  res.json(result)
}))
```

### Migration Patterns

Migrations are located in `infra/database/main/migrations/`.

#### Creating a Migration

```bash
# Generate migration from entity changes
npm run typeorm migration:generate -- -n MigrationName

# Create empty migration
npm run typeorm migration:create -- -n MigrationName
```

#### Migration Structure

```typescript
// infra/database/main/migrations/YYYYMMDDHHMMSS-AddPodcastCategory.ts
import { MigrationInterface, QueryRunner, TableColumn } from 'typeorm'

export class AddPodcastCategory1234567890123 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.addColumn('podcast', new TableColumn({
      name: 'category',
      type: 'varchar',
      isNullable: true
    }))
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropColumn('podcast', 'category')
  }
}
```

## File Structure

```
apps/api/
├── src/
│   ├── controllers/     # Request handlers
│   ├── routes/          # Route definitions
│   ├── middleware/      # Express middleware
│   ├── lib/             # Utilities and helpers
│   │   ├── startup/     # App initialization
│   │   └── rateLimiter.ts
│   └── index.ts         # Entry point
├── package.json
└── tsconfig.json

packages/orm/
├── src/
│   ├── entities/        # TypeORM entities
│   ├── services/        # Data access services
│   ├── subscribers/     # Entity subscribers
│   └── index.ts         # Public exports
├── package.json
└── tsconfig.json

infra/database/main/
├── migrations/          # TypeORM migrations
└── seeds/               # Seed data (if any)
```

## Best Practices

1. **Always use services**: Don't access repositories directly from controllers.
2. **Use transactions**: For operations that modify multiple entities.
3. **Index properly**: Add indexes for frequently queried columns.
4. **Validate at entity level**: Use class-validator decorators when appropriate.
5. **Use DTOs**: Transform entities to DTOs before sending to clients.

## Related Skills

- **[API Patterns](../api/SKILL.md)** - Using ORM in controllers
- **[Global Patterns](../global/SKILL.md)** - Monorepo conventions