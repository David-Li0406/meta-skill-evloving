# Better Auth + MongoDB Integration

Complete guide for integrating Better Auth with MongoDB.

## Installation

```bash
# npm
npm install better-auth mongodb

# pnpm
pnpm add better-auth mongodb

# yarn
yarn add better-auth mongodb

# bun
bun add better-auth mongodb
```

## File Structure

```
project/
├── src/
│   ├── lib/
│   │   ├── auth.ts           # Better Auth config
│   │   ├── auth-client.ts    # Client config
│   │   └── mongodb.ts        # MongoDB client
└── .env
```

## Step-by-Step Setup

### 1. Create MongoDB Client

```typescript
// src/lib/mongodb.ts
import { MongoClient, Db } from "mongodb";

const uri = process.env.MONGODB_URI!;
const options = {};

let client: MongoClient;
let clientPromise: Promise<MongoClient>;

if (process.env.NODE_ENV === "development") {
  // Use global variable in development to preserve connection
  const globalWithMongo = global as typeof globalThis & {
    _mongoClientPromise?: Promise<MongoClient>;
  };

  if (!globalWithMongo._mongoClientPromise) {
    client = new MongoClient(uri, options);
    globalWithMongo._mongoClientPromise = client.connect();
  }
  clientPromise = globalWithMongo._mongoClientPromise;
} else {
  // In production, create new connection
  client = new MongoClient(uri, options);
  clientPromise = client.connect();
}

export async function getDb(): Promise<Db> {
  const client = await clientPromise;
  return client.db(); // Uses database from connection string
}

export { clientPromise };
```

### 2. Configure Better Auth

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { clientPromise } from "./mongodb";

// Get the database instance
const client = await clientPromise;
const db = client.db();

export const auth = betterAuth({
  database: mongodbAdapter(db),
  emailAndPassword: {
    enabled: true,
  },
});

export type Auth = typeof auth;
```

**Alternative with async initialization:**

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { MongoClient } from "mongodb";

let auth: ReturnType<typeof betterAuth>;

async function initAuth() {
  const client = new MongoClient(process.env.MONGODB_URI!);
  await client.connect();
  const db = client.db();

  auth = betterAuth({
    database: mongodbAdapter(db),
    emailAndPassword: {
      enabled: true,
    },
  });

  return auth;
}

export { initAuth, auth };
```

### 3. Collections Created

Better Auth automatically creates these collections:

- `users` - User documents
- `sessions` - Session documents
- `accounts` - OAuth account links
- `verifications` - Email verification tokens

## Document Schemas

### User Document

```typescript
interface UserDocument {
  _id: ObjectId;
  id: string;
  name: string;
  email: string;
  emailVerified: boolean;
  image?: string;
  createdAt: Date;
  updatedAt: Date;
  // Custom fields you add
}
```

### Session Document

```typescript
interface SessionDocument {
  _id: ObjectId;
  id: string;
  expiresAt: Date;
  token: string;
  ipAddress?: string;
  userAgent?: string;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
}
```

### Account Document

```typescript
interface AccountDocument {
  _id: ObjectId;
  id: string;
  accountId: string;
  providerId: string;
  userId: string;
  accessToken?: string;
  refreshToken?: string;
  idToken?: string;
  accessTokenExpiresAt?: Date;
  refreshTokenExpiresAt?: Date;
  scope?: string;
  password?: string;
  createdAt: Date;
  updatedAt: Date;
}
```

## Create Indexes (Recommended)

```typescript
// src/db/setup-indexes.ts
import { getDb } from "@/lib/mongodb";

async function setupIndexes() {
  const db = await getDb();

  // User indexes
  await db.collection("users").createIndex({ email: 1 }, { unique: true });
  await db.collection("users").createIndex({ id: 1 }, { unique: true });

  // Session indexes
  await db.collection("sessions").createIndex({ token: 1 }, { unique: true });
  await db.collection("sessions").createIndex({ userId: 1 });
  await db.collection("sessions").createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });

  // Account indexes
  await db.collection("accounts").createIndex({ userId: 1 });
  await db.collection("accounts").createIndex({ providerId: 1, accountId: 1 });

  console.log("Indexes created");
}

setupIndexes().catch(console.error);
```

