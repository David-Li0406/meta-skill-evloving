# Root Cause Tracing

## The Backward Tracing Technique

When an error occurs deep in a call stack, trace BACKWARD to find the original trigger.

## The Process

### Step 1: Start at the Error
```
Error at line 42: Cannot read property 'id' of undefined
```

### Step 2: Ask "What Called This?"
- Look at the stack trace
- Find the immediate caller
- What value did it pass?

### Step 3: Trace the Value Backward
```
Component A → calls → Component B → calls → Component C (error)
                                      ↑
                                 bad value here
                                      ↑
                              where did it come from?
                                      ↑
                              Component B passed it
                                      ↑
                              where did B get it?
                                      ↑
                              Component A passed null
                                      ↑
                              ROOT CAUSE: A fetched data that was empty
```

### Step 4: Fix at the Source
- Don't add null checks at every layer
- Fix WHERE the bad value originated
- Add validation at the SOURCE

## Example: API Data Flow

```typescript
// Error: Cannot read 'items' of undefined

// DON'T: Add null check where it crashes
if (response?.data?.items) { ... }  // Masks the real problem

// DO: Trace backward
// Where does response come from?
// → fetchData() returns it
// Where does fetchData get response?
// → API call that's returning error status
// ROOT CAUSE: API error handling not catching 404

// FIX at source:
async function fetchData() {
  const response = await api.get('/items');
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
  return response.data;
}
```

## When to Use

- Any "undefined" or "null" error
- Any unexpected value in data
- Any "cannot read property X" errors
- When stack trace is more than 2 levels deep

## Key Principle

**Fix at the source, not at the symptom.**

Adding null checks everywhere creates:
- Technical debt
- Hidden bugs
- Mask the real issue
- More code to maintain

Finding the source creates:
- Clean fix
- No hidden issues
- Better code quality
- Understanding of the system
