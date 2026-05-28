# TypeScript in Roblox-TS Reference

Complete guide to using TypeScript with roblox-ts, including features, limitations, and Luau compilation.

## TypeScript Support

Roblox-TS supports most TypeScript features with some limitations due to Luau constraints.

### Supported Features

**Basic Types:**
```typescript
let num: number = 42;
let str: string = "hello";
let bool: boolean = true;
let arr: number[] = [1, 2, 3];
let tuple: [string, number] = ["test", 42];
```

**Interfaces and Types:**
```typescript
interface Player {
    name: string;
    health: number;
}

type UserId = string | number;

type PlayerData = {
    userId: UserId;
    inventory: string[];
};
```

**Classes:**
```typescript
class Character {
    constructor(
        public name: string,
        private health: number
    ) {}
    
    takeDamage(amount: number) {
        this.health -= amount;
    }
    
    get isAlive() {
        return this.health > 0;
    }
}
```

**Enums:**
```typescript
enum GameState {
    Lobby,
    Playing,
    Ended
}

let state = GameState.Playing;
```

**Generics:**
```typescript
function getFirst<T>(array: T[]): T | undefined {
    return array[0];
}

class Container<T> {
    constructor(private value: T) {}
    getValue(): T {
        return this.value;
    }
}
```

**Union and Intersection Types:**
```typescript
type StringOrNumber = string | number;
type Combined = { name: string } & { age: number };
```

**Type Guards:**
```typescript
function isString(value: unknown): value is string {
    return typeOf(value) === "string";
}

if (isString(value)) {
    print(value.upper());
}
```

**Async/Await (Promise-based):**
```typescript
async function fetchData(): Promise<string> {
    return "data";
}

async function main() {
    const data = await fetchData();
    print(data);
}
```

### Limitations

**No Decorators:**
```typescript
// ❌ Not supported (use Flamework for decorator support)
@Service()
class MyService {}
```

**No Namespace Merging:**
```typescript
// ❌ Not supported
namespace MyNamespace {
    export const value = 10;
}
```

**Limited Reflection:**
```typescript
// ❌ No Object.keys(), Object.entries(), etc. on classes
// Use Map for dynamic key access
```

**No Symbols:**
```typescript
// ❌ Not supported
const sym = Symbol("key");
```

## Arrays vs Maps vs Sets

### Arrays (for ordered collections)

```typescript
const numbers: number[] = [1, 2, 3, 4, 5];

// Methods
numbers.push(6);
numbers.pop();
numbers.shift();
numbers.unshift(0);

// Iteration
numbers.forEach(n => print(n));
const doubled = numbers.map(n => n * 2);
const filtered = numbers.filter(n => n > 3);

// Note: Arrays are 0-indexed in TypeScript
print(numbers[0]); // First element
```

### Maps (for key-value pairs)

Use Map instead of objects for dictionaries:

```typescript
// ✅ Use Map for dynamic keys
const playerScores = new Map<Player, number>();
playerScores.set(player, 100);
const score = playerScores.get(player);

// Iteration
for (const [player, score] of playerScores) {
    print(`${player.Name}: ${score}`);
}

// Methods
playerScores.has(player);
playerScores.delete(player);
playerScores.clear();
playerScores.size();
```

**Why Maps over objects:**
- Objects in TypeScript compile to tables with known keys
- Maps compile to proper Luau dictionaries
- Maps support any key type (objects, numbers, etc.)

```typescript
// ❌ Don't use objects for dynamic keys
const scores: { [key: string]: number } = {};
scores[player.Name] = 100; // Less efficient

// ✅ Use Map instead
const scores = new Map<string, number>();
scores.set(player.Name, 100);
```

### Sets (for unique values)

```typescript
const uniqueIds = new Set<string>();

// Add/remove
uniqueIds.add("id1");
uniqueIds.add("id2");
uniqueIds.add("id1"); // Duplicate ignored
uniqueIds.delete("id1");

// Check
if (uniqueIds.has("id2")) {
    print("Found");
}

// Iteration
for (const id of uniqueIds) {
    print(id);
}

// Size
print(uniqueIds.size());
```

## Export Patterns

### Module Exports (export =)

Use for single-export modules:

```typescript
// utils/math-utils.ts
namespace MathUtils {
    export function add(a: number, b: number) {
        return a + b;
    }
}

export = MathUtils;

// usage
import MathUtils from "utils/math-utils";
MathUtils.add(1, 2);
```

### Named Exports

Use for multiple exports:

```typescript
// utils/string-utils.ts
export function capitalize(str: string) {
    return str.upper().sub(1, 1) + str.lower().sub(2);
}

export function reverse(str: string) {
    return str.reverse();
}

// usage
import { capitalize, reverse } from "utils/string-utils";
```

### Re-exports

```typescript
// shared/index.ts
export * from "./types";
export * from "./constants";
export { default as MathUtils } from "./math-utils";
```

## Type Guards and Narrowing

### Built-in Type Guards

```typescript
// typeof
if (typeOf(value) === "string") {
    print(value.upper());
}

// instanceof
if (part instanceof Part) {
    part.Anchored = true;
}

// classIs (Roblox-specific)
const humanoid = character.FindFirstChild("Humanoid");
if (humanoid && classIs(humanoid, "Humanoid")) {
    humanoid.Health = 100;
}

// typeIs (roblox-ts specific)
import { typeIs } from "@rbxts/t";

if (typeIs("string")(value)) {
    print(value.upper());
}
```

### Custom Type Guards

