# Memento Pattern Examples (TypeScript)

Each example is runnable in Node with ts-node.

## Example 1: Text editor + history caretaker (opaque mementos)

```ts
type Selection = [number, number];

type EditorSnapshot = {
  text: string;
  cursor: number;
  selection: Selection;
};

type Memento = {
  readonly name: string;
  readonly timestamp: number;
  restore(target: Editor): void;
};

class Editor {
  private text = "";
  private cursor = 0;
  private selection: Selection = [0, 0];

  setText(text: string) {
    this.text = text;
    this.cursor = text.length;
    this.selection = [this.cursor, this.cursor];
  }

  insertText(text: string) {
    this.text =
      this.text.slice(0, this.cursor) + text + this.text.slice(this.cursor);
    this.cursor += text.length;
    this.selection = [this.cursor, this.cursor];
  }

  select(from: number, to: number) {
    this.selection = [from, to];
  }

  getState() {
    return { text: this.text, cursor: this.cursor, selection: this.selection };
  }

  createMemento(name: string): Memento {
    const snapshot: EditorSnapshot = {
      text: this.text,
      cursor: this.cursor,
      selection: [this.selection[0], this.selection[1]],
    };
    const timestamp = Date.now();

    return {
      name,
      timestamp,
      restore: (target: Editor) => target.applySnapshot(snapshot),
    };
  }

  restore(memento: Memento) {
    memento.restore(this);
  }

  private applySnapshot(snapshot: EditorSnapshot) {
    this.text = snapshot.text;
    this.cursor = snapshot.cursor;
    this.selection = [snapshot.selection[0], snapshot.selection[1]];
  }
}

class History {
  private stack: Memento[] = [];

  push(m: Memento) {
    this.stack.push(m);
  }

  undo(editor: Editor) {
    const m = this.stack.pop();
    if (m) {
      editor.restore(m);
    }
  }

  listLabels(): string[] {
    return this.stack.map((m) => m.name);
  }
}

const editor = new Editor();
const history = new History();

editor.setText("Hello");
history.push(editor.createMemento("after setText"));
editor.insertText(" world");
console.log(editor.getState());

history.undo(editor);
console.log(editor.getState());
```

## Example 2: Command + Memento undo/redo (two stacks)

```ts
type EditorSnapshot = { text: string; cursor: number };

type Memento = {
  readonly name: string;
  readonly timestamp: number;
  restore(target: Editor): void;
};

class Editor {
  private text = "";
  private cursor = 0;

  setText(text: string) {
    this.text = text;
    this.cursor = text.length;
  }

  insert(text: string) {
    this.text = this.text.slice(0, this.cursor) + text + this.text.slice(this.cursor);
    this.cursor += text.length;
  }

  deleteLast(n: number) {
    const start = Math.max(0, this.cursor - n);
    this.text = this.text.slice(0, start) + this.text.slice(this.cursor);
    this.cursor = start;
  }

  getState() {
    return { text: this.text, cursor: this.cursor };
  }

  createMemento(name: string): Memento {
    const snapshot: EditorSnapshot = { text: this.text, cursor: this.cursor };
    return {
      name,
      timestamp: Date.now(),
      restore: (target: Editor) => target.applySnapshot(snapshot),
    };
  }

  private applySnapshot(snapshot: EditorSnapshot) {
    this.text = snapshot.text;
    this.cursor = snapshot.cursor;
  }
}

interface Command {
  execute(): void;
  undo(): void;
  redo(): void;
}

class InsertTextCommand implements Command {
  private before?: Memento;
  constructor(private editor: Editor, private text: string) {}

  execute() {
    this.before = this.editor.createMemento("before insert");
    this.editor.insert(this.text);
  }

  undo() {
    if (this.before) this.before.restore(this.editor);
  }

  redo() {
    this.execute();
  }
}

class DeleteLastCommand implements Command {
  private before?: Memento;
  constructor(private editor: Editor, private count: number) {}

  execute() {
    this.before = this.editor.createMemento("before delete");
    this.editor.deleteLast(this.count);
  }

  undo() {
    if (this.before) this.before.restore(this.editor);
  }

  redo() {
    this.execute();
  }
}

class CommandHistory {
  private undoStack: Command[] = [];
  private redoStack: Command[] = [];

  run(cmd: Command) {
    cmd.execute();
    this.undoStack.push(cmd);
    this.redoStack = [];
  }

  undo() {
    const cmd = this.undoStack.pop();
    if (!cmd) return;
    cmd.undo();
    this.redoStack.push(cmd);
  }

  redo() {
    const cmd = this.redoStack.pop();
    if (!cmd) return;
    cmd.redo();
    this.undoStack.push(cmd);
  }
}

const editor = new Editor();
const history = new CommandHistory();

history.run(new InsertTextCommand(editor, "Hello"));
history.run(new InsertTextCommand(editor, " world"));
console.log(editor.getState());

history.undo();
console.log(editor.getState());

history.redo();
console.log(editor.getState());
```

## Example 3: Aggregate rollback (transactional update)

```ts
type CartItem = { sku: string; price: number };

type CartSnapshot = {
  items: CartItem[];
  discount: number;
};

type Memento = {
  readonly name: string;
  readonly timestamp: number;
  restore(target: Cart): void;
};

class Cart {
  private items: CartItem[] = [];
  private discount = 0;

  addItem(item: CartItem) {
    this.items = [...this.items, item];
  }

  applyDiscount(amount: number) {
    this.discount += amount;
  }

  total(): number {
    const subtotal = this.items.reduce((sum, i) => sum + i.price, 0);
    return Math.max(0, subtotal - this.discount);
  }

  createMemento(name: string): Memento {
    const snapshot: CartSnapshot = {
      items: this.items.map((i) => ({ ...i })),
      discount: this.discount,
    };
    return {
      name,
      timestamp: Date.now(),
      restore: (target: Cart) => target.applySnapshot(snapshot),
    };
  }

  private applySnapshot(snapshot: CartSnapshot) {
    this.items = snapshot.items.map((i) => ({ ...i }));
    this.discount = snapshot.discount;
  }
}

function tryUpdate(cart: Cart, label: string, fn: () => void): boolean {
  const snap = cart.createMemento(label);
  fn();
  if (cart.total() < 10) {
    snap.restore(cart);
    return false;
  }
  return true;
}

const cart = new Cart();
cart.addItem({ sku: "A", price: 15 });

const ok = tryUpdate(cart, "before discount", () => {
  cart.applyDiscount(10);
});

console.log("updated?", ok, "total", cart.total());
```

## Disambiguation snippet

```ts
// Memento vs Command: Command = action; Memento = state snapshot used for undo.
// Memento vs Prototype: Prototype clones for new instances; Memento snapshots for restoration.
// Memento vs Event Sourcing: Event sourcing stores events; Memento stores snapshots.

type Command = { execute(): void; undo(): void };

type Memento = {
  name: string;
  restore(target: unknown): void;
};
```
