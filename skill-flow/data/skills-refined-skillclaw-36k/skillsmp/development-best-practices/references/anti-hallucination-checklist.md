---
# Anti-Hallucination Checklist

Specific checks to prevent AI agents from inventing code, APIs, or file structures that don't exist.

---

## Overview

**Problem**: AI agents can confidently assert things that don't exist (hallucination)

**Solution**: Systematic verification before making assertions

**Impact**: Prevents bugs, runtime errors, and wasted debugging time

---

## File and Directory Checks

### Before Reading Files

- [ ] Verify file exists using file system check
- [ ] Verify path is correct (absolute vs relative)
- [ ] Check file permissions (readable)
- [ ] Verify file is not empty (if expected to have content)

**Example**:
```typescript
// ❌ BAD: Assume file exists
const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));

// ✅ GOOD: Check existence first
if (!fs.existsSync('config.json')) {
    throw new Error("config.json not found");
}
const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
```

---

### Before Writing Files

- [ ] Verify parent directory exists
- [ ] Create parent directory if needed
- [ ] Check write permissions
- [ ] Verify not overwriting critical file without confirmation

**Example**:
```typescript
// ❌ BAD: Assume directory exists
fs.writeFileSync('./output/results.json', data);

// ✅ GOOD: Ensure directory exists
const dir = path.dirname('./output/results.json');
if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
}
fs.writeFileSync('./output/results.json', data);
```

---

### Before Importing/Requiring Modules

- [ ] Verify module is installed (check package.json)
- [ ] Verify import path is correct
- [ ] Check module exports expected members
- [ ] Verify version compatibility

**Example**:
```typescript
// ❌ BAD: Assume module exists
import { someFunction } from './utils/helpers';

// ✅ GOOD: Verify module path and exports
// First: Check file exists at ./utils/helpers.ts or ./utils/helpers.js
// Then: Read file to verify someFunction is exported
import { someFunction } from './utils/helpers';
```

---

## API and Function Checks

### Before Calling Functions

- [ ] Read actual function signature from source code
- [ ] Verify function parameters (count, types, order)
- [ ] Check return type matches expectations
- [ ] Verify function is exported/accessible

**Example**:
```typescript
// ❌ BAD: Guess function signature
const result = calculateTotal(items, tax, discount, coupon);

// ✅ GOOD: Read actual signature first
// After reading code: calculateTotal(items: Item[]): number
// (tax, discount, coupon handled via config, not parameters)
const result = calculateTotal(items);
```

---

### Before Accessing Object Properties

- [ ] Verify object exists (not null/undefined)
- [ ] Check property exists on object
- [ ] Verify property type matches expectations
- [ ] Handle optional properties gracefully

**Example**:
```typescript
// ❌ BAD: Assume property exists
console.log(user.profile.bio);

// ✅ GOOD: Check each level
if (user && user.profile && user.profile.bio) {
    console.log(user.profile.bio);
} else {
    console.log("No bio available");
}

// Or use optional chaining
console.log(user?.profile?.bio ?? "No bio available");
```

---

### Before Calling External APIs

- [ ] Verify API endpoint exists (check documentation)
- [ ] Verify request method correct (GET, POST, etc.)
- [ ] Check required parameters
- [ ] Verify authentication requirements
- [ ] Test with actual API call, don't assume response structure

**Example**:
```typescript
// ❌ BAD: Assume API structure
const response = await fetch('/api/users');
const users = response.data.users;  // Assumes response.data.users exists

// ✅ GOOD: Validate response structure
const response = await fetch('/api/users');
const data = await response.json();

if (!data || !Array.isArray(data.users)) {
    throw new Error("Unexpected API response structure");
}
const users = data.users;
```

---

## Configuration and Environment Checks

### Before Using Environment Variables

- [ ] Check environment variable is set
- [ ] Verify value is not empty string
- [ ] Validate format if expected (URL, number, etc.)
- [ ] Provide fallback for optional variables

**Example**:
```typescript
// ❌ BAD: Assume env var exists
const apiUrl = process.env.API_URL;
fetch(apiUrl + '/users');

// ✅ GOOD: Validate env var
const apiUrl = process.env.API_URL;
if (!apiUrl) {
    throw new Error("API_URL environment variable not set");
}
if (!apiUrl.startsWith('http')) {
    throw new Error("API_URL must be a valid HTTP URL");
}
fetch(apiUrl + '/users');
```

---

### Before Using Configuration Files

- [ ] Verify config file exists
- [ ] Parse and validate structure
- [ ] Check required fields present
- [ ] Validate field types and values

**Example**:
```typescript
// ❌ BAD: Assume config structure
const config = require('./config.json');
const port = config.server.port;

// ✅ GOOD: Validate config
const config = require('./config.json');
if (!config.server || typeof config.server.port !== 'number') {
    throw new Error("Invalid config: server.port must be a number");
}
const port = config.server.port;
```

---

## Database and Data Checks

### Before Querying Database

- [ ] Verify connection established
- [ ] Check table/collection exists (if DDL not managed)
- [ ] Validate query syntax
- [ ] Test query returns expected structure

**Example**:
```typescript
// ❌ BAD: Assume table exists
const users = await db.query('SELECT * FROM users');

// ✅ GOOD: Handle query errors
try {
    const users = await db.query('SELECT * FROM users');
    if (!Array.isArray(users)) {
        throw new Error("Query did not return array");
    }
} catch (error) {
    console.error("Database query failed:", error);
    throw new Error("Failed to fetch users");
}
```

---

### Before Processing Query Results

