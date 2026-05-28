# Singleton Examples (TypeScript)

## Example 1: Module-level singleton instance

```ts
interface MetricsRegistry {
  increment(name: string): void;
  getCount(name: string): number;
}

class InMemoryMetrics implements MetricsRegistry {
  private counts = new Map<string, number>();

  increment(name: string): void {
    this.counts.set(name, (this.counts.get(name) ?? 0) + 1);
  }

  getCount(name: string): number {
    return this.counts.get(name) ?? 0;
  }
}

export const metrics = new InMemoryMetrics();
```

## Example 2: Classic singleton class

```ts
class Logger {
  private static instance: Logger | null = null;

  private constructor(private readonly prefix: string) {}

  static getInstance(prefix = "app"): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger(prefix);
    }
    return Logger.instance;
  }

  log(message: string): void {
    console.log(`[${this.prefix}] ${message}`);
  }
}

const logger = Logger.getInstance("service");
logger.log("started");
```

## Example 3: Async singleton with cached Promise

```ts
class Client {
  constructor(public readonly baseUrl: string) {}
  async ping(): Promise<void> {
    return;
  }
}

let clientPromise: Promise<Client> | null = null;

export function getClient(): Promise<Client> {
  if (!clientPromise) {
    clientPromise = (async () => {
      const client = new Client("https://api.example.com");
      await client.ping();
      return client;
    })();
  }
  return clientPromise;
}
```

## Test reset hook snippet (use only in tests)

```ts
let registryInstance: MetricsRegistry | null = null;

export function getRegistry(): MetricsRegistry {
  if (!registryInstance) registryInstance = new InMemoryMetrics();
  return registryInstance;
}

export function __resetForTests(): void {
  // WARNING: use only in tests to avoid production state loss.
  registryInstance = null;
}
```
