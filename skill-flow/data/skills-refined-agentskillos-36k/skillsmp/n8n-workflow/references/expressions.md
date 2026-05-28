# n8n Expressions Reference

## 🚨 CRITICAL: Webhook Data Structure

**Most common mistake**: Webhook data is nested under `.body`!

```javascript
// ❌ WRONG - Will return undefined
{{ $json.email }}
{{ $json.name }}

// ✅ CORRECT - Webhook data is under .body
{{ $json.body.email }}
{{ $json.body.name }}
```

**Webhook node wraps all request data:**
- POST body → `$json.body`
- Query params → `$json.query`
- Headers → `$json.headers`

---

## When NOT to Use Expressions

❌ **Code nodes** - Use JavaScript directly, not `{{ }}`
❌ **Webhook paths** - Use static strings
❌ **Credential fields** - Never dynamic

---

## Basic Data Access

### Current Item
```javascript
{{ $json }}                    // Entire JSON object
{{ $json.fieldName }}          // Specific field
{{ $json.nested.deep.value }}  // Nested access
{{ $json['field-with-dash'] }} // Bracket notation
```

### Input Methods
```javascript
{{ $input.first() }}           // First item
{{ $input.last() }}            // Last item
{{ $input.all() }}             // All items as array
{{ $input.item }}              // Current item in loop
```

### Referencing Other Nodes
```javascript
// Single item from node
{{ $('Node Name').item.json.field }}

// All items from node
{{ $('Node Name').all() }}

// First item from node
{{ $('Node Name').first().json.field }}

// Specific item by index
{{ $('Node Name').all()[0].json.field }}

// Item count
{{ $('Node Name').all().length }}
```

---

## Built-in Variables

### Execution Context
```javascript
{{ $execution.id }}            // Execution UUID
{{ $execution.mode }}          // "manual" or "trigger"
{{ $execution.resumeUrl }}     // Resume URL for Wait node
{{ $workflow.id }}             // Workflow ID
{{ $workflow.name }}           // Workflow name
{{ $runIndex }}                // Current run index (starts at 0)
{{ $itemIndex }}               // Current item index in loop
```

### Date and Time
```javascript
{{ $now }}                     // Current DateTime (Luxon)
{{ $today }}                   // Today at midnight
{{ $now.toISO() }}             // ISO string
{{ $now.toFormat('yyyy-MM-dd') }}
{{ $now.plus({ days: 7 }) }}   // Add 7 days
{{ $now.minus({ hours: 1 }) }} // Subtract 1 hour
```

### Environment
```javascript
{{ $env.VARIABLE_NAME }}       // Environment variable
{{ $vars.myVariable }}         // Workflow variable
```

---

## Data Transformation Functions

### String Functions
```javascript
{{ $json.name.toUpperCase() }}
{{ $json.name.toLowerCase() }}
{{ $json.name.trim() }}
{{ $json.text.slice(0, 100) }}
{{ $json.text.split(',') }}
{{ $json.text.replace('old', 'new') }}
{{ $json.text.includes('search') }}
{{ 'prefix_' + $json.id }}
```

### Array Functions
```javascript
{{ $json.items.length }}
{{ $json.items.map(i => i.name) }}
{{ $json.items.filter(i => i.active) }}
{{ $json.items.find(i => i.id === 5) }}
{{ $json.items.reduce((a, b) => a + b.value, 0) }}
{{ $json.items.join(', ') }}
{{ $json.items.includes('value') }}
{{ $json.items.sort((a, b) => a.name.localeCompare(b.name)) }}
```

### Object Functions
```javascript
{{ Object.keys($json) }}
{{ Object.values($json) }}
{{ Object.entries($json) }}
{{ JSON.stringify($json) }}
{{ { ...$json, newField: 'value' } }}
```

### Number Functions
```javascript
{{ Math.round($json.value) }}
{{ Math.floor($json.value) }}
{{ Math.ceil($json.value) }}
{{ Math.abs($json.value) }}
{{ Math.max(...$json.numbers) }}
{{ Number.isFinite($json.value) }}
{{ parseFloat($json.string) }}
{{ parseInt($json.string, 10) }}
```

---

## Conditional Expressions

### Ternary Operator
```javascript
{{ $json.status === 'active' ? 'Yes' : 'No' }}
{{ $json.value > 100 ? 'High' : 'Low' }}
```

### Nullish Coalescing
```javascript
{{ $json.name ?? 'Unknown' }}          // If null/undefined
{{ $json.value || 0 }}                 // If falsy
{{ $json.data?.nested?.field ?? '' }}  // Optional chaining
```

### Logical Operators
```javascript
{{ $json.a && $json.b }}               // Both truthy
{{ $json.a || $json.b }}               // Either truthy
{{ !$json.disabled }}                  // Negation
```

---

## IIFE Pattern (Complex Logic)

For multi-statement expressions, use an Immediately Invoked Function Expression:

```javascript
{{(()=>{
  const items = $('Previous Node').all();
  const filtered = items.filter(i => i.json.status === 'active');
  const count = filtered.length;
  return count > 0 ? `Found ${count} active items` : 'No active items';
})()}}
```

### Date Calculation Example
```javascript
{{(()=>{
  const start = DateTime.fromISO($json.startDate);
  const end = DateTime.fromISO($json.endDate);
  const diff = end.diff(start, 'days');
  return diff.days;
})()}}
```

### Data Aggregation Example
```javascript
{{(()=>{
  const items = $input.all();
  const total = items.reduce((sum, item) => sum + item.json.amount, 0);
  const avg = total / items.length;
  return { total, average: Math.round(avg * 100) / 100 };
})()}}
```

---

## Type Checking

```javascript
{{ typeof $json.value }}                         // 'string', 'number', etc.
{{ Array.isArray($json.items) }}                 // Check if array
{{ $json.value === null }}                       // Check null
{{ $json.value === undefined }}                  // Check undefined
{{ $json.value != null }}                        // Not null/undefined
```

---

## Common Patterns

### Safe Property Access
```javascript
{{ $json.data?.nested?.value ?? 'default' }}
```

### Format Date for Display
```javascript
{{ $now.toFormat('dd/MM/yyyy HH:mm') }}
{{ DateTime.fromISO($json.date).toRelative() }}  // "2 days ago"
```

### Generate UUID
```javascript
{{ $runIndex + '-' + $itemIndex + '-' + Date.now() }}
```

### Parse JSON String
```javascript
{{ JSON.parse($json.jsonString) }}
```

### URL Encoding
```javascript
{{ encodeURIComponent($json.searchTerm) }}
```

### Template Literal
```javascript
{{ `Hello ${$json.name}, your order #${$json.orderId} is ready` }}
```
