# Conditional Types

Create types that depend on conditions, enabling sophisticated type logic.

## Basic Conditional Type

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false
```

## The `infer` Keyword

Extract types from other types:

```typescript
// Extract return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() {
  return { id: 1, name: "John" };
}

type User = ReturnType<typeof getUser>;
// Type: { id: number; name: string; }

// Extract array element type
type ElementType<T> = T extends (infer U)[] ? U : never;

type NumArray = number[];
type Num = ElementType<NumArray>; // number

// Extract promise type
type PromiseType<T> = T extends Promise<infer U> ? U : never;

type AsyncNum = PromiseType<Promise<number>>; // number

// Extract function parameters
type Parameters<T> = T extends (...args: infer P) => any ? P : never;

function foo(a: string, b: number) {}
type FooParams = Parameters<typeof foo>; // [string, number]
```

## Distributive Conditional Types

When the checked type is a naked type parameter, conditional types distribute over unions:

```typescript
type ToArray<T> = T extends any ? T[] : never;

type StrOrNumArray = ToArray<string | number>;
// Type: string[] | number[] (not (string | number)[])
```

To prevent distribution, wrap in a tuple:

```typescript
type ToArrayNonDistributive<T> = [T] extends [any] ? T[] : never;

type StrOrNumArray = ToArrayNonDistributive<string | number>;
// Type: (string | number)[]
```

## Nested Conditions

```typescript
type TypeName<T> = T extends string
  ? "string"
  : T extends number
    ? "number"
    : T extends boolean
      ? "boolean"
      : T extends undefined
        ? "undefined"
        : T extends Function
          ? "function"
          : "object";

type T1 = TypeName<string>; // "string"
type T2 = TypeName<() => void>; // "function"
type T3 = TypeName<{ x: number }>; // "object"
```

## Filtering with Conditional Types

```typescript
// Extract types from union
type ExtractStrings<T> = T extends string ? T : never;

type Mixed = "a" | 1 | "b" | 2 | "c";
type OnlyStrings = ExtractStrings<Mixed>; // "a" | "b" | "c"

// Exclude types from union
type ExcludeStrings<T> = T extends string ? never : T;

type OnlyNumbers = ExcludeStrings<Mixed>; // 1 | 2
```
