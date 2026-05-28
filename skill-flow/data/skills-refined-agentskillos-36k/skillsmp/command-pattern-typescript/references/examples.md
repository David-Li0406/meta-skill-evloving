# Command Examples (TypeScript)

## Example 1: CommandBus with discriminated-union commands

```ts
type Result = { ok: true } | { ok: false; error: string };

type CreateUser = { type: "CreateUser"; payload: { id: string; email: string } };

type DisableUser = { type: "DisableUser"; payload: { id: string } };

type Command = CreateUser | DisableUser;

type Handler<C extends Command> = (cmd: C) => Promise<Result>;

type HandlerMap = {
  CreateUser: Handler<CreateUser>;
  DisableUser: Handler<DisableUser>;
};

class CommandBus {
  constructor(private readonly handlers: HandlerMap) {}

  execute(cmd: Command): Promise<Result> {
    const handler = this.handlers[cmd.type];
    return handler(cmd as any);
  }
}

const bus = new CommandBus({
  CreateUser: async (cmd) => {
    console.log("create", cmd.payload.id);
    return { ok: true };
  },
  DisableUser: async (cmd) => {
    console.log("disable", cmd.payload.id);
    return { ok: true };
  },
});

await bus.execute({ type: "CreateUser", payload: { id: "u1", email: "a@b.com" } });
```

## Example 2: In-memory queue/worker with retries

```ts
type Result = { ok: true } | { ok: false; error: string };

type Command = { type: "SendEmail"; payload: { to: string } };

type Handler = (cmd: Command) => Promise<Result>;

class InMemoryQueue {
  private items: Command[] = [];
  enqueue(cmd: Command): void {
    this.items.push(cmd);
  }
  dequeue(): Command | undefined {
    return this.items.shift();
  }
}

async function worker(queue: InMemoryQueue, handler: Handler, retries = 2): Promise<void> {
  const cmd = queue.dequeue();
  if (!cmd) return;
  let attempt = 0;
  while (attempt <= retries) {
    const res = await handler(cmd);
    if (res.ok) return;
    attempt += 1;
  }
}

const queue = new InMemoryQueue();
queue.enqueue({ type: "SendEmail", payload: { to: "a@b.com" } });
```

## Example 3: Undo with command history

```ts
type Command = { type: "Increment"; amount: number };

type State = { count: number };

class Counter {
  constructor(public state: State) {}
  execute(cmd: Command): void {
    this.state.count += cmd.amount;
  }
  undo(cmd: Command): void {
    this.state.count -= cmd.amount;
  }
}

const history: Command[] = [];
const counter = new Counter({ count: 0 });

const cmd: Command = { type: "Increment", amount: 2 };
counter.execute(cmd);
history.push(cmd);

const last = history.pop();
if (last) counter.undo(last);
```

## Command vs Strategy vs CoR vs Event (tiny sketches)

```ts
// Command: action as object
const cmd = { type: "DoThing", payload: { id: "1" } };

// Strategy: swap one algorithm
interface Strategy { run(x: number): number; }

// CoR: chain with stop/continue
const handlers = [(ctx: any) => ({ type: "continue", ctx }), (ctx: any) => ({ type: "handled" })];

// Event: fact happened
const event = { type: "UserCreated", payload: { id: "1" } };
```
