# Bridge Examples (TypeScript)

## Example 1: Shape × Renderer

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
console.log(svgCircle.draw());
console.log(canvasRect.draw());
```

## Example 2: Service × Storage backend (runtime swap)

```ts
import { writeFile, readFile } from "node:fs/promises";

interface Storage {
  save(key: string, value: string): Promise<void>;
  load(key: string): Promise<string | null>;
}

class MemoryStore implements Storage {
  private data = new Map<string, string>();
  async save(key: string, value: string): Promise<void> {
    this.data.set(key, value);
  }
  async load(key: string): Promise<string | null> {
    return this.data.get(key) ?? null;
  }
}

class FileStore implements Storage {
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

const service = new ReportService(new MemoryStore());
await service.saveReport("r1", "hello");
```

## Bridge vs Strategy vs Adapter (tiny sketches)

```ts
// Bridge: two axes vary (Shape × Renderer)
interface Renderer { drawCircle(x: number, y: number, r: number): string; }
abstract class Shape { constructor(protected r: Renderer) {} abstract draw(): string; }

// Strategy: one axis varies (algorithm)
interface PricingStrategy { price(base: number): number; }
class Cart { constructor(private strategy: PricingStrategy) {} total(base: number) { return this.strategy.price(base); } }

// Adapter: translate external API to internal port
interface PaymentsPort { charge(amount: number): Promise<string>; }
class PaymentsAdapter implements PaymentsPort { constructor(private sdk: any) {} charge(amount: number) { return this.sdk.createCharge(amount); } }
```