- [ ] Check result is not null/undefined
- [ ] Verify result structure matches expectations
- [ ] Handle empty result sets
- [ ] Validate data types

**Example**:
```typescript
// ❌ BAD: Assume result structure
const user = await db.findOne({ id: userId });
console.log(user.email);

// ✅ GOOD: Validate result
const user = await db.findOne({ id: userId });
if (!user) {
    throw new Error(`User ${userId} not found`);
}
if (!user.email) {
    throw new Error("User record missing email field");
}
console.log(user.email);
```

---

## Third-Party Library Checks

### Before Using Library Functions

- [ ] Read actual library documentation
- [ ] Verify function exists in library version
- [ ] Check function signature in docs
- [ ] Test with simple example first
- [ ] Verify return type/structure

**Example**:
```typescript
// ❌ BAD: Guess library API
import lodash from 'lodash';
const result = lodash.deepMerge(obj1, obj2);  // Function doesn't exist

// ✅ GOOD: Read docs first
// Actual function: _.merge(object, [sources])
import _ from 'lodash';
const result = _.merge({}, obj1, obj2);
```

---

### Before Passing Data to Libraries

- [ ] Verify data format matches library expectations
- [ ] Check required vs optional parameters
- [ ] Validate data types
- [ ] Handle library errors gracefully

---

## Testing and Verification Strategies

### Console.log Verification

```typescript
// Use console.log to verify assumptions
console.log("Type of user:", typeof user);
console.log("User keys:", Object.keys(user || {}));
console.log("API response:", JSON.stringify(response, null, 2));
```

### Type Guards

```typescript
// Use type guards to verify structure
function isUser(obj: any): obj is User {
    return obj
        && typeof obj.id === 'string'
        && typeof obj.email === 'string'
        && typeof obj.name === 'string';
}

if (isUser(data)) {
    // Safe to use data as User
    console.log(data.email);
}
```

### Runtime Validation Libraries

```typescript
// Use Zod for runtime validation
import { z } from 'zod';

const UserSchema = z.object({
    id: z.string(),
    email: z.string().email(),
    name: z.string(),
    age: z.number().optional()
});

// Validates and throws if invalid
const user = UserSchema.parse(apiResponse);
```

---

## Common Hallucination Patterns

### Pattern 1: Invented Function Parameters

**Hallucination**: Adding parameters that don't exist

```typescript
// ❌ Hallucinated: function doesn't take these parameters
calculateTotal(items, tax, discount);
```

**Reality Check**: Read actual function signature

```typescript
// ✅ Actual function signature
function calculateTotal(items: Item[]): number
```

---

### Pattern 2: Invented Object Properties

**Hallucination**: Accessing properties that don't exist

```typescript
// ❌ Hallucinated: response doesn't have these properties
const name = response.data.user.fullName;
```

**Reality Check**: Log actual response structure

```typescript
// ✅ Check actual structure
console.log(JSON.stringify(response, null, 2));
// Shows: response = { user: { first_name: "John", last_name: "Doe" } }
const name = `${response.user.first_name} ${response.user.last_name}`;
```

---

### Pattern 3: Invented API Endpoints

**Hallucination**: Calling endpoints that don't exist

```typescript
// ❌ Hallucinated: endpoint doesn't exist
await api.post('/users/create', userData);
```

**Reality Check**: Read API documentation

```typescript
// ✅ Actual endpoint from docs
await api.post('/users', userData);
```

---

### Pattern 4: Invented Configuration Keys

**Hallucination**: Using config keys that don't exist

```typescript
// ❌ Hallucinated: config key doesn't exist
const timeout = config.api.requestTimeout;
```

**Reality Check**: Read config file

```typescript
// ✅ Actual config structure
// config = { api: { timeout: 5000 } }
const timeout = config.api.timeout;
```

---

## Prevention Workflow

### Before Writing Code

1. **Read actual source code** - Don't guess
2. **Check documentation** - Use official docs
3. **Test assumptions** - Console.log, debugger
4. **Verify with simple example** - Test small piece first
5. **Document findings** - Note actual signatures/structures

### During Implementation

1. **Incremental verification** - Test each assumption
2. **Early validation** - Catch errors immediately
3. **Error-first approach** - Handle errors before happy path
4. **Type checking** - Use TypeScript, runtime validation
5. **Defensive coding** - Assume things can fail

### After Implementation

1. **Review assumptions** - Did I verify everything?
2. **Test edge cases** - Null, undefined, empty, invalid
3. **Error scenarios** - What if API fails? File missing?
4. **Integration testing** - Does it work with real data?
5. **Documentation** - Note any deviations from assumptions

---

## Anti-Hallucination Tools

### Static Analysis

- **TypeScript** - Catch type errors at compile time
- **ESLint** - Catch common mistakes
- **Prettier** - Consistent formatting reveals issues

### Runtime Validation

- **Zod** - Runtime schema validation
- **Joi** - Data validation
- **class-validator** - Class-based validation

### Testing

- **Jest** - Unit tests catch incorrect assumptions
- **Testing Library** - Integration tests verify actual behavior
- **Supertest** - API tests verify endpoints exist

---

## Checklist Summary

Before committing code, verify:

- [ ] All file paths verified to exist
- [ ] All function signatures read from actual code
- [ ] All API endpoints verified in documentation
- [ ] All object properties checked for existence
- [ ] All configuration keys verified in config files
- [ ] All environment variables validated
- [ ] All third-party library functions verified in docs
- [ ] All database queries tested with actual data
- [ ] Error handling for all risky operations
- [ ] Type checking or runtime validation in place

---

**Last Updated**: 2025-01-30
