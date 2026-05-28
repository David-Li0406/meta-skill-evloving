# Firebase Configuration

Setting up Firebase Admin SDK for server-side Firestore access.

## Directory Structure

```
lib/
└── firebase/
    ├── index.ts          # Main export (db instance)
    ├── types.ts          # Type utilities
    ├── errors.ts         # DbError class
    ├── seeder.ts         # Seeding utilities (optional)
    └── auto-seed.ts      # Auto-seeding orchestrator (optional)
```

## Firebase Admin SDK Setup

### Main Configuration

```typescript
// lib/firebase/index.ts
import "server-only";

import { cert, getApps, initializeApp } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";

import { env } from "~/data/env/server";

/**
 * Initialize Firebase Admin SDK
 * Only initializes once, returns existing app if already initialized
 */
function initializeFirebase() {
  if (getApps().length > 0) {
    return getApps()[0];
  }

  return initializeApp({
    credential: cert({
      projectId: env.FIREBASE_PROJECT_ID,
      clientEmail: env.FIREBASE_CLIENT_EMAIL,
      // Handle escaped newlines in private key
      privateKey: env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, "\n"),
    }),
  });
}

// Initialize app
const app = initializeFirebase();

// Export Firestore instance
export const db = getFirestore(app);

// Optional: Configure Firestore settings
db.settings({
  ignoreUndefinedProperties: true,
});
```

### Key Points

1. **`server-only`** - Prevents client-side bundling
2. **Singleton pattern** - `getApps().length` check prevents multiple initializations
3. **Environment variables** - Credentials from validated env config
4. **Private key handling** - Replace escaped newlines

## Environment Variables

### Server Environment Schema

```typescript
// data/env/server.ts
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    // Firebase Admin SDK credentials
    FIREBASE_PROJECT_ID: z.string().min(1),
    FIREBASE_CLIENT_EMAIL: z.string().email(),
    FIREBASE_PRIVATE_KEY: z.string().min(1),

    // Optional: Logging level
    LOG_LEVEL: z
      .enum(["fatal", "error", "warn", "info", "debug", "trace"])
      .default("info"),
  },
  experimental__runtimeEnv: {},
});
```

### Required Environment Variables

```bash
# .env.local

# Firebase Admin SDK (from Firebase Console > Project Settings > Service Accounts)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"

# Optional
LOG_LEVEL=info
```

### Getting Firebase Credentials

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project
3. Go to **Project Settings** (gear icon)
4. Select **Service accounts** tab
5. Click **Generate new private key**
6. Download JSON file
7. Extract values:
   - `project_id` → `FIREBASE_PROJECT_ID`
   - `client_email` → `FIREBASE_CLIENT_EMAIL`
   - `private_key` → `FIREBASE_PRIVATE_KEY`

## Type Utilities Export

```typescript
// lib/firebase/types.ts
import type { FieldValue, Timestamp } from "firebase-admin/firestore";

// Re-export Firebase types for convenience
export type { FieldValue, Timestamp };

// Custom type utilities
export type TimestampFields = {
  createdAt: Timestamp;
  updatedAt: Timestamp;
};

export type WithFirestoreTimestamps<T> = {
  [K in keyof T]: T[K] extends Date
    ? Timestamp
    : T[K] extends Date | undefined
      ? Timestamp | undefined
      : T[K];
} & TimestampFields;

export type WithDates<T> = {
  id: string;
} & {
  [K in keyof T]: T[K] extends Date
    ? Date
    : T[K] extends Date | undefined
      ? Date | undefined
      : T[K];
} & {
  createdAt: Date;
  updatedAt: Date;
};

export type CreateDto<T> = {
  [K in keyof T]: T[K] extends Date
    ? FieldValue
    : T[K] extends Date | undefined
      ? FieldValue | undefined
      : T[K];
} & {
  createdAt: FieldValue;
  updatedAt: FieldValue;
};

export type UpdateDto<T> = Partial<{
  [K in keyof T]: T[K] extends Date
    ? FieldValue | Timestamp
    : T[K] extends Date | undefined
      ? FieldValue | Timestamp | undefined
      : T[K];
}> & {
  updatedAt?: FieldValue;
};
```

