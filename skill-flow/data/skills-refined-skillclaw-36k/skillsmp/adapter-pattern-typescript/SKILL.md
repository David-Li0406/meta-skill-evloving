---
name: adapter-pattern-typescript
description: TypeScript/Node object adapters for boundary translation (DTO mapping, error model, sync/async), fitting ports/adapters or NestJS layers, with trade-offs and testing guidance.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Adapter (TypeScript)

## Intent

Translate a mismatched external interface into a stable internal port while keeping mapping logic explicit and testable.

## When to use

- 3rd-party SDK mismatch (shape, naming, error model).
- Legacy boundary you cannot change.
- You need to stabilize your internal interface while external APIs evolve.
- You must translate DTOs between layers (ports/adapters, NestJS services).
- You need to normalize sync/async behavior at a boundary.
- You must translate errors into domain-safe types.
- You want thin, testable mapping at the edge.

## When NOT to use

- You control both sides and can refactor the interface directly.
- Business logic is leaking into the adapter.
- You are over-adapting trivial shapes that can be inlined.
- Performance hot path where extra mapping adds measurable overhead without benefit.
- No stable internal port is needed.
- The adapter would grow into a god object.
- The external API is already aligned with your domain.

## Recommended TS shapes

- Object adapter via composition (preferred).
- Functional adapter (pure mapping layer + thin wrapper).
- Anti-pattern: inheritance adapter / god-adapter (avoid multiple responsibilities).

## Example 1: External SDK -> Internal Port

```ts
// Internal port
export interface UserDirectory {
  getUser(id: string): Promise<{ id: string; email: string; createdAt: Date }>;
}

// External SDK types
type SdkUser = { user_id: string; email_address: string; created_at: string };

class ExternalSdkClient {
  async fetchUser(input: { user_id: string }): Promise<SdkUser> {
    return { user_id: input.user_id, email_address: "a@b.com", created_at: "2024-01-01" };
  }
}

export class UserDirectoryAdapter implements UserDirectory {
  constructor(private readonly sdk: ExternalSdkClient) {}

  async getUser(id: string) {
    const sdkUser = await this.sdk.fetchUser({ user_id: id });
    return {
      id: sdkUser.user_id,
      email: sdkUser.email_address,
      createdAt: new Date(sdkUser.created_at),
    };
  }
}
```

## Example 2: Error model translation

```ts
class SdkError extends Error {
  constructor(public readonly code: string, message: string) {
    super(message);
  }
}

class UserNotFoundError extends Error {}
class UpstreamUnavailableError extends Error {}

class SafeUserDirectoryAdapter implements UserDirectory {
  constructor(private readonly sdk: ExternalSdkClient) {}

  async getUser(id: string) {
    try {
      const sdkUser = await this.sdk.fetchUser({ user_id: id });
      return {
        id: sdkUser.user_id,
        email: sdkUser.email_address,
        createdAt: new Date(sdkUser.created_at),
      };
    } catch (err) {
      const e = err as SdkError;
      if (e.code === "NOT_FOUND") throw new UserNotFoundError();
      throw new UpstreamUnavailableError();
    }
  }
}
```

## Example 3: Sync/async mismatch

```ts
type Callback<T> = (err: Error | null, value?: T) => void;

class LegacyClient {
  getUser(id: string, cb: Callback<SdkUser>): void {
    cb(null, { user_id: id, email_address: "a@b.com", created_at: "2024-01-01" });
  }
}

class LegacyUserDirectoryAdapter implements UserDirectory {
  constructor(private readonly legacy: LegacyClient) {}

  getUser(id: string): Promise<{ id: string; email: string; createdAt: Date }> {
    return new Promise((resolve, reject) => {
      this.legacy.getUser(id, (err, user) => {
        if (err) return reject(err);
        const sdkUser = user as SdkUser;
        resolve({
          id: sdkUser.user_id,
          email: sdkUser.email_address,
          createdAt: new Date(sdkUser.created_at),
        });
      });
    });
  }
}
```

## Testing strategy (pragmatic)

- Unit test pure mapping functions separately from I/O.
- Integration test the adapter with a stubbed SDK client.
- Contract tests for the internal port to prevent drift.

## Common pitfalls

- Adapter becomes business logic instead of translation.
- Leaking SDK types or errors into domain code.
- Double mapping drift (DTOs diverge across layers).
- Hidden breaking changes when the SDK updates.
- Over-mapping trivial shapes that don’t need adaptation.
- Mixing transport concerns with domain rules.
- Inconsistent error translation across methods.
- Skipping tests on edge mappings.

## Checklist for refactors

- Define the target interface (port) first.
- Minimize surface area of the port.
- Map request/response DTOs explicitly.
- Map errors into domain-safe types.
- Keep adapter thin and side-effect boundaries clear.
- Add unit tests for mapping functions.
- Add integration/contract tests for the port.
- Monitor SDK changes and update adapters promptly.

## Output expectations

When invoked, produce:
- Target interface and adapter skeleton.
- A mapping plan (DTOs + error translation).
- A pragmatic test plan for the adapter.
