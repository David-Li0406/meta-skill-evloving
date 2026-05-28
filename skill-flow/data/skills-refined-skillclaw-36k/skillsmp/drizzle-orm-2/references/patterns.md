# Drizzle ORM

## Patterns


---
  #### **Name**
Schema Definition with Foreign Keys
  #### **Description**
Define tables with proper foreign key constraints and indexes
  #### **When**
Creating a new database schema
  #### **Example**
    // schema.ts
    import { pgTable, text, timestamp, uuid, primaryKey } from 'drizzle-orm/pg-core';
    
    export const users = pgTable('users', {
      id: uuid('id').primaryKey().defaultRandom(),
      email: text('email').notNull().unique(),
      name: text('name'),
      createdAt: timestamp('created_at').defaultNow().notNull(),
    });
    
    export const posts = pgTable('posts', {
      id: uuid('id').primaryKey().defaultRandom(),
      title: text('title').notNull(),
      content: text('content'),
      authorId: uuid('author_id')
        .notNull()
        .references(() => users.id, { onDelete: 'cascade' }),
      createdAt: timestamp('created_at').defaultNow().notNull(),
    });
    
    // Indexes for performance
    export const postsAuthorIdx = index('posts_author_idx').on(posts.authorId);
    

---
  #### **Name**
Relations Configuration (Separate from Schema)
  #### **Description**
Define relations for the query API - these don't create DB constraints
  #### **When**
You want to use relational queries with db.query
  #### **Example**
    // relations.ts
    import { relations } from 'drizzle-orm';
    import { users, posts, comments } from './schema';
    
    export const usersRelations = relations(users, ({ many }) => ({
      posts: many(posts),
      comments: many(comments),
    }));
    
    export const postsRelations = relations(posts, ({ one, many }) => ({
      author: one(users, {
        fields: [posts.authorId],
        references: [users.id],
      }),
      comments: many(comments),
    }));
    
    // IMPORTANT: Relations are for query API only!
    // Foreign keys must be defined in the schema with .references()
    

---
  #### **Name**
Relational Query with Single SQL
  #### **Description**
Fetch nested data with exactly one SQL query
  #### **When**
You need related data without N+1 problems
  #### **Example**
    // Fetches user with all posts and comments in ONE query
    const userWithPosts = await db.query.users.findFirst({
      where: eq(users.id, userId),
      with: {
        posts: {
          with: {
            comments: true,
          },
          orderBy: [desc(posts.createdAt)],
          limit: 10,
        },
      },
    });
    
    // This emits a single SQL query using lateral joins
    // No N+1 problem, no multiple round trips
    

---
  #### **Name**
Cloudflare D1 Setup
  #### **Description**
Configure Drizzle for Cloudflare D1 edge database
  #### **When**
Deploying to Cloudflare Workers with D1
  #### **Example**
    // drizzle.config.ts
    import type { Config } from 'drizzle-kit';
    
    export default {
      schema: './src/db/schema.ts',
      out: './drizzle',
      dialect: 'sqlite',
      driver: 'd1-http',
      dbCredentials: {
        accountId: process.env.CLOUDFLARE_ACCOUNT_ID!,
        databaseId: process.env.CLOUDFLARE_D1_ID!,
        token: process.env.CLOUDFLARE_API_TOKEN!,
      },
    } satisfies Config;
    
    // In your Worker
    import { drizzle } from 'drizzle-orm/d1';
    import * as schema from './db/schema';
    
    export default {
      async fetch(request, env) {
        const db = drizzle(env.DB, { schema });
        // Use db.query or db.select/insert/update/delete
      },
    };
    

---
  #### **Name**
Type-Safe Select with Partial Columns
  #### **Description**
Select only needed columns with full type inference
  #### **When**
Optimizing queries to fetch only required data
  #### **Example**
    // Select specific columns - returns typed result
    const usersWithEmail = await db
      .select({
        id: users.id,
        email: users.email,
      })
      .from(users)
      .where(eq(users.active, true));
    
    // Type is automatically inferred as:
    // { id: string; email: string }[]
    
    // With joins
    const postsWithAuthor = await db
      .select({
        postTitle: posts.title,
        authorName: users.name,
      })
      .from(posts)
      .innerJoin(users, eq(posts.authorId, users.id));
    

---
  #### **Name**
Transaction with Rollback
  #### **Description**
Execute multiple operations atomically
  #### **When**
