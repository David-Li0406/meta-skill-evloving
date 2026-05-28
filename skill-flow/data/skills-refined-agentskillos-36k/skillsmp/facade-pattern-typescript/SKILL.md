---
name: facade-pattern-typescript
description: Simplified entrypoint over complex subsystems with TS/Node wiring, hidden lifecycle/ordering, testability via DI, and trade-offs vs Adapter/Mediator/Proxy.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Facade (TypeScript)

## Intent

Provide a small, stable entrypoint to a complex subsystem while hiding wiring, initialization, and call ordering.

## When to use

- A complex framework/subsystem leaks into client code.
- You want to hide initialization and ordering rules.
- You need to reduce coupling to a 3rd-party framework.
- There is repeated wiring/boilerplate across the codebase.
- You want one stable API per subsystem boundary.
- You need to stabilize the surface area during migrations.
- You want to keep client code focused on business flow.

## When NOT to use

- The facade risks becoming a god object.
- A single interface mismatch is the only problem (use Adapter).
- You need peer coordination and bidirectional routing (Mediator).
- The subsystem is already small and cohesive.
- The facade would be a thin pass-through with no value.
- You need full flexibility to use subsystem features directly.
- The facade would mix unrelated concerns.

## Mental model

Facade = boundary API; subsystem stays complex; client only sees the facade.

## Recommended TS shapes

- Class facade with constructor-injected deps (preferred).
- Functional facade (module) when state/lifecycle is minimal.
- Multiple facades per subsystem layer (avoid bloat).

## Example 1: MediaConverter facade

```ts
type Video = { path: string; format: "mp4" | "webm" };

type ConvertOptions = { format: "mp4" | "webm"; bitrateKbps: number };

class Decoder {
  decode(input: Video): string {
    return `raw:${input.path}`;
  }
}

class Encoder {
  encode(raw: string, options: ConvertOptions): Video {
    return { path: `${raw}.${options.format}`, format: options.format };
  }
}

class Optimizer {
  optimize(raw: string): string {
    return `${raw}:optimized`;
  }
}

class MediaConverter {
  constructor(
    private readonly decoder: Decoder,
    private readonly optimizer: Optimizer,
    private readonly encoder: Encoder
  ) {}

  convert(input: Video, options: ConvertOptions): Video {
    const raw = this.decoder.decode(input);
    const optimized = this.optimizer.optimize(raw);
    return this.encoder.encode(optimized, options);
  }
}

const converter = new MediaConverter(new Decoder(), new Optimizer(), new Encoder());
const out = converter.convert({ path: "in", format: "mp4" }, { format: "webm", bitrateKbps: 1200 });
```

## Example 2: Deployment/Infra facade

```ts
type PipelineResult = { buildId: string; deployed: boolean };

class Builder {
  async build(): Promise<string> {
    return "build-123";
  }
}

class Uploader {
  async upload(buildId: string): Promise<void> {
    return;
  }
}

class CdnInvalidator {
  async invalidate(): Promise<void> {
    return;
  }
}

class DeployFacade {
  constructor(
    private readonly builder: Builder,
    private readonly uploader: Uploader,
    private readonly cdn: CdnInvalidator
  ) {}

  async runPipeline(): Promise<PipelineResult> {
    const buildId = await this.builder.build();
    await this.uploader.upload(buildId);
    await this.cdn.invalidate();
    return { buildId, deployed: true };
  }
}

const deploy = new DeployFacade(new Builder(), new Uploader(), new CdnInvalidator());
await deploy.runPipeline();
```

## Testing strategy (pragmatic)

- Fake subsystem ports and assert call order.
- Test facade API behavior separately from subsystem internals.

## Common pitfalls

- God facade that grows across unrelated concerns.
- Leaking subsystem types through the facade API.
- Too many knobs exposed on the facade.
- Doing business logic inside the facade.
- Hiding errors or lifecycle issues from callers.
- Creating multiple facades that drift in behavior.
- Tight coupling to concrete subsystem classes.
- Ignoring backward compatibility on facade API.

## Checklist for refactors

- Define the subsystem boundary.
- Pick the minimal, stable API surface.
- Hide lifecycle and ordering inside the facade.
- Inject subsystem dependencies for testability.
- Split into multiple facades if scope grows.
- Keep return types stable and typed.
- Add tests for ordering and error propagation.
- Document the boundary and ownership.

## Output expectations

When invoked, produce:
- Facade API and subsystem ports.
- A wiring plan (DI or manual).
- Tests for call order and behavior.
