# Mutation Operators Reference

This document describes all mutation types used in mutation testing.

## Arithmetic Operators

| Original | Mutation | Catches |
|----------|----------|---------|
| `a + b` | `a - b` | Missing arithmetic tests |
| `a - b` | `a + b` | Missing arithmetic tests |
| `a * b` | `a / b` | Missing multiplication tests |
| `a / b` | `a * b` | Missing division tests |
| `a % b` | `a * b` | Missing modulo tests |

**Example:**
```typescript
// Original
const total = price * quantity;

// Mutation
const total = price / quantity;  // Would give wrong result for quantity > 1
```

---

## Comparison Operators

| Original | Mutation | Catches |
|----------|----------|---------|
| `>` | `>=` | Off-by-one errors |
| `>=` | `>` | Boundary conditions |
| `<` | `<=` | Off-by-one errors |
| `<=` | `<` | Boundary conditions |
| `==` | `!=` | Equality checks |
| `===` | `!==` | Strict equality |

**Example:**
```typescript
// Original
if (age >= 18) return "adult";

// Mutation
if (age > 18) return "adult";  // Fails for age === 18
```

---

## Logical Operators

| Original | Mutation | Catches |
|----------|----------|---------|
| `&&` | `\|\|` | Logic errors |
| `\|\|` | `&&` | Logic errors |
| `!condition` | `condition` | Negation errors |
| `true` | `false` | Boolean constants |
| `false` | `true` | Boolean constants |

**Example:**
```typescript
// Original
if (isAdmin && isActive) grantAccess();

// Mutation
if (isAdmin || isActive) grantAccess();  // Grants access to non-admins!
```

---

## Increment/Decrement

| Original | Mutation | Catches |
|----------|----------|---------|
| `++i` | `--i` | Counter errors |
| `--i` | `++i` | Counter errors |
| `i++` | `i--` | Post-increment errors |
| `i--` | `i++` | Post-increment errors |
| `i += n` | `i -= n` | Assignment errors |

---

## Null/Undefined Handling

| Original | Mutation | Catches |
|----------|----------|---------|
| `x ?? default` | `default` | Nullish coalescing |
| `x?.prop` | `x.prop` | Optional chaining |
| `x \|\| default` | `x` | Falsy handling |
| `if (x != null)` | `if (x == null)` | Null checks |

**Example:**
```typescript
// Original
const name = user?.name ?? "Guest";

// Mutation
const name = user.name ?? "Guest";  // Crashes if user is null
```

---

## Return Value Mutations

| Original | Mutation | Catches |
|----------|----------|---------|
| `return x` | `return null` | Return value usage |
| `return true` | `return false` | Boolean returns |
| `return []` | `return null` | Array returns |
| `return ""` | `return "mutated"` | String returns |
| `return 0` | `return 1` | Numeric returns |

**Example:**
```typescript
// Original
function isValid(x) { return x > 0; }

// Mutation
function isValid(x) { return false; }  // If tests pass, validation isn't tested
```

---

## Array/Object Mutations

| Original | Mutation | Catches |
|----------|----------|---------|
| `arr.push(x)` | `arr` (no push) | Array modification |
| `arr[0]` | `arr[1]` | Index access |
| `obj.prop` | `obj.otherProp` | Property access |
| `[...arr]` | `arr` | Spread operator |
| `{...obj}` | `obj` | Object spread |

---

## String Mutations

| Original | Mutation | Catches |
|----------|----------|---------|
| `"string"` | `""` | Empty string handling |
| `str.length` | `0` | Length checks |
| `str.includes(x)` | `true` | String matching |
| `str.includes(x)` | `false` | String matching |

---

## Control Flow Mutations

| Original | Mutation | Catches |
|----------|----------|---------|
| `if (cond) { A }` | `if (cond) { }` | Block execution |
| `if (cond) { A } else { B }` | `if (cond) { B } else { A }` | Branch swap |
| `for (...)` | Remove loop | Loop necessity |
| `break` | Remove break | Loop termination |
| `continue` | Remove continue | Loop continuation |

---

## Exception Mutations

| Original | Mutation | Catches |
|----------|----------|---------|
| `throw new Error(x)` | Remove throw | Error handling |
| `try { A } catch { B }` | `try { A } catch { }` | Catch block |
| `catch (e) { handle(e) }` | `catch (e) { }` | Error handling |

**Example:**
```typescript
// Original
if (!user) throw new Error("User required");

// Mutation
if (!user) { }  // No error thrown, continues with null user
```

---

## Function Call Mutations

| Original | Mutation | Catches |
|----------|----------|---------|
| `fn(a, b)` | `fn(b, a)` | Argument order |
| `fn(a)` | `fn()` | Required arguments |
| `await fn()` | `fn()` | Async handling |
| `fn()` | Remove call | Function necessity |

---

## Priority for Security Code

For auth/security code, prioritize testing these mutations:

1. **Comparison operators** - `>=` vs `>` in permission checks
2. **Logical operators** - `&&` vs `||` in access control
3. **Null handling** - Optional chaining in user checks
4. **Return values** - Boolean returns in validation
5. **Exceptions** - Error throwing in auth failures

---

## Common Surviving Mutants

### 1. Boundary Conditions
```typescript
if (x >= limit)  // Often not tested at exactly limit
```

### 2. Default Values
```typescript
value ?? 'default'  // Default path often untested
```

### 3. Error Paths
```typescript
if (!valid) throw new Error()  // Error branch untested
```

### 4. Empty Collections
```typescript
return items.filter(...)  // Empty result often untested
```

### 5. Async Timing
```typescript
await promise  // Race conditions untested
```
