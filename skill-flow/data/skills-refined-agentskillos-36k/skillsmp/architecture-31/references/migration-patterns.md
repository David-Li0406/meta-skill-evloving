# Migration Patterns

Strategies for safely restructuring code without big-bang rewrites.

## Core Philosophy

**Never rewrite from scratch.** Large rewrites fail because:
- You lose institutional knowledge embedded in the old code
- Bugs get reintroduced that were fixed long ago
- Business can't pause while you rebuild
- Scope creep makes completion uncertain

Instead, migrate incrementally. The system stays working throughout.

---

## Strangler Fig Pattern

Gradually replace an old system by building a new one around it, redirecting traffic piece by piece until the old system can be removed.

### How It Works

```
Phase 1: New system intercepts, delegates to old
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│ Request │ ──▶ │ New Facade  │ ──▶ │ Old System  │
└─────────┘     └─────────────┘     └─────────────┘

Phase 2: New system handles some routes
┌─────────┐     ┌─────────────┐     
│ Request │ ──▶ │ New System  │ (route A, B)
└─────────┘     └──────┬──────┘     
                       ▼
               ┌─────────────┐
               │ Old System  │ (route C, D)
               └─────────────┘

Phase 3: Old system removed
┌─────────┐     ┌─────────────┐
│ Request │ ──▶ │ New System  │ (all routes)
└─────────┘     └─────────────┘
```

### Implementation Steps

1. **Create facade:** New entry point that initially just proxies to old system
2. **Identify seams:** Find natural boundaries in the old system
3. **Migrate incrementally:** Move one feature/route at a time to new implementation
4. **Verify parity:** Test that new implementation matches old behavior
5. **Cut over:** Redirect traffic to new implementation
6. **Remove old code:** Once all traffic migrated and stable

### Example: API Migration

```typescript
// Phase 1: Facade proxies everything
class UserApiV2 {
  constructor(private legacyApi: UserApiV1) {}
  
  async getUser(id: string) {
    // Just delegate to old system initially
    return this.legacyApi.getUser(id);
  }
}

// Phase 2: New implementation for some endpoints
class UserApiV2 {
  constructor(
    private legacyApi: UserApiV1,
    private newUserService: NewUserService
  ) {}
  
  async getUser(id: string) {
    // New implementation
    return this.newUserService.findById(id);
  }
  
  async updateUser(id: string, data: UpdateData) {
    // Still delegates to old
    return this.legacyApi.updateUser(id, data);
  }
}

// Phase 3: All endpoints migrated, remove legacy dependency
class UserApiV2 {
  constructor(private userService: NewUserService) {}
  
  async getUser(id: string) {
    return this.userService.findById(id);
  }
  
  async updateUser(id: string, data: UpdateData) {
    return this.userService.update(id, data);
  }
}
```

---

## Branch by Abstraction

Introduce an abstraction layer that allows switching between old and new implementations.

### How It Works

```
Step 1: Introduce abstraction over old code
┌──────────────┐
│  Client Code │
└──────┬───────┘
       ▼
┌──────────────┐     ┌──────────────┐
│  Interface   │ ──▶ │ Old Impl     │
└──────────────┘     └──────────────┘

Step 2: Add new implementation behind same interface
┌──────────────┐
│  Client Code │
└──────┬───────┘
       ▼
┌──────────────┐     ┌──────────────┐
│  Interface   │ ──▶ │ Old Impl     │ (default)
└──────────────┘     └──────────────┘
                     ┌──────────────┐
                     │ New Impl     │ (feature flag)
                     └──────────────┘

Step 3: Switch default to new, keep old as fallback
Step 4: Remove old implementation
```

### Implementation Example

```typescript
// Step 1: Extract interface from existing code
interface PaymentProcessor {
  charge(amount: number, card: CardInfo): Promise<ChargeResult>;
  refund(chargeId: string): Promise<RefundResult>;
}

// Old implementation (existing code)
class StripePaymentProcessor implements PaymentProcessor {
  async charge(amount: number, card: CardInfo) {
    // Existing Stripe implementation
  }
  async refund(chargeId: string) {
    // Existing Stripe implementation  
  }
}

// Step 2: Create new implementation
class NewPaymentProcessor implements PaymentProcessor {
  async charge(amount: number, card: CardInfo) {
    // New, improved implementation
  }
  async refund(chargeId: string) {
    // New implementation
  }
}

// Step 3: Feature flag to switch
function getPaymentProcessor(): PaymentProcessor {
  if (featureFlags.useNewPaymentProcessor) {
    return new NewPaymentProcessor();
  }
  return new StripePaymentProcessor();
}
```

---

## Parallel Implementations

Run both old and new code simultaneously, compare results, but only use old results.

### Use Cases

- High-risk changes where correctness is critical
- When you can't easily test equivalence
- Financial calculations, security logic

