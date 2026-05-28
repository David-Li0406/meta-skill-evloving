# Better Auth + Prisma Integration

Complete guide for integrating Better Auth with Prisma ORM.

## Installation

```bash
# npm
npm install better-auth @prisma/client
npm install -D prisma

# pnpm
pnpm add better-auth @prisma/client
pnpm add -D prisma

# yarn
yarn add better-auth @prisma/client
yarn add -D prisma

# bun
bun add better-auth @prisma/client
bun add -D prisma
```

Initialize Prisma:

```bash
npx prisma init
# or: pnpm prisma init
```

## File Structure

```
project/
├── src/
│   └── lib/
│       ├── auth.ts           # Better Auth config
│       ├── auth-client.ts    # Client config
│       └── prisma.ts         # Prisma client
├── prisma/
│   ├── schema.prisma         # Main schema (includes auth models)
│   └── auth-schema.prisma    # Generated auth schema (copy to main)
└── .env
```

## Step-by-Step Setup

### 1. Create Prisma Client

```typescript
// src/lib/prisma.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query"] : [],
  });

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
```

### 2. Configure Better Auth

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { prisma } from "./prisma";

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql", // "postgresql" | "mysql" | "sqlite"
  }),
  emailAndPassword: {
    enabled: true,
  },
});

export type Auth = typeof auth;
```

### 3. Generate Auth Schema

```bash
# Generate Prisma schema from your auth config
npx @better-auth/cli generate --output prisma/auth-schema.prisma
```

### 4. Add Auth Models to Schema

Copy the generated models from `prisma/auth-schema.prisma` to your `prisma/schema.prisma`:

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// === YOUR APP MODELS ===
model Task {
  id        String   @id @default(cuid())
  title     String
  completed Boolean  @default(false)
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

// === BETTER AUTH MODELS (from auth-schema.prisma) ===
model User {
  id            String    @id
  name          String
  email         String    @unique
  emailVerified Boolean   @default(false)
  image         String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  sessions      Session[]
  accounts      Account[]
  tasks         Task[]    // Your relation
}

model Session {
  id        String   @id
  expiresAt DateTime
  token     String   @unique
  ipAddress String?
  userAgent String?
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([userId])
}

model Account {
  id                    String    @id
  accountId             String
  providerId            String
  userId                String
  user                  User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  accessToken           String?
  refreshToken          String?
  idToken               String?
  accessTokenExpiresAt  DateTime?
  refreshTokenExpiresAt DateTime?
  scope                 String?
  password              String?
  createdAt             DateTime  @default(now())
  updatedAt             DateTime  @updatedAt

  @@index([userId])
}

model Verification {
  id         String   @id
  identifier String
  value      String
  expiresAt  DateTime
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt
}
```

### 5. Run Migrations

```bash
# Create and apply migration
npx prisma migrate dev --name init

# Or push directly (dev only)
npx prisma db push

# Generate Prisma Client
npx prisma generate
```

## Adding Plugins

When you add Better Auth plugins, regenerate the schema:

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { twoFactor, organization } from "better-auth/plugins";
import { prisma } from "./prisma";

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
  plugins: [
    twoFactor(),
    organization(),
  ],
});
```

Then regenerate and migrate:

```bash
# Regenerate schema with new plugin tables
npx @better-auth/cli generate --output prisma/auth-schema.prisma

# Copy new models to schema.prisma manually

# Create migration
npx prisma migrate dev --name add_2fa_and_org

