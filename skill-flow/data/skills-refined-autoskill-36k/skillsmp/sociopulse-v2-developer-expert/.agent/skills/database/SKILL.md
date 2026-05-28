---
name: Database & Prisma Expert
description: Complete knowledge of the PostgreSQL schema, Prisma ORM patterns, indexes, and migration workflows.
---

# Database & Prisma Skill - SocioPulse V2

## Overview

The database uses **PostgreSQL 15+** with **Prisma ORM 5.x**. Schema contains 35+ tables with complex relationships and strategic indexing.

---

## 1. Core Models

### User (Central Model)

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

### Profile (Talent Data)

```prisma
model Profile {
  id        String @id @default(cuid())
  userId    String @unique
  user      User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  // Job & Compliance
  jobId              String?  // "IDE", "ES", "AS"
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

### ReliefMission (SOS)

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
  @@index([city, status])
  @@index([jobId, status]) // Critical for matching
}
```

---

## 2. Enums (Business Logic Locks)

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
  OPEN         // Available for applications
  ASSIGNED     // Talent assigned
  IN_PROGRESS  // Mission ongoing
  COMPLETED    // Finished
  CANCELLED
}

enum MissionUrgency {
  LOW          // < 1 week
  MEDIUM       // < 48h
  HIGH         // < 24h
  CRITICAL     // Immediate (Medical only)
}
```

---

## 3. Relationships

### One-to-One

```prisma
// User ↔ Profile (Talent)
user      User    @relation(fields: [userId], references: [id], onDelete: Cascade)

// User ↔ Establishment (Client)
user      User    @relation(fields: [userId], references: [id], onDelete: Cascade)
```

### One-to-Many

```prisma
// User (Client) → ReliefMissions
missionsAsClient ReliefMission[] @relation("ClientMissions")

// User (Talent) → ReliefMissions
missionsAsTalent ReliefMission[] @relation("TalentMissions")
```

### Many-to-Many

```prisma
// Talent ↔ TalentPools (Favoris)
model TalentPoolMember {
  talentPoolId String
  talentPool   TalentPool @relation(...)
  
  profileId    String
  profile      Profile    @relation(...)
  
  @@unique([talentPoolId, profileId])
}
```

---

## 4. Indexes (Performance Critical)

### Composite Indexes

```prisma
// Geo + status filter (most common query)
@@index([city, status])

// Job-based matching
@@index([jobId, status])

// Urgency filtering
@@index([status, urgencyLevel])
```

### Single Indexes

```prisma
// For WHERE clauses
@@index([email])
@@index([stripeAccountId])

// For ORDER BY
@@index([createdAt])
@@index([averageRating])
```

### Geospatial Queries

```prisma
// Haversine distance calculation
@@index([latitude, longitude])
```

---

## 5. Prisma Client Usage

### Basic Queries

```typescript
// Find unique
const user = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
  include: { profile: true },
});

// Find many with filters
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
// Nested include
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

// Haversine distance (raw SQL)
const nearbyTalents = await prisma.$queryRaw`
  SELECT *,
    ( 6371 * acos(
      cos(radians(${mission.latitude})) * cos(radians(latitude)) *
      cos(radians(longitude) - radians(${mission.longitude})) +
      sin(radians(${mission.latitude})) * sin(radians(latitude))
    )) AS distance
  FROM "Profile"
  WHERE latitude IS NOT NULL
  HAVING distance < ${mission.radiusKm}
  ORDER BY distance;
`;
```

---

## 6. Migrations

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

---

## 7. Seeding

### Seed Script

```typescript
// prisma/seed.ts
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

---

## 8. Best Practices

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

---

*This database architecture ensures data integrity, optimal performance, and scalability through strategic design and indexing.*
