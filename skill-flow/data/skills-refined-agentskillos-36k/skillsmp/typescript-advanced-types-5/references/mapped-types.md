# Mapped Types

Transform existing types by iterating over their properties.

## Basic Mapped Type

```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

interface User {
  id: number;
  name: string;
}

type ReadonlyUser = Readonly<User>;
// Type: { readonly id: number; readonly name: string; }
```

## Optional Properties

```typescript
type Partial<T> = {
  [P in keyof T]?: T[P];
};

type PartialUser = Partial<User>;
// Type: { id?: number; name?: string; }
```

## Removing Modifiers

Use `-` to remove modifiers:

```typescript
type Required<T> = {
  [P in keyof T]-?: T[P];
};

type Mutable<T> = {
  -readonly [P in keyof T]: T[P];
};
```

## Key Remapping (TypeScript 4.1+)

Transform keys with `as` clause:

```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Person {
  name: string;
  age: number;
}

type PersonGetters = Getters<Person>;
// Type: { getName: () => string; getAge: () => number; }
```

## Filtering Properties

Exclude keys by remapping to `never`:

```typescript
type PickByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K];
};

interface Mixed {
  id: number;
  name: string;
  age: number;
  active: boolean;
}

type OnlyNumbers = PickByType<Mixed, number>;
// Type: { id: number; age: number; }

type OmitByType<T, U> = {
  [K in keyof T as T[K] extends U ? never : K]: T[K];
};

type NoNumbers = OmitByType<Mixed, number>;
// Type: { name: string; active: boolean; }
```

## Deep Mapped Types

Apply transformations recursively:

```typescript
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object
    ? T[P] extends Function
      ? T[P]
      : DeepReadonly<T[P]>
    : T[P];
};

type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object
    ? T[P] extends Array<infer U>
      ? Array<DeepPartial<U>>
      : DeepPartial<T[P]>
    : T[P];
};

interface Config {
  server: {
    host: string;
    port: number;
    ssl: {
      enabled: boolean;
      cert: string;
    };
  };
}

type ReadonlyConfig = DeepReadonly<Config>;
// All nested properties are readonly

type PartialConfig = DeepPartial<Config>;
// All nested properties are optional
```

## Combining Mapped Types

```typescript
type Nullable<T> = {
  [P in keyof T]: T[P] | null;
};

type NullablePartial<T> = Nullable<Partial<T>>;

type User = { id: number; name: string };
type NullablePartialUser = NullablePartial<User>;
// Type: { id?: number | null; name?: string | null; }
```
