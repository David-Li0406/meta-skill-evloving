# NestJS Database Reference

## Drizzle ORM (Recommended)

### Setup

```bash
bun add drizzle-orm pg
bun add -D drizzle-kit @types/pg
```

### Configuration

```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/database/schema/index.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  verbose: true,
  strict: true,
});
```

### Schema Definitions

```typescript
// src/database/schema/users.ts
import { pgTable, uuid, varchar, timestamp, boolean, index } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  passwordHash: varchar('password_hash', { length: 255 }).notNull(),
  name: varchar('name', { length: 100 }),
  avatarUrl: varchar('avatar_url', { length: 500 }),
  isActive: boolean('is_active').default(true).notNull(),
  emailVerifiedAt: timestamp('email_verified_at'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
}, (table) => ({
  emailIdx: index('users_email_idx').on(table.email),
  activeIdx: index('users_active_idx').on(table.isActive),
}));

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
  sessions: many(sessions),
}));

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
```

```typescript
// src/database/schema/posts.ts
import { pgTable, uuid, varchar, text, timestamp, boolean } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { users } from './users';

export const posts = pgTable('posts', {
  id: uuid('id').primaryKey().defaultRandom(),
  authorId: uuid('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  title: varchar('title', { length: 255 }).notNull(),
  slug: varchar('slug', { length: 255 }).notNull().unique(),
  content: text('content'),
  isPublished: boolean('is_published').default(false).notNull(),
  publishedAt: timestamp('published_at'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));

export type Post = typeof posts.$inferSelect;
export type NewPost = typeof posts.$inferInsert;
```

```typescript
// src/database/schema/index.ts
export * from './users';
export * from './posts';
export * from './sessions';
```

### Advanced Queries

```typescript
@Injectable()
export class PostRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDB) {}

  // Join with relations
  async findWithAuthor(id: string) {
    return this.db.query.posts.findFirst({
      where: eq(posts.id, id),
      with: {
        author: {
          columns: {
            id: true,
            name: true,
            avatarUrl: true,
          },
        },
      },
    });
  }

  // Complex filtering
  async findPublished(options: {
    authorId?: string;
    search?: string;
    page: number;
    limit: number;
  }) {
    const conditions = [eq(posts.isPublished, true)];

    if (options.authorId) {
      conditions.push(eq(posts.authorId, options.authorId));
    }
    if (options.search) {
      conditions.push(
        or(
          ilike(posts.title, `%${options.search}%`),
          ilike(posts.content, `%${options.search}%`),
        ),
      );
    }

    const offset = (options.page - 1) * options.limit;

    return this.db
      .select({
        post: posts,
        author: {
          id: users.id,
          name: users.name,
        },
      })
      .from(posts)
      .leftJoin(users, eq(posts.authorId, users.id))
      .where(and(...conditions))
      .orderBy(desc(posts.publishedAt))
      .limit(options.limit)
      .offset(offset);
  }

  // Aggregations
  async getAuthorStats(authorId: string) {
    const [stats] = await this.db
      .select({
        totalPosts: count(posts.id),
        publishedPosts: count(sql`case when ${posts.isPublished} then 1 end`),
        latestPost: max(posts.createdAt),
      })
      .from(posts)
      .where(eq(posts.authorId, authorId));

    return stats;
  }

  // Raw SQL when needed
  async findByFullTextSearch(query: string) {
    return this.db.execute(sql`
      SELECT * FROM posts
      WHERE to_tsvector('english', title || ' ' || content)
      @@ plainto_tsquery('english', ${query})
      ORDER BY ts_rank(
        to_tsvector('english', title || ' ' || content),
        plainto_tsquery('english', ${query})
      ) DESC
      LIMIT 20
    `);
  }
}
```

### Transactions

```typescript
@Injectable()
export class OrderService {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDB) {}

  async createOrder(userId: string, items: OrderItem[]) {
    return this.db.transaction(async (tx) => {
      // Create order
      const [order] = await tx
        .insert(orders)
        .values({ userId, status: 'pending' })
        .returning();

      // Create order items and update inventory
      for (const item of items) {
        // Lock inventory row
        const [product] = await tx
          .select()
          .from(products)
          .where(eq(products.id, item.productId))
          .for('update');

        if (!product || product.stock < item.quantity) {
          throw new BadRequestException(`Insufficient stock for ${product?.name}`);
        }

        // Deduct stock
        await tx
          .update(products)
          .set({ stock: sql`${products.stock} - ${item.quantity}` })
          .where(eq(products.id, item.productId));

        // Create order item
        await tx.insert(orderItems).values({
          orderId: order.id,
          productId: item.productId,
          quantity: item.quantity,
          price: product.price,
        });
      }

      // Calculate total
      const total = items.reduce((sum, item) => {
        const product = products.find((p) => p.id === item.productId);
        return sum + product!.price * item.quantity;
      }, 0);

      // Update order total
      const [finalOrder] = await tx
        .update(orders)
        .set({ total })
        .where(eq(orders.id, order.id))
        .returning();

      return finalOrder;
    });
  }
}
```

