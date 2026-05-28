---
name: data-migration
description: Expert migration de donnees - ETL, validation, sync continue
---

# Data Migration

Tu es expert en **migration de donnees** entre systemes.

## Principes Fondamentaux

1. **Zero data loss** : Aucune perte de donnees
2. **Validation** : Verifier avant/apres
3. **Rollback** : Toujours pouvoir revenir
4. **Incremental** : Migrer par batches

## Strategies

### 1. Big Bang Migration

```
┌─────────┐  Downtime  ┌─────────┐
│  OLD    │──────────▶│   NEW   │
│   DB    │  Extract  │   DB    │
└─────────┘  Transform └─────────┘
             Load
```

**Quand** : Petit volume, downtime acceptable
**Risque** : Eleve

### 2. Parallel Run

```
┌─────────┐           ┌─────────┐
│  OLD    │◀────────▶│   NEW   │
│   DB    │   Sync    │   DB    │
└─────────┘           └─────────┘
     │                     │
     └──────── App ────────┘
```

**Quand** : Migration critique, zero downtime
**Risque** : Faible

### 3. CDC (Change Data Capture)

```
┌─────────┐  Initial   ┌─────────┐
│  OLD    │───Load────▶│   NEW   │
│   DB    │            │   DB    │
└────┬────┘            └────▲────┘
     │                      │
     └──── CDC Stream ──────┘
          (Debezium)
```

**Quand** : Gros volumes, sync continue
**Risque** : Faible

## Implementation ETL

### Extract

```typescript
// extract.ts
import { Pool } from 'pg';

const legacyDb = new Pool({ connectionString: LEGACY_DB_URL });

async function* extractUsers(batchSize: number = 1000) {
  let offset = 0;
  let hasMore = true;

  while (hasMore) {
    const { rows } = await legacyDb.query(`
      SELECT id, name, email, created_at, metadata
      FROM users
      ORDER BY id
      LIMIT $1 OFFSET $2
    `, [batchSize, offset]);

    if (rows.length === 0) {
      hasMore = false;
    } else {
      yield rows;
      offset += batchSize;
      console.log(`Extracted ${offset} users...`);
    }
  }
}
```

### Transform

```typescript
// transform.ts
interface LegacyUser {
  id: number;
  name: string;
  email: string;
  created_at: Date;
  metadata: string; // JSON string
}

interface NewUser {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  createdAt: Date;
  settings: UserSettings;
}

function transformUser(legacy: LegacyUser): NewUser {
  const [firstName, ...lastNameParts] = legacy.name.split(' ');
  const lastName = lastNameParts.join(' ') || '';

  // Safe JSON parsing avec fallback
  let metadata: Record<string, unknown> = {};
  if (legacy.metadata) {
    try {
      metadata = JSON.parse(legacy.metadata);
    } catch (error) {
      logger.warn('Invalid metadata JSON', { userId: legacy.id });
      // Continue avec metadata vide plutot que fail
    }
  }

  return {
    id: `user_${legacy.id}`,
    firstName,
    lastName,
    email: legacy.email.toLowerCase(),
    createdAt: legacy.created_at,
    settings: {
      theme: typeof metadata.theme === 'string' ? metadata.theme : 'light',
      notifications: typeof metadata.notifications === 'boolean' ? metadata.notifications : true,
    },
  };
}
```

### Load

```typescript
// load.ts
import { PrismaClient } from '@prisma/client';

const newDb = new PrismaClient();

async function loadUsers(users: NewUser[]): Promise<LoadResult> {
  // Transaction pour garantir l'atomicite du batch
  return await newDb.$transaction(async (tx) => {
    const result = await tx.user.createMany({
      data: users,
      skipDuplicates: true,
    });

    // Verifier que le batch est complet
    if (result.count < users.length * 0.95) {
      // Moins de 95% inseres = probleme potentiel
      logger.warn('Batch incomplete', {
        expected: users.length,
        inserted: result.count,
      });
    }

    return { inserted: result.count, skipped: users.length - result.count };
  }, {
    timeout: 30_000, // 30s timeout par batch
    isolationLevel: 'ReadCommitted',
  });
}
```

### Pipeline Complet

