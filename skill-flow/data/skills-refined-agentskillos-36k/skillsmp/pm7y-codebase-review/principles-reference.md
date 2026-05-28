# Engineering Principles Reference

Detailed guidance for evaluating code against KISS, DRY, POLA, and YAGNI principles.

---

## KISS (Keep It Simple, Stupid)

**Core idea:** The simplest solution that works is usually the best.

### Signs of KISS Violations

**Over-abstraction:**
```csharp
// VIOLATION: Factory for a single implementation
public interface IUserFactory { User Create(UserDto dto); }
public class UserFactory : IUserFactory { ... }
public class UserFactoryProvider { IUserFactory GetFactory() => new UserFactory(); }

// BETTER: Direct instantiation
public User CreateUser(UserDto dto) => new User(dto.Name, dto.Email);
```

**Unnecessary design patterns:**
```typescript
// VIOLATION: Strategy pattern for two fixed options
interface SortStrategy { sort(items: Item[]): Item[] }
class AscendingSort implements SortStrategy { ... }
class DescendingSort implements SortStrategy { ... }
class SortContext { constructor(private strategy: SortStrategy) {} ... }

// BETTER: Simple function
const sortItems = (items: Item[], ascending = true) =>
  [...items].sort((a, b) => ascending ? a.value - b.value : b.value - a.value);
```

**Convoluted control flow:**
```csharp
// VIOLATION: Nested conditions
if (user != null) {
    if (user.IsActive) {
        if (user.HasPermission("read")) {
            return data;
        }
    }
}
return null;

// BETTER: Early returns
if (user == null) return null;
if (!user.IsActive) return null;
if (!user.HasPermission("read")) return null;
return data;
```

### When Complexity Is Justified

- Performance-critical paths with measured bottlenecks
- Genuinely complex domain requirements
- Regulatory or security requirements
- Supporting multiple genuinely different use cases

---

## DRY (Don't Repeat Yourself)

**Core idea:** Every piece of knowledge should have a single, authoritative representation.

### Signs of DRY Violations

**Duplicated logic:**
```typescript
// VIOLATION: Same validation in multiple places
// In UserForm.tsx
const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

// In AdminForm.tsx (copy-pasted)
const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

// BETTER: Shared utility
// In utils/validation.ts
export const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
```

**Repeated configuration:**
```csharp
// VIOLATION: Same connection string in multiple files
// In UserRepository.cs
var connectionString = "Server=localhost;Database=MyDb;...";

// In OrderRepository.cs
var connectionString = "Server=localhost;Database=MyDb;...";

// BETTER: Centralized configuration
// In appsettings.json + DI
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(configuration.GetConnectionString("Default")));
```

**Similar functions with minor variations:**
```typescript
// VIOLATION: Nearly identical fetch functions
async function fetchUsers() {
  const response = await fetch('/api/users');
  if (!response.ok) throw new Error('Failed to fetch');
  return response.json();
}

async function fetchOrders() {
  const response = await fetch('/api/orders');
  if (!response.ok) throw new Error('Failed to fetch');
  return response.json();
}

// BETTER: Generalized function
async function fetchData<T>(endpoint: string): Promise<T> {
  const response = await fetch(`/api/${endpoint}`);
  if (!response.ok) throw new Error(`Failed to fetch ${endpoint}`);
  return response.json();
}
```

### When Duplication Is Acceptable

- **Rule of Three:** Wait until you see the same pattern three times before abstracting
- **Different contexts:** Code that looks similar but serves different purposes
- **Coupling concerns:** When sharing code would create unwanted coupling
- **Clarity:** When abstraction would make code harder to understand

---

## POLA (Principle of Least Astonishment)

**Core idea:** Code should behave as users/developers expect.

### Signs of POLA Violations

**Misleading names:**
```csharp
// VIOLATION: Method does more than name suggests
public User GetUser(int id)
{
    var user = _repository.Find(id);
    user.LastAccessedAt = DateTime.UtcNow; // Unexpected mutation!
    _repository.Save(user);
    return user;
}

// BETTER: Name reflects behavior
public User GetAndUpdateLastAccess(int id) { ... }
// Or: Separate concerns
public User GetUser(int id) => _repository.Find(id);
public void RecordAccess(int userId) { ... }
```

**Unexpected side effects:**
```typescript
// VIOLATION: Getter with side effects
class ShoppingCart {
  get total() {
    this.lastCalculated = new Date(); // Unexpected!
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}

// BETTER: Pure getter
class ShoppingCart {
  get total() {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }

  calculateTotal() {
    this.lastCalculated = new Date();
    return this.total;
  }
}
```