Run once:
```bash
npx tsx src/db/setup-indexes.ts
```

## Querying Auth Collections

```typescript
import { getDb } from "@/lib/mongodb";
import { ObjectId } from "mongodb";

// Get user by email
async function getUserByEmail(email: string) {
  const db = await getDb();
  return db.collection("users").findOne({ email });
}

// Get user with sessions
async function getUserWithSessions(userId: string) {
  const db = await getDb();
  const user = await db.collection("users").findOne({ id: userId });
  const sessions = await db.collection("sessions").find({ userId }).toArray();
  return { user, sessions };
}

// Aggregation: users with session count
async function getUsersWithSessionCount() {
  const db = await getDb();
  return db.collection("users").aggregate([
    {
      $lookup: {
        from: "sessions",
        localField: "id",
        foreignField: "userId",
        as: "sessions",
      },
    },
    {
      $project: {
        id: 1,
        name: 1,
        email: 1,
        sessionCount: { $size: "$sessions" },
      },
    },
  ]).toArray();
}

// Delete expired sessions
async function cleanupExpiredSessions() {
  const db = await getDb();
  return db.collection("sessions").deleteMany({
    expiresAt: { $lt: new Date() },
  });
}
```

## Adding Plugins

```typescript
import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { twoFactor, organization } from "better-auth/plugins";

export const auth = betterAuth({
  database: mongodbAdapter(db),
  plugins: [
    twoFactor(),
    organization(),
  ],
});
```

Plugins create additional collections automatically:
- `twoFactors` - 2FA secrets
- `organizations` - Organization documents
- `members` - Organization members
- `invitations` - Pending invitations

## Custom User Fields

```typescript
export const auth = betterAuth({
  database: mongodbAdapter(db),
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

## Common Issues & Solutions

### Issue: Connection timeout

**Solution:** Use connection pooling and keep-alive:

```typescript
const client = new MongoClient(uri, {
  maxPoolSize: 10,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
});
```

### Issue: Duplicate key error on email

**Solution:** Ensure unique index exists:

```typescript
await db.collection("users").createIndex({ email: 1 }, { unique: true });
```

### Issue: Session not expiring

**Solution:** Create TTL index:

```typescript
await db.collection("sessions").createIndex(
  { expiresAt: 1 },
  { expireAfterSeconds: 0 }
);
```

### Issue: Connection not closing

**Solution:** Handle graceful shutdown:

```typescript
process.on("SIGINT", async () => {
  const client = await clientPromise;
  await client.close();
  process.exit(0);
});
```

## Environment Variables

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/mydb?retryWrites=true&w=majority

# Local MongoDB
MONGODB_URI=mongodb://localhost:27017/mydb

# With replica set
MONGODB_URI=mongodb://localhost:27017,localhost:27018,localhost:27019/mydb?replicaSet=rs0
```

## MongoDB Atlas Setup

1. Create cluster at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create database user
3. Whitelist IP addresses (or use 0.0.0.0/0 for development)
4. Get connection string
5. Add to `.env`

## Full Example

```typescript
// src/lib/mongodb.ts
import { MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI!;

let clientPromise: Promise<MongoClient>;

if (process.env.NODE_ENV === "development") {
  const globalWithMongo = global as typeof globalThis & {
    _mongoClientPromise?: Promise<MongoClient>;
  };

  if (!globalWithMongo._mongoClientPromise) {
    globalWithMongo._mongoClientPromise = new MongoClient(uri).connect();
  }
  clientPromise = globalWithMongo._mongoClientPromise;
} else {
  clientPromise = new MongoClient(uri).connect();
}

export { clientPromise };

// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { nextCookies } from "better-auth/next-js";
import { clientPromise } from "./mongodb";

const client = await clientPromise;
const db = client.db();

export const auth = betterAuth({
  database: mongodbAdapter(db),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  plugins: [nextCookies()],
});
```

## MongoDB Compass

Use MongoDB Compass to view your auth data:
1. Download from [mongodb.com/products/compass](https://www.mongodb.com/products/compass)
2. Connect with your connection string
3. Browse `users`, `sessions`, `accounts` collections
