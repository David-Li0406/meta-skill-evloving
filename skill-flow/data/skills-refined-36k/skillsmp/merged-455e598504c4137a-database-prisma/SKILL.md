---
name: database-prisma
description: Use this skill for managing PostgreSQL databases with Prisma ORM, including schema design, migrations, seeding, and advanced query patterns.
---

# Database & Prisma

## Overview

This skill covers the use of **PostgreSQL 15+** with **Prisma ORM 5.x**. It includes schema design, migrations, seeding, and advanced query patterns.

## Core Principles

1. **Single Source of Truth**: The `schema.prisma` file defines all models.
2. **Type Safety**: Use generated Prisma types everywhere. Never manually type DB responses.
3. **Migrations First**: Always use migrations, never direct SQL in production.

## Schema Location

```
packages/database/
├── prisma/
│   ├── schema.prisma    # Main schema
│   ├── migrations/      # Version-controlled migrations
│   └── seed.ts          # Development seeding
├── src/
│   └── index.ts         # Re-exports prisma client
└── package.json
```

## Core Models

### User

```prisma
model User {
  id            String     @id @default(cuid())
  email         String     @unique
  role          UserRole   @default(CLIENT)
  status        UserStatus @default(PENDING)
  
  // Stripe Connect
  stripeAccountId String? @unique
  stripeOnboarded Boolean @default(false)
  
  // Relations
  profile       Profile?
  establishment Establishment?
  
  @@index([email])
  @@index([role, status]) // Composite for fast filtering
}
```

### Profile

```prisma
model Profile {
  id        String @id @default(cuid())
  userId    String @unique
  user      User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  // Job & Compliance
  jobId              String?  
  complianceStatus   ComplianceStatus @default(PENDING)
  adeliNumber        String?
  
  // Geo matching
  latitude  Float?
  longitude Float?
  radiusKm  Int @default(30)
  
  @@index([jobId])
  @@index([complianceStatus])
  @@index([latitude, longitude]) // For Haversine queries
}
```

### ReliefMission

```prisma
model ReliefMission {
  id              String @id @default(cuid())
  clientId        String
  assignedTalentId String?
  
  // Job matching
  jobId           String?
  specialtiesTags String[] @default([])
  urgencyLevel    MissionUrgency @default(MEDIUM)
  
  // Constraints
  requiresCar     Boolean @default(false)
  requiresNight   Boolean @default(false)
  requiresDiploma Boolean @default(true)
  
  status          MissionStatus @default(OPEN)
  
  @@index([status, urgencyLevel])
  @@index([jobId, status]) // Critical for matching
}
```

## Enums

### User & Role Enums

```prisma
enum UserRole {
  CLIENT
  TALENT
  ADMIN
}

enum UserStatus {
  PENDING
  VERIFIED
  SUSPENDED
  BANNED
}

enum ComplianceStatus {
  PENDING
  SUBMITTED
  VALIDATED
  REJECTED
  EXPIRED
}
```

### Mission Enums

```prisma
enum MissionStatus {
  OPEN
  ASSIGNED
  IN_PROGRESS
  COMPLETED
  CANCELLED
}

enum MissionUrgency {
  LOW
  MEDIUM
  HIGH
  CRITICAL
}
```

## Relationships

### One-to-One

```prisma
// User ↔ Profile (Talent)
user      User    @relation(fields: [userId], references: [id], onDelete: Cascade)
```

### One-to-Many

```prisma
// User (Client) → ReliefMissions
missionsAsClient ReliefMission[] @relation("ClientMissions")
```

### Many-to-Many

```prisma
model TalentPoolMember {
  talentPoolId String
  talentPool   TalentPool @relation(...)
  
  profileId    String
  profile      Profile    @relation(...)
  
  @@unique([talentPoolId, profileId])
}
```

## Indexes

### Composite Indexes

```prisma
@@index([city, status])
@@index([jobId, status])
@@index([status, urgencyLevel])
```

### Single Indexes

```prisma
@@index([email])
@@index([stripeAccountId])
@@index([createdAt])
@@index([averageRating])
```

## Prisma Client Usage

### Basic Queries

```typescript
const user = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
  include: { profile: true },
});

const missions = await prisma.reliefMission.findMany({
  where: {
    status: 'OPEN',
    city: 'Paris',
  },
  orderBy: { createdAt: 'desc' },
  take: 10,
});
```

### Complex Queries

```typescript
const mission = await prisma.reliefMission.findUnique({
  where: { id },
  include: {
    client: {
      include: { establishment: true },
    },
    assignedTalent: {
      include: { profile: true },
    },
    applications: {
      include: { talent: { include: { profile: true } } },
    },
  },
});
```

## Migrations

### Create Migration

```bash
npx prisma migrate dev --name add_specialty_tags
```

### Apply to Production

```bash
npx prisma migrate deploy
```

### Reset Database (Dev)

```bash
npx prisma migrate reset
```

## Seeding

### Seed Script

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  await prisma.user.create({
    data: {
      email: 'admin@sociopulse.fr',
      role: 'ADMIN',
      status: 'VERIFIED',
    },
  });
}

main()
  .catch((e) => console.error(e))
  .finally(() => prisma.$disconnect());
```

### Run Seed

```bash
npx prisma db seed
```

## Best Practices

### DO

✅ Use `select` to avoid over-fetching  
✅ Use `include` strategically (N+1 prevention)  
✅ Add indexes for frequent WHERE/ORDER BY  
✅ Use transactions for multi-step operations  
✅ Validate BEFORE database insert

### DON'T

❌ Use `findMany` without `take` limit  
❌ Forget `onDelete: Cascade` for cleanup  
❌ Create indexes on every field (overhead)  
❌ Use raw SQL when Prisma can do it  
❌ Skip migrations (direct schema push in prod)

*This database architecture ensures data integrity, optimal performance, and scalability through strategic design and indexing.*