### Migrations

```bash
# Generate migration from schema changes
bunx drizzle-kit generate

# Apply migrations
bunx drizzle-kit migrate

# Push schema directly (dev only)
bunx drizzle-kit push

# Open Drizzle Studio
bunx drizzle-kit studio
```

```typescript
// Run migrations programmatically
import { migrate } from 'drizzle-orm/node-postgres/migrator';

async function runMigrations() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const db = drizzle(pool);
  await migrate(db, { migrationsFolder: './drizzle' });
  await pool.end();
}
```

## TypeORM Patterns

For projects using TypeORM:

```typescript
// Entity definition
@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  email: string;

  @Column({ name: 'password_hash' })
  passwordHash: string;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @OneToMany(() => Post, (post) => post.author)
  posts: Post[];
}

// Repository pattern
@Injectable()
export class UserRepository {
  constructor(
    @InjectRepository(User)
    private readonly repo: Repository<User>,
  ) {}

  async findByEmail(email: string): Promise<User | null> {
    return this.repo.findOne({ where: { email } });
  }
}

// Transaction
async transferWithTypeORM(fromId: string, toId: string, amount: number) {
  await this.dataSource.transaction(async (manager) => {
    const from = await manager.findOne(Account, {
      where: { id: fromId },
      lock: { mode: 'pessimistic_write' },
    });

    if (!from || from.balance < amount) {
      throw new BadRequestException('Insufficient funds');
    }

    await manager.decrement(Account, { id: fromId }, 'balance', amount);
    await manager.increment(Account, { id: toId }, 'balance', amount);
  });
}
```

## Prisma Patterns

For projects using Prisma:

```prisma
// schema.prisma
model User {
  id           String   @id @default(uuid())
  email        String   @unique
  passwordHash String   @map("password_hash")
  name         String?
  isActive     Boolean  @default(true) @map("is_active")
  createdAt    DateTime @default(now()) @map("created_at")
  posts        Post[]

  @@map("users")
}
```

```typescript
// Prisma service
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}

// Usage
@Injectable()
export class UserService {
  constructor(private readonly prisma: PrismaService) {}

  async findWithPosts(id: string) {
    return this.prisma.user.findUnique({
      where: { id },
      include: { posts: true },
    });
  }

  async createWithTransaction(data: CreateUserDto) {
    return this.prisma.$transaction(async (tx) => {
      const user = await tx.user.create({ data });
      await tx.auditLog.create({
        data: { action: 'USER_CREATED', entityId: user.id },
      });
      return user;
    });
  }
}
```

## Connection Pooling

```typescript
// Recommended pool settings
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                    // Max connections
  idleTimeoutMillis: 30000,   // Close idle connections after 30s
  connectionTimeoutMillis: 5000, // Timeout for new connections
});

// Health check
async checkDatabaseHealth(): Promise<boolean> {
  try {
    await this.db.execute(sql`SELECT 1`);
    return true;
  } catch {
    return false;
  }
}
```

## Soft Deletes Pattern

```typescript
// Schema with soft delete
export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  // ... other fields
  deletedAt: timestamp('deleted_at'),
});

// Repository methods
@Injectable()
export class UserRepository {
  async findById(id: string): Promise<User | undefined> {
    const [user] = await this.db
      .select()
      .from(users)
      .where(and(eq(users.id, id), isNull(users.deletedAt)))
      .limit(1);
    return user;
  }

  async softDelete(id: string): Promise<void> {
    await this.db
      .update(users)
      .set({ deletedAt: new Date() })
      .where(eq(users.id, id));
  }

  async restore(id: string): Promise<void> {
    await this.db
      .update(users)
      .set({ deletedAt: null })
      .where(eq(users.id, id));
  }

  // Include deleted records
  async findByIdIncludingDeleted(id: string): Promise<User | undefined> {
    const [user] = await this.db
      .select()
      .from(users)
      .where(eq(users.id, id))
      .limit(1);
    return user;
  }
}
```