## Error Utilities Export

```typescript
// lib/firebase/errors.ts
import "server-only";

export class DbError extends Error {
  // ... (see errors.md for full implementation)
}

export function categorizeDbError(
  error: unknown,
  resourceName: string
): DbError {
  // ... (see errors.md for full implementation)
}
```

## Usage in Features

### Creating a Database Module

```typescript
// features/budget/server/db/budget-queries.ts
import "server-only";

import { FieldValue } from "firebase-admin/firestore";

import { db } from "~/lib/firebase";
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { createLogger } from "~/lib/logger";

import type {
  Budget,
  CreateBudgetDto,
  UpdateBudgetDto,
} from "../../types/budget";

// Constants
const COLLECTION = "budgets";
const RESOURCE = "Budget";

// Logger
const logger = createLogger({ module: "budget-db" });

// Transform function
function transformToBudget(
  docId: string,
  data: FirebaseFirestore.DocumentData
): Budget {
  return {
    id: docId,
    ...data,
    createdAt: data.createdAt?.toDate(),
    updatedAt: data.updatedAt?.toDate(),
  } as Budget;
}

// Query functions...
export async function getBudgetById(
  id: string
): Promise<[null, Budget] | [DbError, null]> {
  // ... implementation
}
```

## Firestore Settings

### Available Settings

```typescript
db.settings({
  // Ignore undefined properties when writing documents
  ignoreUndefinedProperties: true,

  // Prefer REST over gRPC (useful in some environments)
  preferRest: false,

  // Custom host for emulator
  host: process.env.FIRESTORE_EMULATOR_HOST,

  // SSL settings
  ssl: true,
});
```

### Using Firestore Emulator

```typescript
// lib/firebase/index.ts
import "server-only";

import { cert, getApps, initializeApp } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";

import { env } from "~/data/env/server";

function initializeFirebase() {
  if (getApps().length > 0) {
    return getApps()[0];
  }

  return initializeApp({
    credential: cert({
      projectId: env.FIREBASE_PROJECT_ID,
      clientEmail: env.FIREBASE_CLIENT_EMAIL,
      privateKey: env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, "\n"),
    }),
  });
}

const app = initializeFirebase();
export const db = getFirestore(app);

// Configure for emulator in development
if (process.env.FIRESTORE_EMULATOR_HOST) {
  db.settings({
    host: process.env.FIRESTORE_EMULATOR_HOST,
    ssl: false,
  });
}
```

## Index File Pattern

### Barrel Export

```typescript
// lib/firebase/index.ts
import "server-only";

// Re-export everything from single entry point
export { db } from "./client";
export { DbError, categorizeDbError } from "./errors";
export type {
  WithFirestoreTimestamps,
  WithDates,
  CreateDto,
  UpdateDto,
} from "./types";
```

### Usage

```typescript
// In feature modules
import { db, DbError, categorizeDbError } from "~/lib/firebase";
import type { WithDates, CreateDto } from "~/lib/firebase";
```

## Security Considerations

1. **Never expose credentials** - Keep in environment variables
2. **Use server-only** - Prevent client-side bundling
3. **Validate environment** - Use T3 Env or similar for validation
4. **Restrict service account** - Use minimal required permissions
5. **Rotate keys periodically** - Update service account keys regularly

## Troubleshooting

### Common Issues

**"Could not load the default credentials"**
- Check environment variables are set correctly
- Verify private key has correct format (with newlines)

**"Permission denied"**
- Verify service account has Firestore access
- Check Firestore security rules (if applicable)

**"Project not found"**
- Verify `FIREBASE_PROJECT_ID` matches Firebase project

**"Multiple app instances"**
- Ensure singleton pattern is used
- Check for multiple initializations in hot reload

### Debug Logging

```typescript
// Temporary debug logging
console.log("Firebase config:", {
  projectId: env.FIREBASE_PROJECT_ID,
  clientEmail: env.FIREBASE_CLIENT_EMAIL,
  privateKeyLength: env.FIREBASE_PRIVATE_KEY.length,
});
```
