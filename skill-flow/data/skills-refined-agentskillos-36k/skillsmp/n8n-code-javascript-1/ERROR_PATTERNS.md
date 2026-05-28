# Error Patterns - JavaScript Code Node

Complete guide to avoiding the most common Code node errors.

---

## Overview

This guide covers the **top 5 error patterns** encountered in n8n Code nodes. Understanding and avoiding these errors will save you significant debugging time.

**Error Frequency**:
1. Empty Code / Missing Return - **38% of failures**
2. Expression Syntax Confusion - **8% of failures**
3. Incorrect Return Wrapper - **5% of failures**
4. Unmatched Expression Brackets - **6% of failures**
5. Missing Null Checks - **Common runtime error**

---

## Error #1: Empty Code or Missing Return Statement

**Frequency**: Most common error (38% of all validation failures)

**What Happens**:
- Workflow execution fails
- Next nodes receive no data
- Error: "Code cannot be empty" or "Code must return data"

### The Problem

```javascript
// ❌ ERROR: No code at all
// (Empty code field)
```

```javascript
// ❌ ERROR: Code executes but doesn't return anything
const items = $input.all();

// Process items
for (const item of items) {
  console.log(item.json.name);
}

// Forgot to return!
```

```javascript
// ❌ ERROR: Early return path exists, but not all paths return
const items = $input.all();

if (items.length === 0) {
  return [];  // ✅ This path returns
}

// Process items
const processed = items.map(item => ({json: item.json}));

// ❌ Forgot to return processed!
```

### The Solution

```javascript
// ✅ CORRECT: Always return data
const items = $input.all();

// Process items
const processed = items.map(item => ({
  json: {
    ...item.json,
    processed: true
  }
}));

return processed;  // ✅ Return statement present
```

```javascript
// ✅ CORRECT: Return empty array if no items
const items = $input.all();

if (items.length === 0) {
  return [];  // Valid: empty array when no data
}

// Process and return
return items.map(item => ({json: item.json}));
```

```javascript
// ✅ CORRECT: All code paths return
const items = $input.all();

if (items.length === 0) {
  return [];
} else if (items.length === 1) {
  return [{json: {single: true, data: items[0].json}}];
} else {
  return items.map(item => ({json: item.json}));
}

// All paths covered
```

### Checklist

- [ ] Code field is not empty
- [ ] Return statement exists
- [ ] ALL code paths return data (if/else branches)
- [ ] Return format is correct (`[{json: {...}}]`)
- [ ] Return happens even on errors (use try-catch)

---

## Error #2: Expression Syntax Confusion

**Frequency**: 8% of validation failures

**What Happens**:
- Syntax error in code execution
- Error: "Unexpected token" or "Expression syntax is not valid in Code nodes"
- Template variables not evaluated

### The Problem

n8n has TWO distinct syntaxes:
1. **Expression syntax** `{{ }}` - Used in OTHER nodes (Set, IF, HTTP Request)
2. **JavaScript** - Used in CODE nodes (no `{{ }}`)

Many developers mistakenly use expression syntax inside Code nodes.

```javascript
// ❌ WRONG: Using n8n expression syntax in Code node
const userName = "{{ $json.name }}";
const userEmail = "{{ $json.body.email }}";

return [{
  json: {
    name: userName,
    email: userEmail
  }
}];

// Result: Literal string "{{ $json.name }}", NOT the value!
```

```javascript
// ❌ WRONG: Trying to evaluate expressions
const value = "{{ $now.toFormat('yyyy-MM-dd') }}";
```

### The Solution

```javascript
// ✅ CORRECT: Use JavaScript directly (no {{ }})
const userName = $json.name;
const userEmail = $json.body.email;

return [{
  json: {
    name: userName,
    email: userEmail
  }
}];
```

```javascript
// ✅ CORRECT: JavaScript template literals (use backticks)
const message = `Hello, ${$json.name}! Your email is ${$json.email}`;

return [{
  json: {
    greeting: message
  }
}];
```

```javascript
// ✅ CORRECT: Direct variable access
const item = $input.first().json;

return [{
  json: {
    name: item.name,
    email: item.email,
    timestamp: new Date().toISOString()  // JavaScript Date, not {{ }}
  }
}];
```

### Comparison Table