```typescript
// migrate.ts
import { z } from 'zod';
import pLimit from 'p-limit';

// Configuration avec validation
const MigrationConfigSchema = z.object({
  batchSize: z.number().int().min(100).max(10000).default(1000),
  concurrency: z.number().int().min(1).max(10).default(3),
  retryAttempts: z.number().int().min(0).max(5).default(3),
});

type MigrationConfig = z.infer<typeof MigrationConfigSchema>;

// Constantes de retention (pas de magic numbers)
const RETENTION_POLICIES = {
  ACTIVITY_LOGS_DAYS: parseInt(process.env.RETENTION_ACTIVITY_LOGS || '365'),
  MARKETING_CONSENT_DAYS: parseInt(process.env.RETENTION_MARKETING || '730'),
} as const;

/**
 * Migration avec parallelisation controlee
 *
 * QUAND utiliser parallel vs sequential:
 * - PARALLEL: Batches independants, pas de contraintes d'ordre
 * - SEQUENTIAL: Foreign keys, ordre chronologique requis
 */
async function migrateUsers(config?: Partial<MigrationConfig>): Promise<MigrationResult> {
  const { batchSize, concurrency, retryAttempts } = MigrationConfigSchema.parse(config ?? {});

  const stats = {
    extracted: 0,
    transformed: 0,
    loaded: 0,
    errors: 0,
  };

  // Limiter la concurrence pour eviter de surcharger la DB
  const limit = pLimit(concurrency);
  const pendingBatches: Promise<void>[] = [];

  // AbortController pour cancel propre en cas d'erreur critique
  const abortController = new AbortController();
  let criticalError: Error | null = null;

  try {
    for await (const batch of extractUsers(batchSize)) {
      // Check si abort demande par un batch precedent
      if (abortController.signal.aborted) {
        logger.warn('Migration aborted, skipping remaining batches');
        break;
      }

      stats.extracted += batch.length;

      // Traitement parallele des batches avec error isolation
      const batchPromise = limit(async () => {
        const transformed = batch
          .map((user) => {
            try {
              return transformUser(user);
            } catch (error: unknown) {
              stats.errors++;
              const message = error instanceof Error ? error.message : 'Unknown error';
              logger.error('Transform error', { userId: user.id, error: message });
              return null;
            }
          })
          .filter((u): u is NewUser => u !== null);

        stats.transformed += transformed.length;

        // Retry avec backoff exponentiel + jitter
        await retryWithBackoff(
          () => loadUsers(transformed),
          retryAttempts
        );
        stats.loaded += transformed.length;
      });

      pendingBatches.push(batchPromise);
    }

    // Attendre tous les batches avec Promise.allSettled pour isoler les erreurs
    const results = await Promise.allSettled(pendingBatches);

    // Analyser les resultats
    const failures = results.filter(
      (r): r is PromiseRejectedResult => r.status === 'rejected'
    );

    if (failures.length > 0) {
      const failureReasons = failures.map(f => f.reason?.message || 'Unknown');
      logger.error('Some batches failed', { count: failures.length, reasons: failureReasons });

      // Decider si c'est un echec total (>10% failed)
      if (failures.length / results.length > 0.1) {
        return { success: false, stats, error: `${failures.length} batches failed` };
      }
    }

    return { success: true, stats };
  } catch (error: unknown) {
    abortController.abort();
    const message = error instanceof Error ? error.message : 'Unknown error';
    return { success: false, stats, error: message };
  }
}

// Helper pour retry avec backoff exponentiel + jitter
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxAttempts: number,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error: unknown) {
      if (attempt === maxAttempts) throw error;

      // Exponential backoff avec jitter (±25%) pour eviter thundering herd
      const exponentialDelay = baseDelay * Math.pow(2, attempt - 1);
      const jitter = exponentialDelay * 0.25 * (Math.random() * 2 - 1);
      const delay = Math.min(exponentialDelay + jitter, 30_000); // Cap a 30s

      logger.debug('Retry scheduled', { attempt, delay, maxAttempts });
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
  throw new Error('Unreachable');
}
```

### Migration Sequentielle (quand necessaire)

```typescript
// Utiliser quand l'ordre est important (FK, timestamps)
async function migrateSequential(): Promise<MigrationResult> {
  for await (const batch of extractUsers(1000)) {
    // ⚠️ Sequential: chaque batch attend le precedent
    await processBatch(batch);
  }
}
```

## Validation

### Pre-Migration

```typescript
async function preMigrationChecks(): Promise<CheckResult[]> {
  return [
    await checkSourceConnectivity(),
    await checkTargetConnectivity(),
    await checkDiskSpace(),
    await checkRowCounts(),
    await checkDataIntegrity(),
  ];
}
```

### Post-Migration

