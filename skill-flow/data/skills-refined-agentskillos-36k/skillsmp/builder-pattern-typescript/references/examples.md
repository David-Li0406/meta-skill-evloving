# Builder Examples (TypeScript)

## Example 1: House fluent builder (with optional director routine)

```ts
type Heating = "gas" | "electric" | "none";

type House = Readonly<{
  floors: number;
  hasPool: boolean;
  hasGarden: boolean;
  heating: Heating;
}>;

class HouseBuilder {
  private floors = 1;
  private hasPool = false;
  private hasGarden = false;
  private heating: Heating = "none";

  reset(): this {
    this.floors = 1;
    this.hasPool = false;
    this.hasGarden = false;
    this.heating = "none";
    return this;
  }

  withFloors(floors: number): this {
    this.floors = floors;
    return this;
  }

  addPool(): this {
    this.hasPool = true;
    return this;
  }

  addGarden(): this {
    this.hasGarden = true;
    return this;
  }

  setHeating(type: Heating): this {
    this.heating = type;
    return this;
  }

  build(): House {
    return Object.freeze({
      floors: this.floors,
      hasPool: this.hasPool,
      hasGarden: this.hasGarden,
      heating: this.heating,
    });
  }
}

class HouseDirector {
  buildFamilyHouse(builder: HouseBuilder): House {
    return builder.reset().withFloors(2).addGarden().setHeating("gas").build();
  }
}

const house = new HouseBuilder().withFloors(3).addPool().build();
const director = new HouseDirector();
const familyHouse = director.buildFamilyHouse(new HouseBuilder());
```

## Example 2: Car + Manual builders with shared Director

```ts
type Car = Readonly<{ model: string; seats: number; hasSportPackage: boolean }>;

type Manual = Readonly<{ title: string; steps: string[] }>;

interface BuildSteps<T> {
  reset(): this;
  setModel(model: string): this;
  setSeats(seats: number): this;
  enableSportPackage(): this;
  build(): T;
}

class CarBuilder implements BuildSteps<Car> {
  private model = "";
  private seats = 0;
  private sport = false;

  reset(): this {
    this.model = "";
    this.seats = 0;
    this.sport = false;
    return this;
  }

  setModel(model: string): this {
    this.model = model;
    return this;
  }

  setSeats(seats: number): this {
    this.seats = seats;
    return this;
  }

  enableSportPackage(): this {
    this.sport = true;
    return this;
  }

  build(): Car {
    return Object.freeze({
      model: this.model,
      seats: this.seats,
      hasSportPackage: this.sport,
    });
  }
}

class ManualBuilder implements BuildSteps<Manual> {
  private title = "";
  private steps: string[] = [];

  reset(): this {
    this.title = "";
    this.steps = [];
    return this;
  }

  setModel(model: string): this {
    this.title = `${model} Manual`;
    this.steps.push(`Describe ${model} features`);
    return this;
  }

  setSeats(seats: number): this {
    this.steps.push(`Explain ${seats} seats`);
    return this;
  }

  enableSportPackage(): this {
    this.steps.push("Include sport package instructions");
    return this;
  }

  build(): Manual {
    return Object.freeze({ title: this.title, steps: [...this.steps] });
  }
}

class Director {
  makeSportsCar<T>(builder: BuildSteps<T>): T {
    return builder.reset().setModel("Sports").setSeats(2).enableSportPackage().build();
  }

  makeSUV<T>(builder: BuildSteps<T>): T {
    return builder.reset().setModel("SUV").setSeats(5).build();
  }
}

const director = new Director();
const sportsCar = director.makeSportsCar(new CarBuilder());
const sportsManual = director.makeSportsCar(new ManualBuilder());
const suv = director.makeSUV(new CarBuilder());
```

## Minimal no-director usage

```ts
const customCar = new CarBuilder().setModel("Custom").setSeats(4).build();
```

## Product immutability snippet

```ts
const immutable = Object.freeze({ name: "House", floors: 2 } as const);
```
