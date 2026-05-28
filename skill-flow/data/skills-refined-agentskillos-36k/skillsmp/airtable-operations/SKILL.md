---
name: airtable-operations
description: Airtable API operations for the MI Platform base. Use when creating, reading, updating, or querying Airtable records, working with batch operations, or handling pagination. Covers rate limiting, filterByFormula patterns, linked records, and upsert operations.
user-invocable: false
---

# Airtable Operations for MI Platform

## Base Configuration

```
Base ID: appEEWaGtGUwOyOhm
API: https://api.airtable.com/v0/{baseId}/{tableIdOrName}
Auth: Authorization: Bearer {AIRTABLE_API_KEY}
```

## Table IDs (Use IDs, Not Names)

| Table | ID | Primary Field |
|-------|-----|---------------|
| Forces | `tblbAjBEdpv42Smpw` | name |
| Contacts | `tbl0u9vy71jmyaDx1` | force (linked) |
| Signals | `tblez9trodMzKKqXq` | title |
| Opportunities | `tblJgZuI3LM2Az5id` | name |

## Rate Limits (Critical)

- **5 requests/second** per base — ALWAYS add delays
- Batch create/update: **max 10 records** per request
- List records: **max 100 records** per page

```javascript
// Required delay between requests
const sleep = (ms) => new Promise(r => setTimeout(r, 200));

// Batch helper
const chunk = (arr, size) => {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
};
```

## CRUD Operations

### Create Records (Batch)

