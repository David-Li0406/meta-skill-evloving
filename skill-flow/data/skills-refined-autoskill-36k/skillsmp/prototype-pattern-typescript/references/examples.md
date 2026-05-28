# Prototype Examples (TypeScript)

## Example 1: Shape hierarchy with clone() + copy constructor

```ts
interface Prototype<T> {
  clone(): T;
}

abstract class Shape implements Prototype<Shape> {
  constructor(public x: number, public y: number, public color: string) {}
  abstract clone(): Shape;
}

class Circle extends Shape {
  constructor(x: number, y: number, color: string, public radius: number) {
    super(x, y, color);
  }

  static from(source: Circle): Circle {
    return new Circle(source.x, source.y, source.color, source.radius);
  }

  clone(): Circle {
    return Circle.from(this);
  }
}

class Rectangle extends Shape {
  constructor(x: number, y: number, color: string, public width: number, public height: number) {
    super(x, y, color);
  }

  clone(): Rectangle {
    return new Rectangle(this.x, this.y, this.color, this.width, this.height);
  }
}

const c1 = new Circle(5, 5, "red", 10);
const c2 = c1.clone();
const r1 = new Rectangle(0, 0, "blue", 4, 8);
const r2 = r1.clone();
```

## Example 2: Prototype registry with presets

```ts
interface Prototype<T> {
  clone(): T;
}

class Circle implements Prototype<Circle> {
  constructor(public x: number, public y: number, public color: string, public radius: number) {}
  clone(): Circle {
    return new Circle(this.x, this.y, this.color, this.radius);
  }
}

class PrototypeRegistry<T extends Prototype<T>> {
  private items = new Map<string, T>();

  register(name: string, prototype: T): void {
    this.items.set(name, prototype);
  }

  create(name: string): T {
    const proto = this.items.get(name);
    if (!proto) throw new Error(`Unknown prototype: ${name}`);
    return proto.clone();
  }
}

const registry = new PrototypeRegistry<Circle>();
registry.register("defaultCircle", new Circle(0, 0, "blue", 10));
registry.register("largeRedCircle", new Circle(0, 0, "red", 50));

const a = registry.create("defaultCircle");
const b = registry.create("largeRedCircle");
```

## Shallow vs deep clone (explicit)

```ts
type Style = { border: { color: string; width: number }; tags: string[] };

class Box implements Prototype<Box> {
  constructor(public width: number, public style: Style) {}

  clone(): Box {
    return new Box(this.width, {
      border: { ...this.style.border },
      tags: [...this.style.tags],
    });
  }
}

const original = new Box(10, { border: { color: "black", width: 1 }, tags: ["ui"] });
const copy = original.clone();
```

## JSON cloning is bad for classes (Date + method)

```ts
class Report {
  constructor(public createdAt: Date) {}
  ageMs(now: Date): number {
    return now.getTime() - this.createdAt.getTime();
  }
}

const report = new Report(new Date("2024-01-01"));
const jsonClone = JSON.parse(JSON.stringify(report)) as Report;

console.log(typeof jsonClone.createdAt); // string, not Date
try {
  console.log(jsonClone.ageMs(new Date()));
} catch (err) {
  console.log("Method missing on JSON clone");
}
```
