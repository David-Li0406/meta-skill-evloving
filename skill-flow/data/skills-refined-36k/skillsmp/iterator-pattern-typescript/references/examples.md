# Iterator Examples (TypeScript)

## Example 1: Tree iterables with dfs() and bfs()

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

const tree = new Tree({
  value: "a",
  children: [{ value: "b", children: [] }, { value: "c", children: [] }],
});

for (const v of tree.dfs()) console.log(v);
for (const v of tree.bfs()) console.log(v);
```

## Example 2: AsyncIterable over paginated data

```ts
type Page = { items: string[]; nextCursor?: string };

type PageSource = (cursor?: string) => Promise<Page>;

const source: PageSource = async (cursor) => {
  if (!cursor) return { items: ["a", "b"], nextCursor: "2" };
  if (cursor === "2") return { items: ["c"], nextCursor: undefined };
  return { items: [], nextCursor: undefined };
};

async function* paginate(src: PageSource, start?: string): AsyncIterable<string> {
  let cursor: string | undefined = start;
  while (true) {
    const page = await src(cursor);
    for (const item of page.items) yield item;
    if (!page.nextCursor) return;
    cursor = page.nextCursor;
  }
}

for await (const item of paginate(source)) {
  console.log(item);
}
```

## Example 3: Explicit iterator class with cleanup

```ts
class RangeIterator implements Iterator<number> {
  private current: number;
  constructor(private readonly start: number, private readonly end: number) {
    this.current = start;
  }

  next(): IteratorResult<number> {
    if (this.current > this.end) return { done: true, value: undefined };
    return { done: false, value: this.current++ };
  }

  return(): IteratorResult<number> {
    // cleanup hook
    return { done: true, value: undefined };
  }
}

const it = new RangeIterator(1, 3);
console.log(it.next());
console.log(it.next());
console.log(it.return?.());
```

## Iterator vs Generator vs Visitor vs Composite (tiny sketches)

```ts
// Iterator: traversal contract
interface Iterator<T> { next(): IteratorResult<T>; }

// Generator: implementation technique
function* gen() { yield 1; yield 2; }

// Visitor: operation over elements
interface Visitor { visit(value: number): void; }

// Composite: tree structure
interface Node { children: Node[]; }
```
