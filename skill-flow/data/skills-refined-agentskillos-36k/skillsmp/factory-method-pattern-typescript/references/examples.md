# Factory Method Examples (TypeScript)

## Example 1: Transport logistics (runnable)

```ts
interface Transport {
  deliver(): void;
}

class Truck implements Transport {
  deliver() {
    console.log("Deliver by land");
  }
}

class Ship implements Transport {
  deliver() {
    console.log("Deliver by sea");
  }
}

abstract class Logistics {
  planDelivery(): void {
    const transport = this.createTransport();
    transport.deliver();
  }

  protected abstract createTransport(): Transport;
}

class RoadLogistics extends Logistics {
  protected createTransport(): Transport {
    return new Truck();
  }
}

class SeaLogistics extends Logistics {
  protected createTransport(): Transport {
    return new Ship();
  }
}

const logistics = new RoadLogistics();
logistics.planDelivery();
```

## Example 2: Cross-platform UI (dialog/buttons)

```ts
interface Button {
  render(): void;
}

class WindowsButton implements Button {
  render() {
    console.log("Render Windows button");
  }
}

class WebButton implements Button {
  render() {
    console.log("Render Web button");
  }
}

abstract class Dialog {
  open(): void {
    const button = this.createButton();
    button.render();
  }

  protected abstract createButton(): Button;
}

class WindowsDialog extends Dialog {
  protected createButton(): Button {
    return new WindowsButton();
  }
}

class WebDialog extends Dialog {
  protected createButton(): Button {
    return new WebButton();
  }
}

new WebDialog().open();
```

## Registry-based factory variant

```ts
interface Transport {
  deliver(): void;
}

class Truck implements Transport {
  deliver() {
    console.log("Deliver by land");
  }
}

class Ship implements Transport {
  deliver() {
    console.log("Deliver by sea");
  }
}

type TransportKind = "truck" | "ship";

type TransportFactory = () => Transport;

const registry: Record<TransportKind, TransportFactory> = {
  truck: () => new Truck(),
  ship: () => new Ship(),
};

function createTransport(kind: TransportKind): Transport {
  return registry[kind]();
}

createTransport("truck").deliver();
```

## Cache/pool-returning factory method variant

```ts
interface Transport {
  deliver(): void;
}

class Truck implements Transport {
  deliver() {
    console.log("Deliver by land");
  }
}

class Ship implements Transport {
  deliver() {
    console.log("Deliver by sea");
  }
}

type TransportKind = "truck" | "ship";

type TransportFactory = () => Transport;

const registry: Record<TransportKind, TransportFactory> = {
  truck: () => new Truck(),
  ship: () => new Ship(),
};

const cache = new Map<TransportKind, Transport>();

function getTransport(kind: TransportKind): Transport {
  const existing = cache.get(kind);
  if (existing) return existing;
  const created = registry[kind]();
  cache.set(kind, created);
  return created;
}

getTransport("ship").deliver();
```