```typescript
async function validateMigration(): Promise<ValidationResult> {
  const checks = [];

  // 1. Row counts
  const sourceCount = await legacyDb.query('SELECT COUNT(*) FROM users');
  const targetCount = await newDb.user.count();

  checks.push({
    name: 'row_count',
    source: sourceCount.rows[0].count,
    target: targetCount,
    match: sourceCount.rows[0].count === targetCount,
  });

  // 2. Sample validation
  const sampleIds = await getSampleIds(100);
  for (const id of sampleIds) {
    const sourceUser = await legacyDb.query('SELECT * FROM users WHERE id = $1', [id]);
    const targetUser = await newDb.user.findUnique({ where: { id: `user_${id}` } });

    const transformed = transformUser(sourceUser.rows[0]);
    const match = deepEqual(transformed, targetUser);

    if (!match) {
      checks.push({
        name: `sample_${id}`,
        match: false,
        diff: deepDiff(transformed, targetUser),
      });
    }
  }

  // 3. Checksum
  const sourceChecksum = await calculateChecksum(legacyDb, 'users');
  const targetChecksum = await calculateChecksum(newDb, 'user');

  checks.push({
    name: 'checksum',
    match: sourceChecksum === targetChecksum,
  });

  return {
    valid: checks.every((c) => c.match),
    checks,
  };
}
```

## CDC avec Debezium

```yaml
# docker-compose.yml
services:
  debezium:
    image: debezium/connect:2.4
    environment:
      BOOTSTRAP_SERVERS: kafka:9092
      GROUP_ID: debezium-connect
      CONFIG_STORAGE_TOPIC: debezium_connect_configs
      OFFSET_STORAGE_TOPIC: debezium_connect_offsets

  # Configuration du connector
  # POST /connectors
  # {
  #   "name": "legacy-users-connector",
  #   "config": {
  #     "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
  #     "database.hostname": "legacy-db",
  #     "database.port": "5432",
  #     "database.user": "replicator",
  #     "database.password": "***",
  #     "database.dbname": "legacy",
  #     "table.include.list": "public.users",
  #     "topic.prefix": "legacy"
  #   }
  # }
```

```typescript
// cdc-consumer.ts
import { Kafka } from 'kafkajs';

const kafka = new Kafka({ brokers: ['kafka:9092'] });
const consumer = kafka.consumer({ groupId: 'migration-consumer' });

await consumer.subscribe({ topic: 'legacy.public.users' });

await consumer.run({
  eachMessage: async ({ message }) => {
    // Safe JSON parsing
    let payload: DebeziumPayload;
    try {
      payload = JSON.parse(message.value?.toString() || '{}');
    } catch (error) {
      logger.error('Invalid CDC message', { offset: message.offset });
      return; // Skip malformed message
    }

    if (payload.op === 'c' || payload.op === 'u') {
      // Create or Update
      const newUser = transformUser(payload.after);
      await newDb.user.upsert({
        where: { id: newUser.id },
        create: newUser,
        update: newUser,
      });
    } else if (payload.op === 'd') {
      // Delete
      await newDb.user.delete({
        where: { id: `user_${payload.before.id}` },
      });
    }
  },
});
```

## Rollback

```typescript
// rollback.ts
async function rollbackMigration(migrationId: string): Promise<void> {
  // 1. Arreter les writes vers la nouvelle DB
  await featureFlags.disable('use-new-db');

  // 2. Restaurer le backup pre-migration
  await restoreBackup(migrationId);

  // 3. Verifier l'integrite
  await validateSourceData();

  // 4. Notifier
  await notify.send('Migration rolled back', { migrationId });
}
```

## Checklist

```markdown
## Pre-Migration
- [ ] Backup de la source
- [ ] Backup de la cible
- [ ] Tester en staging
- [ ] Plan de rollback documente
- [ ] Fenetres de maintenance planifiee
- [ ] Communication aux stakeholders

## Migration
- [ ] Desactiver les writes (si necessaire)
- [ ] Executer ETL
- [ ] Valider row counts
- [ ] Valider samples
- [ ] Valider checksums

## Post-Migration
- [ ] Activer le nouveau systeme
- [ ] Monitorer les erreurs
- [ ] Valider avec les utilisateurs
- [ ] Archiver les logs de migration
- [ ] Documenter les decisions
```

## Voir Aussi

- `migration/sync` pour sync continue
- `migration/rollback` pour strategies de retour
- `testing/regression` pour tests post-migration