| Context | Syntax | Example |
|---------|--------|---------|
| Set node | `{{ }}` expressions | `{{ $json.name }}` |
| IF node | `{{ }}` expressions | `{{ $json.age > 18 }}` |
| HTTP Request URL | `{{ }}` expressions | `{{ $json.userId }}` |
| **Code node** | **JavaScript** | `$json.name` |
| **Code node strings** | **Template literals** | `` `Hello ${$json.name}` `` |

### Quick Fix Guide

```javascript
// WRONG → RIGHT conversions

// ❌ "{{ $json.field }}"
// ✅ $json.field

// ❌ "{{ $now }}"
// ✅ new Date().toISOString()

// ❌ "{{ $node['HTTP Request'].json.data }}"
// ✅ $node["HTTP Request"].json.data

// ❌ `{{ $json.firstName }} {{ $json.lastName }}`
// ✅ `${$json.firstName} ${$json.lastName}`
```

---

## Error #3: Incorrect Return Wrapper Format

**Frequency**: 5% of validation failures

**What Happens**:
- Error: "Return value must be an array of objects"
- Error: "Each item must have a json property"
- Next nodes receive malformed data

### The Problem

Code nodes MUST return:
- **Array** of objects
- Each object MUST have a **`json` property**

```javascript
// ❌ WRONG: Returning object instead of array
return {
  json: {
    result: 'success'
  }
};
// Missing array wrapper []
```

```javascript
// ❌ WRONG: Returning array without json wrapper
return [
  {id: 1, name: 'Alice'},
  {id: 2, name: 'Bob'}
];
// Missing json property
```

```javascript
// ❌ WRONG: Returning plain value
return "processed";
```

```javascript
// ❌ WRONG: Returning items without mapping
return $input.all();
// Works if items already have json property, but not guaranteed
```

```javascript
// ❌ WRONG: Incomplete structure
return [{data: {result: 'success'}}];
// Should be {json: {...}}, not {data: {...}}
```

### The Solution

```javascript
// ✅ CORRECT: Single result
return [{
  json: {
    result: 'success',
    timestamp: new Date().toISOString()
  }
}];
```

```javascript
// ✅ CORRECT: Multiple results
return [
  {json: {id: 1, name: 'Alice'}},
  {json: {id: 2, name: 'Bob'}},
  {json: {id: 3, name: 'Carol'}}
];
```

```javascript
// ✅ CORRECT: Transforming array
const items = $input.all();

return items.map(item => ({
  json: {
    id: item.json.id,
    name: item.json.name,
    processed: true
  }
}));
```

```javascript
// ✅ CORRECT: Empty result
return [];
// Valid when no data to return
```

```javascript
// ✅ CORRECT: Conditional returns
if (shouldProcess) {
  return [{json: {result: 'processed'}}];
} else {
  return [];
}
```

### Return Format Checklist

- [ ] Return value is an **array** `[...]`
- [ ] Each array element has **`json` property**
- [ ] Structure is `[{json: {...}}]` or `[{json: {...}}, {json: {...}}]`
- [ ] NOT `{json: {...}}` (missing array wrapper)
- [ ] NOT `[{...}]` (missing json property)

### Common Scenarios

```javascript
// Scenario 1: Single object from API
const response = $input.first().json;

// ✅ CORRECT
return [{json: response}];

// ❌ WRONG
return {json: response};


// Scenario 2: Array of objects
const users = $input.all();

// ✅ CORRECT
return users.map(user => ({json: user.json}));

// ❌ WRONG
return users;  // Risky - depends on existing structure


// Scenario 3: Computed result
const total = $input.all().reduce((sum, item) => sum + item.json.amount, 0);

// ✅ CORRECT
return [{json: {total}}];

// ❌ WRONG
return {total};


// Scenario 4: No results
// ✅ CORRECT
return [];

// ❌ WRONG
return null;
```

---

## Error #4: Unmatched Expression Brackets

**Frequency**: 6% of validation failures

**What Happens**:
- Parsing error during save
- Error: "Unmatched expression brackets"
- Code appears correct but fails validation

### The Problem

This error typically occurs when:
1. Strings contain unbalanced quotes
2. Multi-line strings with special characters
3. Template literals with nested brackets

```javascript
// ❌ WRONG: Unescaped quote in string
const message = "It's a nice day";
// Single quote breaks string
```

