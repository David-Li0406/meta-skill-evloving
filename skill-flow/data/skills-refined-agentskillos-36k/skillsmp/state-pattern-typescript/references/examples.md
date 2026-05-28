# State Pattern Examples (TypeScript)

Each example is runnable in Node with ts-node.

## Example 1: Document lifecycle (Draft -> Moderation -> Published)

```ts
type Role = "author" | "moderator";

class TransitionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "TransitionError";
  }
}

interface DocumentState {
  key: string;
  requestReview(ctx: Document, role: Role): void;
  approve(ctx: Document, role: Role): void;
  reject(ctx: Document, role: Role): void;
  publish(ctx: Document, role: Role): void;
}

class Document {
  private state: DocumentState = new DraftState();
  private title: string;

  constructor(title: string) {
    this.title = title;
  }

  changeState(state: DocumentState) {
    this.state = state;
  }

  get stateKey(): string {
    return this.state.key;
  }

  requestReview(role: Role) {
    this.state.requestReview(this, role);
  }

  approve(role: Role) {
    this.state.approve(this, role);
  }

  reject(role: Role) {
    this.state.reject(this, role);
  }

  publish(role: Role) {
    this.state.publish(this, role);
  }
}

class DraftState implements DocumentState {
  key = "draft";

  requestReview(ctx: Document, role: Role) {
    if (role !== "author") throw new TransitionError("Only author can request review");
    ctx.changeState(new ModerationState());
  }

  approve(): void {
    throw new TransitionError("Draft cannot be approved directly");
  }

  reject(): void {
    throw new TransitionError("Draft cannot be rejected");
  }

  publish(): void {
    throw new TransitionError("Draft must be reviewed before publish");
  }
}

class ModerationState implements DocumentState {
  key = "moderation";

  requestReview(): void {
    throw new TransitionError("Already in review");
  }

  approve(ctx: Document, role: Role) {
    if (role !== "moderator") throw new TransitionError("Moderator required");
    ctx.changeState(new PublishedState());
  }

  reject(ctx: Document, role: Role) {
    if (role !== "moderator") throw new TransitionError("Moderator required");
    ctx.changeState(new DraftState());
  }

  publish(): void {
    throw new TransitionError("Must approve before publish");
  }
}

class PublishedState implements DocumentState {
  key = "published";

  requestReview(): void {
    throw new TransitionError("Published docs cannot re-enter review");
  }

  approve(): void {
    throw new TransitionError("Already published");
  }

  reject(): void {
    throw new TransitionError("Published docs cannot be rejected");
  }

  publish(): void {
    throw new TransitionError("Already published");
  }
}

const doc = new Document("Spec");
try {
  doc.publish("author");
} catch (e) {
  console.log("illegal transition:", (e as Error).message);
}

doc.requestReview("author");
try {
  doc.approve("author");
} catch (e) {
  console.log("illegal transition:", (e as Error).message);
}

doc.approve("moderator");
console.log("state:", doc.stateKey);
```

## Example 2: Payment/order lifecycle with typed errors

```ts
type PaymentAction = "authorize" | "capture" | "refund" | "fail";

class PaymentTransitionError extends Error {
  constructor(public action: PaymentAction, public from: string) {
    super(`Illegal transition: ${from} -> ${action}`);
    this.name = "PaymentTransitionError";
  }
}

interface PaymentState {
  key: string;
  authorize(ctx: Payment): void;
  capture(ctx: Payment): void;
  refund(ctx: Payment): void;
  fail(ctx: Payment): void;
}

class Payment {
  private state: PaymentState = new PendingState();
  private amount: number;

  constructor(amount: number) {
    this.amount = amount;
  }

  changeState(state: PaymentState) {
    this.state = state;
  }

  get stateKey(): string {
    return this.state.key;
  }

  authorize() {
    this.state.authorize(this);
  }

  capture() {
    this.state.capture(this);
  }

  refund() {
    this.state.refund(this);
  }

  fail() {
    this.state.fail(this);
  }
}

class PendingState implements PaymentState {
  key = "pending";
  authorize(ctx: Payment) {
    ctx.changeState(new AuthorizedState());
  }
  capture(): void {
    throw new PaymentTransitionError("capture", this.key);
  }
  refund(): void {
    throw new PaymentTransitionError("refund", this.key);
  }
  fail(ctx: Payment) {
    ctx.changeState(new FailedState());
  }
}

class AuthorizedState implements PaymentState {
  key = "authorized";
  authorize(): void {
    throw new PaymentTransitionError("authorize", this.key);
  }
  capture(ctx: Payment) {
    ctx.changeState(new CapturedState());
  }
  refund(ctx: Payment) {
    ctx.changeState(new RefundedState());
  }
  fail(ctx: Payment) {
    ctx.changeState(new FailedState());
  }
}

class CapturedState implements PaymentState {
  key = "captured";
  authorize(): void {
    throw new PaymentTransitionError("authorize", this.key);
  }
  capture(): void {
    throw new PaymentTransitionError("capture", this.key);
  }
  refund(ctx: Payment) {
    ctx.changeState(new RefundedState());
  }
  fail(): void {
    throw new PaymentTransitionError("fail", this.key);
  }
}

class RefundedState implements PaymentState {
  key = "refunded";
  authorize(): void {
    throw new PaymentTransitionError("authorize", this.key);
  }
  capture(): void {
    throw new PaymentTransitionError("capture", this.key);
  }
  refund(): void {
    throw new PaymentTransitionError("refund", this.key);
  }
  fail(): void {
    throw new PaymentTransitionError("fail", this.key);
  }
}

class FailedState implements PaymentState {
  key = "failed";
  authorize(): void {
    throw new PaymentTransitionError("authorize", this.key);
  }
  capture(): void {
    throw new PaymentTransitionError("capture", this.key);
  }
  refund(): void {
    throw new PaymentTransitionError("refund", this.key);
  }
  fail(): void {
    throw new PaymentTransitionError("fail", this.key);
  }
}

const payment = new Payment(50);
try {
  payment.capture();
} catch (e) {
  console.log((e as Error).message);
}

payment.authorize();
payment.capture();
console.log("state:", payment.stateKey);
```

