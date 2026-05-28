# Composite Examples (TypeScript)

## Example 1: Product/Box order pricing composite

```ts
interface Item {
  totalPrice(): number;
}

class Product implements Item {
  constructor(private readonly name: string, private readonly price: number) {}
  totalPrice(): number {
    return this.price;
  }
}

class Box implements Item {
  private readonly children: Item[] = [];
  constructor(private readonly packagingCost: number) {}

  add(item: Item): void {
    this.children.push(item);
  }

  totalPrice(): number {
    return this.packagingCost + this.children.reduce((sum, c) => sum + c.totalPrice(), 0);
  }
}

const smallBox = new Box(1.5);
smallBox.add(new Product("Book", 10));
smallBox.add(new Product("Pen", 2));

const bigBox = new Box(3);
bigBox.add(smallBox);
bigBox.add(new Product("Headphones", 50));

console.log(bigBox.totalPrice());
```

## Example 2: UI render tree composite

```ts
interface Node {
  render(): string;
}

class TextNode implements Node {
  constructor(private readonly text: string) {}
  render(): string {
    return this.text;
  }
}

class ButtonNode implements Node {
  constructor(private readonly label: string) {}
  render(): string {
    return `<button>${this.label}</button>`;
  }
}

class ContainerNode implements Node {
  private readonly children: Node[] = [];
  constructor(private readonly tag: string) {}

  add(child: Node): void {
    this.children.push(child);
  }

  render(): string {
    const inner = this.children.map((c) => c.render()).join("");
    return `<${this.tag}>${inner}</${this.tag}>`;
  }
}

const root = new ContainerNode("div");
root.add(new TextNode("Hello"));
root.add(new ButtonNode("Click"));
console.log(root.render());
```

## Traversal helper + cycle guard

```ts
interface Node {
  children(): Node[];
  render(): string;
}

class Leaf implements Node {
  constructor(private readonly text: string) {}
  children(): Node[] {
    return [];
  }
  render(): string {
    return this.text;
  }
}

class CompositeNode implements Node {
  private readonly nodes: Node[] = [];
  add(node: Node): void {
    this.nodes.push(node);
  }
  children(): Node[] {
    return this.nodes.slice();
  }
  render(): string {
    return this.nodes.map((n) => n.render()).join("");
  }
}

function walk(node: Node, visit: (n: Node) => void, seen = new Set<Node>()): void {
  if (seen.has(node)) return;
  seen.add(node);
  visit(node);
  for (const child of node.children()) walk(child, visit, seen);
}
```

## Composite vs Decorator vs Visitor (tiny sketches)

```ts
// Composite: part-whole tree
interface Component { render(): string; }
class Leaf implements Component { render() { return "leaf"; } }
class Group implements Component { constructor(private children: Component[]) {} render() { return this.children.map(c => c.render()).join(""); } }

// Decorator: wrap one object
class Decorator implements Component { constructor(private inner: Component) {} render() { return `*${this.inner.render()}*`; } }

// Visitor: add new operations without changing node classes
interface Visitor { visitLeaf(l: Leaf): void; visitGroup(g: Group): void; }
```
