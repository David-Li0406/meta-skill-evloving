# Lua to TypeScript Migration Reference

Guide for converting Lua code to TypeScript.

## Basic Syntax Changes

### Variables
```lua
-- Lua
local x = 10
```
```typescript
// TypeScript
const x = 10; // or let for mutable
```

### Functions
```lua
-- Lua
local function add(a, b)
    return a + b
end
```
```typescript
// TypeScript
function add(a: number, b: number): number {
    return a + b;
}
```

### Arrays
```lua
-- Lua (1-indexed)
local arr = {1, 2, 3}
print(arr[1]) -- 1
```
```typescript
// TypeScript (0-indexed!)
const arr = [1, 2, 3];
print(arr[0]); // 1
```

### Dictionaries
```lua
-- Lua
local dict = {
    name = "Player",
    health = 100
}
```
```typescript
// TypeScript - Use Map for dynamic keys
const dict = new Map<string, unknown>();
dict.set("name", "Player");
dict.set("health", 100);

// Or interface for known keys
interface PlayerData {
    name: string;
    health: number;
}
```

### Classes
```lua
-- Lua
local MyClass = {}
MyClass.__index = MyClass

function MyClass.new()
    local self = setmetatable({}, MyClass)
    return self
end

function MyClass:method()
    -- use self
end
```
```typescript
// TypeScript
class MyClass {
    constructor() {}
    
    method() {
        // use this
    }
}
```

## Common Patterns

### nil → undefined
```lua
if value == nil then
```
```typescript
if (value === undefined) {
```

### Equality
```lua
if a == b then
```
```typescript
if (a === b) {
```

### Not Equal
```lua
if a ~= b then
```
```typescript
if (a !== b) {
```

### String Concatenation
```lua
local str = "Hello " .. name
```
```typescript
const str = `Hello ${name}`;
```

### Iteration
```lua
for i, v in ipairs(array) do
    print(i, v)
end
```
```typescript
array.forEach((v, i) => {
    print(i, v);
});
```

## Services
```lua
local Players = game:GetService("Players")
```
```typescript
import { Players } from "@rbxts/services";
```

## Key Differences

1. Arrays are 0-indexed
2. Use `this` not `self`
3. Use `===` not `==`
4. Use `undefined` not `nil`
5. Semicolons required
6. Use Map for dictionaries
7. Type everything

## Quick Migration Checklist

- [ ] Convert variables to const/let
- [ ] Add type annotations
- [ ] Change array indices (1-based → 0-based)
- [ ] Replace nil with undefined
- [ ] Use === instead of ==
- [ ] Convert string concatenation to template literals
- [ ] Import services from @rbxts/services
- [ ] Use Map for dictionaries
- [ ] Convert classes to TypeScript classes
- [ ] Add semicolons