```javascript
// ❌ WRONG: Unbalanced brackets in regex
const pattern = /\{(\w+)\}/;  // JSON storage issue
```

```javascript
// ❌ WRONG: Multi-line string with quotes
const html = "
  <div class="container">
    <p>Hello</p>
  </div>
";
// Quote balance issues
```

### The Solution

```javascript
// ✅ CORRECT: Escape quotes
const message = "It\\'s a nice day";
// Or use different quotes
const message = "It's a nice day";  // Double quotes work
```

```javascript
// ✅ CORRECT: Escape regex properly
const pattern = /\\{(\\w+)\\}/;
```

```javascript
// ✅ CORRECT: Template literals for multi-line
const html = `
  <div class="container">
    <p>Hello</p>
  </div>
`;
// Backticks handle multi-line and quotes
```

```javascript
// ✅ CORRECT: Escape backslashes
const path = "C:\\\\Users\\\\Documents\\\\file.txt";
```

### Escaping Guide

| Character | Escape As | Example |
|-----------|-----------|---------|
| Single quote in single-quoted string | `\\'` | `'It\\'s working'` |
| Double quote in double-quoted string | `\\"` | `"She said \\"hello\\""` |
| Backslash | `\\\\` | `"C:\\\\path"` |
| Newline | `\\n` | `"Line 1\\nLine 2"` |
| Tab | `\\t` | `"Column1\\tColumn2"` |

### Best Practices

```javascript
// ✅ BEST: Use template literals for complex strings
const message = `User ${name} said: "Hello!"`;

// ✅ BEST: Use template literals for HTML
const html = `
  <div class="${className}">
    <h1>${title}</h1>
    <p>${content}</p>
  </div>
`;

// ✅ BEST: Use template literals for JSON
const jsonString = `{
  "name": "${name}",
  "email": "${email}"
}`;
```

---

## Error #5: Missing Null Checks / Undefined Access

**Frequency**: Very common runtime error

**What Happens**:
- Workflow execution stops
- Error: "Cannot read property 'X' of undefined"
- Error: "Cannot read property 'X' of null"
- Crashes on missing data

### The Problem

```javascript
// ❌ WRONG: No null check - crashes if user doesn't exist
const email = item.json.user.email;
```

```javascript
// ❌ WRONG: Assumes array has items
const firstItem = $input.all()[0].json;
```

```javascript
// ❌ WRONG: Assumes nested property exists
const city = $json.address.city;
```

```javascript
// ❌ WRONG: No validation before array operations
const names = $json.users.map(user => user.name);
```

### The Solution

```javascript
// ✅ CORRECT: Optional chaining
const email = item.json?.user?.email || 'no-email@example.com';
```

```javascript
// ✅ CORRECT: Check array length
const items = $input.all();

if (items.length === 0) {
  return [];
}

const firstItem = items[0].json;
```

```javascript
// ✅ CORRECT: Guard clauses
const data = $input.first().json;

if (!data.address) {
  return [{json: {error: 'No address provided'}}];
}

const city = data.address.city;
```

```javascript
// ✅ CORRECT: Default values
const users = $json.users || [];
const names = users.map(user => user.name || 'Unknown');
```

```javascript
// ✅ CORRECT: Try-catch for risky operations
try {
  const email = item.json.user.email.toLowerCase();
  return [{json: {email}}];
} catch (error) {
  return [{
    json: {
      error: 'Invalid user data',
      details: error.message
    }
  }];
}
```

### Safe Access Patterns

```javascript
// Pattern 1: Optional chaining (modern, recommended)
const value = data?.nested?.property?.value;

// Pattern 2: Logical OR with default
const value = data.property || 'default';

// Pattern 3: Ternary check
const value = data.property ? data.property : 'default';

// Pattern 4: Guard clause
if (!data.property) {
  return [];
}
const value = data.property;

// Pattern 5: Try-catch
try {
  const value = data.nested.property.value;
} catch (error) {
  const value = 'default';
}
```

### Webhook Data Safety

```javascript
// Webhook data requires extra safety

// ❌ RISKY: Assumes all fields exist
const name = $json.body.user.name;
const email = $json.body.user.email;

// ✅ SAFE: Check each level
const body = $json.body || {};
const user = body.user || {};
const name = user.name || 'Unknown';
const email = user.email || 'no-email';

// ✅ BETTER: Optional chaining
const name = $json.body?.user?.name || 'Unknown';
const email = $json.body?.user?.email || 'no-email';
```

