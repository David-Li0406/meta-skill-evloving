# Template Literal Types

Create string-based types with pattern matching and transformation.

## Basic Template Literal

```typescript
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`;
// Type: "onClick" | "onFocus" | "onBlur"
```

## String Manipulation Utilities

Built-in intrinsic string types:

```typescript
type UppercaseGreeting = Uppercase<"hello">; // "HELLO"
type LowercaseGreeting = Lowercase<"HELLO">; // "hello"
type CapitalizedName = Capitalize<"john">; // "John"
type UncapitalizedName = Uncapitalize<"John">; // "john"
```

## Combining with Unions

Template literals distribute over unions:

```typescript
type Color = "red" | "blue" | "green";
type Size = "sm" | "md" | "lg";

type ColorSize = `${Color}-${Size}`;
// Type: "red-sm" | "red-md" | "red-lg" | "blue-sm" | "blue-md" | "blue-lg" | "green-sm" | "green-md" | "green-lg"
```

## Pattern Matching with `infer`

Extract parts of strings:

```typescript
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<`/${Rest}`>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type Params = ExtractRouteParams<"/users/:userId/posts/:postId">;
// Type: "userId" | "postId"
```

## Path Building

Create dot-notation paths for nested objects:

```typescript
type Path<T> = T extends object
  ? {
      [K in keyof T]: K extends string
        ? `${K}` | `${K}.${Path<T[K]>}`
        : never;
    }[keyof T]
  : never;

interface Config {
  server: {
    host: string;
    port: number;
  };
  database: {
    url: string;
  };
}

type ConfigPath = Path<Config>;
// Type: "server" | "database" | "server.host" | "server.port" | "database.url"
```

## CSS-in-JS Type Safety

```typescript
type CSSProperty = "margin" | "padding" | "border";
type CSSDirection = "top" | "right" | "bottom" | "left";

type DirectionalCSS = `${CSSProperty}-${CSSDirection}`;
// Type: "margin-top" | "margin-right" | ... | "border-left"

type CSSValue = `${number}${"px" | "rem" | "em" | "%"}`;

const spacing: Record<DirectionalCSS, CSSValue> = {
  "margin-top": "10px",
  "padding-left": "1rem",
  // ... etc
};
```

## HTTP Method Types

```typescript
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
type Endpoint = "/users" | "/posts" | "/comments";

type APIRoute = `${HTTPMethod} ${Endpoint}`;
// Type: "GET /users" | "POST /users" | ... | "PATCH /comments"
```

## Getter/Setter Generation

```typescript
type Getter<T extends string> = `get${Capitalize<T>}`;
type Setter<T extends string> = `set${Capitalize<T>}`;

type PropertyAccessors<T> = {
  [K in keyof T as Getter<string & K>]: () => T[K];
} & {
  [K in keyof T as Setter<string & K>]: (value: T[K]) => void;
};

interface State {
  count: number;
  name: string;
}

type StateAccessors = PropertyAccessors<State>;
// Type: {
//   getCount: () => number;
//   getName: () => string;
//   setCount: (value: number) => void;
//   setName: (value: string) => void;
// }
```
