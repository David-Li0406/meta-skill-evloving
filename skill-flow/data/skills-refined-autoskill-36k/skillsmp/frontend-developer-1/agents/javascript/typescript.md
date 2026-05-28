---
name: TypeScript Expert
description: Expert en TypeScript - typage, interfaces, generics et utility types
workflows:
  - id: ts-setup
    template: wf-creation
    phase: Production
    name: Setup TypeScript
    duration: 0.5-1 jour
  - id: ts-migration
    template: wf-refonte
    phase: Migration
    name: Migration JS vers TypeScript
    duration: 5-15 jours
---

# Agent TypeScript

## Responsabilité

Implémenter un typage TypeScript robuste et maintenable pour améliorer la qualité et la documentation du code.

### Ce que je fais
- Définir des types et interfaces appropriés
- Utiliser les generics efficacement
- Appliquer les utility types
- Configurer TypeScript pour le projet

### Ce que je ne fais PAS
- Écrire la logique métier → `javascript-moderne.md`
- Gérer les frameworks spécifiques → `frameworks/`
- Configurer le build → `tooling/`

---

## Tu NE fais PAS

- ❌ Écrire la logique métier JavaScript → `javascript/javascript-moderne`
- ❌ Gérer les frameworks spécifiques (React, Vue, Next) → `frameworks/*`
- ❌ Configurer le build et bundling → `tooling/build-tools`
- ❌ Tester le code → `testing/*`

---

## Types de Base

### Types primitifs

```typescript
// Primitifs
const name: string = 'John';
const age: number = 30;
const isActive: boolean = true;
const data: null = null;
const value: undefined = undefined;

// Arrays
const numbers: number[] = [1, 2, 3];
const strings: Array<string> = ['a', 'b', 'c'];

// Tuples
const pair: [string, number] = ['age', 30];
const triple: [string, number, boolean] = ['John', 30, true];

// Enum
enum Status {
  Pending = 'PENDING',
  Active = 'ACTIVE',
  Completed = 'COMPLETED'
}

// Const enum (inline à la compilation)
const enum Direction {
  Up,
  Down,
  Left,
  Right
}

// Union types
type StringOrNumber = string | number;
type Status = 'pending' | 'active' | 'completed';

// Literal types
type Theme = 'light' | 'dark';
type Size = 'sm' | 'md' | 'lg' | 'xl';
```

### Objects et Interfaces

```typescript
// Interface (extensible, pour objets)
interface User {
  id: string;
  name: string;
  email: string;
  age?: number; // optionnel
  readonly createdAt: Date; // lecture seule
}

// Extension d'interface
interface Admin extends User {
  permissions: string[];
  role: 'admin';
}

// Type alias (pour unions, intersections, mapped types)
type UserOrAdmin = User | Admin;
type UserWithRole = User & { role: string };

// Index signatures
interface Dictionary {
  [key: string]: string;
}

interface NumberMap {
  [key: string]: number;
}

// Record type (préféré pour dictionnaires)
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>;
```

## Generics

### Fonctions génériques

```typescript
// Generic simple
function identity<T>(value: T): T {
  return value;
}

const str = identity('hello'); // type: string
const num = identity(42); // type: number

// Multiple generics
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second];
}

// Generic avec contrainte
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: 'John', age: 30 };
const name = getProperty(user, 'name'); // type: string
const age = getProperty(user, 'age'); // type: number

// Generic avec valeur par défaut
function createArray<T = string>(length: number, value: T): T[] {
  return Array(length).fill(value);
}
```

### Interfaces et Classes génériques

```typescript
// Interface générique
interface Response<T> {
  data: T;
  status: number;
  message: string;
}

interface PaginatedResponse<T> extends Response<T[]> {
  page: number;
  totalPages: number;
  totalItems: number;
}

// Usage
type UserResponse = Response<User>;
type UsersResponse = PaginatedResponse<User>;

// Classe générique
class Repository<T extends { id: string }> {
  private items: Map<string, T> = new Map();

  add(item: T): void {
    this.items.set(item.id, item);
  }

  get(id: string): T | undefined {
    return this.items.get(id);
  }

  getAll(): T[] {
    return Array.from(this.items.values());
  }
}

const userRepo = new Repository<User>();
```

## Utility Types

### Types de transformation

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

// Partial - tous les champs optionnels
type PartialUser = Partial<User>;
// { id?: string; name?: string; email?: string; age?: number; }

// Required - tous les champs requis
type RequiredUser = Required<PartialUser>;

// Readonly - tous les champs en lecture seule
type ReadonlyUser = Readonly<User>;

// Pick - sélectionner certains champs
type UserPreview = Pick<User, 'id' | 'name'>;
// { id: string; name: string; }

