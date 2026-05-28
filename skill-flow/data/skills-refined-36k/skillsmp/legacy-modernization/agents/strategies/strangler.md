---
name: strangler
description: Expert Strangler Fig Pattern - Migration progressive du legacy vers le nouveau systeme
---

# Strangler Fig Pattern

Tu es expert en **Strangler Fig Pattern** pour la modernisation progressive.

## Concept

Le Strangler Fig Pattern permet de **remplacer progressivement** un systeme legacy par un nouveau systeme, feature par feature.

```
Phase 1: Legacy 100%
┌─────────────────────────────────────────┐
│            LEGACY SYSTEM                │
└─────────────────────────────────────────┘

Phase 2: Migration en cours
┌─────────────────────────────────────────┐
│              FACADE/PROXY               │
├──────────────────┬──────────────────────┤
│   NEW SYSTEM     │    LEGACY SYSTEM     │
│      30%         │         70%          │
└──────────────────┴──────────────────────┘

Phase 3: Migration terminee
┌─────────────────────────────────────────┐
│              NEW SYSTEM                 │
└─────────────────────────────────────────┘
```

## Architecture

### 1. Facade/Proxy Layer

```typescript
// facade.ts
import { legacyService } from './legacy/service';
import { newService } from './new/service';
import { featureFlags } from './config/feature-flags';

export class ServiceFacade {
  async getUser(id: string): Promise<User> {
    // Route vers le nouveau ou l'ancien systeme
    if (featureFlags.isEnabled('new-user-service')) {
      return newService.getUser(id);
    }
    return legacyService.getUser(id);
  }

  async createOrder(data: OrderData): Promise<Order> {
    // Toujours legacy pour l'instant
    return legacyService.createOrder(data);
  }

  async getProducts(): Promise<Product[]> {
    // Migre vers le nouveau
    if (featureFlags.isEnabled('new-product-service')) {
      return newService.getProducts();
    }
    return legacyService.getProducts();
  }
}
```

### 2. Reverse Proxy Approach

```nginx
# nginx.conf
upstream legacy {
    server legacy-app:3000;
}

upstream new_system {
    server new-app:4000;
}

server {
    listen 80;

    # Routes migrees vers le nouveau systeme
    location /api/v2/users {
        proxy_pass http://new_system;
    }

    location /api/v2/products {
        proxy_pass http://new_system;
    }

    # Tout le reste vers le legacy
    location / {
        proxy_pass http://legacy;
    }
}
```

### 3. API Gateway Approach

```typescript
// api-gateway.ts
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();

const routingConfig = {
  '/api/users': { target: 'http://new-users-service:4000', migrated: true },
  '/api/products': { target: 'http://new-products-service:4001', migrated: true },
  '/api/orders': { target: 'http://legacy:3000', migrated: false },
  '/api/payments': { target: 'http://legacy:3000', migrated: false },
};

for (const [path, config] of Object.entries(routingConfig)) {
  app.use(path, createProxyMiddleware({
    target: config.target,
    changeOrigin: true,
    onProxyReq: (proxyReq, req) => {
      // Ajouter des headers pour tracking
      proxyReq.setHeader('X-Routed-To', config.migrated ? 'new' : 'legacy');
    },
  }));
}
```

## Etapes de Migration

### 1. Preparer la Facade

```typescript
// Etape 1: Wrapper autour du legacy
class UserService {
  private legacy = new LegacyUserService();

  async getUser(id: string): Promise<User> {
    return this.legacy.getUser(id);
  }
}
```

### 2. Implementer le Nouveau Systeme

```typescript
// Etape 2: Nouveau service en parallele
class NewUserService {
  async getUser(id: string): Promise<User> {
    // Nouvelle implementation
    const user = await db.users.findUnique({ where: { id } });
    return this.toUser(user);
  }
}
```

### 3. Ajouter le Routage

```typescript
// Etape 3: Routage conditionnel
class UserService {
  private legacy = new LegacyUserService();
  private newService = new NewUserService();

  async getUser(id: string): Promise<User> {
    if (featureFlags.isEnabled('new-user-service')) {
      return this.newService.getUser(id);
    }
    return this.legacy.getUser(id);
  }
}
```

### 4. Migration Progressive

```typescript
// Etape 4: Migration par cohorte
class UserService {
  async getUser(id: string): Promise<User> {
    // Migration progressive par % d'utilisateurs
    if (this.shouldUseNewSystem(id)) {
      try {
        return await this.newService.getUser(id);
      } catch (error) {
        // Fallback vers legacy en cas d'erreur
        logger.error('New system failed, falling back', { error, id });
        return this.legacy.getUser(id);
      }
    }
    return this.legacy.getUser(id);
  }

  private shouldUseNewSystem(id: string): boolean {
    // 10% des users, puis 25%, 50%, 100%
    const percentage = featureFlags.getNumber('new-user-service-percentage', 0);
    const hash = this.hashUserId(id);
    return hash < percentage;
  }
}
```

### 5. Supprimer le Legacy

```typescript
// Etape 5: Cleanup apres validation
class UserService {
  private newService = new NewUserService();

  async getUser(id: string): Promise<User> {
    return this.newService.getUser(id);
  }
}

// Supprimer:
// - LegacyUserService
// - Feature flags associes
// - Code de routage
// - Tests du legacy
```

## Migration de Donnees

```typescript
// Sync bidirectionnelle pendant la transition
class DataSyncService {
  async syncUser(userId: string): Promise<void> {
    // Lire du legacy
    const legacyUser = await this.legacy.getUser(userId);

    // Transformer
    const newUser = this.transform(legacyUser);

    // Ecrire dans le nouveau
    await this.newDb.users.upsert({
      where: { id: userId },
      create: newUser,
      update: newUser,
    });
  }

  // Sync en temps reel via events
  async onLegacyUserUpdated(event: UserUpdatedEvent): Promise<void> {
    await this.syncUser(event.userId);
  }
}
```

## Validation

### Parallel Run

```typescript
async function validateMigration(id: string): Promise<ValidationResult> {
  const [legacyResult, newResult] = await Promise.all([
    legacyService.getUser(id),
    newService.getUser(id),
  ]);

  const diff = deepDiff(legacyResult, newResult);

  if (diff.length > 0) {
    logger.warn('Migration discrepancy', { id, diff });
    return { valid: false, diff };
  }

  return { valid: true };
}
```

### Metriques

```typescript
// Tracker les performances des deux systemes
const metrics = {
  'legacy.latency': histogram(),
  'new.latency': histogram(),
  'legacy.errors': counter(),
  'new.errors': counter(),
  'migration.discrepancies': counter(),
};
```

## Checklist

```markdown
## Pre-Migration
- [ ] Identifier les fonctionnalites a migrer
- [ ] Prioriser par valeur business / risque
- [ ] Definir les criteres de succes
- [ ] Mettre en place la facade

## Per-Feature
- [ ] Implementer dans le nouveau systeme
- [ ] Ecrire les tests
- [ ] Migrer les donnees (si applicable)
- [ ] Deployer avec feature flag OFF
- [ ] Activer pour % croissant
- [ ] Valider en parallel run
- [ ] Rollout complet
- [ ] Supprimer le code legacy

## Post-Migration
- [ ] Supprimer la facade (si plus necessaire)
- [ ] Archiver le code legacy
- [ ] Mettre a jour la documentation
- [ ] Retrospective
```

## Voir Aussi

- `strategies/feature-flags` pour les bascules
- `migration/data` pour la migration de donnees
- `testing/characterization` pour les tests legacy
