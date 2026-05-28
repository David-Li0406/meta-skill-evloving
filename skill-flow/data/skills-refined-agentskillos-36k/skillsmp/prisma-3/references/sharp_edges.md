# Prisma - Sharp Edges

## N Plus One Queries

### **Id**
n-plus-one-queries
### **Summary**
Fetching relations causes N+1 queries
### **Severity**
high
### **Situation**
Slow API responses, many database calls
### **Why**
  Accessing relations in loop triggers queries.
  Each access = new database call.
  Compounds with list size.
  
### **Solution**
  import { prisma } from "@/lib/prisma";
  
  // WRONG - N+1 queries
  const users = await prisma.user.findMany();
  for (const user of users) {
    // Each iteration = new query!
    const posts = await prisma.post.findMany({
      where: { authorId: user.id }
    });
  }
  
  // CORRECT - include relation
  const users = await prisma.user.findMany({
    include: {
      posts: true  // Single JOIN query
    }
  });
  
  // CORRECT - select specific fields
  const users = await prisma.user.findMany({
    select: {
      id: true,
      email: true,
      posts: {
        select: { id: true, title: true },
        where: { published: true },
        take: 5
      }
    }
  });
  
  // CORRECT - use _count for counts
  const users = await prisma.user.findMany({
    include: {
      _count: { select: { posts: true } }
    }
  });
  // Access: user._count.posts
  
  // For complex cases - batch manually
  const users = await prisma.user.findMany();
  const userIds = users.map(u => u.id);
  const posts = await prisma.post.findMany({
    where: { authorId: { in: userIds } }
  });
  // Group posts by author in memory
  
### **Symptoms**
  - Slow API responses
  - Many queries in logs
  - Database CPU spikes
### **Detection Pattern**
await.*findMany.*for.*await

## Connection Exhaustion

### **Id**
connection-exhaustion
### **Summary**
Too many database connections
### **Severity**
high
### **Situation**
"Connection timeout" or "Too many clients"
### **Why**
  New PrismaClient per request.
  Serverless scales connections.
  No connection pooling.
  
### **Solution**
  // WRONG - new client per request
  export async function handler(req, res) {
    const prisma = new PrismaClient();  // New connection!
    const users = await prisma.user.findMany();
    return res.json(users);
    // Connection may not close!
  }
  
  // CORRECT - singleton pattern
  // lib/prisma.ts
  import { PrismaClient } from "@prisma/client";
  
  const globalForPrisma = global as unknown as {
    prisma: PrismaClient | undefined;
  };
  
  export const prisma = globalForPrisma.prisma ?? new PrismaClient();
  
  if (process.env.NODE_ENV !== "production") {
    globalForPrisma.prisma = prisma;
  }
  
  // Configure connection pool
  const prisma = new PrismaClient({
    datasources: {
      db: {
        url: process.env.DATABASE_URL
      }
    }
  });
  
  // In DATABASE_URL, add pool config:
  // ?connection_limit=5&pool_timeout=10
  
  // For serverless - use external pooler
  // Supabase: ?pgbouncer=true
  // Neon: Use pooled connection string
  // PlanetScale: Built-in pooling
  
  // Or use Prisma Accelerate
  import { withAccelerate } from "@prisma/extension-accelerate";
  
  const prisma = new PrismaClient().$extends(withAccelerate());
  
### **Symptoms**
  - Too many clients already
  - Connection timeouts
  - Cold starts fail
### **Detection Pattern**
new PrismaClient\(\)

## Missing Directurl

### **Id**
missing-directurl
### **Summary**
Migrations fail with pooled connection
### **Severity**
high
### **Situation**
Prisma migrate fails, can't connect
### **Why**
  Pooled URLs can't run DDL.
  Migrations need direct connection.
  Wrong URL for migrations.
  
### **Solution**
  // schema.prisma - use both URLs
  datasource db {
    provider  = "postgresql"
    url       = env("DATABASE_URL")        // Pooled for queries
    directUrl = env("DIRECT_DATABASE_URL")  // Direct for migrations
  }
  
  // .env
  # Pooled connection (for application)
  DATABASE_URL="postgresql://user:pass@pooler.host:6543/db?pgbouncer=true"
  
  # Direct connection (for migrations)
  DIRECT_DATABASE_URL="postgresql://user:pass@direct.host:5432/db"
  
  // For different providers:
  
  // Supabase
  DATABASE_URL="postgresql://...@db.xxx.supabase.co:6543/postgres?pgbouncer=true"
  DIRECT_DATABASE_URL="postgresql://...@db.xxx.supabase.co:5432/postgres"
  
  // Neon
  DATABASE_URL="postgresql://...@ep-xxx.us-east-2.aws.neon.tech/db?sslmode=require"
  DIRECT_DATABASE_URL="postgresql://...@ep-xxx.us-east-2.aws.neon.tech/db?sslmode=require"
  
  // PlanetScale (uses relationMode instead)
  datasource db {
    provider     = "mysql"
    url          = env("DATABASE_URL")
    relationMode = "prisma"  // Handles foreign keys in Prisma
  }
  