// Omit - exclure certains champs
type UserWithoutId = Omit<User, 'id'>;
// { name: string; email: string; age: number; }

// Record - créer un type objet
type UsersByRole = Record<'admin' | 'user', User[]>;

// Exclude - exclure d'une union
type NotAdmin = Exclude<'admin' | 'user' | 'guest', 'admin'>;
// 'user' | 'guest'

// Extract - extraire d'une union
type OnlyAdmin = Extract<'admin' | 'user' | 'guest', 'admin' | 'superadmin'>;
// 'admin'

// NonNullable - exclure null et undefined
type ValidString = NonNullable<string | null | undefined>;
// string

// ReturnType - type de retour d'une fonction
type FetchResult = ReturnType<typeof fetchUser>;

// Parameters - types des paramètres
type FetchParams = Parameters<typeof fetchUser>;

// Awaited - type résolu d'une Promise
type ResolvedUser = Awaited<Promise<User>>;
// User
```

### Mapped Types

```typescript
// Mapped type custom
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

type NullableUser = Nullable<User>;

// Avec modification de clés
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<User>;
// { getId: () => string; getName: () => string; ... }

// Conditional mapped type
type OptionalIfUndefined<T> = {
  [K in keyof T as undefined extends T[K] ? K : never]?: T[K];
} & {
  [K in keyof T as undefined extends T[K] ? never : K]: T[K];
};
```

## Conditional Types

```typescript
// Type conditionnel simple
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false

// Inférence avec infer
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type Unwrapped = UnwrapPromise<Promise<User>>; // User

// Array element type
type ArrayElement<T> = T extends (infer E)[] ? E : never;

type Element = ArrayElement<string[]>; // string

// Function return type custom
type AsyncReturnType<T extends (...args: any) => Promise<any>> =
  T extends (...args: any) => Promise<infer R> ? R : never;
```

## Type Guards

```typescript
// typeof guard
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase(); // value est string
  }
  return value.toFixed(2); // value est number
}

// instanceof guard
function handleError(error: Error | string) {
  if (error instanceof Error) {
    return error.message;
  }
  return error;
}

// in guard
interface Dog {
  bark(): void;
}

interface Cat {
  meow(): void;
}

function speak(animal: Dog | Cat) {
  if ('bark' in animal) {
    animal.bark();
  } else {
    animal.meow();
  }
}

// Custom type guard
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    'email' in value
  );
}

// Usage
function processData(data: unknown) {
  if (isUser(data)) {
    console.log(data.name); // TypeScript sait que c'est un User
  }
}

// Assertion function
function assertIsUser(value: unknown): asserts value is User {
  if (!isUser(value)) {
    throw new Error('Not a valid user');
  }
}
```

## Patterns Avancés

### Discriminated Unions

```typescript
// Tag commun pour discriminer
interface LoadingState {
  status: 'loading';
}

interface SuccessState<T> {
  status: 'success';
  data: T;
}

interface ErrorState {
  status: 'error';
  error: Error;
}

type AsyncState<T> = LoadingState | SuccessState<T> | ErrorState;

function renderState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'loading':
      return 'Loading...';
    case 'success':
      return `Data: ${JSON.stringify(state.data)}`;
    case 'error':
      return `Error: ${state.error.message}`;
  }
}
```

### Template Literal Types

```typescript
type EventName = 'click' | 'focus' | 'blur';
type Handler = `on${Capitalize<EventName>}`;
// 'onClick' | 'onFocus' | 'onBlur'

type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Endpoint = '/users' | '/posts';
type Route = `${HTTPMethod} ${Endpoint}`;
// 'GET /users' | 'GET /posts' | 'POST /users' | ...

// Extraction avec infer
type ExtractParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<`/${Rest}`>
    : T extends `${infer _Start}:${infer Param}`
      ? Param
      : never;

type Params = ExtractParams<'/users/:userId/posts/:postId'>;
// 'userId' | 'postId'
```

## Configuration tsconfig.json

```json
{
  "compilerOptions": {
    // Cible et modules
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],

    // Strictness
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "isolatedModules": true,

    // Output
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",

    // Paths
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },

    // Checks
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Mots-clés de routage

`TypeScript`, `types`, `interface`, `type`, `generic`, `utility types`, `Partial`, `Pick`, `Omit`, `Record`, `conditional types`, `type guard`, `infer`, `tsconfig`, `strict`

## Livrables

| Livrable | Description |
|----------|-------------|
| Types et interfaces | Définitions TypeScript pour le domaine métier et APIs |
| Types génériques | Utility types et helpers de typage réutilisables |
| Configuration tsconfig | Fichier tsconfig.json optimisé avec règles strictes |
