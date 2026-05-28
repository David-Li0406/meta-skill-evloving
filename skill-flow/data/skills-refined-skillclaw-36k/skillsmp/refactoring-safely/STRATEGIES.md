# Refactoring Strategies

Detailed patterns for extract, inline, rename, and move refactorings.

## Extract Patterns

### Extract Function

**Goal:** Pull code into a named function for reuse and clarity.

**When:**
- Code block is reused
- Function is too long
- Code block needs a descriptive name
- Complex conditional logic

**Steps:**

1. Identify code to extract
2. Determine parameters needed
3. Determine return value
4. Create function signature
5. Copy code to new function
6. Replace original with call
7. Run tests
8. Commit

**Example:**

```typescript
// Before
function createUser(data: UserInput) {
  // Validation block - candidate for extraction
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password too short');
  }
  if (!data.name || data.name.trim().length === 0) {
    throw new Error('Name required');
  }

  // ... rest of function
}

// After
function validateUserInput(data: UserInput): void {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password too short');
  }
  if (!data.name || data.name.trim().length === 0) {
    throw new Error('Name required');
  }
}

function createUser(data: UserInput) {
  validateUserInput(data);
  // ... rest of function
}
```

**Checklist:**
- [ ] New function has clear, descriptive name
- [ ] All required variables passed as parameters
- [ ] Return type is explicit
- [ ] Original logic unchanged
- [ ] Tests still pass

### Extract Class

**Goal:** Group related data and methods into a cohesive unit.

