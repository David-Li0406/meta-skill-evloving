---
name: proxy-pattern-typescript
description: Same-interface substitution for lifecycle control (lazy init/close/retry) and cross-cutting concerns (caching/logging/auth) in TS/Node, with trade-offs vs Decorator/Adapter/Facade.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Proxy (TypeScript)

## Intent

Provide a drop-in stand-in that implements the same interface as the real service while controlling access, lifecycle, or cross-cutting behavior.

## When to use

- You need a drop-in stand-in that preserves the same interface.
- Lazy init is required for an expensive or remote service.
- You want caching or logging without changing clients.
- Access control should be enforced at the boundary.
- Lifecycle (connect/close/retry) must be centralized.
- The real service is remote or flaky and needs shielding.
- You want to swap proxy vs real at wiring time.

## When NOT to use

- You need a different interface (Adapter).
- You need a simplified subsystem API (Facade).
- The client wants explicit behavior stacking (Decorator).
- The indirection adds no value.
- The proxy would own business logic.
- Performance overhead is unacceptable.
- The service is simple and local.

## Mental model

Proxy = same interface + indirection point; clients stay unaware.

## Recommended TS shapes

- Interface + RealService + Proxy class (preferred).
- Factory/wiring function to choose proxy vs real.
- Async init with cached Promise for concurrency safety.

## Example 1: Virtual proxy (lazy init)

```ts
interface ProfileService {
  getProfile(id: string): Promise<{ id: string; name: string }>;
}

class RealProfileService implements ProfileService {
  constructor(private readonly baseUrl: string) {}
  async getProfile(id: string): Promise<{ id: string; name: string }> {
    return { id, name: `user-${id}` };
  }
}

class ProfileServiceProxy implements ProfileService {
  private servicePromise: Promise<RealProfileService> | null = null;

  constructor(private readonly baseUrl: string) {}

  private async getService(): Promise<RealProfileService> {
    if (!this.servicePromise) {
      this.servicePromise = Promise.resolve(new RealProfileService(this.baseUrl));
    }
    return this.servicePromise;
  }

  async getProfile(id: string) {
    const svc = await this.getService();
    return svc.getProfile(id);
  }
}

const svc: ProfileService = new ProfileServiceProxy("https://api.example.com");
await svc.getProfile("123");
```

## Example 2: Caching proxy with TTL

```ts
interface Repo {
  get(id: string): Promise<string | null>;
}

class InMemoryRepo implements Repo {
  private data = new Map<string, string>([["a", "1"]]);
  async get(id: string): Promise<string | null> {
    return this.data.get(id) ?? null;
  }
}

type CacheEntry = { value: string | null; expiresAt: number };

class CachingRepoProxy implements Repo {
  private cache = new Map<string, CacheEntry>();

  constructor(private readonly inner: Repo, private readonly ttlMs: number) {}

  async get(id: string): Promise<string | null> {
    const now = Date.now();
    const cached = this.cache.get(id);
    if (cached && cached.expiresAt > now) return cached.value;
    const value = await this.inner.get(id);
    this.cache.set(id, { value, expiresAt: now + this.ttlMs });
    return value;
  }

  invalidate(id: string): void {
    this.cache.delete(id);
  }
}

const repo: Repo = new CachingRepoProxy(new InMemoryRepo(), 1000);
await repo.get("a");
```

## Example 3: Protection + logging proxy

```ts
interface BillingService {
  charge(userId: string, amountCents: number): Promise<boolean>;
}

class RealBillingService implements BillingService {
  async charge(userId: string, amountCents: number): Promise<boolean> {
    return amountCents > 0;
  }
}

class BillingProxy implements BillingService {
  constructor(private readonly inner: BillingService, private readonly token: string) {}

  async charge(userId: string, amountCents: number): Promise<boolean> {
    if (!this.token) throw new Error("unauthorized");
    console.log({ userId, amountCents, action: "charge" });
    return this.inner.charge(userId, amountCents);
  }
}

const billing: BillingService = new BillingProxy(new RealBillingService(), "token");
await billing.charge("u1", 500);
```

## Testing strategy (pragmatic)

- Test proxy behavior with fake RealService.
- Verify delegation and side-effects explicitly.
- Avoid time-based flakiness by controlling clocks for TTL.

## Common pitfalls

- Hidden latency from proxy logic.
- Cache staleness without invalidation strategy.
- Double-init race when async init is not cached.
- Swallowing errors or changing error semantics silently.
- Proxy doing too much beyond access/lifecycle concerns.
- Tight coupling to concrete implementations.
- Inconsistent behavior between proxy and real service.
- Overusing proxy where direct access is fine.

## Checklist for refactors

- Define the service interface first.
- Decide proxy responsibility (auth, cache, lazy init, logging).
- Keep interface identical between proxy and real.
- Make async init safe with cached Promise.
- Document semantics (timeouts, retries, cache TTL).
- Wire proxy vs real at composition root.
- Test with fakes and explicit assertions.
- Monitor for added latency or failure modes.

## Output expectations

When invoked, produce:
- Service interface and proxy responsibilities.
- Wiring plan (proxy vs real).
- Failure/cache semantics and tests.