```typescript
function isPlayer(obj: unknown): obj is Player {
    return (obj as Player).Character !== undefined;
}

function hasHumanoid(character: Model): character is Model & { Humanoid: Humanoid } {
    const humanoid = character.FindFirstChild("Humanoid");
    return humanoid !== undefined && classIs(humanoid, "Humanoid");
}

// Usage
if (hasHumanoid(character)) {
    character.Humanoid.Health = 100; // Type-safe
}
```

## Promises and Async/Await

### Creating Promises

```typescript
function wait(seconds: number): Promise<void> {
    return new Promise(resolve => {
        task.wait(seconds);
        resolve();
    });
}

function fetchData(id: string): Promise<string> {
    return new Promise((resolve, reject) => {
        const success = pcall(() => {
            // Fetch logic
            return "data";
        });
        
        if (success[0]) {
            resolve(success[1] as string);
        } else {
            reject(success[1]);
        }
    });
}
```

### Using Async/Await

```typescript
async function loadPlayer(userId: string) {
    try {
        const data = await fetchData(userId);
        print("Loaded:", data);
        return data;
    } catch (error) {
        warn("Failed to load:", error);
        return undefined;
    }
}

// Calling async functions
loadPlayer("123").then(data => {
    if (data) print("Success");
});

// Or await in another async function
async function main() {
    const data = await loadPlayer("123");
}
```

### Promise Utilities

```typescript
// Promise.all - wait for all promises
const results = await Promise.all([
    fetchData("1"),
    fetchData("2"),
    fetchData("3")
]);

// Promise.race - first to complete
const first = await Promise.race([
    fetchData("1"),
    wait(5).then(() => "timeout")
]);

// Promise.allSettled - wait for all, get results and errors
const outcomes = await Promise.allSettled([
    fetchData("1"),
    fetchData("2")
]);
```

## Destructuring

### Array Destructuring

```typescript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
print(first);  // 1
print(second); // 2
print(rest);   // [3, 4, 5]

// Swapping
let a = 1, b = 2;
[a, b] = [b, a];
```

### Object Destructuring

```typescript
const player = { Name: "Player1", Health: 100 };
const { Name, Health } = player;

// With renaming
const { Name: playerName, Health: hp } = player;

// With defaults
const { Name, Health = 100 } = player;
```

### Function Parameters

```typescript
function greet({ name, age }: { name: string; age: number }) {
    print(`Hello ${name}, age ${age}`);
}

greet({ name: "Bob", age: 25 });
```

## Spread and Rest

### Spread Operator

```typescript
// Arrays
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2]; // [1,2,3,4,5,6]

// Objects (shallow copy)
const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 }; // { a: 1, b: 2, c: 3 }
```

### Rest Parameters

```typescript
function sum(...numbers: number[]) {
    return numbers.reduce((a, b) => a + b, 0);
}

sum(1, 2, 3, 4, 5); // 15
```

## Optional Chaining and Nullish Coalescing

### Optional Chaining (?.)

```typescript
const humanoid = character?.FindFirstChild("Humanoid") as Humanoid | undefined;
const health = humanoid?.Health;

// Array access
const first = array?.[0];

// Function calls
const result = callback?.();
```

### Nullish Coalescing (??)

```typescript
const health = player.Health ?? 100; // 100 if Health is undefined

// Different from ||
const value = 0 || 100;  // 100 (0 is falsy)
const value = 0 ?? 100;  // 0 (0 is not nullish)
```

## Template Literals

```typescript
const name = "Player1";
const health = 100;

const message = `${name} has ${health} HP`;
print(message); // "Player1 has 100 HP"

// Multi-line
const description = `
    Name: ${name}
    Health: ${health}
    Status: Alive
`;
```

## Type Assertions

```typescript
// as keyword
const part = workspace.FindFirstChild("MyPart") as Part;

// Non-null assertion
const part = workspace.FindFirstChild("MyPart")!;

// Const assertion
const config = {
    maxPlayers: 10,
    gameName: "MyGame"
} as const; // Makes all properties readonly
```

## Utility Types

```typescript
// Partial - makes all properties optional
interface Player {
    name: string;
    health: number;
}
type PartialPlayer = Partial<Player>;

// Required - makes all properties required
type RequiredPlayer = Required<PartialPlayer>;

// Readonly
type ReadonlyPlayer = Readonly<Player>;

// Pick - select specific properties
type PlayerName = Pick<Player, "name">;

// Omit - exclude specific properties
type PlayerWithoutHealth = Omit<Player, "health">;

// Record - create object type with keys
type PlayerScores = Record<string, number>;
```

## Best Practices

1. **Use strict mode** - Enable `strict: true` in tsconfig
2. **Prefer unknown over any** - Use type guards to narrow
3. **Use Maps for dictionaries** - Not objects with dynamic keys
4. **Leverage type inference** - Don't over-annotate
5. **Use const assertions** - For immutable data
6. **Destructure carefully** - Only what you need
7. **Handle promises properly** - Always catch errors
8. **Use type guards** - For runtime safety with Roblox instances

## Common Pitfalls

**Array indexing:**
```typescript
// ❌ Wrong (Lua style)
const first = array[1];

// ✅ Correct (0-indexed)
const first = array[0];
```

**Dictionary iteration:**
```typescript
// ❌ Don't use objects for dynamic keys
const dict: { [key: string]: number } = {};

// ✅ Use Map
const dict = new Map<string, number>();
```

**Self reference:**
```typescript
// ❌ No self parameter
function method(self: MyClass) {}

// ✅ Use this
class MyClass {
    method() {
        print(this);
    }
}
```

**Equality:**
```typescript
// ✅ Use === not ==
if (value === undefined) {}

// ✅ Use !== not ~=
if (value !== nil) {}
```
