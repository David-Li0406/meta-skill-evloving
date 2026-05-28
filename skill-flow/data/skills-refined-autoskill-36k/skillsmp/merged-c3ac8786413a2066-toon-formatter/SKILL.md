---
name: toon-formatter
description: Use this skill to AGGRESSIVELY apply TOON v2.0 format for structured data to achieve 30-60% token savings, especially for arrays with 5+ items and uniform structures.
---

# TOON v2.0 Formatter Skill (AGGRESSIVE MODE)

## Purpose

**AGGRESSIVELY** apply TOON v2.0 format to save 30-60% tokens on structured data. Use TOON **by default** for biggish, regular data. Use native Zig encoder for 20x performance.

## When to Use (AGGRESSIVE)

**TOON ALL DAY** - Use automatically for:
- ✅ Arrays with ≥ 5 similar items
- ✅ Tables, logs, events, transactions, analytics
- ✅ API responses with uniform structure (≥60% field overlap)
- ✅ Database query results
- ✅ Repeatedly-used, structured data in prompts
- ✅ RAG pipelines, tool calls, agents passing data around
- ✅ Benchmarks/evals where prompt size = money
- ✅ Shape is more important than labels
- ✅ You know what each column means
- ✅ Can declare headers once, go row-by-row

**MAYBE, BUT NOT AUTOMATICALLY** - Be selective when:
- ⚠️ Human collaborators reading/editing data a lot
- ⚠️ APIs/tools expect JSON (use JSON on wire, TOON in prompts)
- ⚠️ Structure is uneven (many optional keys, weird nesting)

**NO, JUST DON'T** - Stick to JSON/text for:
- ❌ Short arrays (< 5 items)
- ❌ One-off examples in docs
- ❌ Narrative text, instructions, essays
- ❌ Deep, irregular trees where hierarchy matters

## What is TOON v2.0?

**TOON (Token-Oriented Object Notation) v2.0** reduces token consumption by 30-60% for structured data:

### Three Array Types

**1. Tabular** (uniform objects ≥5 items):
```
[count]{field1,field2,field3}:
  value1,value2,value3
  value1,value2,value3
```

**2. Inline** (primitives ≤10):
```
fieldName[count]: value1,value2,value3
```

**3. Expanded** (non-uniform):
```
- name: Alice
  role: admin
- name: Bob
  level: 5
```

### Three Delimiters

**Comma** (default, most compact):
```
[count]{field1,field2}: value1,value2
```

**Tab** (for data with commas):
```
[count\t]{field1,field2}: value1	value2
```

**Pipe** (markdown-like):
```
[count|]{field1,field2}: value1|value2
```

### Key Folding

**Flatten nested objects** (25-35% extra savings):
```
server.host: localhost
server.port: 8080
database.host: db.example.com
```

## Process

### 1. Detect Suitable Data

When encountering array data, check if it meets TOON criteria:
- ✅ Array with ≥5 items
- ✅ Objects with ≥60% field uniformity (most objects share same fields)
- ✅ Flat or moderately nested structure

**How to check uniformity:**
1. Extract all field names from all objects
2. Count how many objects have the most common set of fields
3. Calculate: `(objects with common fields / total objects) × 100`
4. If ≥60%, uniformity is good for TOON

### 2. Estimate Token Savings

**Quick estimation method:**
- **JSON tokens** ≈ `(item count × field count × 4) + overhead`
- **TOON tokens** ≈ `20 (header) + (item count × field count × 2)`
- **Savings** ≈ `(JSON - TOON) / JSON × 100%`

### 3. Apply TOON v2.0 Aggressively

**AGGRESSIVE MODE: Use Zig encoder for optimal results**

If data meets criteria:

**Method 1: Use Zig Encoder** (Recommended - 20x faster):
```bash
.claude/utils/toon/zig-out/bin/toon encode data.json \
  --delimiter tab \
  --key-folding \
  > data.toon
```

**Method 2: Manual TOON** (for inline generation):
1. Detect array type (inline/tabular/expanded)
2. Choose delimiter (comma/tab/pipe)
3. Apply key folding if nested objects
4. Build TOON header: `[N]{fields}:` or `key[N]: values`
5. Output formatted TOON

### 4. Show Formatted Output

**Immediately show in TOON with brief explanation:**

```
📊 API Endpoints (15 items, TOON format - saved 40.1% tokens):

[15]{method,path,description,auth,rateLimit}:
  GET,/api/users,List all users,required,100/min
  POST,/api/users,Create new user,required,50/min
  ...
```

