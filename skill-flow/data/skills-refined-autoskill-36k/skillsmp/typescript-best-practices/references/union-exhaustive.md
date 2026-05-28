# Union Types & Exhaustive Handling

> **When to use:** For defining types that can be one of several distinct shapes (e.g., for states, events, or API responses) and ensuring all cases are handled at compile time.

## Discriminated Unions

Use a common literal property to enable type narrowing:

```typescript
// DO: Discriminated union with literal discriminator
type Result<TData, TError> =
  | { success: true; data: TData }
  | { success: false; error: TError };

function handleResult(result: Result<User, string>) {
  if (result.success) {
    // TypeScript knows: result.data is User
    console.log(result.data.name);
  } else {
    // TypeScript knows: result.error is string
    console.error(result.error);
  }
}

// DO: Use 'type' or 'kind' as discriminator for events/actions
type Action =
  | { type: 'INCREMENT'; amount: number }
  | { type: 'DECREMENT'; amount: number }
  | { type: 'RESET' };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'INCREMENT':
      return state + action.amount;
    case 'DECREMENT':
      return state - action.amount;
    case 'RESET':
      return 0;
  }
}
```

**Best practices:**
- Use `type`, `kind`, or `status` as discriminator names
- Discriminator values should be string literals for readability
- Use `satisfies never` for exhaustive handling (see below)

## Exhaustive Handling

Use `satisfies never` to ensure all cases are handled. TypeScript will error if any case is missed.

### Switch Statement

```typescript
type Route = '/home' | '/about' | '/contact';

function handleRoute(route: Route) {
  switch (route) {
    case '/home':
      return <HomePage />;
    case '/about':
      return <AboutPage />;
    case '/contact':
      return <ContactPage />;
    default:
      route satisfies never; // Error if any route is unhandled
  }
}
```

### Ternary with IIFE

For ternary expressions, use an IIFE to add exhaustive check:

```typescript
type MessageType = 'error' | 'warning' | 'info';

const Component = messageType === 'error'
  ? ErrorMessage
  : messageType === 'warning'
  ? WarningMessage
  : messageType === 'info'
  ? InfoMessage
  : (() => {
      messageType satisfies never;
      throw new Error(`Unknown message type: ${messageType}`);
    })();
```

### Partial Exhaustive (Subset Handling)

When you need to handle a subset of types and explicitly allow others to pass through:

```typescript
type ActionType = 'create' | 'update' | 'delete' | 'login' | 'signUp';

// Define which actions bypass normal handling
type PassthroughActions = readonly ['login', 'signUp'];
const passthroughActions: PassthroughActions = ['login', 'signUp'] satisfies ReadonlyArray<ActionType>;
type PassthroughAction = PassthroughActions[number];

function handleAction(actionType: ActionType) {
  switch (actionType) {
    case 'create':
      return createItem();
    case 'update':
      return updateItem();
    case 'delete':
      return deleteItem();
    default:
      // Ensure only PassthroughActions reach here, not forgotten cases
      actionType satisfies PassthroughAction;
      return handlePassthrough(actionType);
  }
}
```

If you add a new `ActionType` but forget to handle it, the `satisfies PassthroughAction` will error unless you explicitly add it to `PassthroughActions`.
