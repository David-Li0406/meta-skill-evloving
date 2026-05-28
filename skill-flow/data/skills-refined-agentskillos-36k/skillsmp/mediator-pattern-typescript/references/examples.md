# Mediator Examples (TypeScript)

## Example 1: Dialog mediator with typed events

```ts
type DialogEvent =
  | { type: "toggleAdvanced"; enabled: boolean }
  | { type: "submit" }
  | { type: "input"; field: "name" | "email"; value: string };

interface DialogMediator {
  notify(sender: string, event: DialogEvent): void;
}

class Checkbox {
  constructor(private readonly mediator: DialogMediator) {}
  setChecked(enabled: boolean) {
    this.mediator.notify("checkbox", { type: "toggleAdvanced", enabled });
  }
}

class Textbox {
  constructor(private readonly mediator: DialogMediator, public readonly field: "name" | "email") {}
  setValue(value: string) {
    this.mediator.notify("textbox", { type: "input", field: this.field, value });
  }
}

class Button {
  constructor(private readonly mediator: DialogMediator) {}
  click() {
    this.mediator.notify("button", { type: "submit" });
  }
}

class Dialog implements DialogMediator {
  private advancedEnabled = false;
  private values: Record<string, string> = {};

  notify(_sender: string, event: DialogEvent): void {
    if (event.type === "toggleAdvanced") {
      this.advancedEnabled = event.enabled;
    } else if (event.type === "input") {
      this.values[event.field] = event.value;
    } else if (event.type === "submit") {
      if (!this.values.name) throw new Error("name required");
      if (this.advancedEnabled && !this.values.email) throw new Error("email required");
    }
  }
}

const dialog = new Dialog();
const checkbox = new Checkbox(dialog);
const name = new Textbox(dialog, "name");
const email = new Textbox(dialog, "email");
const submit = new Button(dialog);

checkbox.setChecked(true);
name.setValue("A");
email.setValue("a@b.com");
submit.click();
```

## Example 2: Workflow mediator coordinating services

```ts
type Order = { id: string; userId: string; sku: string };

type WorkflowResult = { ok: true } | { ok: false; reason: string };

class AuthService {
  async verify(userId: string): Promise<boolean> {
    return userId.length > 0;
  }
}

class InventoryService {
  async reserve(sku: string): Promise<boolean> {
    return sku.length > 0;
  }
}

class PaymentService {
  async charge(userId: string): Promise<boolean> {
    return userId.length > 0;
  }
}

class OrderWorkflowMediator {
  constructor(
    private readonly auth: AuthService,
    private readonly inventory: InventoryService,
    private readonly payment: PaymentService
  ) {}

  async placeOrder(order: Order): Promise<WorkflowResult> {
    if (!(await this.auth.verify(order.userId))) return { ok: false, reason: "auth" };
    if (!(await this.inventory.reserve(order.sku))) return { ok: false, reason: "inventory" };
    if (!(await this.payment.charge(order.userId))) return { ok: false, reason: "payment" };
    return { ok: true };
  }
}

const mediator = new OrderWorkflowMediator(new AuthService(), new InventoryService(), new PaymentService());
await mediator.placeOrder({ id: "o1", userId: "u1", sku: "sku" });
```

## Example 3: Mediator via typed event hub

```ts
type Event =
  | { type: "SearchChanged"; query: string }
  | { type: "SearchSubmitted" };

type Handler<E extends Event> = (event: E) => void;

class EventHub {
  private handlers: { [K in Event["type"]]?: Handler<any>[] } = {};

  on<T extends Event["type"]>(type: T, handler: Handler<Extract<Event, { type: T }>>) {
    this.handlers[type] = this.handlers[type] ?? [];
    this.handlers[type]!.push(handler);
  }

  emit(event: Event) {
    this.handlers[event.type]?.forEach((h) => h(event));
  }
}

class SearchMediator {
  constructor(private readonly hub: EventHub) {
    this.hub.on("SearchChanged", (e) => {
      if (e.query.length > 2) this.hub.emit({ type: "SearchSubmitted" });
    });
  }
}

const hub = new EventHub();
new SearchMediator(hub);
hub.emit({ type: "SearchChanged", query: "abc" });
```

## Mediator vs Observer vs Facade vs Command (tiny sketches)

```ts
// Mediator: coordination logic
class Mediator { notify(sender: object, event: string): void {} }

// Observer: pub/sub
class EventBus { on(_e: string, _h: Function) {} emit(_e: string) {} }

// Facade: simplified subsystem API
class Facade { run(): void {} }

// Command: action as object
const cmd = { type: "DoThing", payload: { id: "1" } };
```