Multiple database operations must succeed or fail together
  #### **Example**
    await db.transaction(async (tx) => {
      // Insert user
      const [user] = await tx
        .insert(users)
        .values({ email: 'new@example.com', name: 'New User' })
        .returning();
    
      // Insert default settings for user
      await tx.insert(userSettings).values({
        userId: user.id,
        theme: 'dark',
        notifications: true,
      });
    
      // If any operation fails, everything rolls back
      // No partial state in database
    });
    

## Anti-Patterns


---
  #### **Name**
Confusing Relations with Foreign Keys
  #### **Description**
Defining relations without the corresponding foreign key constraint
  #### **Why**
    Relations are for the Drizzle query API only - they don't create database
    constraints. Without .references(), there's no foreign key, no cascade
    delete, and no referential integrity. Your database can have orphaned records.
    
  #### **Instead**
    // WRONG: Relation without foreign key
    export const posts = pgTable('posts', {
      authorId: uuid('author_id').notNull(), // Missing .references()!
    });
    export const postsRelations = relations(posts, ({ one }) => ({
      author: one(users, { fields: [posts.authorId], references: [users.id] }),
    }));
    
    // RIGHT: Foreign key AND relation
    export const posts = pgTable('posts', {
      authorId: uuid('author_id')
        .notNull()
        .references(() => users.id, { onDelete: 'cascade' }), // FK constraint!
    });
    // Then define relation for query API
    

---
  #### **Name**
Using Push in Production
  #### **Description**
Running drizzle-kit push against production databases
  #### **Why**
    push applies changes directly without migration history. You lose traceability,
    can't rollback, and team members have no record of changes. Fine for local dev,
    dangerous for production.
    
  #### **Instead**
    # Development: push for rapid iteration
    npx drizzle-kit push
    
    # Production: generate migrations, review, then apply
    npx drizzle-kit generate
    # Review the generated SQL in drizzle/
    npx drizzle-kit migrate
    

---
  #### **Name**
Implicit Any from Missing Schema Import
  #### **Description**
Not passing schema to drizzle() for relational queries
  #### **Why**
    db.query requires the schema to be passed to drizzle(). Without it, you get
    runtime errors or empty results. TypeScript won't catch this if you don't
    have strict mode.
    
  #### **Instead**
    // WRONG: No schema, db.query won't work
    const db = drizzle(client);
    const result = await db.query.users.findMany(); // Runtime error!
    
    // RIGHT: Pass schema for relational queries
    import * as schema from './schema';
    const db = drizzle(client, { schema });
    const result = await db.query.users.findMany(); // Works!
    

---
  #### **Name**
Over-Selecting with SELECT *
  #### **Description**
Using .select() without specifying columns
  #### **Why**
    Fetching all columns when you need 2 wastes bandwidth, especially on edge
    where every byte counts. Drizzle's type inference works best with explicit
    column selection.
    
  #### **Instead**
    // WRONG: Select all columns
    const users = await db.select().from(users);
    
    // RIGHT: Select only what you need
    const users = await db
      .select({ id: users.id, name: users.name })
      .from(users);
    

---
  #### **Name**
Manual N+1 Queries
  #### **Description**
Fetching related data in a loop instead of using relational queries
  #### **Why**
    Each query is a database round trip. 100 users = 101 queries (1 for users,
    100 for posts). Use relational queries to get nested data in a single query.
    
  #### **Instead**
    // WRONG: N+1 problem
    const allUsers = await db.select().from(users);
    for (const user of allUsers) {
      const userPosts = await db.select().from(posts)
        .where(eq(posts.authorId, user.id));
      // 101 queries for 100 users!
    }
    
    // RIGHT: Single query with relational
    const usersWithPosts = await db.query.users.findMany({
      with: { posts: true },
    });
    // 1 query, uses lateral joins
    

---
  #### **Name**
Raw SQL Injection
  #### **Description**
Interpolating user input directly into sql`` template
  #### **Why**
    SQL injection is alive and well. Never trust user input, even with template
    literals. Use parameterized queries or Drizzle's built-in operators.
    
  #### **Instead**
    // WRONG: SQL injection vulnerability
    const results = await db.execute(
      sql`SELECT * FROM users WHERE name = '${userInput}'`
    );
    
    // RIGHT: Parameterized with sql.placeholder or eq()
    const results = await db
      .select()
      .from(users)
      .where(eq(users.name, userInput)); // Drizzle escapes automatically
    