## Example 3: Connection state machine with retry/backoff and serialization

```ts
class ConnectionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ConnectionError";
  }
}

interface ConnectionState {
  key: string;
  connect(ctx: Connection): void;
  onConnected(ctx: Connection): void;
  onFailure(ctx: Connection): void;
  disconnect(ctx: Connection): void;
}

class Connection {
  private state: ConnectionState;
  attempts = 0;
  maxAttempts = 3;

  constructor(state: ConnectionState = ReadyState.instance) {
    this.state = state;
  }

  get stateKey(): string {
    return this.state.key;
  }

  changeState(state: ConnectionState) {
    this.state = state;
  }

  connect() {
    this.state.connect(this);
  }

  onConnected() {
    this.state.onConnected(this);
  }

  onFailure() {
    this.state.onFailure(this);
  }

  disconnect() {
    this.state.disconnect(this);
  }

  static fromKey(key: string): ConnectionState {
    switch (key) {
      case ReadyState.instance.key:
        return ReadyState.instance;
      case ConnectingState.instance.key:
        return ConnectingState.instance;
      case ConnectedState.instance.key:
        return ConnectedState.instance;
      case DisconnectedState.instance.key:
        return DisconnectedState.instance;
      default:
        throw new ConnectionError(`Unknown state key: ${key}`);
    }
  }
}

class ReadyState implements ConnectionState {
  static instance = new ReadyState();
  key = "ready";
  connect(ctx: Connection) {
    ctx.attempts = 0;
    ctx.changeState(ConnectingState.instance);
  }
  onConnected(): void {
    throw new ConnectionError("Cannot connect without calling connect()");
  }
  onFailure(): void {
    throw new ConnectionError("No connection attempt in progress");
  }
  disconnect(): void {
    throw new ConnectionError("Not connected");
  }
}

class ConnectingState implements ConnectionState {
  static instance = new ConnectingState();
  key = "connecting";
  connect(): void {
    throw new ConnectionError("Already connecting");
  }
  onConnected(ctx: Connection) {
    ctx.changeState(ConnectedState.instance);
  }
  onFailure(ctx: Connection) {
    ctx.attempts += 1;
    if (ctx.attempts >= ctx.maxAttempts) {
      ctx.changeState(DisconnectedState.instance);
    }
  }
  disconnect(ctx: Connection) {
    ctx.changeState(DisconnectedState.instance);
  }
}

class ConnectedState implements ConnectionState {
  static instance = new ConnectedState();
  key = "connected";
  connect(): void {
    throw new ConnectionError("Already connected");
  }
  onConnected(): void {
    throw new ConnectionError("Already connected");
  }
  onFailure(ctx: Connection) {
    ctx.changeState(DisconnectedState.instance);
  }
  disconnect(ctx: Connection) {
    ctx.changeState(DisconnectedState.instance);
  }
}

class DisconnectedState implements ConnectionState {
  static instance = new DisconnectedState();
  key = "disconnected";
  connect(ctx: Connection) {
    ctx.changeState(ConnectingState.instance);
  }
  onConnected(): void {
    throw new ConnectionError("Not connecting");
  }
  onFailure(): void {
    throw new ConnectionError("Not connecting");
  }
  disconnect(): void {
    throw new ConnectionError("Already disconnected");
  }
}

const conn = new Connection();
conn.connect();
conn.onFailure();
conn.onFailure();
conn.onFailure();
console.log("state:", conn.stateKey);

const restored = Connection.fromKey("connected");
const conn2 = new Connection(restored);
try {
  conn2.onConnected();
} catch (e) {
  console.log("illegal transition:", (e as Error).message);
}
```

## Disambiguation snippet

```ts
// State vs Strategy: Strategy is chosen externally; State changes based on lifecycle.
// State vs FSM table: FSM stores transitions as data; State uses polymorphic behavior objects.
// State vs workflow engine: workflow engines handle persisted, long-running orchestration.

type State = { handle(ctx: unknown): void };

type Strategy = { execute(input: unknown): unknown };

type FsmTable = Record<string, Record<string, string>>;
```