```javascript
async function createRecords(tableId, records) {
  const url = `https://api.airtable.com/v0/appEEWaGtGUwOyOhm/${tableId}`;
  const batches = chunk(records, 10);
  const results = [];

  for (const batch of batches) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.AIRTABLE_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        records: batch.map(r => ({ fields: r })),
        typecast: true  // Auto-convert field values
      })
    });

    const data = await response.json();
    if (data.error) throw new Error(data.error.message);
    results.push(...data.records);
    await sleep(200);
  }

  return results;
}
```

### Read Records with Pagination

```javascript
async function listAllRecords(tableId, options = {}) {
  const { filterByFormula, fields, sort, view } = options;
  const records = [];
  let offset = null;

  do {
    const params = new URLSearchParams();
    if (filterByFormula) params.append('filterByFormula', filterByFormula);
    if (fields) fields.forEach(f => params.append('fields[]', f));
    if (sort) params.append('sort[0][field]', sort.field);
    if (view) params.append('view', view);
    if (offset) params.append('offset', offset);

    const url = `https://api.airtable.com/v0/appEEWaGtGUwOyOhm/${tableId}?${params}`;
    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${process.env.AIRTABLE_API_KEY}` }
    });

    const data = await response.json();
    if (data.error) throw new Error(data.error.message);

    records.push(...data.records);
    offset = data.offset;

    if (offset) await sleep(200);
  } while (offset);

  return records;
}
```

### Update Records (Batch)

```javascript
async function updateRecords(tableId, records) {
  // records = [{ id: 'recXXX', fields: { ... } }, ...]
  const url = `https://api.airtable.com/v0/appEEWaGtGUwOyOhm/${tableId}`;
  const batches = chunk(records, 10);
  const results = [];

  for (const batch of batches) {
    const response = await fetch(url, {
      method: 'PATCH',  // PATCH for partial update, PUT for full replace
      headers: {
        'Authorization': `Bearer ${process.env.AIRTABLE_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ records: batch, typecast: true })
    });

    const data = await response.json();
    if (data.error) throw new Error(data.error.message);
    results.push(...data.records);
    await sleep(200);
  }

  return results;
}
```

### Upsert Pattern (G-011 Compliant)

**Never use find → delete → create loops.** Use upsert instead:

```javascript
async function upsertRecords(tableId, records, matchField) {
  // records = [{ fields: { external_id: 'xxx', ... } }, ...]
  const url = `https://api.airtable.com/v0/appEEWaGtGUwOyOhm/${tableId}`;
  const batches = chunk(records, 10);
  const results = [];

  for (const batch of batches) {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${process.env.AIRTABLE_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        performUpsert: {
          fieldsToMergeOn: [matchField]  // e.g., 'external_id'
        },
        records: batch.map(r => ({ fields: r })),
        typecast: true
      })
    });

    const data = await response.json();
    if (data.error) throw new Error(data.error.message);
    results.push(...data.records);
    await sleep(200);
  }

  return results;
}
```

## filterByFormula Patterns

```javascript
// Exact match
`{name}="Hampshire Constabulary"`

// Contains (case-insensitive)
`SEARCH("police", LOWER({title}))`

// Multiple conditions (AND)
`AND({status}="new", {type}="job_posting")`

// Multiple conditions (OR)
`OR({status}="new", {status}="enriched")`

// Not empty
`{force}!=""`

// Date comparisons
`IS_AFTER({created_at}, "2025-01-01")`
`DATETIME_DIFF(NOW(), {last_contact}, 'days') > 30`

// Linked record lookup (by record ID)
`FIND("rec123", ARRAYJOIN({force}))`
```

## Field Types Reference

| Type | API Format | Notes |
|------|------------|-------|
| Single Line Text | `"value"` | |
| Long Text | `"multiline\nvalue"` | |
| Number | `123` or `123.45` | |
| Checkbox | `true` / `false` | |
| Single Select | `"Option Name"` | With typecast: auto-creates |
| Multiple Select | `["Opt1", "Opt2"]` | |
| Date | `"2025-01-23"` | ISO 8601 |
| DateTime | `"2025-01-23T10:30:00.000Z"` | ISO 8601 with time |
| Linked Record | `["recXXX", "recYYY"]` | Array of record IDs |
| Attachment | `[{url: "..."}]` | |

## MI Platform Table Schemas

### Signals Table

| Field | Type | Notes |
|-------|------|-------|
| title | Single Line Text | Job title / signal name |
| type | Single Select | `job_posting`, `competitor`, `news`, etc. |
| source | Single Select | `indeed`, `competitor`, `bright_data` |
| force | Linked Record → Forces | |
| status | Single Select | `new`, `classified`, `archived` |
| external_id | Single Line Text | For deduplication (upsert key) |
| role_category | Single Select | `investigator`, `forensic`, `intelligence`, etc. |
| ai_confidence | Number | 0-100 |
| raw_data | Long Text | JSON blob |

### Opportunities Table

| Field | Type | Notes |
|-------|------|-------|
| name | Single Line Text | Generated from force + signals |
| force | Linked Record → Forces | |
| signals | Linked Record → Signals | Multiple |
| status | Single Select | `new`, `enriched`, `sent`, `won`, `lost` |
| priority | Single Select | `P1`, `P2`, `P3` |
| contact | Linked Record → Contacts | |
| draft_subject | Single Line Text | |
| draft_body | Long Text | |
| why_now | Long Text | AI context summary |

## Error Handling

```javascript
async function safeAirtableRequest(fn) {
  try {
    return await fn();
  } catch (error) {
    if (error.message.includes('RATE_LIMIT')) {
      // Back off and retry
      await sleep(1000);
      return await fn();
    }
    if (error.message.includes('INVALID_PERMISSIONS')) {
      console.error('Check API key permissions');
    }
    throw error;
  }
}
```

## Common Patterns

### Find Force by Name

```javascript
const forces = await listAllRecords('tblbAjBEdpv42Smpw', {
  filterByFormula: `{name}="${forceName}"`
});
return forces[0]?.id;
```

### Get Signals for Force

```javascript
const signals = await listAllRecords('tblez9trodMzKKqXq', {
  filterByFormula: `AND({force}="${forceRecordId}", {status}="new")`,
  sort: { field: 'created_at', direction: 'desc' }
});
```

### Create Opportunity from Signals

```javascript
await createRecords('tblJgZuI3LM2Az5id', [{
  name: `${forceName} - ${new Date().toISOString().slice(0,10)}`,
  force: [forceRecordId],  // Linked record = array
  signals: signalIds,       // Array of signal record IDs
  status: 'new',
  priority: hasCompetitor ? 'P1' : 'P2'
}]);
```