**Non-obvious API design:**
```csharp
// VIOLATION: Boolean parameters with unclear meaning
public void CreateUser(string name, bool flag1, bool flag2, bool flag3) { ... }
CreateUser("John", true, false, true); // What do these mean?

// BETTER: Named parameters or builder
public void CreateUser(UserOptions options) { ... }
CreateUser(new UserOptions {
    Name = "John",
    IsAdmin = true,
    SendWelcomeEmail = false,
    RequireMfa = true
});
```

**Inconsistent return values:**
```typescript
// VIOLATION: Sometimes returns null, sometimes throws
function findUser(id: number): User | null {
  if (id < 0) throw new Error('Invalid ID'); // Throws for invalid input
  return users.find(u => u.id === id) ?? null; // Returns null for not found
}

// BETTER: Consistent behavior
function findUser(id: number): User | null {
  if (id < 0) return null; // Consistent: all "not found" cases return null
  return users.find(u => u.id === id) ?? null;
}

// Or: Always throw for any failure
function getUser(id: number): User {
  if (id < 0) throw new Error('Invalid ID');
  const user = users.find(u => u.id === id);
  if (!user) throw new Error('User not found');
  return user;
}
```

### POLA Guidelines

- Methods named `Get*` should not modify state
- Methods named `Set*` or `Update*` should not return data as primary purpose
- Properties should be cheap and side-effect free
- Boolean parameters should be replaced with enums or option objects
- Error handling should be consistent within a module

---

## YAGNI (You Aren't Gonna Need It)

**Core idea:** Don't implement features until they're actually needed.

### Signs of YAGNI Violations

**Unused code:**
```typescript
// VIOLATION: Implemented "just in case"
export function formatDate(date: Date, format: string): string { ... }
export function formatDateLocalized(date: Date, locale: string): string { ... } // Never used
export function formatDateRange(start: Date, end: Date): string { ... } // Never used
export function formatRelativeDate(date: Date): string { ... } // Never used

// BETTER: Only what's needed
export function formatDate(date: Date, format: string): string { ... }
// Add others when actually needed
```

**Premature abstraction:**
```csharp
// VIOLATION: Interface for single implementation with no plans for more
public interface IEmailService { Task SendAsync(Email email); }
public class SmtpEmailService : IEmailService { ... }
// Plus: IEmailServiceFactory, EmailServiceOptions, EmailServiceBuilder...

// BETTER: Concrete class until abstraction is needed
public class EmailService { public Task SendAsync(Email email) { ... } }
// Add interface when second implementation or testing requires it
```

**Over-configurable systems:**
```typescript
// VIOLATION: Configuration nobody asked for
interface ButtonConfig {
  label: string;
  onClick: () => void;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'primary' | 'secondary' | 'tertiary' | 'ghost' | 'link';
  loading?: boolean;
  disabled?: boolean;
  fullWidth?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
  tooltip?: string;
  analyticsId?: string;
  testId?: string;
  // ... 20 more options
}

// BETTER: What's actually used
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}
// Extend when new requirements arise
```

**Speculative generality:**
```csharp
// VIOLATION: Generic repository for one entity type
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(T entity);
    Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate);
    Task<int> CountAsync();
    Task<bool> ExistsAsync(int id);
    // ... more methods never used
}

// Only used as:
public class UserRepository : IRepository<User> { ... }

// BETTER: Start specific
public class UserRepository
{
    public Task<User?> GetByIdAsync(int id) { ... }
    public Task<User> CreateAsync(User user) { ... }
}
// Generalize when second entity type needs same pattern
```

### YAGNI Guidelines

- Write code for today's requirements, not tomorrow's possibilities
- Delete unused code rather than commenting it out
- Add configuration options only when requested
- Prefer concrete implementations; abstract when you have 2+ variants
- Question "just in case" additions in code review

---

## Balancing Principles

These principles can conflict. Use judgment:

| Situation | Priority |
|-----------|----------|
| Performance-critical code | KISS may yield to optimization |
| Security code | Explicit may be better than DRY |
| API design | POLA is paramount |
| New features | YAGNI first, refactor to DRY later |
| Complex domain | Accept some complexity (KISS doesn't mean trivial) |

**General rule:** Apply the principle that reduces overall cognitive load and maintenance burden.

---

## Detection Checklist

When reviewing code, ask:

**KISS:**
- [ ] Is there a simpler way to achieve this?
- [ ] Would a junior developer understand this?
- [ ] Are there design patterns used where simple code would work?

**DRY:**
- [ ] Have I seen this logic elsewhere?
- [ ] Is this configuration repeated?
- [ ] Could this be a shared utility?

**POLA:**
- [ ] Does the function name describe what it actually does?
- [ ] Are there hidden side effects?
- [ ] Would a new team member be surprised by this behavior?

**YAGNI:**
- [ ] Is this feature currently used?
- [ ] Was this added "just in case"?
- [ ] Is this abstraction earning its complexity cost?
