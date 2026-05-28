# Abstraction Decision Examples

Concrete examples of when to abstract and when to duplicate.

## Rule of Three in Action

### Scenario: Display Name Formatting

**First occurrence:**
```tsx
// UserProfile.tsx
<span>{user.firstName} {user.lastName}</span>
```

**Second occurrence:**
```tsx
// UserCard.tsx - DUPLICATE, don't abstract yet
<span>{user.firstName} {user.lastName}</span>
```

**Third occurrence - NOW abstract:**
```tsx
// user-utils.ts
export function getDisplayName(user: User): string {
  return `${user.firstName} ${user.lastName}`;
}
```

### Why Wait?

By the third occurrence, you know:
- The pattern is stable
- The use cases are truly the same
- The abstraction has proven value

## Wrong Abstraction Evolution

### Stage 1: Looks Good
```tsx
function formatUserName(user: User) {
  return `${user.firstName} ${user.lastName}`;
}
```

### Stage 2: First Conditional (Warning)
```tsx
function formatUserName(user: User, includeTitle?: boolean) {
  const name = `${user.firstName} ${user.lastName}`;
  return includeTitle && user.title ? `${user.title} ${name}` : name;
}
```

### Stage 3: More Conditionals (Problem)
```tsx
function formatUserName(
  user: User,
  includeTitle?: boolean,
  lastNameFirst?: boolean,
  abbreviated?: boolean
) {
  let name = '';
  if (lastNameFirst) {
    name = `${user.lastName}, ${user.firstName}`;
  } else {
    name = `${user.firstName} ${user.lastName}`;
  }
  if (abbreviated) {
    name = `${user.firstName[0]}. ${user.lastName}`;
  }
  if (includeTitle && user.title) {
    name = `${user.title} ${name}`;
  }
  return name;
}
```

### Recovery: Back to Duplication
```tsx
// UserProfile.tsx - formal display
`${user.title} ${user.firstName} ${user.lastName}`

// UserCard.tsx - casual display
`${user.firstName} ${user.lastName}`

// UserList.tsx - compact display
`${user.firstName[0]}. ${user.lastName}`
```

Now each caller has exactly what it needs. No conditionals.

## Speculative Generality Examples

### ❌ Over-Engineered (YAGNI Violation)

```typescript
// "We might need different notification channels"
interface NotificationChannel {
  send(message: string): Promise<void>;
}

class EmailChannel implements NotificationChannel { ... }
class SlackChannel implements NotificationChannel { ... }
class SMSChannel implements NotificationChannel { ... }

class NotificationService {
  constructor(private channels: NotificationChannel[]) {}

  async notify(message: string) {
    await Promise.all(this.channels.map(c => c.send(message)));
  }
}

// Usage: only email is ever used
const service = new NotificationService([new EmailChannel()]);
```

### ✅ Pragmatic (YAGNI Applied)

```typescript
// Just send email - that's all we need today
async function sendNotificationEmail(message: string) {
  await emailClient.send({ to: config.notifyEmail, body: message });
}
```

When you actually need Slack, add it then. Don't build the abstraction until you have the second concrete case.

## Abstraction Red Flags

### Red Flag 1: Only One Implementation

```typescript
// Abstract class with single implementation = speculative
abstract class BaseRepository<T> {
  abstract findById(id: string): Promise<T>;
  abstract save(entity: T): Promise<void>;
}

class UserRepository extends BaseRepository<User> { ... }
// No other repositories extend BaseRepository
```

**Fix:** Just write `UserRepository` directly. Add abstraction when you have 3 repositories.

### Red Flag 2: Forwarding Methods

```typescript
// Service that just forwards to repository
class UserService {
  constructor(private repo: UserRepository) {}

  getUser(id: string) { return this.repo.findById(id); }
  saveUser(user: User) { return this.repo.save(user); }
}
```

**Fix:** Call repository directly until service has actual business logic.

### Red Flag 3: Config Objects for Single Use

```typescript
interface ButtonConfig {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
  type?: 'button' | 'submit';
  ariaLabel?: string;
}
```

**Fix:** Props are fine. Config objects make sense when shared across systems, not for single components.

## Good Abstraction Indicators

✅ **Multiple Proven Users**
```typescript
// Three different features use this transformation
function normalizePhoneNumber(phone: string): string {
  return phone.replace(/\D/g, '').slice(-10);
}
```

✅ **Encapsulates Complexity**
```typescript
// Hides retry logic, error handling, auth refresh
async function apiCall<T>(endpoint: string): Promise<T> {
  // Real complexity here justifies the abstraction
}
```

✅ **Prevents Bugs**
```typescript
// Type-safe ID prevents mixing user/order IDs
type UserId = string & { __brand: 'UserId' };
type OrderId = string & { __brand: 'OrderId' };
```

✅ **Emerged from Duplication**
```typescript
// After seeing same pattern 3 times, extracted
function withErrorBoundary<P>(Component: React.ComponentType<P>) {
  return function Wrapped(props: P) {
    return (
      <ErrorBoundary fallback={<ErrorState />}>
        <Component {...props} />
      </ErrorBoundary>
    );
  };
}
```

## The Abstraction Checklist

Before creating any abstraction:

- [ ] Do I have 3+ concrete use cases? (Rule of Three)
- [ ] Are the use cases truly identical, not just similar? (AHA)
- [ ] Does this solve today's problem, not tomorrow's? (YAGNI)
- [ ] Does this keep related code together? (Colocation)
- [ ] Can I explain this abstraction in one sentence?
- [ ] Would a new team member understand why this exists?

If any answer is "no", reconsider.

## Refactoring Wrong Abstractions

When you've inherited a wrong abstraction:

1. **Inline everything** - Copy code back to each caller
2. **Delete the abstraction** - Remove the shared code
3. **Observe the callers** - What do they actually have in common?
4. **Wait** - Let the right abstraction emerge from actual patterns
5. **Extract carefully** - Only what's truly shared