### **Symptoms**
  - prepared statement already exists
  - Migrations hang
  - cannot run DDL
### **Detection Pattern**
directUrl|pgbouncer

## Enum Sync Issue

### **Id**
enum-sync-issue
### **Summary**
TypeScript enum out of sync with database
### **Severity**
medium
### **Situation**
Type errors after schema change
### **Why**
  Prisma generate not run after change.
  Client cached in node_modules.
  IDE not picking up new types.
  
### **Solution**
  # After schema changes, always:
  npx prisma generate
  
  # If still not working:
  rm -rf node_modules/.prisma
  npx prisma generate
  
  # Restart TypeScript server in VS Code:
  # Cmd/Ctrl + Shift + P -> "TypeScript: Restart TS Server"
  
  # For CI/CD - always generate before build
  // package.json
  {
    "scripts": {
      "build": "prisma generate && next build",
      "postinstall": "prisma generate"
    }
  }
  
  # Check generated types location
  # node_modules/.prisma/client/index.d.ts
  
  # Import types correctly
  import { User, Post, Role } from "@prisma/client";
  import type { Prisma } from "@prisma/client";
  
  // Use Prisma namespace for input types
  type UserCreateInput = Prisma.UserCreateInput;
  type UserWhereInput = Prisma.UserWhereInput;
  
### **Symptoms**
  - Property does not exist
  - Enum values not found
  - Old type definitions
### **Detection Pattern**
prisma generate|\.prisma/client

## Transaction Timeout

### **Id**
transaction-timeout
### **Summary**
Long transactions fail or block
### **Severity**
medium
### **Situation**
Transaction times out, data inconsistent
### **Why**
  Default timeout too short.
  Long operations in transaction.
  Locks held too long.
  
### **Solution**
  // Default transaction timeout is 5 seconds
  
  // Increase timeout for long operations
  const result = await prisma.$transaction(
    async (tx) => {
      // Long operations here
      const users = await tx.user.findMany();
      for (const user of users) {
        await tx.user.update({
          where: { id: user.id },
          data: { processedAt: new Date() }
        });
      }
    },
    {
      maxWait: 10000,  // Max time to acquire lock (ms)
      timeout: 30000   // Max time for transaction (ms)
    }
  );
  
  // Better: batch operations
  await prisma.$transaction(async (tx) => {
    // Single updateMany instead of loop
    await tx.user.updateMany({
      where: { processedAt: null },
      data: { processedAt: new Date() }
    });
  });
  
  // For very long operations - chunk outside transaction
  const users = await prisma.user.findMany({
    where: { processedAt: null }
  });
  
  // Process in batches
  const BATCH_SIZE = 100;
  for (let i = 0; i < users.length; i += BATCH_SIZE) {
    const batch = users.slice(i, i + BATCH_SIZE);
    await prisma.$transaction(
      batch.map(user =>
        prisma.user.update({
          where: { id: user.id },
          data: { processedAt: new Date() }
        })
      )
    );
  }
  
### **Symptoms**
  - Transaction timeout errors
  - Inconsistent data
  - Database locks
### **Detection Pattern**
\$transaction.*timeout

## Cascade Delete Danger

### **Id**
cascade-delete-danger
### **Summary**
Cascade delete removes more than expected
### **Severity**
high
### **Situation**
Related data unexpectedly deleted
### **Why**
  onDelete: Cascade removes children.
  Not always intended.
  Hard to recover.
  
### **Solution**
  // Understand delete behaviors:
  
  // CASCADE - delete children when parent deleted
  model Post {
    author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade)
    authorId String
  }
  // Deleting User deletes all their Posts!
  
  // SetNull - set FK to null
  model Post {
    author   User?  @relation(fields: [authorId], references: [id], onDelete: SetNull)
    authorId String?  // Must be optional
  }
  // Deleting User sets authorId to null
  
  // Restrict - prevent delete if children exist
  model Post {
    author   User   @relation(fields: [authorId], references: [id], onDelete: Restrict)
    authorId String
  }
  // Error if trying to delete User with Posts
  
  // NoAction - database handles it (usually Restrict)
  model Post {
    author   User   @relation(fields: [authorId], references: [id], onDelete: NoAction)
    authorId String
  }
  
  // Best practice: Soft delete
  model User {
    id        String    @id
    deletedAt DateTime?  // Null = active
    posts     Post[]
  }
  
  // Soft delete query
  await prisma.user.update({
    where: { id: userId },
    data: { deletedAt: new Date() }
  });
  
  // Filter out deleted in queries
  const users = await prisma.user.findMany({
    where: { deletedAt: null }
  });
  
### **Symptoms**
  - Related data disappeared
  - "Row not found" errors
  - Data integrity issues
### **Detection Pattern**
onDelete.*Cascade