# Regenerate client
npx prisma generate
```

## Plugin-Specific Models

### Two-Factor Authentication

```prisma
model TwoFactor {
  id          String  @id
  secret      String
  backupCodes String
  userId      String  @unique
  user        User    @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

### Organization Plugin

```prisma
model Organization {
  id        String   @id
  name      String
  slug      String   @unique
  logo      String?
  createdAt DateTime @default(now())
  metadata  String?
  members   Member[]
}

model Member {
  id             String       @id
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id], onDelete: Cascade)
  userId         String
  user           User         @relation(fields: [userId], references: [id], onDelete: Cascade)
  role           String
  createdAt      DateTime     @default(now())

  @@unique([organizationId, userId])
}

model Invitation {
  id             String       @id
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id], onDelete: Cascade)
  email          String
  role           String?
  status         String
  expiresAt      DateTime
  inviterId      String
  inviter        User         @relation(fields: [inviterId], references: [id], onDelete: Cascade)
}
```

## Custom User Fields

```typescript
// src/lib/auth.ts
export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
  user: {
    additionalFields: {
      role: {
        type: "string",
        defaultValue: "user",
      },
      plan: {
        type: "string",
        defaultValue: "free",
      },
    },
  },
});
```

After adding custom fields, regenerate and add to schema:

```prisma
model User {
  id            String    @id
  name          String
  email         String    @unique
  emailVerified Boolean   @default(false)
  image         String?
  role          String    @default("user")   // Custom field
  plan          String    @default("free")   // Custom field
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  // ... relations
}
```

## Querying Auth Tables with Prisma

```typescript
import { prisma } from "@/lib/prisma";

// Get user by email
const user = await prisma.user.findUnique({
  where: { email: "test@example.com" },
});

// Get user with sessions
const userWithSessions = await prisma.user.findUnique({
  where: { id: userId },
  include: { sessions: true },
});

// Get user with accounts (OAuth connections)
const userWithAccounts = await prisma.user.findUnique({
  where: { id: userId },
  include: { accounts: true },
});

// Count active sessions
const sessionCount = await prisma.session.count({
  where: { userId },
});

// Delete expired sessions
await prisma.session.deleteMany({
  where: {
    expiresAt: { lt: new Date() },
  },
});
```

## Common Issues & Solutions

### Issue: Prisma Client not generated

```
Error: @prisma/client did not initialize yet
```

**Solution:**

```bash
npx prisma generate
```

### Issue: Schema drift

```
Error: The database schema is not in sync with your Prisma schema
```

**Solution:**

```bash
# For development
npx prisma db push --force-reset

# For production (create migration first)
npx prisma migrate dev
```

### Issue: Relation not defined

```
Error: Unknown field 'user' in 'include'
```

**Solution:** Ensure relations are properly defined in both models:

```prisma
model Session {
  userId String
  user   User @relation(fields: [userId], references: [id])
}

model User {
  sessions Session[]
}
```

### Issue: Type errors after schema change

**Solution:**

```bash
npx prisma generate
# Restart TypeScript server in IDE
```

## Environment Variables

```env
# PostgreSQL
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"

# MySQL
DATABASE_URL="mysql://user:password@localhost:3306/mydb"

# SQLite
DATABASE_URL="file:./dev.db"

# PostgreSQL with connection pooling (Supabase, Neon)
DATABASE_URL="postgresql://user:password@host:5432/mydb?pgbouncer=true"
DIRECT_URL="postgresql://user:password@host:5432/mydb"
```

For connection pooling (Supabase, Neon, etc.):

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

## Production Considerations

1. **Always use migrations** in production:
   ```bash
   npx prisma migrate deploy
   ```

2. **Use connection pooling** for serverless:
   ```prisma
   datasource db {
     provider  = "postgresql"
     url       = env("DATABASE_URL")
     directUrl = env("DIRECT_URL")
   }
   ```

3. **Optimize queries** with select/include:
   ```typescript
   const user = await prisma.user.findUnique({
     where: { id },
     select: { id: true, name: true, email: true },
   });
   ```

4. **Handle Prisma in serverless** (Next.js, Vercel):
   ```typescript
   // Use the singleton pattern shown above in prisma.ts
   ```

## Full Example

```typescript
// src/lib/prisma.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}

// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { nextCookies } from "better-auth/next-js";
import { twoFactor } from "better-auth/plugins";
import { prisma } from "./prisma";

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  plugins: [
    nextCookies(),
    twoFactor(),
  ],
});
```

## Prisma Studio

View and edit your auth data:

```bash
npx prisma studio
```

Opens at `http://localhost:5555` - useful for debugging auth issues.
