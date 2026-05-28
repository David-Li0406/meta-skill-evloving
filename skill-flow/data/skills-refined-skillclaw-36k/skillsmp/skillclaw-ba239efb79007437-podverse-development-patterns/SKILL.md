---
name: podverse-development-patterns
description: Use this skill when you need a reference for common development patterns in the Podverse API and ORM applications.
---

# Skill body

This skill provides a consolidated reference for common patterns used in the Podverse API and ORM applications, including route definitions, controller patterns, entity definitions, and service patterns.

## Monorepo Context

- **API app location**: `apps/api/`
- **ORM package location**: `packages/orm/`
- **Shared helpers**: `@podverse/helpers` (from `packages/helpers/`)
- **Key Dependencies**:
  - `@podverse/helpers`: Types, DTOs, utilities
  - `@podverse/orm`: Database entities and services
  - `typeorm`: ORM framework
  - `@podverse/mq`: Message queue operations
  - `@podverse/parser`: Feed parsing
  - `@podverse/external-services`: Third-party service integrations
  - `@podverse/notifications`: Push notifications

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

This skill combines the essential patterns from both the Podverse API and ORM, providing a comprehensive guide for developers working within the Podverse ecosystem.