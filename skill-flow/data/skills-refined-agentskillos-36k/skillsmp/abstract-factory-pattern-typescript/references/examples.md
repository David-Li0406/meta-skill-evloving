# Abstract Factory Examples (TypeScript)

## Example 1: Furniture shop (runnable)

```ts
interface Chair {
  sitOn(): void;
}

interface Sofa {
  lieOn(): void;
}

interface CoffeeTable {
  put(item: string): void;
}

interface FurnitureFactory {
  createChair(): Chair;
  createSofa(): Sofa;
  createCoffeeTable(): CoffeeTable;
}

class ModernChair implements Chair {
  sitOn() {
    console.log("Sit on a modern chair");
  }
}

class ModernSofa implements Sofa {
  lieOn() {
    console.log("Lie on a modern sofa");
  }
}

class ModernCoffeeTable implements CoffeeTable {
  put(item: string) {
    console.log(`Place ${item} on a modern coffee table`);
  }
}

class VictorianChair implements Chair {
  sitOn() {
    console.log("Sit on a victorian chair");
  }
}

class VictorianSofa implements Sofa {
  lieOn() {
    console.log("Lie on a victorian sofa");
  }
}

class VictorianCoffeeTable implements CoffeeTable {
  put(item: string) {
    console.log(`Place ${item} on a victorian coffee table`);
  }
}

class ModernFurnitureFactory implements FurnitureFactory {
  createChair(): Chair {
    return new ModernChair();
  }
  createSofa(): Sofa {
    return new ModernSofa();
  }
  createCoffeeTable(): CoffeeTable {
    return new ModernCoffeeTable();
  }
}

class VictorianFurnitureFactory implements FurnitureFactory {
  createChair(): Chair {
    return new VictorianChair();
  }
  createSofa(): Sofa {
    return new VictorianSofa();
  }
  createCoffeeTable(): CoffeeTable {
    return new VictorianCoffeeTable();
  }
}

function furnishRoom(factory: FurnitureFactory) {
  const chair = factory.createChair();
  const sofa = factory.createSofa();
  const table = factory.createCoffeeTable();
  chair.sitOn();
  sofa.lieOn();
  table.put("magazine");
}

const factory = new ModernFurnitureFactory();
furnishRoom(factory);
```

## Example 2: Cross-platform UI family (runnable)

```ts
interface Button {
  render(): void;
}

interface Checkbox {
  toggle(): void;
}

interface UIControlFactory {
  createButton(): Button;
  createCheckbox(): Checkbox;
}

class WinButton implements Button {
  render() {
    console.log("Render Windows button");
  }
}

class WinCheckbox implements Checkbox {
  toggle() {
    console.log("Toggle Windows checkbox");
  }
}

class MacButton implements Button {
  render() {
    console.log("Render Mac button");
  }
}

class MacCheckbox implements Checkbox {
  toggle() {
    console.log("Toggle Mac checkbox");
  }
}

class WindowsUIFactory implements UIControlFactory {
  createButton(): Button {
    return new WinButton();
  }
  createCheckbox(): Checkbox {
    return new WinCheckbox();
  }
}

class MacUIFactory implements UIControlFactory {
  createButton(): Button {
    return new MacButton();
  }
  createCheckbox(): Checkbox {
    return new MacCheckbox();
  }
}

function renderSettings(factory: UIControlFactory) {
  factory.createButton().render();
  factory.createCheckbox().toggle();
}

renderSettings(new MacUIFactory());
```

## Function-object abstract factory (preferred TS style)

```ts
type Variant = "modern" | "victorian";

interface Chair {
  sitOn(): void;
}

interface Sofa {
  lieOn(): void;
}

interface CoffeeTable {
  put(item: string): void;
}

type FurnitureFactory = {
  createChair(): Chair;
  createSofa(): Sofa;
  createCoffeeTable(): CoffeeTable;
};

class ModernChair implements Chair {
  sitOn() {
    console.log("Sit on a modern chair");
  }
}

class ModernSofa implements Sofa {
  lieOn() {
    console.log("Lie on a modern sofa");
  }
}

class ModernCoffeeTable implements CoffeeTable {
  put(item: string) {
    console.log(`Place ${item} on a modern coffee table`);
  }
}

class VictorianChair implements Chair {
  sitOn() {
    console.log("Sit on a victorian chair");
  }
}

class VictorianSofa implements Sofa {
  lieOn() {
    console.log("Lie on a victorian sofa");
  }
}

class VictorianCoffeeTable implements CoffeeTable {
  put(item: string) {
    console.log(`Place ${item} on a victorian coffee table`);
  }
}

const factories: Record<Variant, FurnitureFactory> = {
  modern: {
    createChair: () => new ModernChair(),
    createSofa: () => new ModernSofa(),
    createCoffeeTable: () => new ModernCoffeeTable(),
  },
  victorian: {
    createChair: () => new VictorianChair(),
    createSofa: () => new VictorianSofa(),
    createCoffeeTable: () => new VictorianCoffeeTable(),
  },
};

const factory = factories.modern;
factory.createChair().sitOn();
```

## Config selects factory (initializer)

```ts
type Variant = "win" | "mac";

interface Button {
  render(): void;
}

interface Checkbox {
  toggle(): void;
}

type UIControlFactory = {
  createButton(): Button;
  createCheckbox(): Checkbox;
};

class WinButton implements Button {
  render() {
    console.log("Render Windows button");
  }
}

class WinCheckbox implements Checkbox {
  toggle() {
    console.log("Toggle Windows checkbox");
  }
}

class MacButton implements Button {
  render() {
    console.log("Render Mac button");
  }
}

class MacCheckbox implements Checkbox {
  toggle() {
    console.log("Toggle Mac checkbox");
  }
}

const factories: Record<Variant, UIControlFactory> = {
  win: {
    createButton: () => new WinButton(),
    createCheckbox: () => new WinCheckbox(),
  },
  mac: {
    createButton: () => new MacButton(),
    createCheckbox: () => new MacCheckbox(),
  },
};

function initFactoryFromConfig(config: { variant: Variant }): UIControlFactory {
  return factories[config.variant];
}

const factory = initFactoryFromConfig({ variant: "mac" });
factory.createButton().render();
```