### Array Safety

```javascript
// ❌ RISKY: No length check
const items = $input.all();
const firstId = items[0].json.id;

// ✅ SAFE: Check length
const items = $input.all();

if (items.length > 0) {
  const firstId = items[0].json.id;
} else {
  // Handle empty case
  return [];
}

// ✅ BETTER: Use $input.first()
const firstItem = $input.first();
const firstId = firstItem.json.id;  // Built-in safety
```

### Object Property Safety

```javascript
// ❌ RISKY: Direct access
const config = $json.settings.advanced.timeout;

// ✅ SAFE: Step by step with defaults
const settings = $json.settings || {};
const advanced = settings.advanced || {};
const timeout = advanced.timeout || 30000;

// ✅ BETTER: Optional chaining
const timeout = $json.settings?.advanced?.timeout ?? 30000;
// Note: ?? (nullish coalescing) vs || (logical OR)
```

---

## Error Prevention Checklist

Use this checklist before deploying Code nodes:

### Code Structure
- [ ] Code field is not empty
- [ ] Return statement exists
- [ ] All code paths return data

### Return Format
- [ ] Returns array: `[...]`
- [ ] Each item has `json` property: `{json: {...}}`
- [ ] Format is `[{json: {...}}]`

### Syntax
- [ ] No `{{ }}` expression syntax (use JavaScript)
- [ ] Template literals use backticks: `` `${variable}` ``
- [ ] All quotes and brackets balanced
- [ ] Strings properly escaped

### Data Safety
- [ ] Null checks for optional properties
- [ ] Array length checks before access
- [ ] Webhook data accessed via `.body`
- [ ] Try-catch for risky operations
- [ ] Default values for missing data

### Testing
- [ ] Test with empty input
- [ ] Test with missing fields
- [ ] Test with unexpected data types
- [ ] Check browser console for errors

---

## Quick Error Reference

| Error Message | Likely Cause | Fix |
|---------------|--------------|-----|
| "Code cannot be empty" | Empty code field | Add meaningful code |
| "Code must return data" | Missing return statement | Add `return [...]` |
| "Return value must be an array" | Returning object instead of array | Wrap in `[...]` |
| "Each item must have json property" | Missing `json` wrapper | Use `{json: {...}}` |
| "Unexpected token" | Expression syntax `{{ }}` in code | Remove `{{ }}`, use JavaScript |
| "Cannot read property X of undefined" | Missing null check | Use optional chaining `?.` |
| "Cannot read property X of null" | Null value access | Add guard clause or default |
| "Unmatched expression brackets" | Quote/bracket imbalance | Check string escaping |

---

## Debugging Tips

### 1. Use console.log()

```javascript
const items = $input.all();
console.log('Items count:', items.length);
console.log('First item:', items[0]);

// Check browser console (F12) for output
```

### 2. Return Intermediate Results

```javascript
// Debug by returning current state
const items = $input.all();
const processed = items.map(item => ({json: item.json}));

// Return to see what you have
return processed;
```

### 3. Try-Catch for Troubleshooting

```javascript
try {
  // Your code here
  const result = riskyOperation();
  return [{json: {result}}];
} catch (error) {
  // See what failed
  return [{
    json: {
      error: error.message,
      stack: error.stack
    }
  }];
}
```

### 4. Validate Input Structure

```javascript
const items = $input.all();

// Check what you received
console.log('Input structure:', JSON.stringify(items[0], null, 2));

// Then process
```

---

## Error #6: Loop Processing Mistakes (CRITICAL)

**Frequency**: Very common in Split in Batches workflows

**What Happens**:
- Loop processes only first item repeatedly
- Data accumulation fails or is incomplete
- "Time paradox" errors (referencing future nodes)
- Stale/cached data in debug mode

### The Problem #1: Using .first() Inside Loops

**MOST CRITICAL LOOP ERROR**: Using `.first()` instead of `.item` inside loops

```javascript
// ❌ WRONG: .first() always returns iteration #1
const currentPage = $('Split in Batches').first().json;

// Loop iteration 1: Gets page 1 ✓
// Loop iteration 2: Gets page 1 ✗ (should be page 2!)
// Loop iteration 3: Gets page 1 ✗ (should be page 3!)
// Result: Only first item processed, rest ignored
```

