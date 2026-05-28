---
name: javascript-excellence
description: JavaScript and TypeScript best practices inspired by DHH's philosophy - writing elegant, maintainable, and expressive code
---

# JavaScript Excellence

This skill embodies DHH's coding philosophy adapted for JavaScript and TypeScript - emphasizing clarity, simplicity, and expressiveness.

## Core Principles

1. **Clarity over Cleverness**: Code should be obvious, not clever
2. **Simplicity over Complexity**: The simplest solution is usually the best
3. **Expressiveness**: Code should read like prose
4. **DRY (Don't Repeat Yourself)**: Eliminate duplication ruthlessly
5. **Convention over Configuration**: Sensible defaults, customize when needed
6. **No Premature Abstraction**: Wait until patterns emerge

## Language Best Practices

### Use Modern JavaScript Features

✅ **Do use modern syntax:**
```typescript
// Destructuring
const { name, email } = user;

// Spread operators
const newUser = { ...user, verified: true };

// Optional chaining
const street = user?.address?.street;

// Nullish coalescing
const name = user.name ?? "Anonymous";

// Template literals
const greeting = `Hello, ${name}!`;
```

❌ **Don't write old-style code:**
```typescript
// Don't
var name = user.name ? user.name : "Anonymous";
var newUser = Object.assign({}, user, { verified: true });
```

### Prefer Const and Let

✅ **Do use const by default:**
```typescript
const users = await getUsers();
const total = users.length;
```

❌ **Don't use var:**
```typescript
var users = await getUsers();  // No!
```

### Use Meaningful Names

✅ **Do use descriptive names:**
```typescript
async function sendWelcomeEmail(user: User) {
  const emailContent = buildWelcomeEmail(user);
  await emailService.send(emailContent);
}
```

❌ **Don't use cryptic abbreviations:**
```typescript
async function sndWlcmEml(u: User) {  // What?
  const ec = bldWlcmEml(u);
  await es.snd(ec);
}
```

## TypeScript Best Practices

### Use Type Inference

✅ **Do let TypeScript infer:**
```typescript
const users = await db.user.findMany();  // Type is inferred
const count = users.length;               // Type is inferred

function double(n: number) {
  return n * 2;  // Return type inferred as number
}
```

❌ **Don't over-specify:**
```typescript
const users: User[] = await db.user.findMany();  // Redundant
const count: number = users.length;               // Redundant

function double(n: number): number {  // Return type unnecessary
  return n * 2;
}
```

### Use Discriminated Unions for State

✅ **Do model states explicitly:**
```typescript
type LoadingState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function render(state: LoadingState<User>) {
  switch (state.status) {
    case "idle":
      return <div>Not started</div>;
    case "loading":
      return <div>Loading...</div>;
    case "success":
      return <div>{state.data.name}</div>;  // data is available!
    case "error":
      return <div>Error: {state.error.message}</div>;
  }
}
```

❌ **Don't use boolean flags:**
```typescript
type LoadingState<T> = {
  isLoading: boolean;
  isError: boolean;
  data?: T;
  error?: Error;
};
// Can have invalid states like isLoading=true and isError=true
```

### Keep Types Simple

✅ **Do use simple types:**
```typescript
type User = {
  id: string;
  name: string;
  email: string;
};

type CreateUserInput = Pick<User, "name" | "email">;
```

❌ **Don't over-engineer types:**
```typescript
type DeepPartial<T> = T extends object
  ? { [P in keyof T]?: DeepPartial<T[P]> }
  : T;

type RecursiveRequired<T> = {
  [P in keyof T]-?: RecursiveRequired<T[P]>;
};
// Unless you really need this complexity!
```

## Function Patterns

### Keep Functions Small and Focused

✅ **Do write focused functions:**
```typescript
async function createUser(data: CreateUserInput) {
  const hashedPassword = await hashPassword(data.password);
  const user = await db.user.create({
    data: { ...data, password: hashedPassword }
  });
  await sendWelcomeEmail(user);
  return user;
}

async function hashPassword(password: string) {
  return bcrypt.hash(password, 10);
}

async function sendWelcomeEmail(user: User) {
  // Email logic here
}
```

❌ **Don't write giant functions:**
```typescript
async function createUser(data: CreateUserInput) {
  // 200 lines of mixed concerns
  // password hashing
  // validation
  // database access
  // email sending
  // logging
  // etc.
}
```

### Use Early Returns

✅ **Do use guard clauses:**
```typescript
function processPayment(amount: number, user: User) {
  if (amount <= 0) {
    throw new Error("Invalid amount");
  }
  
  if (!user.paymentMethod) {
    throw new Error("No payment method");
  }
  
  if (user.balance < amount) {
    throw new Error("Insufficient balance");
  }
  
  // Happy path at the end
  return chargePayment(user, amount);
}
```

❌ **Don't nest deeply:**
```typescript
function processPayment(amount: number, user: User) {
  if (amount > 0) {
    if (user.paymentMethod) {
      if (user.balance >= amount) {
        return chargePayment(user, amount);
      } else {
        throw new Error("Insufficient balance");
      }
    } else {
      throw new Error("No payment method");
    }
  } else {
    throw new Error("Invalid amount");
  }
}
```

### Use Async/Await Consistently

✅ **Do use async/await:**
```typescript
async function loadUserData(userId: string) {
  const user = await db.user.findUnique({ where: { id: userId } });
  const posts = await db.post.findMany({ where: { userId } });
  return { user, posts };
}
```

❌ **Don't mix promises and async/await:**
```typescript
async function loadUserData(userId: string) {
  const user = await db.user.findUnique({ where: { id: userId } });
  return db.post.findMany({ where: { userId } }).then(posts => {
    return { user, posts };
  });
}
```

## Object and Array Patterns

### Use Destructuring

✅ **Do destructure:**
```typescript
function createPost({ title, content, authorId }: CreatePostInput) {
  return db.post.create({
    data: { title, content, authorId }
  });
}

const { name, email } = user;
const [first, second, ...rest] = items;
```

### Use Array Methods

✅ **Do use functional array methods:**
```typescript
const activeUsers = users.filter(u => u.active);
const userNames = users.map(u => u.name);
const totalScore = scores.reduce((sum, score) => sum + score, 0);
const hasAdmin = users.some(u => u.role === "admin");
```

❌ **Don't use for loops unnecessarily:**
```typescript
const activeUsers = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].active) {
    activeUsers.push(users[i]);
  }
}
```

### Use Object Methods

✅ **Do use Object methods:**
```typescript
const keys = Object.keys(user);
const values = Object.values(user);
const entries = Object.entries(user);

const merged = Object.assign({}, defaults, overrides);
// Or better:
const merged = { ...defaults, ...overrides };
```

## Error Handling

### Use Try-Catch for Async

✅ **Do handle errors:**
```typescript
async function getUser(id: string) {
  try {
    return await db.user.findUnique({ where: { id } });
  } catch (error) {
    logger.error("Failed to fetch user", { error, id });
    throw new Error("User not found");
  }
}
```

### Create Custom Errors

✅ **Do use custom error classes:**
```typescript
class NotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "NotFoundError";
  }
}

class ValidationError extends Error {
  constructor(message: string, public fields: string[]) {
    super(message);
    this.name = "ValidationError";
  }
}

// Usage
if (!user) {
  throw new NotFoundError("User not found");
}
```

## Code Organization

### Group Related Code

✅ **Do organize by feature:**
```
src/
  features/
    auth/
      login.ts
      signup.ts
      session.ts
    posts/
      create.ts
      list.ts
      edit.ts
```

❌ **Don't organize by type:**
```
src/
  controllers/
    authController.ts
    postController.ts
  services/
    authService.ts
    postService.ts
  models/
    user.ts
    post.ts
```

### Extract Reusable Logic

✅ **Do extract when patterns emerge:**
```typescript
// After seeing this pattern 3+ times
function requireAuth<T>(
  handler: (userId: string, input: T) => Promise<Response>
) {
  return async (input: T) => {
    const userId = await getUserId();
    if (!userId) {
      throw redirect("/login");
    }
    return handler(userId, input);
  };
}

// Use it
export const loader = requireAuth(async (userId, { params }) => {
  // userId is guaranteed to exist
});
```

❌ **Don't abstract too early:**
```typescript
// Don't create "BaseController" after one use
class BaseController {
  // Generic abstraction nobody asked for
}
```

## Comments and Documentation

### Write Self-Documenting Code

✅ **Do write clear code:**
```typescript
function calculateTotalPrice(items: CartItem[]) {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const tax = subtotal * TAX_RATE;
  return subtotal + tax;
}
```

❌ **Don't comment obvious code:**
```typescript
// Calculate total price
function calc(items: CartItem[]) {
  // Sum all items
  const s = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  // Calculate tax
  const t = s * TAX_RATE;
  // Return total
  return s + t;
}
```

### Comment the "Why", Not the "What"

✅ **Do explain reasoning:**
```typescript
// We disable scroll lock on mobile because iOS Safari has issues
// with position:fixed when the keyboard is open. See issue #123
if (isMobile) {
  disableScrollLock();
}
```

❌ **Don't state the obvious:**
```typescript
// Check if mobile
if (isMobile) {
  // Disable scroll lock
  disableScrollLock();
}
```

## Testing Patterns

### Write Readable Tests

✅ **Do write clear tests:**
```typescript
test("creates user with hashed password", async () => {
  const input = { email: "test@example.com", password: "secret123" };
  
  const user = await createUser(input);
  
  expect(user.email).toBe(input.email);
  expect(user.password).not.toBe(input.password);
  expect(await verifyPassword(input.password, user.password)).toBe(true);
});
```

### Test Behavior, Not Implementation

✅ **Do test outcomes:**
```typescript
test("returns 404 when post not found", async () => {
  const response = await app.request("/posts/invalid-id");
  expect(response.status).toBe(404);
});
```

❌ **Don't test internals:**
```typescript
test("calls database with correct query", async () => {
  const spy = vi.spyOn(db, "query");
  await getPost("123");
  expect(spy).toHaveBeenCalledWith({ id: "123" });
});
```

## Anti-Patterns to Avoid

### 1. Callback Hell

❌ **Don't nest callbacks:**
```typescript
getUser(userId, (error, user) => {
  if (error) return handleError(error);
  getPosts(user.id, (error, posts) => {
    if (error) return handleError(error);
    // ...more nesting
  });
});
```

✅ **Do use async/await:**
```typescript
const user = await getUser(userId);
const posts = await getPosts(user.id);
```

### 2. Mutation Everywhere

❌ **Don't mutate unnecessarily:**
```typescript
function addItem(cart: Cart, item: Item) {
  cart.items.push(item);  // Mutates input
  return cart;
}
```

✅ **Do prefer immutability:**
```typescript
function addItem(cart: Cart, item: Item) {
  return {
    ...cart,
    items: [...cart.items, item]
  };
}
```

### 3. God Objects

❌ **Don't create giant classes:**
```typescript
class UserManager {
  createUser() {}
  updateUser() {}
  deleteUser() {}
  authenticateUser() {}
  sendEmail() {}
  generateReport() {}
  // 50 more methods...
}
```

✅ **Do use focused modules:**
```typescript
// user.ts
export function createUser() {}
export function updateUser() {}

// auth.ts
export function authenticate() {}

// email.ts
export function sendEmail() {}
```

## Remember

DHH's philosophy in JavaScript:
- Write code that reads naturally
- Prefer simplicity over cleverness
- Eliminate duplication
- Keep functions small and focused
- Use the language's features effectively
- Don't abstract too early
- Make invalid states unrepresentable
- Test behavior, not implementation

Your code should be a joy to read and maintain.
