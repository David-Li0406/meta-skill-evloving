---
name: decorator-pattern-typescript
description: TypeScript/Node decorator pattern using wrapper objects (not TS language decorators), same-interface composition, order sensitivity, and trade-offs vs Adapter/Proxy.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Decorator (TypeScript)

## Intent

Attach additional behavior to an object while keeping the same interface, enabling runtime composition of multiple wrappers.

## When to use

- Cross-cutting concerns around a port (logging, metrics, caching, retry, validation).
- Stackable behaviors configured per environment or route.
- You want to avoid subclass explosion.
- Client code must call the same interface regardless of features.
- You need runtime composition of responsibilities.
- Different orders of behavior should be selectable.
- You want thin, testable wrappers around a stable interface.

## When NOT to use

- Order complexity makes behavior hard to predict.
- Wrapper stacks are difficult to debug.
- Interface mismatch requires Adapter instead.
- Only one fixed variant is needed.
- Performance hotspots cannot tolerate extra wrapping.
- Behavior should be enforced centrally, not per instance.
- Wrappers would embed domain logic rather than cross-cutting concerns.

## Mental model

Component interface; concrete component; wrappers that delegate then add behavior.

## Recommended TS shapes

- Interface + composition wrappers (preferred).
- Factory function to assemble stacks from config.
- Avoid TS “@decorator” syntax confusion: use explicit wrapper objects.

## Example 1: Notifier decorators (Email + Slack + SMS)

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

## Example 2: Repository decorators (timing + retry + cache)

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

class RepoDecorator implements Repo {
  constructor(protected readonly inner: Repo) {}
  get(id: string): Promise<string | null> {
    return this.inner.get(id);
  }
}

class TimingDecorator extends RepoDecorator {
  async get(id: string): Promise<string | null> {
    const start = Date.now();
    const result = await this.inner.get(id);
    console.log(`timing=${Date.now() - start}ms`);
    return result;
  }
}

class RetryDecorator extends RepoDecorator {
  async get(id: string): Promise<string | null> {
    try {
      return await this.inner.get(id);
    } catch {
      return this.inner.get(id);
    }
  }
}

class CacheDecorator extends RepoDecorator {
  private cache = new Map<string, string | null>();
  async get(id: string): Promise<string | null> {
    if (this.cache.has(id)) return this.cache.get(id) ?? null;
    const result = await this.inner.get(id);
    this.cache.set(id, result);
    return result;
  }
}

const repo: Repo = new TimingDecorator(new RetryDecorator(new CacheDecorator(new InMemoryRepo())));
await repo.get("a");
```

## Testing strategy (pragmatic)

- Test wrappers with fakes or stubs.
- Test stack assembly from config.
- Assert call order explicitly when order matters.

## Common pitfalls

- Confusing Decorator with Adapter.
- Order-dependent bugs in wrapper stacks.
- Double side effects (e.g., duplicate logging).
- Hidden latency from stacked behaviors.
- Leaking concrete types through wrappers.
- Over-decorating trivial code paths.
- Missing tests for ordering and composition.
- Wrappers become business logic containers.

## Checklist for refactors

- Define a stable interface first.
- Extract cross-cutting behavior into thin wrappers.
- Decide and document wrapper order.
- Provide a stack assembly function/config.
- Keep wrappers small and focused.
- Add observability for order-dependent effects.
- Test wrappers in isolation and in stacks.
- Monitor latency added by decorators.

## Output expectations

When invoked, produce:
- Interface and wrapper list.
- Stack assembly plan and order.
- A test plan for wrappers and stacks.
