---
name: database-prisma-expert
description: Use this skill when you need comprehensive knowledge of PostgreSQL and Prisma ORM, including schema design, migrations, and advanced querying techniques.
---

# Skill body

## Overview

This skill covers the use of **PostgreSQL 15+** and **Prisma ORM 5.x** for database management, including schema design, migrations, and advanced query patterns.

## Core Principles

1. **Single Source of Truth**: The `schema.prisma` file defines all models.
2. **Type Safety**: Use generated Prisma types everywhere. Never manually type DB responses.
3. **Migrations First**: Always use migrations, never direct SQL in production.

## Core Models

### User Model

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

### Profile Model

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

### Mission Model

```prisma
model Mission {
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

enum MissionStatus {
  OPEN         // Available for applications
  ASSIGNED     // Talent assigned
  IN_PROGRESS  // Mission ongoing
  COMPLETED    // Finished
  CANCELLED
}
```

## Commands

```bash
# Generate Prisma client (after schema change)
pnpm db:generate

# Create and apply migration
pnpm db:migrate --name describe_change

# Push changes (prototyping only, no migration)
pnpm db:push

# Open Prisma Studio
pnpm db:studio

# Seed database
pnpm db:seed
```

## Transactions

**ALWAYS** use transactions for multi-step operations:

```typescript
await prisma.$transaction(async (tx) => {
  const mission = await tx.mission.create({ data: missionData });
  await tx.notification.create({ 
    data: { userId: mission.userId, type: 'MISSION_CREATED' } 
  });
  return mission;
});
```

## Best Practices

- Use explicit relation names for clarity.
- Implement soft deletes by adding a `deletedAt` field to models.
- Always use migrations for production changes to ensure consistency.

```prisma
model User {
  deletedAt DateTime?
}
```