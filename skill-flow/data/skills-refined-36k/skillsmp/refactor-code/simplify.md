# Code Simplification

Simplifies verbose, nested, or complicated logic while preserving exact behavior.

## Simplification Patterns

### Early Returns (Guard Clauses)

```javascript
// Before
function process(data) {
  if (data) {
    if (data.isValid) {
      if (data.items.length > 0) {
        return result;
      }
    }
  }
  return null;
}

// After
function process(data) {
  if (!data) return null;
  if (!data.isValid) return null;
  if (data.items.length === 0) return null;
  return result;
}
```

### Simplify Conditionals

**Unnecessary else after return:**
```javascript
// Before
if (condition) {
  return x;
} else {
  return y;
}

// After
if (condition) return x;
return y;
```

**Boolean returns:**
```javascript
// Before
if (value > 10) { return true; } else { return false; }

// After
return value > 10;
```

### Reduce Nesting

**Extract conditions into well-named variables:**
```javascript
// Before
if (user.age >= 18 && user.hasVerifiedEmail && !user.isBanned) { ... }

// After
const canAccess = user.age >= 18 && user.hasVerifiedEmail && !user.isBanned;
if (canAccess) { ... }
```

### Use Modern Syntax

**Optional chaining:**
```javascript
// Before
const name = user && user.profile && user.profile.name;

// After
const name = user?.profile?.name;
```

**Nullish coalescing:**
```javascript
// Before
const value = data !== null && data !== undefined ? data : defaultValue;

// After
const value = data ?? defaultValue;
```

**Destructuring:**
```javascript
// Before
const name = props.name;
const age = props.age;

// After
const { name, age } = props;
```

### Simplify Loops

```javascript
// Before
const results = [];
for (let i = 0; i < items.length; i++) {
  if (items[i].isActive) {
    results.push(items[i].name);
  }
}

// After
const results = items.filter(i => i.isActive).map(i => i.name);
```

### Remove Redundancy

```javascript
// Before
const temp = calculateValue();
return temp;

// After
return calculateValue();
```

## Guidelines

- **Preserve behavior exactly**
- **Match surrounding style**: If codebase doesn't use arrow functions, don't introduce them
- **Don't over-simplify**: Readability > cleverness
- **Consider debugging**: Ternaries and chained methods are harder to debug
