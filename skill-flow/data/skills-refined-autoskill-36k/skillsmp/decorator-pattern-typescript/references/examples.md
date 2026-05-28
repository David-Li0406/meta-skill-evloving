# Decorator Examples (TypeScript)

## Example 1: Notifier + stacked decorators

```ts
interface Notifier {
  notify(message: string): void;
}

class EmailNotifier implements Notifier {
  notify(message: string): void {
    console.log(`Email: ${message}`);
  }
}

class NotifierDecorator implements Notifier {
  constructor(protected readonly inner: Notifier) {}
  notify(message: string): void {
    this.inner.notify(message);
  }
}

class SlackDecorator extends NotifierDecorator {
  notify(message: string): void {
    super.notify(message);
    console.log(`Slack: ${message}`);
  }
}

class SmsDecorator extends NotifierDecorator {
  notify(message: string): void {
    super.notify(message);
    console.log(`SMS: ${message}`);
  }
}

const notifier = new SmsDecorator(new SlackDecorator(new EmailNotifier()));
notifier.notify("Build finished");
```

## Example 2: HttpClient decorators (timing + retry + cache)

```ts
interface HttpClient {
  get(url: string): Promise<string>;
}

class SimpleHttpClient implements HttpClient {
  async get(url: string): Promise<string> {
    return `data:${url}`;
  }
}

class HttpClientDecorator implements HttpClient {
  constructor(protected readonly inner: HttpClient) {}
  get(url: string): Promise<string> {
    return this.inner.get(url);
  }
}

class TimingDecorator extends HttpClientDecorator {
  async get(url: string): Promise<string> {
    const start = Date.now();
    const result = await this.inner.get(url);
    console.log(`timing=${Date.now() - start}ms`);
    return result;
  }
}

class RetryDecorator extends HttpClientDecorator {
  async get(url: string): Promise<string> {
    try {
      return await this.inner.get(url);
    } catch {
      return this.inner.get(url);
    }
  }
}

class CacheDecorator extends HttpClientDecorator {
  private cache = new Map<string, string>();
  async get(url: string): Promise<string> {
    if (this.cache.has(url)) return this.cache.get(url)!;
    const result = await this.inner.get(url);
    this.cache.set(url, result);
    return result;
  }
}

// Order matters: cache outside retry vs retry outside cache
const clientA: HttpClient = new CacheDecorator(new RetryDecorator(new TimingDecorator(new SimpleHttpClient())));
const clientB: HttpClient = new RetryDecorator(new CacheDecorator(new TimingDecorator(new SimpleHttpClient())));
await clientA.get("/a");
await clientB.get("/b");
```

## Decorator vs Adapter vs Proxy (tiny sketches)

```ts
// Decorator: same interface, add behavior
interface Svc { run(): void; }
class SvcDecorator implements Svc { constructor(private inner: Svc) {} run() { this.inner.run(); } }

// Adapter: change interface to target
interface Target { execute(): void; }
class Adapter implements Target { constructor(private adaptee: { doThing(): void }) {} execute() { this.adaptee.doThing(); } }

// Proxy: control access/lifecycle
class ProxySvc implements Svc { constructor(private inner: Svc) {} run() { /* auth/lazy */ this.inner.run(); } }
```