## Best Practices

### Always Show Format Decision

When working with data, always indicate which format you're using and why:

```
📊 Using TOON (estimated 42% token savings)
[count]{fields}:...
```

or

```
ℹ️ Using JSON (deeply nested structure, TOON not suitable)
{...}
```

### When NOT to Use TOON

Explain when JSON is better:

- **Deeply nested data**: TOON excels with flat/tabular structures
- **Low uniformity** (<70%): Different fields per object reduces TOON benefits
- **Small arrays** (<10 items): Overhead not worth it
- **Single records**: Use JSON for clarity

### Performance Tips

1. **Batch processing**: Convert large datasets once, reuse TOON format
2. **Uniformity matters**: Higher field overlap = better savings
3. **Nested arrays**: TOON supports nested structures but savings diminish
4. **Type coercion**: TOON preserves types (numbers, booleans, dates)

## Examples

### Example 1: API Response

**Input:**
```javascript
const apiResponse = await fetch('/api/users').then(r => r.json());
// 150 users returned
```

**Output:**
```
API Response (150 users):
Format: TOON (saves 41.2%, 1,847 tokens saved)

[150]{id,name,email,role,lastLogin}:
  1,Alice Smith,alice@example.com,admin,2024-01-15T10:30:00Z
  2,Bob Jones,bob@example.com,user,2024-01-15T09:15:00Z
  ...
```

### Example 2: Database Query

**Input:**
```sql
SELECT * FROM transactions WHERE date > '2024-01-01' LIMIT 500;
```

**Output:**
```
Query Results (500 transactions):
Format: TOON (saves 38.9%, 3,421 tokens saved)

[500]{id,date,amount,merchant,category,status}:
  1,2024-01-15,42.50,Starbucks,Food & Drink,completed
  2,2024-01-15,125.00,Shell Gas,Transportation,completed
  ...
```

### Example 3: Metrics Dashboard

**Input:**
```typescript
const metrics = analyzePerformance();
// Returns array of route performance metrics
```

**Output:**
```
Performance Metrics (45 routes):
Format: TOON (saves 44.1%, 892 tokens saved)

[45]{route,avgTime,p95,requests,errors}:
  /api/users,125,340,15420,3
  /api/products,89,210,8932,0
  /api/orders,450,1250,3421,12
  ...
```

### Example 4: Mixed Data (JSON Better)

**Input:**
```javascript
const complexData = {
  metadata: { version: '1.0', timestamp: '...' },
  results: [
    { id: 1, data: { nested: { deep: 'value' } } },
    // Highly nested, non-uniform
  ]
};
```

**Output:**
```
ℹ️ Using JSON format (TOON not recommended):
- Deeply nested structure
- Low uniformity (45%)
- Small array (only 5 items)

{
  "metadata": { "version": "1.0", ... },
  "results": [ ... ]
}
```

## Integration with Other Skills

### Financial Analysis
When analyzing transactions or financial data, use TOON for large result sets:
- Transaction histories (100+ items)
- Account balances across multiple accounts
- Payment logs and audit trails

### Data Export
When exporting data, check if TOON is suitable:
- If ≥5 items and ≥60% uniform → use TOON
- Otherwise → use JSON

### API Documentation
Document API endpoints in TOON format for compact reference:

```
# API Endpoints

[15]{method,path,auth,rateLimit,description}:
  GET,/api/users,required,100/min,List all users
  POST,/api/users,required,50/min,Create new user
  ...
```

## Commands

Use with these TOON v2.0 commands:
- `/toon-encode <file> [--delimiter tab] [--key-folding]` - JSON → TOON v2.0
- `/toon-validate <file> [--strict]` - Validate TOON file
- `/analyze-tokens <file>` - Compare JSON vs TOON savings
- `/convert-to-toon <file>` - Legacy command (use toon-encode)

## Resources

- **Zig Encoder**: `.claude/utils/toon/toon.zig` (601 lines, 20x faster)
- **User Guide**: `.claude/docs/toon-guide.md`
- **Examples**: `.claude/utils/toon/examples/` (9 files)
- **Guides**: `.claude/utils/toon/guides/` (4 files)
- **FAQ**: `.claude/docs/FAQ.md`
- **TOON Spec**: https://github.com/toon-format/spec
- **Official Site**: https://toonformat.dev

## Success Metrics

Track TOON usage effectiveness:
- Average token savings: 30-60%
- Accuracy improvement: +3-5% (per official benchmarks)
- Context window freed: 15K+ tokens on large datasets
- User satisfaction: Faster responses, more context available