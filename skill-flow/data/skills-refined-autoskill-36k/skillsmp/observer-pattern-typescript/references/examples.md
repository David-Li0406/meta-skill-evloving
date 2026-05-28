# Observer Pattern Examples (TypeScript)

Each example is runnable in Node with ts-node.

## Example 1: Store back-in-stock notifications (classic Observer)

```ts
type RestockEvent = Readonly<{ sku: string; quantity: number }>; 

type Listener = (event: RestockEvent) => void;

type Unsubscribe = () => void;

class InventoryStore {
  private listenersBySku = new Map<string, Set<Listener>>();

  subscribe(sku: string, listener: Listener): Unsubscribe {
    const set = this.listenersBySku.get(sku) ?? new Set<Listener>();
    set.add(listener);
    this.listenersBySku.set(sku, set);

    return () => {
      const existing = this.listenersBySku.get(sku);
      if (!existing) return;
      existing.delete(listener);
      if (existing.size === 0) this.listenersBySku.delete(sku);
    };
  }

  restock(sku: string, quantity: number) {
    const event: RestockEvent = Object.freeze({ sku, quantity });
    const listeners = this.listenersBySku.get(sku);
    if (!listeners) return;
    for (const listener of listeners) {
      try {
        listener(event);
      } catch (err) {
        console.error("listener failed", err);
      }
    }
  }
}

const store = new InventoryStore();
const unsubscribe = store.subscribe("SKU-1", (e) => {
  console.log("notify customer A", e.sku, e.quantity);
});
store.subscribe("SKU-1", (e) => {
  console.log("notify customer B", e.sku, e.quantity);
});

store.restock("SKU-1", 25);
unsubscribe();
store.restock("SKU-1", 10);
```

## Example 2: Typed EventBus with unsubscribe and error isolation

```ts
type EventMap = {
  "user.created": Readonly<{ id: string; email: string }>;
  "order.submitted": Readonly<{ id: string; amount: number }>;
};

type Unsubscribe = () => void;

type Listener<K extends keyof EventMap> = (event: EventMap[K]) => void;

class EventBus<Events extends Record<string, Readonly<unknown>>> {
  private listeners: { [K in keyof Events]?: Set<Listener<K>> } = {};

  on<K extends keyof Events>(eventName: K, listener: Listener<K>): Unsubscribe {
    const set = (this.listeners[eventName] ??= new Set());
    set.add(listener as Listener<any>);
    return () => this.off(eventName, listener);
  }

  off<K extends keyof Events>(eventName: K, listener: Listener<K>) {
    this.listeners[eventName]?.delete(listener as Listener<any>);
  }

  emit<K extends keyof Events>(eventName: K, payload: Events[K]) {
    const listeners = this.listeners[eventName];
    if (!listeners) return;
    for (const listener of listeners) {
      try {
        listener(payload);
      } catch (err) {
        console.error("listener failed", err);
      }
    }
  }
}

const bus = new EventBus<EventMap>();

const off = bus.on("user.created", (e) => {
  console.log("welcome", e.email);
});

bus.on("order.submitted", (e) => {
  console.log("order", e.id, e.amount);
});

bus.emit("user.created", Object.freeze({ id: "u1", email: "a@b.com" }));

off();
```

## Example 3: Domain events in a service (side-effects isolated)

```ts
type DomainEventMap = {
  "user.registered": Readonly<{ id: string; email: string }>;
  "user.disabled": Readonly<{ id: string }>; 
};

type Listener<K extends keyof DomainEventMap> = (event: DomainEventMap[K]) => void;

type Unsubscribe = () => void;

class DomainEvents {
  private listeners: { [K in keyof DomainEventMap]?: Set<Listener<K>> } = {};

  on<K extends keyof DomainEventMap>(eventName: K, listener: Listener<K>): Unsubscribe {
    const set = (this.listeners[eventName] ??= new Set());
    set.add(listener as Listener<any>);
    return () => this.off(eventName, listener);
  }

  off<K extends keyof DomainEventMap>(eventName: K, listener: Listener<K>) {
    this.listeners[eventName]?.delete(listener as Listener<any>);
  }

  emit<K extends keyof DomainEventMap>(eventName: K, payload: DomainEventMap[K]) {
    const listeners = this.listeners[eventName];
    if (!listeners) return;
    for (const listener of listeners) {
      try {
        listener(payload);
      } catch (err) {
        console.error("listener failed", err);
      }
    }
  }
}

class UserService {
  constructor(private events: DomainEvents) {}

  register(email: string) {
    const id = `u-${Math.random().toString(16).slice(2)}`;
    this.events.emit("user.registered", Object.freeze({ id, email }));
    return id;
  }

  disable(id: string) {
    this.events.emit("user.disabled", Object.freeze({ id }));
  }
}

const events = new DomainEvents();

events.on("user.registered", (e) => {
  console.log("send welcome email", e.email);
});

events.on("user.registered", (e) => {
  console.log("metric: user.registered", e.id);
});

events.on("user.disabled", (e) => {
  console.log("audit user disabled", e.id);
});

const service = new UserService(events);
service.register("a@b.com");
service.disable("u-123");
```

## Disambiguation snippet

```ts
// Observer vs Mediator: Observer broadcasts; Mediator coordinates peer interactions.
// Observer vs Pub/Sub: Pub/Sub routes via broker/topic; Observer binds to a publisher instance.
// Observer vs EventEmitter: EventEmitter is an implementation of Observer with a specific API.
// Observer vs Event Sourcing: Observer reacts to events; event sourcing persists events as source of truth.

type Observer = { update(event: unknown): void };

type Mediator = { notify(sender: unknown, event: unknown): void };

type PubSub = { publish(topic: string, payload: unknown): void };
```