**Why this happens**: `.first()` returns the **first execution result** stored in memory, which is always iteration #1. It doesn't change as the loop progresses.

### The Solution #1: Use .item for Loop Data

```javascript
// ✅ CORRECT: .item automatically matches current iteration
const currentPage = $('Split in Batches').item.json;

// Loop iteration 1: Gets page 1 ✓
// Loop iteration 2: Gets page 2 ✓
// Loop iteration 3: Gets page 3 ✓
// Result: All items processed correctly
```

**Rule**: Inside a loop, use `.item` for any node that's part of the loop (changes each iteration).

### The Problem #2: Manual Data Accumulation

```javascript
// ❌ WRONG: Using this.getContext/setContext to accumulate
let results = this.getContext('accumulated') || [];
results.push(currentResult);
this.setContext('accumulated', results);

// Problems:
// - Fragile and error-prone
// - Unnecessary complexity
// - Can lose data on errors
// - Doesn't work well with retries
```

**Why this is wrong**: n8n **automatically tracks** every execution of every node in a loop. You don't need to manually accumulate anything!

### The Solution #2: Use .all() After Loop

```javascript
// ✅ CORRECT: n8n automatically stores all executions
// Inside loop: Just return current result
return [{
  json: {
    pageNumber: currentPage.pageNumber,
    videoUrl: generatedVideoUrl
  }
}];

// After loop completes (Done branch): Collect everything
const allVideos = $('Video Generation Node').all().map(item => item.json);
// Gets ALL results from ALL loop iterations automatically!
```

**Rule**: Never use `this.getContext()` or `this.setContext()` for data collection. Use `.all()` after the loop.

### The Problem #3: Referencing Future Nodes

```javascript
// ❌ WRONG: "Time paradox" - referencing a node that hasn't run yet
// Current node: Inside loop, step 2
const futureData = $('Final Aggregation Node').json;  // This is AFTER the loop!

// Error: Node hasn't executed yet, data doesn't exist
```

**Why this fails**: You can't reference data from nodes that haven't executed yet. The workflow runs sequentially.

### The Solution #3: Proper Workflow Order

```javascript
// ✅ CORRECT: Only reference nodes that have already executed

// Inside loop: Reference previous steps or pre-loop nodes
const currentItem = $('Split in Batches').item.json;  // Current loop node
const prevStep = $('Previous Loop Step').item.json;   // Previous in loop
const config = $('Pre-Loop Config').first().json;     // Before loop started

// After loop (Done branch): Now you can aggregate
const allResults = $('Node Inside Loop').all().map(item => item.json);
```

**Rule**: Only reference nodes that have already executed in the workflow sequence.

### The Problem #4: Debug Mode Stale Data

```javascript
// ❌ RISKY: In Execute Node (debug), may show cached data
const data = $('Previous Node').all();

// Problem: In single-step debug mode, this might show
// old cached data from a previous full workflow run
```

### The Solution #4: Use $input in Debug

```javascript
// ✅ SAFE: Always reflects actual input to current node
const data = $input.all();

// This shows the ACTUAL data flowing into this node right now
```

**Rule**: In debug/Execute Node mode, prefer `$input` over `$('NodeName')` to see real-time data.

### Complete Loop Pattern Example

```javascript
// ========================================
// INSIDE THE LOOP (Processing each item)
// ========================================

// ✅ CORRECT: Get current iteration data
const currentPage = $('Split in Batches').item.json;

// ✅ CORRECT: Get static config from before loop
const prompts = $('Initialize Prompts').first().json.videoPrompts;

// ✅ CORRECT: Match and process current item
const matchedPrompt = prompts.find(p => p.pageNumber === currentPage.pageNumber);

// ✅ CORRECT: Return only current result (don't accumulate!)
return [{
  json: {
    pageNumber: currentPage.pageNumber,
    imageUrl: currentPage.imageUrl,
    prompt: matchedPrompt ? matchedPrompt.prompt : 'Default'
  }
}];

// ========================================
// AFTER LOOP COMPLETES (Done branch)
// ========================================

// ✅ CORRECT: Get original structure
const originalData = $('Initialize Prompts').first().json;
const pages = originalData.pages;

// ✅ CORRECT: Collect ALL loop results with .all()
const allVideos = $('Video Generation Node').all().map(item => item.json);

// ✅ CORRECT: Merge loop results with original structure
const finalResult = pages.map(page => {
  const video = allVideos.find(v => v.pageNumber === page.pageNumber);
  return {
    ...page,
    videoUrl: video ? video.videoUrl : null
  };
});

return [{
  json: {
    courseTitle: originalData.courseTitle,
    totalVideos: allVideos.length,
    pages: finalResult
  }
}];
```

