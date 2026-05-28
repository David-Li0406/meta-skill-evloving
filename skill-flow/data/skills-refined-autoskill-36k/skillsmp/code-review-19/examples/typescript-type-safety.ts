// TypeScript Code Review: Type Safety Patterns
// This file demonstrates type-safe patterns for TypeScript code review.

// =============================================================================
// Discriminated Unions
// =============================================================================

// Pattern: Use discriminated unions for state management
type RequestState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function handleRequestState<T>(state: RequestState<T>): string {
  switch (state.status) {
    case 'idle':
      return 'Ready to load';
    case 'loading':
      return 'Loading...';
    case 'success':
      return `Loaded: ${JSON.stringify(state.data)}`;
    case 'error':
      return `Error: ${state.error.message}`;
  }
  // TypeScript ensures all cases are handled
}

// Pattern: API response handling
type ApiResult<T> = { success: true; data: T } | { success: false; error: string };

function processApiResult<T>(result: ApiResult<T>): T | null {
  if (result.success) {
    return result.data; // TypeScript knows data exists
  }
  console.error(result.error); // TypeScript knows error exists
  return null;
}

// =============================================================================
// Type Guards
// =============================================================================

// Custom type guard
interface Dog {
  type: 'dog';
  bark: () => void;
}

interface Cat {
  type: 'cat';
  meow: () => void;
}

type Animal = Dog | Cat;

function isDog(animal: Animal): animal is Dog {
  return animal.type === 'dog';
}

function makeSound(animal: Animal): void {
  if (isDog(animal)) {
    animal.bark(); // TypeScript knows it's a Dog
  } else {
    animal.meow(); // TypeScript knows it's a Cat
  }
}

// Type guard for API responses
interface User {
  id: string;
  name: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    typeof (value as User).id === 'string' &&
    'name' in value &&
    typeof (value as User).name === 'string' &&
    'email' in value &&
    typeof (value as User).email === 'string'
  );
}

// Array type guard
function isUserArray(value: unknown): value is User[] {
  return Array.isArray(value) && value.every(isUser);
}

// =============================================================================
// Branded Types
// =============================================================================

// Prevent mixing up similar types
type UserId = string & { readonly brand: unique symbol };
type PostId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId;
}

function createPostId(id: string): PostId {
  return id as PostId;
}

function fetchUserById(userId: UserId): Promise<User> {
  // Can't accidentally pass a PostId here
  return fetch(`/api/users/${userId}`).then((r) => r.json());
}

// Example usage:
// const userId = createUserId('user-123');
// const postId = createPostId('post-456');
// fetchUserById(userId); // OK
// fetchUserById(postId); // Type error!

// =============================================================================
// Const Assertions
// =============================================================================

// Without const assertion
const configMutable = {
  endpoint: '/api',
  timeout: 5000,
};
// Type: { endpoint: string; timeout: number }

// With const assertion
const configImmutable = {
  endpoint: '/api',
  timeout: 5000,
} as const;
// Type: { readonly endpoint: "/api"; readonly timeout: 5000 }

// Useful for action types
const ActionTypes = {
  ADD_USER: 'ADD_USER',
  REMOVE_USER: 'REMOVE_USER',
  UPDATE_USER: 'UPDATE_USER',
} as const;

type ActionType = (typeof ActionTypes)[keyof typeof ActionTypes];
// Type: "ADD_USER" | "REMOVE_USER" | "UPDATE_USER"

// =============================================================================
// Template Literal Types
// =============================================================================

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiEndpoint = '/users' | '/posts' | '/comments';

type ApiRoute = `${HttpMethod} ${ApiEndpoint}`;
// Type: "GET /users" | "GET /posts" | "GET /comments" | "POST /users" | ...

// Event handler pattern
type EventName = 'click' | 'focus' | 'blur';
type EventHandler = `on${Capitalize<EventName>}`;
// Type: "onClick" | "onFocus" | "onBlur"

// =============================================================================
// Utility Types
// =============================================================================

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
}

// Partial - all properties optional
type UserUpdate = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Pick - select specific properties
type UserCredentials = Pick<User, 'email' | 'name'>;

// Omit - exclude specific properties
type UserWithoutId = Omit<User, 'id' | 'createdAt'>;

// Record - dictionary type
type UserById = Record<string, User>;

// Readonly - all properties readonly
type ImmutableUser = Readonly<User>;

// Extract - extract types from union
type AdminOrUser = Extract<User['role'], 'admin' | 'moderator'>;

// Exclude - exclude types from union
type NonAdminRole = Exclude<User['role'], 'admin'>;

// =============================================================================
// Mapped Types
// =============================================================================

// Make all properties optional and nullable
type Nullable<T> = {
  [P in keyof T]: T[P] | null;
};

// Make all properties required and non-nullable
type NonNullableProperties<T> = {
  [P in keyof T]-?: NonNullable<T[P]>;
};

// Add prefix to all keys
type Prefixed<T, P extends string> = {
  [K in keyof T as `${P}${string & K}`]: T[K];
};

// Example: Form state
type FormFields = {
  name: string;
  email: string;
  age: number;
};

type FormState = {
  values: FormFields;
  errors: Partial<Record<keyof FormFields, string>>;
  touched: Partial<Record<keyof FormFields, boolean>>;
};

// =============================================================================
// Conditional Types
// =============================================================================

// Extract array element type
type ArrayElement<T> = T extends readonly (infer E)[] ? E : never;

type Users = User[];
type SingleUser = ArrayElement<Users>; // User

// Unwrap Promise
type Awaited<T> = T extends Promise<infer U> ? U : T;

type UserPromise = Promise<User>;
type ResolvedUser = Awaited<UserPromise>; // User

// Function return type extraction
type AsyncReturnType<T extends (...args: unknown[]) => Promise<unknown>> = T extends (
  ...args: unknown[]
) => Promise<infer R>
  ? R
  : never;

// =============================================================================
// Strict Function Types
// =============================================================================

// Proper function parameter types
type Handler<T> = (event: T) => void;

interface ClickEvent {
  type: 'click';
  x: number;
  y: number;
}

interface KeyEvent {
  type: 'key';
  key: string;
}

const handleClick: Handler<ClickEvent> = (event) => {
  console.log(event.x, event.y);
};

const handleKey: Handler<KeyEvent> = (event) => {
  console.log(event.key);
};

// Type-safe event emitter
type EventMap = {
  click: ClickEvent;
  key: KeyEvent;
};

class TypedEventEmitter<T extends Record<string, unknown>> {
  private listeners: { [K in keyof T]?: Array<(event: T[K]) => void> } = {};

  on<K extends keyof T>(event: K, listener: (event: T[K]) => void): void {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event]!.push(listener);
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    this.listeners[event]?.forEach((listener) => listener(data));
  }
}

// Usage
const emitter = new TypedEventEmitter<EventMap>();
emitter.on('click', (e) => console.log(e.x)); // e is ClickEvent
emitter.on('key', (e) => console.log(e.key)); // e is KeyEvent

export {
  handleRequestState,
  processApiResult,
  isDog,
  isUser,
  createUserId,
  createPostId,
  TypedEventEmitter,
};
