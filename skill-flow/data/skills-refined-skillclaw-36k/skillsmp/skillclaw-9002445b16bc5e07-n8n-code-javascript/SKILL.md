---
name: n8n-code-javascript
description: Use this skill when writing JavaScript code in n8n Code nodes, utilizing $input/$json/$node syntax, making HTTP requests, working with dates, troubleshooting errors, or selecting execution modes.
---

# JavaScript Code Node

Expert guidance for writing JavaScript code in n8n Code nodes.

---

## Quick Start

```javascript
// Basic template for Code nodes
const items = $input.all();

// Process data
const processed = items.map(item => ({
  json: {
    ...item.json,
    processed: true,
    timestamp: new Date().toISOString()
  }
}));

return processed;
```

### Essential Rules

1. **Choose "Run Once for All Items" mode** (recommended for most use cases).
2. **Access data**: Use `$input.all()`, `$input.first()`, or `$input.item`.
3. **CRITICAL**: Must return `[{json: {...}}]` format.
4. **CRITICAL**: Webhook data is under `$json.body` (not `$json` directly).
5. **Built-ins available**: `$helpers.httpRequest()`, DateTime (Luxon), `$jmespath()`.

---

## Mode Selection Guide

The Code node offers two execution modes. Choose based on your use case:

### Run Once for All Items (Recommended - Default)

**Use this mode for:** 95% of use cases.

- **How it works**: Code executes **once** regardless of input count.
- **Data access**: Use `$input.all()` or the `items` array.
- **Best for**: Aggregation, filtering, batch processing, transformations, API calls with all data.
- **Performance**: Faster for multiple items (single execution).

```javascript
// Example: Calculate total from all items
const allItems = $input.all();
const total = allItems.reduce((sum, item) => sum + (item.json.amount || 0), 0);

return [{
  json: {
    total,
    count: allItems.length,
    average: total / allItems.length
  }
}];
```

**When to use:**
- ✅ Comparing items across the dataset.
- ✅ Calculating totals, averages, or statistics.
- ✅ Sorting or ranking items.
- ✅ Deduplication.
- ✅ Building aggregated reports.
- ✅ Combining data from multiple items.

### Run Once for Each Item

**Use this mode for:** Specialized cases only.

- **How it works**: Code executes **separately** for each input item.
- **Data access**: Use `$input.item` or `$item`.
- **Best for**: Item-specific logic, independent operations, per-item validation.
- **Performance**: Slower for large datasets (multiple executions).

```javascript
// Example: Add processing timestamp to each item
const item = $input.item;

return [{
  json: {
    ...item.json,
    processed: true,
    timestamp: new Date().toISOString()
  }
}];
```