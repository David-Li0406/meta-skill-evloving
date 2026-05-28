---
name: bridge-pattern-typescript
description: Split two varying axes into abstraction + implementation using TS/Node composition, enable runtime swapping, and compare trade-offs vs Strategy/Adapter.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Bridge (TypeScript)

## Intent

Separate a high-level abstraction from its implementation so both can vary independently without cross-product subclasses.

## When to use

- Cross-product subclasses are forming (two or more axes vary).
- You need orthogonal dimensions to evolve independently.
- Runtime swapping of implementations is required.
- The abstraction API should stay stable while implementations change.
- You want to avoid large conditional matrices for type × platform.
- Multiple backends share the same high-level workflow.
- You need to test abstraction logic independently of implementation.

## When NOT to use

- Only one axis varies; Strategy or simple composition is enough.
- The implementation is stable and unlikely to change.
- The abstraction and implementation are tightly coupled.
- The extra indirection adds complexity without value.
- You can model variation with a simple config object.
- The hierarchy is small and manageable.
- You’re introducing Bridge prematurely without cross-product pressure.

## Mental model

- Abstraction = high-level API and workflow.
- Implementation = pluggable backend (port) injected into the abstraction.

## Recommended TS shapes

- Interface for implementation + constructor injection (preferred).
- Functional bridge with higher-order functions when classes are overkill.

## Example 1: Renderer bridge (shape × renderer)

```ts
interface Renderer {
  drawCircle(x: number, y: number, r: number): string;
  drawRect(x: number, y: number, w: number, h: number): string;
}

class SvgRenderer implements Renderer {
  drawCircle(x: number, y: number, r: number): string {
    return `<circle cx="${x}" cy="${y}" r="${r}" />`;
  }
  drawRect(x: number, y: number, w: number, h: number): string {
    return `<rect x="${x}" y="${y}" width="${w}" height="${h}" />`;
  }
}

class CanvasRenderer implements Renderer {
  drawCircle(x: number, y: number, r: number): string {
    return `canvas.circle(${x},${y},${r})`;
  }
  drawRect(x: number, y: number, w: number, h: number): string {
    return `canvas.rect(${x},${y},${w},${h})`;
  }
}

abstract class Shape {
  constructor(protected readonly renderer: Renderer) {}
  abstract draw(): string;
}

class Circle extends Shape {
  constructor(renderer: Renderer, private readonly x: number, private readonly y: number, private readonly r: number) {
    super(renderer);
  }
  draw(): string {
    return this.renderer.drawCircle(this.x, this.y, this.r);
  }
}

class Rectangle extends Shape {
  constructor(renderer: Renderer, private readonly x: number, private readonly y: number, private readonly w: number, private readonly h: number) {
    super(renderer);
  }
  draw(): string {
    return this.renderer.drawRect(this.x, this.y, this.w, this.h);
  }
}

const svgCircle = new Circle(new SvgRenderer(), 10, 10, 5);
const canvasRect = new Rectangle(new CanvasRenderer(), 0, 0, 20, 10);
```

## Example 2: Storage bridge (report × backend)

```ts
interface Storage {
  save(key: string, value: string): Promise<void>;
  load(key: string): Promise<string | null>;
}

class MemoryStorage implements Storage {
  private data = new Map<string, string>();
  async save(key: string, value: string): Promise<void> {
    this.data.set(key, value);
  }
  async load(key: string): Promise<string | null> {
    return this.data.get(key) ?? null;
  }
}

import { writeFile, readFile } from "node:fs/promises";

class FileStorage implements Storage {
  constructor(private readonly dir: string) {}
  async save(key: string, value: string): Promise<void> {
    await writeFile(`${this.dir}/${key}.txt`, value, "utf8");
  }
  async load(key: string): Promise<string | null> {
    try {
      return await readFile(`${this.dir}/${key}.txt`, "utf8");
    } catch {
      return null;
    }
  }
}

class ReportService {
  constructor(private readonly store: Storage) {}

  async saveReport(id: string, contents: string): Promise<void> {
    await this.store.save(id, contents);
  }

  async loadReport(id: string): Promise<string | null> {
    return this.store.load(id);
  }
}

const reports = new ReportService(new MemoryStorage());
await reports.saveReport("r1", "hello");
```

## Testing strategy (pragmatic)

- Test abstraction with fake implementations.
- Test implementations separately with focused integration tests.

## Common pitfalls

- Naming confusion between abstraction and implementation.
- Leaking implementation details into abstraction APIs.
- Too many tiny interfaces without clear axes.
- Forgetting to inject implementations at runtime.
- Overusing Bridge when only one axis varies.
- Coupling abstraction to a specific implementation.
- Inconsistent behavior across implementations.
- Cross-product explosion still present due to partial refactor.

## Checklist for refactors

- Identify the two axes of variation.
- Define a stable abstraction API.
- Define an implementation port interface.
- Inject implementation into abstraction.
- Remove cross-product subclasses and conditionals.
- Add runtime wiring or DI for implementation selection.
- Test abstraction with fake implementations.
- Add integration tests per implementation.

## Output expectations

When invoked, produce:
- The two axes and their boundaries.
- Interfaces for abstraction and implementation.
- A wiring plan and minimal examples.
