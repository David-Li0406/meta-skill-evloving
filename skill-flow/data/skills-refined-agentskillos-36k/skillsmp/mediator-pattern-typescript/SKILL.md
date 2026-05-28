---
name: mediator-pattern-typescript
description: Reduce many-to-many dependencies via a mediator for UI/workflow coordination with typed events; TS/Node composition; trade-offs vs Observer/Facade/Command; avoid God Object drift.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Mediator (TypeScript)

## Intent

Centralize coordination so components don’t talk to each other directly, reducing many-to-many coupling.

## When to use

- Many-to-many coupling makes changes ripple everywhere.
- Coordination rules are non-trivial and scattered.
- Components should be reusable across contexts.
- UI/workflow orchestration needs a single source of truth.
- You need explicit ordering and constraints between components.
- You want a stable coordination contract instead of peer references.
- You want to test collaboration rules in one place.

## When NOT to use

- Interactions are simple and localized.
- A Facade is enough (simplify a subsystem API).
- Pure pub/sub (Observer) is sufficient.
- The mediator would become a God Object.
- Components already have clear ownership and boundaries.
- The coordination logic is trivial.
- You can solve it with direct calls safely.

## Mental model

Components emit signals; mediator interprets and coordinates actions among components.

## Recommended TS shapes

- Narrow mediator interface + constructor injection into components.
- Typed event hub mediator (discriminated union events) for decoupling and testability.

## Example 1: Dialog mediator (UI controls)

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

## Example 2: Workflow mediator (services)

```ts
type Order = { id: string; userId: string; sku: string };

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

  async placeOrder(order: Order): Promise<boolean> {
    if (!(await this.auth.verify(order.userId))) return false;
    if (!(await this.inventory.reserve(order.sku))) return false;
    if (!(await this.payment.charge(order.userId))) return false;
    return true;
  }
}

const mediator = new OrderWorkflowMediator(new AuthService(), new InventoryService(), new PaymentService());
await mediator.placeOrder({ id: "o1", userId: "u1", sku: "sku" });
```

## Testing strategy (pragmatic)

- Unit test mediator rules with fakes.
- Integration test a whole collaboration scenario.

## Common pitfalls

- God Object drift.
- Too generic mediator with no clear boundary.
- Components still reaching into peers directly.
- Untyped event strings causing breakage.
- Hidden side effects in mediator rules.
- Overuse of a global mediator singleton.
- Tight coupling between mediator and concrete components.
- Ignoring feature-scoped mediators.

## Checklist for refactors

- Map interactions and peer dependencies.
- Extract coordination rules into mediator.
- Define a narrow mediator contract.
- Inject mediator into components.
- Delete peer references and direct calls.
- Scope mediators per feature or workflow.
- Add tests for orchestration rules.
- Keep mediator small and focused.

## Output expectations

When invoked, produce:
- Interaction map and mediator contract/events.
- Wiring plan for components and mediator.
- Minimal runnable TS examples.
