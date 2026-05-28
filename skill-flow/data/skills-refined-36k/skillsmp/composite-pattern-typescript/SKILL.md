---
name: composite-pattern-typescript
description: TypeScript guidance for tree structures with uniform leaf/composite operations, including trade-offs and disambiguation vs Decorator/Visitor.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Composite (TypeScript)

## Intent

Represent part-whole trees so clients can treat leaves and composites uniformly with recursive operations.

## When to use

- Your domain is a tree structure with arbitrary nesting.
- You need uniform operations over leaves and groups.
- Recursive aggregation is required (sum/render/validate).
- Client code should avoid leaf/container branching.
- You need to add new node types without changing traversal logic.
- The same operation should apply across the entire tree.
- You want to centralize traversal behavior in node classes.

## When NOT to use

- The structure is a graph/mesh or contains cycles.
- Shared nodes require Flyweight or explicit reference management.
- The common interface becomes too generic to be meaningful.
- Operations are not uniform across leaves and containers.
- Performance demands direct iteration over flat lists.
- You need to add many new operations (consider Visitor).
- Nodes are too heterogeneous to share behavior.

## Mental model

Leaf does work; Composite delegates to children and aggregates results.

## Recommended TS shapes

- Minimal Component interface + Leaf + Composite (preferred).
- Functional composite (plain objects + functions) when classes are overkill.
- Optional: iterator/walk method for traversal.

## Example 1: Order pricing (Product + Box)

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

## Example 2: UI render tree

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

## Testing strategy (pragmatic)

- Test leaves in isolation.
- Test composite aggregation and traversal behavior.

## Common pitfalls

- Leaking child arrays and exposing mutation.
- Type checks creep back in (if leaf vs container).
- Cycles cause infinite recursion.
- Overly broad component interface.
- Mixing unrelated behaviors into the component contract.
- Deep trees causing stack issues without safeguards.
- Forgetting to handle empty composites.
- Inconsistent traversal order.

## Checklist for refactors

- Confirm the structure is a tree.
- Define the smallest common interface.
- Choose leaf/composite responsibilities clearly.
- Add traversal API if callers need walking.
- Avoid cycles or guard them.
- Keep children collections private/readonly.
- Add tests for nested aggregation.
- Verify recursion depth or add iterative traversal if needed.

## Output expectations

When invoked, produce:
- Component interface and leaf/composite types.
- Traversal plan and aggregation logic.
- Minimal examples tailored to the user.
