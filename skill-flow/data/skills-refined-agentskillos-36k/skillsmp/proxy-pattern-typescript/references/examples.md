# Proxy Examples (TypeScript)

## Example 1: Lazy-init proxy with cached Promise

```ts
interface SearchService {
  search(q: string): Promise<string[]>;
}

class RealSearchService implements SearchService {
  constructor(private readonly endpoint: string) {}
  async search(q: string): Promise<string[]> {
    return [`${q}@${this.endpoint}`];
  }
}

class SearchServiceProxy implements SearchService {
  private initPromise: Promise<RealSearchService> | null = null;

  constructor(private readonly endpoint: string) {}

  private async getReal(): Promise<RealSearchService> {
    if (!this.initPromise) {
      this.initPromise = Promise.resolve(new RealSearchService(this.endpoint));
    }
    return this.initPromise;
  }

  async search(q: string): Promise<string[]> {
    const real = await this.getReal();
    return real.search(q);
  }
}

const svc: SearchService = new SearchServiceProxy("https://search.local");
await svc.search("cats");
```

## Example 2: Caching proxy with TTL

```ts
interface HttpClient {
  get(url: string): Promise<string>;
}

class SimpleHttpClient implements HttpClient {
  async get(url: string): Promise<string> {
    return `data:${url}`;
  }
}

type CacheEntry = { value: string; expiresAt: number };

class CachingHttpClientProxy implements HttpClient {
  private cache = new Map<string, CacheEntry>();

  constructor(private readonly inner: HttpClient, private readonly ttlMs: number) {}

  async get(url: string): Promise<string> {
    const now = Date.now();
    const cached = this.cache.get(url);
    if (cached && cached.expiresAt > now) return cached.value;
    const value = await this.inner.get(url);
    this.cache.set(url, { value, expiresAt: now + this.ttlMs });
    return value;
  }

  invalidate(url: string): void {
    this.cache.delete(url);
  }
}

const client: HttpClient = new CachingHttpClientProxy(new SimpleHttpClient(), 500);
await client.get("/a");
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

## Proxy vs Decorator vs Adapter vs Facade (tiny sketches)

```ts
// Proxy: same interface, controls access/lifecycle
interface Svc { run(): void; }
class ProxySvc implements Svc { constructor(private inner: Svc) {} run() { /* auth/lazy */ this.inner.run(); } }

// Decorator: same interface, adds behavior
class DecoratorSvc implements Svc { constructor(private inner: Svc) {} run() { this.inner.run(); /* extra */ } }

// Adapter: different interface -> target
interface Target { execute(): void; }
class Adapter implements Target { constructor(private adaptee: { doThing(): void }) {} execute() { this.adaptee.doThing(); } }

// Facade: new simplified API over subsystem
class Facade { run(): void { /* call multiple internals */ } }
```
