---
name: Drizzle ORM Management
description: Comprehensive management of the database using Drizzle ORM, emphasizing enterprise-level data access patterns, transactions, and synchronization.
---

# Drizzle ORM Management Skill

This skill governs all database interactions within the golf league application. It ensures data integrity, performance, and a clear separation of concerns through an enterprise-level architecture.

## Architecture Guidelines

To maintain scalability and testability, all data access MUST follow this three-tier architecture:

### 1. Repository Layer (`src/db/repositories/`)
- **Responsibility**: Pure database interaction (Select, Insert, Update, Delete).
- **Rules**:
    - No business logic.
    - Export granular, reusable query functions.
    - Handle Drizzle-specific logic (joins, filters, etc.).
    - Example: `getRoundWithMatches(roundId: string)`

### 2. Service Layer (`src/lib/services/`)
- **Responsibility**: Business logic and domain rules.
- **Rules**:
    - Coordinate multiple repository calls.
    - Ensure data consistency (e.g., updating a score must trigger a handicap recalculation).
    - Use transactions for atomic operations.
    - State-independent (stateless).
    - Example: `completeRound(roundId: string)`

### 3. Action Layer (`src/actions/`)
- **Responsibility**: Triggering services from the UI.
- **Rules**:
    - Manage Server Action state (loading, error, success).
    - Handle revalidation (e.g., `revalidatePath`).
    - Authenticate and authorize the request.

## Data Synchronization Patterns

### Transactional Atomicity
Always wrap operations that affect multiple tables in `db.transaction`. If any part fails, the entire operation must roll back.

```typescript
await db.transaction(async (tx) => {
  await tx.insert(scores).values(...);
  await updatePlayerHandicap(userId, orgId, tx); // Pass the transaction object!
});
```

### Round Simulation
To keep the system in sync during development or testing, use the `SimulationService`. It must:
1.  **Assign default tees** to any players missing them (required for score generation).
2.  Assign random but realistic scores (based on player handicap).
3.  Apply Net Double Bogey adjustments.
4.  Calculate Match results.
5.  Update Player Handicaps for the league.

## Common Operations

### Adding Data
- Always use the Repository to insert.
- Ensure all required fields are populated according to the schema.

### Deleting Data
- Use soft deletes where appropriate (adding a `deletedAt` column) or implement cascade rules in the schema.
- Default to strict cascading for junction tables like `match_players` or `scores`.

## Environment & Hoisting
When running scripts with `npx tsx`, static imports (e.g., `import { db } from "@/db"`) are hoisted above configuration calls like `dotenv.config()`. To ensure the database connection correctly picks up the environment variables from `.env.local`, all scripts MUST follow this pattern:

1.  Import and configure `dotenv` with `override: true`.
2.  Use dynamic `import()` for any file that depends on the database connection.

```typescript
import { config } from 'dotenv';
config({ path: '.env.local', override: true });

async function run() {
    // Dynamically import AFTER config
    const { db } = await import("@/db");
    const { simulationService } = await import("@/lib/services/simulation.service");
    
    // ... logic
}
run();
```

## CLI Tools

### Round Simulation
To simulate a round and sync handicaps, run:
```bash
npx tsx skills/drizzle/scripts/simulate.ts <roundId>
```

### Reset Scores
To delete ALL scores and reset ALL rounds to 'scheduled':
```bash
npx tsx skills/drizzle/scripts/clear-scores.ts
```

## Verification
- Every repository function should have a corresponding test in `__tests__/repositories/`.
- Every service should have an integration test in `__tests__/services/`.