### How It Works

```typescript
async function processOrder(order: Order): Promise<Result> {
  // Run both implementations
  const [oldResult, newResult] = await Promise.all([
    oldProcessor.process(order),
    newProcessor.process(order).catch(e => ({ error: e }))
  ]);
  
  // Compare results (async, don't block)
  compareResults(oldResult, newResult, order).catch(logDiscrepancy);
  
  // Return old result (safe)
  return oldResult;
}

async function compareResults(old: Result, new: Result, context: any) {
  if (!deepEqual(old, new)) {
    await alerting.send({
      type: 'result_mismatch',
      old,
      new, 
      context,
      timestamp: new Date()
    });
  }
}
```

### Progression

1. **Shadow mode:** New code runs, results compared, old results used
2. **Verification mode:** After N comparisons match, start using new results
3. **Cutover:** Remove old code once confident

---

## Feature Flags for Migration

Control rollout granularity with feature flags.

### Flag Strategies

| Strategy | Use When | Example |
|----------|----------|---------|
| Boolean | All or nothing | `useNewCheckout: true` |
| Percentage | Gradual rollout | `newCheckoutPercent: 10` |
| User segment | Test with specific users | `newCheckoutUsers: ['beta-testers']` |
| Request attribute | Route-specific | `newCheckoutForMobile: true` |

### Implementation Pattern

```typescript
class FeatureFlags {
  async isEnabled(flag: string, context: FlagContext): Promise<boolean> {
    const config = await this.getConfig(flag);
    
    if (config.type === 'boolean') {
      return config.enabled;
    }
    
    if (config.type === 'percentage') {
      // Consistent hashing so same user always gets same result
      const hash = this.hash(context.userId + flag);
      return hash % 100 < config.percentage;
    }
    
    if (config.type === 'segment') {
      return config.segments.includes(context.userSegment);
    }
    
    return false;
  }
}

// Usage
async function checkout(cart: Cart, user: User) {
  if (await flags.isEnabled('new-checkout', { userId: user.id })) {
    return newCheckout(cart, user);
  }
  return legacyCheckout(cart, user);
}
```

---

## Data Migration

### Dual-Write Pattern

Write to both old and new data stores during migration.

```typescript
class UserRepository {
  constructor(
    private legacyDb: LegacyDatabase,
    private newDb: NewDatabase,
    private migrationMode: 'legacy' | 'dual-write' | 'new'
  ) {}
  
  async save(user: User) {
    switch (this.migrationMode) {
      case 'legacy':
        return this.legacyDb.save(user);
        
      case 'dual-write':
        // Write to both, read from legacy
        await Promise.all([
          this.legacyDb.save(user),
          this.newDb.save(user)
        ]);
        return;
        
      case 'new':
        return this.newDb.save(user);
    }
  }
  
  async find(id: string) {
    // Always read from source of truth for current mode
    if (this.migrationMode === 'new') {
      return this.newDb.find(id);
    }
    return this.legacyDb.find(id);
  }
}
```

### Migration Phases

1. **Dual-write:** Write to both, read from old
2. **Backfill:** Migrate historical data to new store
3. **Verify:** Compare data in both stores
4. **Switch read:** Read from new, still write to both
5. **Stop dual-write:** Write only to new
6. **Decommission:** Remove old store

---

## Rollback Planning

Every migration needs a rollback plan.

### Rollback Checklist

- [ ] Can we revert the code change quickly?
- [ ] Will data written during migration be compatible with old code?
- [ ] Do we have feature flags to disable new behavior?
- [ ] Have we tested the rollback procedure?
- [ ] What's the maximum safe time in new state before rollback becomes risky?

### Rollback Strategy Template

```markdown
## Rollback Plan: [Migration Name]

### Trigger Conditions
- Error rate > X%
- Latency p99 > Y ms
- Business metric drops > Z%

### Rollback Steps
1. Disable feature flag `new-feature-enabled`
2. Verify traffic shifted to old path (check metrics)
3. If data migration was in progress: [specific steps]

### Point of No Return
After [condition], rollback is not possible because [reason].
Mitigation: [forward-fix strategy]

### Contacts
- On-call: @team-oncall
- Migration owner: @engineer
```

---

## Anti-Patterns

### Big Bang Rewrite

"We'll just rewrite it from scratch, it'll be cleaner."

**Why it fails:**
- Underestimated scope
- Lost bug fixes and edge case handling
- Team context switching
- No incremental value delivery

### Incomplete Migrations

Starting a migration but never finishing. Now you have two systems to maintain.

**Prevention:**
- Timebox migrations
- Track migration debt
- Prioritize completion over starting new migrations

### Testing Only the Happy Path

New implementation works for common cases but fails on edge cases the old code handles.

**Prevention:**
- Characterization tests before starting
- Parallel running to catch discrepancies
- Gradual rollout with monitoring
