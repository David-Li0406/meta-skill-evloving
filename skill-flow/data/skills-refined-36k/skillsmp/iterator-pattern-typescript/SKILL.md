---
name: iterator-pattern-typescript
description: Traverse without exposing representation; multiple traversal orders; pause/resume; TS Iterable/generators and async iterables; trade-offs vs Generator/Visitor/Composite.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Iterator (TypeScript)

## Intent

Provide traversal over a collection without exposing its internal representation, supporting multiple traversal strategies.

## When to use

- The structure is complex (tree/graph/pagination/remote API).
- You need multiple traversal orders (DFS/BFS).
- You want pause/resume iteration with explicit state.
- You need parallel iterators without shared cursor state.
- Traversal logic is duplicated across the codebase.
- You want to hide representation and expose a simple iteration API.
- You need sync and async traversal options.

## When NOT to use

- Simple arrays are enough.
- Traversal is a one-off loop.
- Only one trivial order exists and won’t change.
- You can use built-in `map/filter/reduce` directly.
- The abstraction would add complexity without value.
- The collection does not need encapsulation.
- You are applying it purely for pattern completeness.

## Recommended TS shapes

- `Iterable<T>` + generator-based iterator (preferred).
- Explicit iterator class for complex state (cursor/pagination).
- `AsyncIterable<T>` for remote/paginated sources.

## Example 1: Tree traversal (DFS & BFS)

```ts
type TreeNode = { value: string; children: TreeNode[] };

class Tree {
  constructor(private readonly root: TreeNode) {}

  *dfs(): Iterable<string> {
    function* walk(node: TreeNode): Iterable<string> {
      yield node.value;
      for (const child of node.children) yield* walk(child);
    }
    yield* walk(this.root);
  }

  *bfs(): Iterable<string> {
    const queue: TreeNode[] = [this.root];
    while (queue.length) {
      const node = queue.shift()!;
      yield node.value;
      queue.push(...node.children);
    }
  }
}
```

## Example 2: Paginated API iterator (AsyncIterable)

```ts
type Page = { items: string[]; nextCursor?: string };

type PageSource = (cursor?: string) => Promise<Page>;

async function* paginate(source: PageSource, start?: string): AsyncIterable<string> {
  let cursor: string | undefined = start;
  while (true) {
    const page = await source(cursor);
    for (const item of page.items) yield item;
    if (!page.nextCursor) return;
    cursor = page.nextCursor;
  }
}
```

## Example 3: Snapshot vs live iteration

```ts
class List {
  private items: string[] = [];
  add(item: string) {
    this.items.push(item);
  }
  *snapshot(): Iterable<string> {
    const copy = this.items.slice();
    for (const item of copy) yield item;
  }
}
```

## Testing strategy (pragmatic)

- Deterministic order tests for DFS/BFS.
- Property tests for coverage (no missing nodes).
- Async iterator tests with fake page sources.

## Common pitfalls

- Leaking internal representation.
- Mixing traversal with business logic.
- Mutation during iteration causing surprises.
- Off-by-one cursor bugs.
- Inconsistent traversal order across iterators.
- Exposing child arrays directly.
- Unbounded async iteration without stop conditions.
- Overusing complex iterators for simple lists.

## Checklist for refactors

- Identify traversal duplication.
- Define iterator contract and result type.
- Name traversal orders explicitly.
- Keep collection focused on storage/access.
- Add async iterators for I/O sources.
- Document snapshot vs live semantics.
- Add tests for traversal order.
- Avoid exposing internals through iterators.

## Output expectations

When invoked, produce:
- Traversal orders and iterator APIs.
- State model (cursor) and pause/resume plan.
- Minimal runnable TS examples.