### Loop Error Quick Reference

| Error | Wrong Code | Correct Code | Impact |
|-------|-----------|--------------|---------|
| Using .first() in loop | `$('Loop').first().json` | `$('Loop').item.json` | Only first item processed |
| Manual accumulation | `this.setContext('data', arr)` | Use `.all()` after loop | Fragile, unnecessary |
| Referencing future nodes | `$('Node After Loop').json` | Reorder or use after loop | Data doesn't exist yet |
| Stale debug data | `$('Node').all()` in Execute | `$input.all()` | Shows cached data |
| Wrong static reference | `$('Config').item.json` | `$('Config').first().json` | Config changes each loop |

### Loop Data Access Decision Tree

```
Are you INSIDE a loop?
├─ YES → Is this data from a node INSIDE the loop?
│   ├─ YES → Use .item (changes each iteration)
│   │   Example: $('Loop Node').item.json
│   │
│   └─ NO → Is this data from BEFORE the loop?
│       └─ YES → Use .first() (static config)
│           Example: $('Pre-Loop Config').first().json
│
└─ NO → Are you AFTER the loop (Done branch)?
    └─ YES → Use .all() to collect all results
        Example: $('Node Inside Loop').all()
```

### Common Loop Scenarios

#### Scenario 1: Process Each Page with Global Config

```javascript
// Inside loop
const currentPage = $('Split in Batches').item.json;      // ✅ .item
const globalConfig = $('Initialize Config').first().json;  // ✅ .first()

return [{
  json: {
    pageId: currentPage.id,
    apiKey: globalConfig.apiKey  // Same for all iterations
  }
}];
```

#### Scenario 2: Collect All Results After Loop

```javascript
// After loop (Done branch)
const allResults = $('Process Page').all().map(item => item.json);  // ✅ .all()

return [{
  json: {
    totalProcessed: allResults.length,
    results: allResults
  }
}];
```

#### Scenario 3: Merge Loop Results with Original Data

```javascript
// After loop (Done branch)
const originalPages = $('Initialize Data').first().json.pages;  // ✅ .first()
const processedPages = $('Process Page').all().map(item => item.json);  // ✅ .all()

const merged = originalPages.map(page => {
  const processed = processedPages.find(p => p.id === page.id);
  return { ...page, ...processed };
});

return [{json: {pages: merged}}];
```

### Loop Error Prevention Checklist

- [ ] Inside loop: Use `.item` for loop node data
- [ ] Inside loop: Use `.first()` for pre-loop config
- [ ] After loop: Use `.all()` to collect results
- [ ] Never use `this.getContext/setContext` for accumulation
- [ ] Only reference nodes that have already executed
- [ ] In debug mode: Use `$input` instead of `$('NodeName')`
- [ ] Test with multiple items (not just one)

---

## Summary

**Top 6 Errors to Avoid**:
1. **Empty code / missing return** (38%) - Always return data
2. **Expression syntax `{{ }}`** (8%) - Use JavaScript, not expressions
3. **Wrong return format** (5%) - Always `[{json: {...}}]`
4. **Unmatched brackets** (6%) - Escape strings properly
5. **Missing null checks** - Use optional chaining `?.`
6. **Loop processing mistakes** - Use `.item` in loops, `.all()` after loops

**Quick Prevention**:
- Return `[{json: {...}}]` format
- Use JavaScript, NOT `{{ }}` expressions
- Check for null/undefined before accessing
- Inside loops: Use `.item` for loop data, `.first()` for config
- After loops: Use `.all()` to collect results
- Never use `this.getContext/setContext` for data accumulation
- Test with empty and invalid data
- Use browser console for debugging

**See Also**:
- [SKILL.md](SKILL.md) - Overview and best practices
- [DATA_ACCESS.md](DATA_ACCESS.md) - Safe data access patterns including complete loop examples
- [COMMON_PATTERNS.md](COMMON_PATTERNS.md) - Working examples
