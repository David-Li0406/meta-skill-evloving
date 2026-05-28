---
name: command-pattern-typescript
description: Represent actions as objects for decoupled invocation, queue/schedule/retry/audit, and optional undo/redo; TS/Node async-friendly command bus; trade-offs vs Strategy/CoR/Events.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Command (TypeScript)

## Intent

Turn an operation into a first-class object so it can be queued, logged, retried, or undone independently of the caller.

## When to use

- You need queue/schedule semantics for actions.
- Auditing/logging of actions is required.
- Undo/redo or compensation is needed.
- Multiple invokers trigger the same action.
- You want a uniform execution API.
- You need retries around side-effecting operations.
- You want to decouple invokers from receivers.

## When NOT to use

- Simple direct calls are enough.
- You only need to swap one algorithm (Strategy).
- Your flow is event-only (use Events).
- All steps must always run in a fixed pipeline.
- The action will never be queued/logged/replayed.
- You need a different interface (Adapter).
- The overhead outweighs the benefit.

## Recommended TS shapes

- Discriminated-union command types + handler map (preferred).
- OO command objects with `execute()` (alternative).
- Optional middleware around CommandBus (metrics/logging).

## Example 1: CommandBus + two commands

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

## Example 2: Queue + retry (in-memory)

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
```

## Example 3: Undoable commands

```ts
type UndoResult = { ok: true } | { ok: false; error: string };

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

## Testing strategy (pragmatic)

- Unit test handlers with fakes.
- Test bus wiring with known commands.
- Make retry deterministic via injected clock/random.

## Common pitfalls

- Mixing command with event semantics.
- Mutable payloads that change after enqueue.
- Leaky receiver dependencies inside commands.
- Hard-to-replay side effects.
- Overly generic command types.
- Missing idempotency where retries exist.
- Confusing command results with domain events.
- Unclear ownership of execution context.

## Checklist for refactors

- Identify invokers vs receivers.
- Define command types and payloads.
- Centralize wiring in a CommandBus.
- Add Result typing and retries where needed.
- Make commands immutable.
- Document side effects and idempotency.
- Add observability around execution.
- Add tests for command handling and ordering.

## Output expectations

When invoked, produce:
- Command types, handlers, and wiring.
- Queue/retry plan with Result typing.
- Minimal examples and tests.