**When:**
- Multiple functions operate on same data
- Data clumps appear together repeatedly
- Feature envy (methods using other class's data)

**Steps:**

1. Identify data that belongs together
2. Identify methods that operate on that data
3. Create new class with data as properties
4. Move methods to new class
5. Update call sites
6. Run tests
7. Commit

**Example:**

```typescript
// Before: Date range logic scattered
function getReportTitle(startDate: Date, endDate: Date) {
  return `Report: ${startDate.toISOString()} - ${endDate.toISOString()}`;
}

function isValidRange(startDate: Date, endDate: Date) {
  return startDate < endDate;
}

function getDaysBetween(startDate: Date, endDate: Date) {
  const diff = endDate.getTime() - startDate.getTime();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

// After: DateRange class
class DateRange {
  constructor(
    public readonly start: Date,
    public readonly end: Date
  ) {}

  isValid(): boolean {
    return this.start < this.end;
  }

  getDaysBetween(): number {
    const diff = this.end.getTime() - this.start.getTime();
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  }

  toString(): string {
    return `${this.start.toISOString()} - ${this.end.toISOString()}`;
  }
}

function getReportTitle(range: DateRange) {
  return `Report: ${range.toString()}`;
}
```

**Checklist:**
- [ ] Class has single responsibility
- [ ] Data and methods are cohesive
- [ ] Old call sites updated
- [ ] Tests still pass

### Extract Module

**Goal:** Split large file into focused modules.

**When:**
- File has multiple distinct responsibilities
- File is too long (>500 lines)
- Parts could be reused independently

**Steps:**

1. Identify cohesive code blocks
2. Create new file with descriptive name
3. Move exports to new file
4. Update imports in original file
5. Update imports in all consumers
6. Run tests
7. Commit

**Example:**

```typescript
// Before: utils.ts with mixed concerns
export function formatDate(d: Date): string { ... }
export function parseDate(s: string): Date { ... }
export function formatCurrency(n: number): string { ... }
export function parseCurrency(s: string): number { ... }
export function validateEmail(e: string): boolean { ... }
export function validatePhone(p: string): boolean { ... }

// After: Split into focused modules

// date-utils.ts
export function formatDate(d: Date): string { ... }
export function parseDate(s: string): Date { ... }

// currency-utils.ts
export function formatCurrency(n: number): string { ... }
export function parseCurrency(s: string): number { ... }

// validators.ts
export function validateEmail(e: string): boolean { ... }
export function validatePhone(p: string): boolean { ... }

// utils.ts (re-exports for backwards compatibility)
export * from './date-utils';
export * from './currency-utils';
export * from './validators';
```

## Inline Patterns

### Inline Function

**Goal:** Remove unnecessary indirection.

**When:**
- Function body is as clear as name
- Function is trivial wrapper
- Function is only called once
- Over-abstraction hurts readability

**Steps:**

1. Find all call sites
2. Replace each call with function body
3. Adjust variable names as needed
4. Remove function definition
5. Run tests
6. Commit

**Example:**

```typescript
// Before: Over-abstracted
function getFullName(user: User): string {
  return formatFullName(user.firstName, user.lastName);
}

function formatFullName(first: string, last: string): string {
  return `${first} ${last}`;
}

// After: Inlined
function getFullName(user: User): string {
  return `${user.firstName} ${user.lastName}`;
}
```

**Checklist:**
- [ ] All call sites updated
- [ ] No remaining references to removed function
- [ ] Code is clearer, not just shorter
- [ ] Tests still pass

### Inline Variable

**Goal:** Remove unnecessary temporary variables.

**When:**
- Variable name adds no clarity
- Variable used only once immediately after assignment
- Expression is simple enough to understand inline

**Steps:**

1. Verify variable is assigned once
2. Replace variable usage with expression
3. Remove variable declaration
4. Run tests
5. Commit

**Example:**

```typescript
// Before
function getDiscount(order: Order): number {
  const basePrice = order.items.reduce((sum, i) => sum + i.price, 0);
  const discountRate = 0.1;
  const discount = basePrice * discountRate;
  return discount;
}

// After
function getDiscount(order: Order): number {
  const basePrice = order.items.reduce((sum, i) => sum + i.price, 0);
  return basePrice * 0.1;
}
```

**Caution:** Don't inline if:
- Expression is complex
- Variable name documents meaning
- Expression has side effects

## Rename Patterns

### Rename Variable/Function

**Goal:** Make code self-documenting with clear names.

**Steps:**

1. Identify all usages (global search)
2. Check for shadowing in inner scopes
3. Rename all occurrences
4. Run tests
5. Commit

**Naming Guidelines:**

| Element | Convention | Examples |
|---------|------------|----------|
| Boolean | `is`, `has`, `should`, `can` | `isValid`, `hasItems`, `shouldRetry` |
| Function | Verb + noun | `createUser`, `validateInput`, `fetchData` |
| Variable | Descriptive noun | `userList`, `orderTotal`, `errorMessage` |
| Constant | UPPER_SNAKE or clear name | `MAX_RETRIES`, `defaultTimeout` |

**Example:**

```typescript
// Before
function proc(d: unknown) {
  const res = validate(d);
  if (res) {
    return transform(d);
  }
  return null;
}

// After
function processUserData(rawData: unknown) {
  const isValid = validateUserData(rawData);
  if (isValid) {
    return transformToUserModel(rawData);
  }
  return null;
}
```

### Rename File

**Goal:** File name matches its primary export or purpose.

**Steps:**

1. Create new file with correct name
2. Copy content to new file
3. Update all imports to use new path
4. Delete old file
5. Run tests
6. Commit

**Or with git (preserves history):**

```bash
git mv src/old-name.ts src/new-name.ts
# Then update imports
```

## Move Patterns

### Move Function

**Goal:** Place function where it belongs (with its data or peers).

**When:**
- Function uses more data from another module
- Function doesn't fit current module's purpose
- Breaking up a large module

**Steps:**

1. Copy function to target module
2. Update function to use new imports
3. Export from target module
4. Update original to re-export (or update all call sites)
5. Remove from original module
6. Run tests
7. Commit

**Example:**

```typescript
// Before: validateEmail in user.ts but only uses string operations
// user.ts
export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// After: Move to validators.ts
// validators.ts
export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// user.ts (re-export for compatibility or update all imports)
export { validateEmail } from './validators';
```

### Move File to Different Directory

**Goal:** Better organize project structure.

**Steps:**

1. Identify new location
2. Move file (`git mv` to preserve history)
3. Update all import paths
4. Update any path-based references (configs, tests)
5. Run tests
6. Commit

**Finding All Imports:**

```bash
# Find files importing the module
rg -l "from ['\"].*old-path" --type ts

# Or with specific file
rg -l "from ['\"].*user-utils" --type ts
```

### Move Class Member

**Goal:** Move field/method to more appropriate class.

**When:**
- Feature envy (method uses another class more)
- Better encapsulation
- Reducing coupling

**Steps:**

1. Create member in target class
2. Update to use target's data
3. Delegate from source to target
4. Update external call sites to use target
5. Remove delegation in source
6. Run tests
7. Commit

## Combining Refactorings

Often you'll chain refactorings. Keep them separate:

```
Commit 1: Extract validateOrder function
Commit 2: Move validateOrder to validators module
Commit 3: Rename validateOrder to validateOrderInput
```

**Not:**
```
Commit 1: Extract, move, and rename validateOrder
```

Benefits of separate commits:
- Easier to review
- Easier to revert if one step fails
- Clear history of changes
- Each step is verified independently
