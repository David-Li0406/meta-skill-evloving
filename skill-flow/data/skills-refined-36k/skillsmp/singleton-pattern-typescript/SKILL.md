---
name: singleton-pattern-typescript
description: TypeScript/Node singleton patterns (module instance, classic singleton class, DI singleton scope) with trade-offs on testability and hidden deps, plus safe usage guidance.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Singleton (TypeScript)

## Intent

Ensure a single shared instance for a process-wide concern while making usage explicit and testable.

## When to use

- Process-wide cache or registry (metrics, tracing, feature flags).
- Config snapshot loaded once at startup.
- Expensive initialization that should happen only once.
- A shared resource must be centralized to avoid duplication.
- You need a single in-memory coordinator for the process.
- The instance is infrastructure, not domain logic.
- You can provide a clear reset or injection strategy for tests.

## When NOT to use

- Domain logic or business rules (avoid global state).
- Hidden dependencies make code harder to reason about.
- Global mutable state would leak across tests.
- Tests require isolation or multiple instances.
- A simple DI singleton-scope is available and cleaner.
- The instance lifecycle depends on user/session scope.
- You cannot define a clear ownership or reset strategy.

## Recommended TS shapes

- Module-level instance (preferred).
- DI singleton-scope (preferred if you have a container).
- Classic singleton class (only when needed).

## Example 1: Module-level singleton (Config)

```ts
type Config = Readonly<{ env: string; apiBaseUrl: string }>;

class ConfigLoader {
  private config: Config | null = null;

  init(env: string, apiBaseUrl: string): void {
    if (this.config) return;
    this.config = Object.freeze({ env, apiBaseUrl });
  }

  get(): Config {
    if (!this.config) throw new Error("Config not initialized");
    return this.config;
  }
}

export const config = new ConfigLoader();
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

## Example 3: Async singleton initialization

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

## Testing strategy (pragmatic)

- Prefer injecting an interface and a test double.
- If you export a singleton, provide a test-only reset hook guarded by environment.

## Common pitfalls

- Hidden coupling through global access.
- State leaks between tests.
- Async initialization races without a cached promise.
- Using singleton for domain rules or business logic.
- Unclear lifecycle or ownership.
- Hard-coded configuration at import time.
- Skipping observability of shared state.
- Overusing singleton when DI scope is enough.

## Checklist for refactors

- Define why it must be single and process-wide.
- Prefer DI singleton scope when available.
- Expose an interface and inject it where possible.
- Use module-level instance for simple cases.
- Add an explicit init and/or reset strategy.
- Avoid static state in domain logic.
- Ensure async init is guarded against races.
- Add tests for singleton behavior and resets.

## Output expectations

When invoked, produce:
- The chosen singleton form and reasoning.
- A wiring/injection plan for dependencies.
- A test isolation approach (reset or injection).
